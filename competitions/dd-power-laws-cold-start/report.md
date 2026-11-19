# Power Laws: Cold Start Energy Forecasting — pilot

Ngày audit: 19/11/2026. Edition kết thúc 10/2018, không phải edition 2019 chỉ vì bài winners xuất bản 2019. Đây là nghiên cứu nguồn tĩnh **partial**, chưa reproduction.

Entry points: [pipeline](pipeline.md), [evidence](evidence.json), [kế hoạch thí nghiệm](experiment_plan.md), [quality review](quality_review.md), [state](state.json), [nguồn](sources.md).

## A — Bài toán và ràng buộc

Input là consumption theo giờ, temperature và metadata của series mới; history chỉ 1–14 ngày trọn ngày. Output tùy series: 24 giá trị giờ của ngày kế tiếp, 7 tổng ngày của tuần kế tiếp, hoặc 2 tổng tuần của hai tuần kế tiếp. Đơn vị consumption là Wh, không phải công suất W. Temperature tương lai được cung cấp trong submission template: đây là điều kiện competition cần nhớ khi chuyển sang forecasting vận hành. [cold-task]

Official problem cho phép holiday lists và pretrained models có thể phát hành mở; không suy ra mọi external data đều được dùng. Geographic location không được công bố. Chưa xác minh submission/day và mọi thay đổi rules trong lịch sử. [cold-rules-scope]

## B — Dataset

Các bảng: `consumption_train.csv`, `cold_start_test.csv`, `meta.csv`, `submission_format.csv`; khóa dự đoán là `pred_id`, kiểm tra uniqueness theo `(series_id,timestamp)`. Train cung cấp các đoạn 4 tuần. Metadata có surface, base_temperature và lịch nghỉ từng weekday. Temperature có giá trị sai/thiếu theo mô tả chính thức. [cold-task]

Write-up Guillermo công bố 758 **series**, 672 timestamps/series, khoảng 40% temperature thiếu; số series theo weekly/daily/hourly là 192/191/242. Đây là **published statistics**, chưa được dự án đo lại. Không đổi “series” thành “building độc lập”: chính write-up nghi có nhiều series từ cùng building. [cold-published-stats]

Trang open data hiện chuyển người dùng sang Schneider Exchange và yêu cầu account; dự án chưa đăng ký/tải data. Sự tương đương giữa archive hiện tại và CSV competition chưa được xác minh. [cold-access]

## C — Metric và ảnh hưởng

Theo official problem, metric minimize:

\[
S=\frac1N\sum_{i=1}^{N}|\hat y_i-y_i|\frac{w_i}{m_i},\quad
w_i=\begin{cases}1&hourly\\24/7&daily\\12&weekly\end{cases}
\]

`m_i` là true mean của prediction window tương ứng, không phải trung bình history dùng để normalize model. Các output cùng window của một series chia sẻ true mean window đó. Không có true future mean khi inference. Implementation top-one tính relative absolute errors, nhân weight theo độ dài 24/7/2, concatenate rồi mean; đây là code đội thi, không phải bằng chứng đã có mã scorer server. [cold-metric]

Vì có chia `m_i`, cùng sai số Wh sẽ bị phạt mạnh hơn ở series tiêu thụ thấp. Vì weight bù số output, daily/weekly không bị giảm đóng góp chỉ do ít dòng hơn. Tuy nhiên denominator là **tổng số output N**, không được tự đổi sang mean của từng series/horizon.

Ví dụ **illustrative**: một series ở mỗi horizon đều có 10% relative error. Weighted numerator của mỗi series đều là 2.4; tổng 7.2 chia 33 output cho score ≈0.21818, không phải 0.1. Vì vậy không so NMAE công bố trực tiếp với “11% error” trong mô tả blog. Có script kiểm tra số học ở [metric_examples.py](../../scripts/metric_examples.py).

Unknown: true mean bằng 0, negative prediction, clipping/NaN và rounding server. Không tự thêm eps vào metric rồi gọi official.

## D — EDA thiết kế riêng

Chưa đo dữ liệu. Các phép đo cần làm khi có bản được phép dùng:

| Phép đo | Population / cách tính | Lý do |
|---|---|---|
| History length × horizon | mỗi series, count timestamps và số ngày đầy đủ | Cold-start regime nào thiếu dữ liệu nhất |
| Cadence/gaps | sort timestamp, histogram delta theo series | Không để shift(i) biến lag giờ thành lag dòng sai |
| Consumption scale | min/max/mean/zero-rate theo series và theo history-only | Kiểm tra normalization và denominator gần 0 |
| Temperature missingness | rate theo series, time, split; không gộp toàn bảng | Missingness có thể thay đổi giữa các series |
| Similar/repeated series | metadata overlap và profile similarity, xác minh thủ công | Series ID chưa chắc là đơn vị độc lập |
| Local validation | tái tạo history 1–14 ngày và từng horizon | Random row split không mô phỏng task |

Output đề xuất: `series_summary.csv`, `history_horizon_counts.csv`, `gap_audit.csv`, dataset hash + command. Những tên này là artifact dự kiến, chưa tồn tại.

## E — Baseline

Official repository dẫn baseline LSTM; chưa audit implementation và score trên đúng final test, nên không ghi baseline score giả định. Từ write-up top-one có thể dựng baseline persistence/repeat weekday; đó là kế hoạch thí nghiệm, chưa phải kết quả đã đo. [cold-baseline]

## F — Top results

Nguồn là bảng **Winning Submissions** trong repository tổ chức ở commit `a22192b86b31c9f9f9f55cf108f1c3aa9c9ce9b1`. Scores dưới đây là published. [cold-results]

| Rank | Team | Public | Private |
|---:|---|---:|---:|
| 1 | last_minute_team | 0.272444 | 0.257776 |
| 2 | valilenk | 0.289542 | 0.259703 |
| 3 | LastRocky | 0.298222 | 0.261503 |

Không quy private gap giữa hai đội thành gain của ensemble hay normalization.

## G — Pipeline

[Pipeline forensic](pipeline.md) mô tả top-one từ submission thành phần đến patch cuối; top-three có parsing, feature ordering, normalization eps, tensor shapes, train/inference và aggregation. Top-two có đường code/env riêng. Những phần chưa truy được giữ partial, không gọi full winning-run reconstruction.

Chi tiết nổi bật: hourly LSTM của LastRocky nhận `(batch,1,168)`, tức 168 lag là feature dimension trong **một timestep**, không phải chuỗi 168 timestep. Layer dropout cho metadata có nhánh output không được nối vào Dense tiếp theo. Cả hai đều là lý do phải đọc execution graph thay vì tên “LSTM + dropout”. [cold-shape]

## H — Reverse engineering

**Decision: scale daily bằng hourly extrema ×24.** Observation có code; tác giả giải thích daily history đôi khi chỉ có 1 điểm nên normalization thông thường khó dùng. Cơ chế suy luận: hourly history vẫn có nhiều giá trị để ước lượng range. Không có controlled ablation trong nguồn đã đọc chứng minh đây là nguyên nhân thắng. So history-only hourly scaling với daily scaling, giữ split/model/seed và report theo cold-start length. [cold-normalize; cold-hypothesis]

**Decision: mô hình theo horizon và ensemble.** Tác giả top-one cho biết hai thành viên gộp approach cuối giải. Giả thuyết complementary errors hợp lý nhưng cần OOF correlation và matched-budget single/ensemble để kiểm tra. Patch dự đoán sau blend là bước khác, không gộp tác dụng vào ensemble. [cold-team-blend]

## I — Validation và leakage

LastRocky tạo tail holdout theo series và dùng dữ liệu history của cold-start series trong training/tuning. History đã được cung cấp không mặc nhiên là leakage. Tuy nhiên extrema preprocessing được tính từ toàn bộ observed history trước local tail split: validation không hoàn toàn mô phỏng chỉ biết prefix tại local cutoff. Đây là rủi ro cần đo, **không phải kết luận vi phạm competition**. Cluster/near-duplicate series cũng cần audit trước khi coi series split là building split. [cold-split; cold-validation-risk]

## J — Evidence và ablation

Đã xác minh cấu trúc pipeline và published results. Chưa có bảng controlled ablation được audit đầy đủ, chưa đo variance/seeds. So sánh public/private chỉ cho thấy kết quả thay đổi trên hai tập, không chứng minh causal benefit. Kế hoạch phân biệt normalization, horizon modeling và patch nằm trong experiment plan.

## K — Failure analysis

Nguồn Guillermo nêu series biến động/holiday và nghi repeated buildings; chưa có error slices do dự án đo. Các ca cần kiểm tra: 1 ngày history, range≈0, temperature thiếu, holiday không biết location, forecast recursive dài 14 ngày. Không khẳng định tỷ lệ lỗi cho các ca này. [cold-published-stats]

## L — Compute và reproducibility

Top-two README công bố 128 GB RAM và GTX 1080 Ti 11 GB, fastai 1.0.19/Python 3.7; đây là setup tác giả, không phải minimum hay timing đo ở đây. Top-one hướng dẫn cài legacy seq2seq/recurrentshop; dependency URLs chưa pin đầy đủ. Top-three tree có ba LightGBM model text nhưng không thấy đủ neural/XGB files mà inference yêu cầu. Reproduction hiện **blocked**, đọc/kiểm tra số học vẫn khả thi. [cold-compute; cold-assets]

## M — So sánh các đội

| Khía cạnh | last_minute_team | valilenk | LastRocky |
|---|---|---|---|
| Approach công bố | Hai thành viên, custom NN/seq2seq + blend và patch | NN fastai, dự báo giờ rồi aggregate | Tree + NN, hourly/daily |
| Thứ cần đọc kỹ | Final team launcher khác final_solution của một thành viên | Feature scaling và target reconstruction | eps, recursive state, per-step mixture |
| Validation | Cluster/fold logic, chưa trace mọi config | Code feature/training riêng | Local tails cold-start series |
| Rào cản | Legacy deps, selected predictions và exact run | Legacy fastai/GPU | Thiếu đủ assets cho inference |

Các approach ở bảng từ [cold-results], chi tiết forensic có claim riêng ở pipeline. Chưa có matched-compute so sánh.

## N — Kiến thức rút ra

1. Metric aggregation phải khớp output unit: hourly/daily/weekly không thể gộp tùy ý.
2. Normalization có thể cần đơn vị quan sát nhỏ hơn target aggregate; kiểm tra origin cutoff để tránh validation optimistic.
3. Entry point và bước patch cuối quyết định artifact thực sự nộp; tên folder “final” chưa đủ.

Đây là kiến thức gắn với case này; [knowledge cards](../../techniques/knowledge_cards.json) giữ claim IDs và tests, chưa tuyên bố generality đã thực nghiệm.

## O — Unknowns và audit

Chưa biết đủ winning run config/assets, archive equivalence, official scorer edge cases, dependency defaults và measured EDA. Review là self-review. `state.json` ghi trạng thái từng module và bước tiếp tục. Task này không được đánh dấu complete vì report dài.

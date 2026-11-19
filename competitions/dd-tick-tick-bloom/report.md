# Tick Tick Bloom — pilot vệ tinh và dữ liệu nhiều nguồn

Audit 19/11/2026. Edition kết thúc 02/2023. Trạng thái **partial/source research**. [Pipeline](pipeline.md), [claims](evidence.json), [nguồn](sources.md), [experiment plan](experiment_plan.md), [review](quality_review.md), [state](state.json).

## A — Task

Mỗi sample là tổ hợp ngày–tọa độ của một phép lấy mẫu nước thực địa. Predict severity cyanobacteria **1–5**, không phải raw density. Input metadata, satellite imagery và optional climate/elevation. Các location test thuộc geographic areas tách khỏi train. Chỉ dùng dữ liệu đã có **tại hoặc trước ngày lấy mẫu**; bốn nguồn được cho phép là Sentinel-2, Landsat, NOAA HRRR và Copernicus DEM qua access points chỉ định. [bloom-task]

## B — Dataset

`metadata.csv`: uid, latitude, longitude, date, split; `train_labels.csv`: uid, region, severity, density; template có uid/region/severity. Region dùng cả metric và modeling. Feature data không phải một zip ảnh đã sẵn: cần truy vấn satellite/climate theo vị trí/thời gian. Sentinel-2 visible10m, Landsat30m là số liệu **published** trong task; không phải kích thước ảnh mỗi sample do dự án đo. [bloom-task]

Các mức density (cells/mL): level1 <20, 000; level2 [20, 000, 100, 000); level3 [100, 000, 1, 000, 000); level4 [1, 000, 000, 10, 000, 000); level5 ≥10, 000, 000. Threshold density xác định label, khác threshold biến regression prediction thành severity integer. [bloom-labels]

Open-data page cho phép sử dụng với attribution và trỏ SeaBASS archive. Chưa tải archive, xác minh mapping về CSV competition, hoặc audit riêng terms/version của từng external API. [bloom-access]

## C — Metric

Minimize **trung bình RMSE của bốn vùng**:

\[
S=\frac14\sum_{r\in\{west,midwest,south,northeast\}}\sqrt{\frac1{n_r}\sum_{i\in r}(y_i-\hat y_i)^2}.
\]

Ở đây `n_r` khác nhau giữa vùng. Đây là ký hiệu viết lại cho rõ population; công thức hiển thị official có chỉ số tổng không nhất quán, nhưng mô tả và công thức bốn RMSE rõ. Không thay bằng pooled RMSE và không RMSE của raw density. Severity nộp phải là integer. [bloom-metric]

Một vùng ít samples vẫn chiếm1/4 metric; chính sách chỉ cải thiện vùng đông có thể kém macro score. Squared error phạt nhầm nhiều bậc mạnh hơn nhầm một bậc; khoảng density giữa các severity không tuyến tính nhưng metric khoảng cách severity là tuyến tính trước bình phương.

Ví dụ **illustrative**: west có9 errors0; ba vùng còn lại mỗi vùng một error2 → region-average1.5, pooled RMSE1.0. Kiểm tra ở metric_examples.py. UNKNOWN: server xử lý noninteger/empty regions/NaN cụ thể; không đoán từ sklearn defaults.

## D — EDA theo bài toán

Chưa có measurements từ data. Checklist cần đo theo **uid**, không dùng số satellite rows làm số independent labels:

| Phân tích | Phương pháp | Quyết định liên quan |
|---|---|---|
| Region×severity×date | Count uid unique; rate theo vùng và thời kỳ | Metric macro, sampling, model riêng vùng |
| Spatial isolation | Kiểm tra nearest train-test distance, location/time overlap | CV sát task, tránh leakage địa điểm |
| Image availability | Rate missing theo platform/region/date; samples trước satellite acquisition | Fallback và selection bias |
| Imagery age/cloud/coverage | Distribution days_before_sample, cloud_cover, valid water pixels | Chọn scene, không nhìn tương lai |
| Resolution/area | Water pixels và footprint, không chỉ image size | Thống kê màu có đại diện water body không |
| Label noise | Density/severity boundary consistency; repeated location/date | Robust loss và error cases |
| Geographic quality | Flag coordinate outliers, provider grouping nếu available | Học source-specific bias |

Mọi denominator/split/version phải ghi; class count và gain chưa đo không được điền số minh họa vào report.

## E — Baseline

Repository tổ chức dẫn benchmark LightGBM với satellite summary features; chưa audit baseline code hoặc score trên exact final test. Không dùng điểm “gần gấp đôi” từ blog như controlled ablation. Regression tree là baseline phù hợp để kiểm tra mà không cần bắt đầu bằng CNN. [bloom-baseline]

## F — Results

Published trong repo tổ chức commit `c59c9ab9e3d376bfd24a2b85e821776100d46230`. [bloom-results]

| Prediction rank | User | Public | Private |
|---:|---|---:|---:|
| 1 | sheep | 0.7554 | 0.7608 |
| 2 | apwheele | 0.7476 | 0.7616 |
| 3 | karelds | 0.7698 | 0.7844 |

Write-up bonus có ranking riêng: karelds1, sheep2. Public rank/score không quyết định prediction winner cuối; apwheele có public thấp hơn sheep nhưng private cao hơn. Không gộp hai giải. [bloom-results]

## G — Pipeline

[Pipeline forensic](pipeline.md) truy top-one feature→model→regional routing→rounding→CSV; top-three scene selection, 88/67-dimensional feature construction, UID grouping, model train/inference và fallback. Top-two có đường ensemble trees được đối chiếu. Những số feature dimensions là đếm từ code lists, không phải dataset statistics.

## H — Reverse engineering

**Model khác nhau theo vùng:** official summary mô tả top-one dùng LightGBM cho midwest/northeast và spatial KNN cho south/west. Author nói chất lượng location/data ảnh hưởng lựa chọn. Đây là author rationale; chưa có measured ablation ở đây chứng minh bỏ imagery luôn tốt ở hai vùng đó. Giả thuyết ít tín hiệu imagery/chất lượng coordinate khiến model phức tạp overfit cần test bằng geographic holdout và feature ablations. [bloom-regions; bloom-hypothesis]

**Ordinal regression + rounding:** severity có thứ tự; model regress rồi map integer phù hợp cấu trúc metric. Top-one thresholds1.65/2.55 khác nearest integer; khả năng chúng điều chỉnh bias là suy luận. Phải tune threshold chỉ trên inner folds, đo outer spatial holdout để phân biệt calibration thật với overfit. [bloom-round]

## I — Validation

Official test unseen areas. Top-one KMeans100 trên longitude/latitude → GroupKFold5; KMeans random_state không được chỉ định trong Model.py, lặp100 lần không có bảo đảm cùng splits. Top-three StratifiedGroupKFold theo UID giữ các scenes cùng sample trong fold, **không chứng minh location/time disjoint**; hai UID ở cùng lake vẫn có thể ở hai folds. Hai satellite tables được split riêng cũng cần kiểm tra OOF alignment trước ensemble. Đây là rủi ro, chưa đo mức ảnh hưởng. [bloom-validation; bloom-third-split]

## J — Ablation evidence

Không có số gain controlled đã xác minh trong pilot. Author top-three báo đã thử precipitation/wind/elevation không hữu ích hoặc overfit; chỉ coi là author-reported negative results, không coi là universal finding. Cần nguồn đầy đủ và matched data/split để định lượng. [bloom-negative]

## K — Failure cases

Không imagery, water body dưới resolution, cloud/old scene, coordinate kém, region nhỏ, new lake/provider và severity4/5 hiếm là các slices cần kiểm tra. Top-three fallback mean vùng có thể thiếu cả region nếu không ảnh nào: code chưa guard rõ; chưa quan sát exception thực tế. Top-one inverse-distance KNN không có eps zero-distance trong Model.py. [bloom-fallback; bloom-code-risks]

## L — Compute / engineering

Top-one README công bố Ryzen5950X, RAM128 GB, Ubuntu20.04 và lưu ý predownloaded imagery không kèm repository. Model.py train100×5=500 boosters cho hai vùng gộp, không phải một LightGBM đơn. Đây là số vòng code dự kiến nếu không lỗi/early exit, không phải log xác nhận500 models winning run. External download có thể là bottleneck; chưa đo runtime hoặc chi phí API. [bloom-topone-code; bloom-compute]

Legacy pandas/numpy/LightGBM APIs là blocker khi chạy môi trường mới; không sửa source trước faithful comparison. Chưa truy toàn bộ acquisition defaults, projection, mask interpolation và library versions.

## M — Cross-team

| Khía cạnh | sheep | apwheele | karelds |
|---|---|---|---|
| Representation | Water-color stats + weather, region routing | Tabular date/location/elevation/satellite | Multiband stats+indices+climate cho Landsat |
| Model | LightGBM + spatial KNN | LGBM/XGB/CatBoost ensemble | LightGBM theo region×satellite×fold |
| Output | Custom thresholds hai vùng; round KNN hai vùng | Mean, clip1–5, round, int | Mean scene/fold/satellite rồi round, region fallback |
| CV caveat | Geographic clusters, stochastic splits | Chưa audit đầy đủ split weights | UID group không chắc lake-disjoint |
| Reproduction caveat | Download data ngoài repo | SQL prep/idempotency và features | External archives/scene data/version |

Nguồn: [bloom-regions], [bloom-second], [bloom-third-features], [bloom-round], [bloom-fallback]. Không suy contribution riêng từ private score gap0.0008.

## N — Knowledge

Giá trị học tập chính: bắt đầu từ **prediction unit và metric groups**, kiểm tra khả dụng feature theo thời gian; mô hình có thể chuyển từ image sang engineered tabular features. Per-region routing, missing-data fallback và threshold order là bộ phận thực sự của solution. Các card chỉ lưu bằng chứng case này, không khẳng định tree luôn tốt hơn CNN.

## O — Unknowns

Full dataset statistics, archive/competition equivalence, exact winning model hashes, acquisition pipeline, default interpolation, spatial split robustness và score reproduction chưa hoàn thành. Có một intermediate KNN dataframe dùng nhầm biến trong top-one Model.py nhưng output cuối south/west lấy test_df đã gán KNN; phân tích phải theo cuối file, không kết luận final hoàn toàn bỏ KNN. [bloom-code-risks]

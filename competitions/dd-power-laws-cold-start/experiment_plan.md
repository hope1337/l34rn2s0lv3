# Kế hoạch kiểm chứng — Cold Start

Trạng thái: chưa chạy training/inference; chưa có dataset được phép sử dụng trong workspace. Feasibility: static/numerical checks được, full reproduction blocked bởi data/account/assets/legacy dependencies. Không có GPU budget đã chốt.

| ID | Hypothesis / intervention | Controls / evaluation | Điều kiện bác bỏ hoặc giới hạn |
|---|---|---|---|
| CS-1 | Hourly-derived daily normalization tốt hơn daily-only ở history 1 ngày | Cùng model, history windows, split và seeds; report NMAE từng history length/horizon | Gain không ổn định qua group holdouts hoặc mất khi dùng history-prefix-only |
| CS-2 | Full-observed extrema làm local validation lạc quan | Fit extrema trên prefix vs toàn observed series; giữ future targets riêng | Không khác đáng kể thì không kết luận có optimism material |
| CS-3 | Ensemble giảm lỗi nhờ diversity | Single components vs blend trên cùng OOF, lưu correlations và per-series errors | Gain do một component mạnh hơn/tuning budget, không có complementarity |
| CS-4 | Team patch hữu ích nhưng phụ thuộc cohort | Cùng base blend, patch on/off; report affected IDs và heldout matching rule | Chỉ cải thiện leaderboard cohort, không chuyển giao holdout |
| CS-5 | Shape `(1,168)` có behavior khác `(168,1)` | Faithful shape trước, alternative là experiment riêng; matched parameter/compute caveats | Không gọi alternative là reproduction; không quy gain chỉ shape nếu size khác |

Thứ tự chạy khi đủ điều kiện: kiểm tra schema/timestamp và metric toy → repeat baseline → một LightGBM CPU subset → CS-1/2 → NN/ensemble nếu budget cho phép. Không chạy toàn bộ suite legacy ngay.

Mỗi run cần: source commit, dataset filenames/version/checksums, group/time split IDs, history length, seed list, Python/package lock, hardware, command, config, stderr/stdout, per-series predictions và metric implementation hash. Dùng cùng split cho paired comparison; report mean, dispersion và group bootstrap nếu đủ groups. Runtime/VRAM hiện UNKNOWN; bắt đầu bằng smoke subset có stop cap do người chạy chọn, sau đó mới ước lượng full budget.

Không có kết quả thực nghiệm nào trong tài liệu này.

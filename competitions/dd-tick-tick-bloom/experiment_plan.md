# Kế hoạch kiểm chứng — Bloom

Chưa chạy experiments; chưa có official data/imagery trong workspace. Trạng thái partial/conceptual; full reproduction blocked ở archive equivalence, API snapshots và compute budget.

1. **Metric vs selection:** tạo CPU toy checks macro-regional RMSE và rounding; sau đó so model-selection theo pooled vs region-average OOF trên cùng splits.
2. **Spatial CV:** UID GroupKFold vs lake/location-disjoint holdout. Giữ feature acquisition, seed và model; báo score từng vùng và khoảng cách train-test. Reject giả thuyết CV tốt nếu advantage mất ở unseen-area holdout.
3. **Scene weighting:** current per-record mean vs equal satellite-family mean, rồi round. Giữ predictions cố định, không retrain; report coverage và số scenes/uid. Gain thiếu stability theo vùng là giới hạn.
4. **Rounding:** nearest integer vs top-one custom thresholds, threshold fit chỉ trong inner folds, outer geographic folds bất biến. Không tune trên final test.
5. **Imagery/no imagery routing:** same-budget tabular/weather/KNN/imagery ablations theo vùng. Muốn chứng minh model routing hữu ích phải đo interaction region×features, không chỉ overall score.
6. **Edge cases:** image missing toàn vùng, zero KDTree distance, mask interpolation và green/blue ratio denominator0. Faithful behavior được ghi lại trước khi đề xuất sửa. Những sửa đổi là experiments mới, không gọi reproduction nguyên bản.

Manifest mỗi run: original labels hash, uid/location split files, satellite platform/acquisition timestamps/bands/projection/scale và request/cache hash; code commit/env; seed; commands; hardware/cost logs; raw/rounded per-uid predictions; scorer version. Không mở rộng request dataset nếu chưa kiểm tra quyền truy cập và disk/network budget.

Chi phí chưa đo. Bắt đầu một subset CPU một vùng/mộtfold để ước lượng training và I/O, sau đó xác định budget; không mặc định500 boosters hoặc tải lại toàn bộ imagery.

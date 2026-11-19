# Kế hoạch kiểm chứng — Hateful Memes

Chưa chạy model, chưa có dataset agreement được accept. Full reproduction blocked; numerical checks và static code audit có thể làm ngay.

| Test | Intervention | Controls / outcome |
|---|---|---|
| HM-1 | Mean probability vs majority+max/min | Cùng model prediction CSVs và ID alignment; ROC-AUC, accuracy, Brier/ECE riêng; không chọn rule bằng final test |
| HM-2 | Row permutation / missing model CSV | Synthetic fixtures, assert exact ID set/ordering và expected number of models; reject silent positional misalignment |
| HM-3 | Add data components | Original train vs +dev_seen-only vs +manual Memotion; same outer confounder-aware holdout và compute; report mean/variance |
| HM-4 | Diversity | Best single family, within-family ensemble, cross-family ensemble; matched budgets where feasible, OOF correlation và leave-one-out |
| HM-5 | Rule override | Same ensemble proba with/without top-one rule; subgroup false positive/negative và calibration khi có annotation được phép | 
| HM-6 | Selection bias | Inner sweep/top 27 vs untouched outer holdout; compare number of candidates and selection variance |

H1 “voting experts cải thiện generalization” bị bác bỏ nếu chỉ dev score tăng hoặc AUC outer giảm. H2 “rule đáng chuyển giao” không được xác nhận bằng aggregate leaderboard score; cần error slices và sự phù hợp với task thực tế. Không triển khai demographic heuristic mặc định.

Trước model runs: xác minh license dataset/external annotations/checkpoints; pin MMF/feature extractors/tokenizer, Docker digest và dependency lock; data/feature hashes; mapping ID và confounder groups; tạo run manifest gồm command/config/seed/hardware/time/logs/raw CSVs. Không biết budget thì thử một checkpoint/subset trước; không tự chạy96-config sweep hoặc27-model inference.

Các số AUC trong report là published results; tài liệu này chưa có result tự đo.

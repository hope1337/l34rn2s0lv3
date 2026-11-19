# Hateful Memes Phase 2 — pilot ảnh–văn bản

Audit 19/11/2026. Edition2020, **Phase 2 final evaluation**, không gộp Phase 1 ongoing practice. Nghiên cứu nguồn tĩnh partial. [Pipeline](pipeline.md), [evidence](evidence.json), [sources](sources.md), [experiments](experiment_plan.md), [review](quality_review.md), [state](state.json).

## A — Task và protocol

Input: meme ID, ảnh và text đã được cung cấp; không cần OCR để lấy text classification cơ bản. Output probability hateful và binary label. Phase 2 dùng `test_unseen`, tối đa3 submissions, final prize ranking theo best ROC-AUC. Phase 1 public test không quyết định prize. Timeline official01–31/10/2020. [memes-task]

OCR của top-one có mục đích khác: mask/inpaint text khỏi ảnh để trích visual features, không mâu thuẫn với việc task đã cung cấp text. Không dùng câu “OCR required” cho toàn competition. [memes-preprocess]

## B — Dataset

JSONL `train`, `dev_seen`, `dev_unseen`, `test_seen`, `test_unseen`; ảnh trong img; join bằng ID/path. Train/dev có label0/1; test không có label. Official page có câu “three files” nhưng ngay sau đó liệt kê năm JSONL: report giữ danh sách explicit, không truyền lại con số cũ. Có overlap giữa dev sets theo official description. [memes-task]

Dataset access agreement riêng, khác license code; dự án chưa accept, tải ảnh hay xác minh link download còn hoạt động. Các external datasets/annotations/features của đội thi cũng cần kiểm tra riêng. [memes-access]

## C — Metric

Ranking maximize ROC-AUC trên cột `proba`; accuracy tính từ `label` chỉ để tham khảo. Schema bắt buộc id/proba/label. [memes-metric]

Biểu diễn toán học binary AUC để giải thích ranking:

\[
\operatorname{AUC}=\frac1{n_+n_-}\sum_{i:y_i=1}\sum_{j:y_j=0}
\left[\mathbf1(p_i>p_j)+\tfrac12\mathbf1(p_i=p_j)\right].
\]

Đây là diễn giải toán học chuẩn cho empirical ROC-AUC, không phải xác nhận mọi chi tiết scorer server. Monotonic transformation **strictly increasing chung cho mọi sample** giữ thứ hạng/AUC; chọn label threshold riêng có thể thay accuracy mà không thay AUC nếu proba không đổi. Ngược lại voting rồi lấy max/min probability có thể đổi ranking giữa samples, không đơn thuần calibration. UNKNOWN: clipping, NaN rejection, treatment của malformed probabilities trong evaluator triển khai.

## D — EDA riêng cho multimodal confounders

Không có measured EDA. Cần đo image/text pairing integrity và IDs giữ leading zeros/path mappings; image size/channels, text length/language/tokenization truncation; label distribution và overlap theo từng split; exact/near-duplicate ảnh và text **riêng rẽ**; confounder pairs khác label; subgroup error/calibration nếu có annotation được phép dùng. Đơn vị đo là meme, nhưng split cần xét nhóm confounders/template chứ không chỉ meme ID.

Script của HateDetectron ghi published counts8500 train +100 dev_seen-only +328 manual Memotion=8928; code assert dev_seen-only100, dev_unseen-only140. Đây là **tác giả mô tả và assertion trong code**, chưa là measurement của dự án. [memes-expanded-data]

## E — Baselines

Official repository dẫn MMF starter và benchmark blog. Chưa chạy text-only/image-only/fusion baseline, không ghi score không xác minh. Text-only và image-only đặc biệt hữu ích để kiểm tra model có học tương tác hay chỉ shortcut; phải đánh giá trên confounder-aware holdout. [memes-baseline]

## F — Kết quả cuối

Repository tổ chức ở commit `0cc41becf86a83e8b0e9df34886e1bb506f9762b` công bố bảng Phase 2 dưới đây; cột chỉ ghi **Score**, không tự thêm public/private labels không có trong bảng. [memes-results]

| Rank | Team | Score ROC-AUC |
|---:|---|---:|
| 1 | alfred lab | 0.8450 |
| 2 | Muennighoff | 0.8310 |
| 3 | HateDetectron | 0.8108 |
| 4 | kingsterdam | 0.8053 |
| 5 | burebista | 0.7943 |

Code thật nằm ở các repo tác giả; kho tổ chức chủ yếu chứa links/PDF. Pipeline report pin riêng code top-one/top-three. Không gộp current repo HEAD với phiên bản chắc chắn đã chạy2020.

## G — Pipeline

[Pipeline](pipeline.md) mô tả top-one preprocessing và một cấu hình UNITER, ensemble/rule cuối; top-three data extension, sweep, checkpoint selection và exact majority vote max/min; top-two được so từ author README nhưng chưa pin/trace training code nên partial.

Điểm forensic đáng chú ý: top-one ensemble average probabilities nhưng giữ label column từ CSV đầu, rồi rule override proba mà không recompute label. Top-three notebook concat theo vị trí dòng, hardcode majority cutoff13 và có exception swallowing. Đây là implementation observations, không chứng minh file final trên leaderboard có lỗi. [memes-alfred-ensemble; memes-vote-code]

## H — Reverse engineering

**Top-one thêm ERNIE-ViL:** tác giả nói mục tiêu là diversity, không chủ yếu cải tiến riêng model. Giả thuyết decorrelated errors cần OOF correlation và remove-one-member ablation; có thêm architecture không tự chứng minh diversity hữu ích. [memes-diversity]

**Top-three chọn majority rồi max/min:** tác giả đưa rationale “experts” theo loại hate. Code cho thấy rule đúng là positive-majority lấy max, negative-majority lấy min. Cơ chế giả thuyết: tăng separation nhóm có quyết định thống nhất, nhưng có thể đẩy false positive rất tự tin và đổi ranking xấu. Cần so mean-proba và voting trên nested heldout; không coi diễn giải authors là causal proof. [memes-vote-rationale; memes-vote-code; memes-vote-hypothesis]

## I — Validation / leakage

Top-three loại phần dev_seen trùng dev_unseen trước mở rộng train; đó chỉ là ID/image-path overlap, chưa kiểm tra template/near-duplicate hoặc confounder pairs. Sweep và chọn27 best dựa dev_unseen lặp đi lặp lại có selection bias; cần outer holdout để ước lượng generalization. Không gọi việc dùng dev_seen-only là leakage vào hidden test khi chưa có bằng chứng. [memes-expanded-data; memes-sweep]

Top-one config mẫu train trên train_dev_all và validation dev_seen; cần đọc database building chính xác để biết membership, không suy từ filename rằng mọi ensemble component có validation độc lập. [memes-uniter-config]

## J — Ablation / evidence

Published final scores verified; code mechanism verified trong scope đã đọc. Chưa audit toàn bộ papers/ablation tables và chưa chạy comparisons. Không quy gap0.014 giữa top 1/top 2 cho demographic tags, inpainting, backbone hay rule riêng lẻ.

## K — Failures

Các lỗi cần xem: text-only shortcut, confounder mới, OCR/inpaint làm mất ngữ cảnh, missing entity service, false positive của keyword/demographic heuristic, ID row mismatch, low-confidence probability tails. Chưa có subgroup rates đo ở đây. Top-one rule có assumptions mạnh về demographic tags, nên không mặc định chuyển nó thành moderation production policy. [memes-rule-risk]

## L — Compute / reproducibility

Top-one README công bố GCP n1-highmem16, RAM104 GB, 4 T4, 500 GB disk và fp16; một số bước có thể chạy1 T4, VL-BERT cần4 T4 theo tác giả. Không coi đây là budget đã cấp cho dự án. Top-three notebook pin torch1.6/torchvision0.7 nhưng clone MMF no_feats branch không pin commit, có đường dẫn Colab hardcoded và signed URL lịch sử. Không chạy nguyên notebook. [memes-hardware; memes-legacy]

End-to-end notebook top-three vượt giới hạn snapshot8MB, chưa đọc training/feature extraction đầy đủ. Inference notebook, scripts sweep/data extension đã đọc. Missing assets/service/version là blockers thật, không chỉ “cần thêm GPU”.

## M — Cross-team

| Team | Representation / model | Aggregation | Hạn chế audit |
|---|---|---|---|
| alfred lab | Clean image + RoI/entity/tags; extended VL-BERT, UNITER/VILLA, ERNIE-ViL | Mean selected CSVs rồi rule override | Exact chosen models và đầy đủ dependency/defaults chưa trace |
| Muennighoff | RoI features; one-stream và two-stream V+L models | Average predictions | README đọc nhưng code commit/training trace chưa hoàn thành |
| HateDetectron | Detectron visual features + VisualBERT; bổ sung labeled data | Top27 dev models, majority class rồi extreme proba | Full end2end notebook chưa đọc; checkpoint availability chưa test |

Nguồn: [memes-results], [memes-top-two], [memes-preprocess], [memes-vote-code]. Không gọi one-stream chắc chắn tốt hơn nói chung chỉ từ author narrative.

## N — Knowledge

Giữ probability ranking và binary decision như hai artifacts riêng; phép gộp probabilities, row alignment và bước rule cuối có thể đổi metric. Data expansion phải giữ dev/test isolation theo nhóm phù hợp, không chỉ ID. Các observation này có provenance trong knowledge cards, chưa có reproduced gain.

## O — Unknowns

Dataset permission/current access; exact winning component CSVs và order/hashes; preprocessing model versions/weights; MMF defaults/tokenization/loss; full training trace; independent ablations; subgroup robustness. Audit hiện self-review, report partial. Không có measured EDA hoặc reproduction result.

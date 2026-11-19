# AI Competition Research Lab

> **MASTER PROJECT BRIEF / IMPLEMENTATION SPECIFICATION**  
> Phiên bản: `v0.1` — tổng hợp từ cuộc trao đổi ngày **18/11/2026**.  
> Ngôn ngữ tài liệu: Tiếng Việt; prompt lõi cho AI agent: Tiếng Anh.  
> Mục đích: Cung cấp **đủ bối cảnh, mục tiêu, yêu cầu, nguyên tắc, checklist, kiến trúc gợi ý và roadmap** để một AI coding/research agent có thể triển khai dự án từng bước mà không cần đọc lại cuộc hội thoại.

## 0. Cách đọc tài liệu này

- **[YÊU CẦU CỦA USER]**: điều người dùng trực tiếp yêu cầu; không được tự ý lược bỏ.
- **[ĐỀ XUẤT]**: những ý tưởng/thiết kế mà assistant đề xuất trong cuộc trao đổi; được dùng làm mặc định ban đầu nhưng có thể tinh chỉnh bằng bằng chứng.
- **[CHƯA XÁC MINH]**: thông tin cần agent tra cứu và kiểm chứng trước khi xem là sự thật.
- **[CẦN QUYẾT ĐỊNH]**: chưa được chốt; agent không nên giả định user đã lựa chọn.

**Quan trọng:** Đây là bản đặc tả/định hướng nghiên cứu. Danh sách nguồn bên dưới là các **đầu mối khám phá**, chưa phải danh sách hàng trăm competition được kiểm định xong. Các ví dụ về kỹ thuật, điểm số, quy trình và metadata là **ví dụ hoặc thiết kế đề xuất**, không phải kết quả thống kê đã được thực hiện.

---

# PHẦN I — BỐI CẢNH, MỤC TIÊU VÀ TRIẾT LÝ

## 1. Động cơ hình thành dự án

**[YÊU CẦU CỦA USER]** Người khởi xướng là một **Machine Learning researcher**, đã có nền tảng nghiên cứu nhưng tự thấy còn thiếu nhiều kỹ năng **áp dụng ML/AI vào tình huống thực tế**. Mong muốn xây dựng một Project để:

1. Tìm và tìm hiểu những cuộc thi AI/ML uy tín, chất lượng tại Việt Nam và quốc tế.
2. Hiểu chính xác bài toán, bộ dữ liệu, metric, baseline và những ràng buộc thực tế.
3. Phân tích sâu cách các đội đứng đầu giải quyết bài toán.
4. Tìm hiểu và học các phương pháp/kỹ thuật của đội top, kể cả những chi tiết triển khai tưởng chừng rất nhỏ.
5. Reverse engineering lý do lựa chọn phương pháp, phân biệt bằng chứng công bố và suy luận của agent.
6. Dần phát triển khả năng giải quyết bài toán ML mới một cách chủ động, có căn cứ thực nghiệm.
7. Tích lũy kho kiến thức lớn phục vụ **học tập lâu dài**; **không ngại vài trăm hay hàng nghìn competition** nếu đủ giá trị.

**[ĐỀ XUẤT]** Tên làm việc: **AI Competition Research Lab**, có thể được hiểu như một **AI Competition Intelligence & Research System**.

Không chỉ là tập hợp winning write-ups, mà phải là một hệ thống **nghiên cứu, kiểm chứng và tích lũy tri thức ML có thể tái sử dụng**.

## 2. Sự khác nhau giữa đọc paper và giải bài toán thực tế

Quy trình ML research thường được mô tả ngắn gọn:

`Paper → Architecture → Training → Evaluation`

Trong các competition và dự án thực tế, thường phải đối mặt với chuỗi quyết định phức tạp hơn:

`Problem Understanding → Data Understanding & Validation → Baseline & Experimentation → Optimization & Engineering → Robust Solution`

Bao gồm:

- Hiểu objective thực sự và các giới hạn của bài toán.
- EDA và chất lượng/độ tin cậy của labels.
- Data leakage, distribution shift và chiến lược validation.
- Thiết kế baseline, experiment, ablation và error analysis.
- Sampling, preprocessing, augmentation, loss, optimization, inference, ensemble.
- Computational cost, latency, robustness, reproducibility và khả năng triển khai.

**Luận điểm chính:** Đội top không nhất thiết thắng nhờ kiến trúc mới/phức tạp hơn. Đôi khi khác biệt lớn nằm ở validation, preprocessing, augmentation, postprocessing, ensemble, cách đánh giá lỗi hoặc một phép tính nhỏ.

## 3. Các nguyên tắc xuyên suốt

1. **Evidence first:** Mọi phát biểu thực nghiệm hay mô tả chi tiết pipeline cần nguồn kiểm chứng.
2. **Implementation-level, không chỉ concept-level:** “Dùng YOLO + Mosaic + AdamW + ensemble” là mô tả chưa đủ. Cần truy ra cách triển khai thực tế, trình tự và parameters.
3. **Không bịa thông tin:** Không tự suy diễn thành “facts” khi thiếu source, code, data hoặc cấu hình.
4. **Ba mức nhận định:** `VERIFIED`, `INFERRED/HYPOTHESIS`, `UNKNOWN` (chi tiết ở phần Reverse Engineering).
5. **Không mặc định winner luôn đúng:** Tách chiến thuật tối ưu leaderboard khỏi phương pháp robust và production-ready.
6. **Ưu tiên khả năng tái hiện:** Bất cứ chi tiết nào còn thiếu phải ghi nhận rõ là blocker/unknown.
7. **Chú trọng tính chuyển giao:** Không chỉ “đội A đã làm gì”, mà “khi nào, tại sao, điều kiện nào kỹ thuật đó hữu ích”.
8. **Không gộp các phiên bản khác nhau:** Tách `competition × year × track × evaluation version` nếu khác nhau.
9. **Học từ cả thất bại:** Thu thập những quyết định hoặc experiments thất bại nếu có bằng chứng.
10. **Cần cơ chế kiểm tra chéo:** Việc agent đưa ra câu trả lời dài không đồng nghĩa với nghiên cứu đầy đủ.

## 4. Tầm nhìn kết quả dài hạn

Sau khi phân tích nhiều competition, hệ thống không chỉ trả lời:

> “Top 1 của competition X làm gì?”

mà phải có khả năng trả lời:

> “Với bài toán object detection có severe class imbalance, các winning solutions thường làm gì, tại sao, trong điều kiện nào, có ablation chứng minh không, và cost/latency ra sao?”

Một số câu hỏi kiến thức muốn tích lũy:

- Khi nào pseudo-labeling giúp generalization? Khi nào có hại?
- Vì sao Group K-Fold có thể tốt hơn random K-Fold ở dataset có nhóm tương quan?
- Diversity giữa các mô hình đóng góp thế nào vào ensemble?
- TTA cải thiện bao nhiêu so với chi phí inference?
- Hard example mining giúp gì, và khi nào gây bias?
- Cách chuyển kỹ thuật từ competition sang hệ thống thực tế có hạn mức GPU/latency/maintenance?

---

# PHẦN II — PHẠM VI: 2 TASK CHÍNH BAN ĐẦU VÀ 2 TASK TIẾP NỐI

## 5. Phạm vi ưu tiên

### Task 1 — Competition Discovery & Curation **[YÊU CẦU CỦA USER]**

**Mục tiêu:** Lập danh sách lớn, có sàng lọc kỹ, gồm các competition ML/AI uy tín và đáng nghiên cứu từ Kaggle, Zalo AI, VinAI/VinBigData và nhiều hệ sinh thái khác ở Việt Nam, quốc tế. Không đặt giới hạn vài chục competition. **Độ sâu và chất lượng xác minh quan trọng hơn tốc độ.**

### Task 2 — Deep Competition & Top Solution Analysis **[YÊU CẦU CỦA USER]**

Thiết lập prompt/tiêu chuẩn nghiên cứu để agent phân tích **ít nhất 7 nội dung**:

1. Giải thích tác vụ.
2. Sơ lược bộ dữ liệu.
3. Giải thích đánh giá/metric, các thành phần ảnh hưởng và cơ chế ảnh hưởng.
4. Thống kê dữ liệu theo đúng modality và theo từng competition; không dùng checklist chung một cách máy móc.
5. Kết quả các đội top.
6. Pipeline cực kỳ chi tiết, **không bỏ sót chi tiết quan trọng**, kể cả normalization, thao tác cộng/trừ/nhân/chia, thresholds, thứ tự transforms, casts, reductions, postprocessing v.v.
7. Reverse Engineering: Tại sao chọn phương pháp/kỹ thuật? Sử dụng giải thích từ đội top nếu có; khi không có thì agent có thể tự đưa ra giả thuyết khoa học, **nhưng phải gắn nhãn là suy luận chứ không phải sự thật được xác nhận**.

### Task 3 — Reproduction & Experimental Verification **[ĐỀ XUẤT]**

- Reproduce baseline/solution trong điều kiện hợp pháp, khả thi.
- Kiểm chứng các giả thuyết bằng experiments và ablations.
- Ghi lại code, environment, compute, logs, chi phí và những kết quả không thành công.

### Task 4 — Knowledge Synthesis & Retrieval **[ĐỀ XUẤT]**

- Chuẩn hóa kỹ thuật thành knowledge cards.
- Liên kết kỹ thuật, dữ liệu, bài toán, điều kiện áp dụng, tradeoffs và bằng chứng qua nhiều competition.
- Xây dựng hệ thống search/query về transferable ML knowledge.

**Thứ tự:** Ưu tiên Task 1 và Task 2 trước. Task 3 và Task 4 không bị quên, nhưng có thể triển khai dần khi quy trình Task 1–2 đã vững.

---

# PHẦN III — TASK 1: COMPETITION CATALOG

## 6. Các nguồn cần tìm kiếm

Danh sách nguồn ban đầu được đề cập trong cuộc trò chuyện, **không giới hạn ở đây**:

| Nguồn | URL tham khảo | Lĩnh vực/giá trị tiềm năng |
|---|---|---|
| Kaggle Competitions | https://www.kaggle.com/competitions | Tabular, CV, NLP, forecasting; discussion, notebook, winning write-ups |
| DrivenData | https://www.drivendata.org/ | Bài toán xã hội/thực tế; một số winning solutions có code |
| DrivenData competition winners | https://github.com/drivendataorg/competition-winners | Kho code winning solutions để phân tích/tái hiện |
| AIcrowd Challenges | https://www.aicrowd.com/challenges | RL, agents, robotics, NLP, research challenges |
| Grand Challenge | https://grand-challenge.org/challenges/ | Medical imaging, segmentation, detection, clinical AI |
| EvalAI | https://eval.ai/ | Benchmark, perception, multimodal, reasoning |
| NeurIPS Competitions | https://blog.neurips.cc/2026/07/28/neurips-2026-competitions-announced/ | Competition gắn với nghiên cứu mới; phải tìm từng track/year |
| AI City Challenge | https://www.aicitychallenge.org/ | Tracking, traffic/video understanding, ứng dụng CV |
| SemEval | https://semeval.github.io/ | NLP shared tasks; system-description papers |
| Zalo AI Challenge | https://challenge.zalo.ai/ | Bài toán ứng dụng, AI tiếng Việt, speech, agentic AI |
| VLSP | https://vlsp.org.vn/ | Vietnamese NLP/speech/shared tasks |
| HCMC AI Challenge | https://aichallenge.hochiminhcity.gov.vn/ | Bài toán AI ứng dụng trong nước |
| AIHUB.ML Competitions | https://aihub.ml/competitions/ | Cộng đồng Việt Nam, shared tasks |
| VinBigData Kaggle competition | https://www.kaggle.com/competitions/vinbigdata-chest-xray-abnormalities-detection | Ví dụ medical object detection có nguồn công khai |

**Nguồn tổng hợp/winning solutions cũng đã được nhắc đến:**

- GitHub: `TaeyanG4/kaggle-top-solutions-and-strategies` — cần xác minh URL, tình trạng cập nhật, license, độ đầy đủ.
- GitHub: `juliusuhlmann/kaggle-first-place-solutions` — cần xác minh URL, phạm vi, ngày cập nhật, độ tin cậy.
- Kaggle “Solution Write-up” documentation — tra cứu URL chuẩn và lịch sử thay đổi.

**Lưu ý định danh:** VinAI và VinBigData không được mặc nhiên coi là cùng một đơn vị tổ chức competition. Một cuộc thi do VinBigData tổ chức trên Kaggle đã được nhắc đến, nhưng **chưa xác minh một cổng competition tương đương thuộc VinAI**. Agent phải phân biệt organizer/sponsor/platform.

**Lưu ý thời gian:** Tại ngày 18/11/2026, một số competition 2026 có thể chưa kết thúc hoặc chưa có kết quả chính thức; không được suy đoán người chiến thắng, leaderboard cuối cùng hoặc mô tả winning solution khi chưa công bố.

**Discovery nên mở rộng** sang các hội nghị và cộng đồng liên quan (thông qua tìm kiếm có xác minh), không tự động coi mọi benchmark leaderboard là competition. Có thể khảo sát thêm CVPR/ICCV/ECCV workshops, MICCAI, ISBI, WMT, IWSLT, các challenge audio/speech, time series, recommender systems, robotics, multimodal và các giải trong nước khác.

## 7. Hai lớp catalog

### 7.1. Discovery Catalog

Kho đầu vào quy mô lớn, có thể là hàng trăm/hàng nghìn entry. Một entry tối thiểu phải có:

- Định danh và URL chính thức hoặc nguồn đủ tin cậy để truy vết.
- Organizer, platform, year, track, trạng thái tổ chức.
- Modality và task sơ bộ.
- Tình trạng kiểm chứng / ngày kiểm chứng.

Không nên xóa competition chỉ vì không đủ write-up; cần giữ như mục `archive / needs audit / low analysis feasibility`.

### 7.2. Curated Research Catalog

Danh sách đã qua audit, có nhận định chất lượng và mức độ phù hợp:

- Dữ liệu có thể truy cập theo quy định hay không?
- Metric và rules có đủ rõ?
- Có final leaderboard chính thức và phân biệt public/private?
- Có top solution write-ups/papers/code/config/checkpoints?
- Mức tái hiện có khả thi không?
- Competition còn ý nghĩa học tập với kỹ thuật hiện tại không?
- Có vấn đề về leakage, gian lận hoặc license không?

## 8. Quality scoring đề xuất: 100 điểm

| Tiêu chí | Trọng số |
|---|---:|
| Chất lượng và độ rõ ràng của task/evaluation | 15 |
| Độ sâu của top solution write-ups | 20 |
| Code công khai và khả năng tái hiện | 20 |
| Dataset access và khả năng phân tích | 15 |
| Giá trị kỹ thuật/kiến thức mới | 15 |
| Giá trị thực tế/khả năng chuyển giao | 10 |
| Độ tin cậy của organizer và kết quả | 5 |
| **Tổng** | **100** |

**Tiers đề xuất:**

- `A (80–100)`: Nên ưu tiên phân tích và reproduce sâu.
- `B (60–79)`: Có giá trị; bị giới hạn ở một vài nguồn hoặc độ tái hiện.
- `C/Archive (<60)`: Tham khảo hoặc đánh giá lại sau.
- `UNRATED`: Chưa đủ bằng chứng; không gán điểm giả định.

**Chấm điểm phải có justification và evidence** cho từng tiêu chí, không đơn thuần trả về số. Trọng số và cutoffs là heuristic ban đầu, cần calibration sau một số cuộc thi mẫu.

**Không cho điểm cao vượt qua red flags một cách tự động:** sự thiếu minh bạch, cheating, license restrictions, không có final results xác thực v.v. cần cảnh báo riêng.

## 9. Metadata schema đề xuất

```yaml
id: kaggle-vinbigdata-cxr-2021
title: VinBigData Chest X-ray Abnormalities Detection
platform: Kaggle
organizer: VinBigData
year: 2021
track: main
competition_url: https://www.kaggle.com/competitions/vinbigdata-chest-xray-abnormalities-detection

domain: Medical Computer Vision
task: Object Detection
modalities: [Medical Image]
status: Finished

data_access: Check required
solution_writeups: To be audited
winning_code: To be audited
reproducibility: Unknown

learning_value:
  - Medical image detection
  - Annotation quality
  - Evaluation methodology

research_status: Not Started
quality_score: null
quality_tier: UNRATED
last_verified_at: null
sources: []
```

**Cần phân biệt fields** `unknown`, `not_applicable`, `not_public`, `not_checked` và `verified`. Không gộp tất cả thành `false`.

Schema mở rộng nên chứa:

- Original name, alias, unique id, canonical link.
- Year/track, organizer, platform, official dates, competition status.
- Language, domain, task type, modality, input/output, number of classes/targets (nếu xác minh).
- Metric name + chính xác cách aggregate.
- Rules: pretrained/external data/compute/team/submit restrictions.
- Dataset links, access requirements, license, size (nếu có evidence).
- Official leaderboard, public/private split, score direction.
- Top teams, ranks, team pages, write-ups, papers, Github code, config, model weights.
- Availability/reproducibility level, audit evidence, blockers, quality score per criterion.
- Knowledge tags, duplicate/related competitions, status research pipeline.
- Last verification time, source timestamps, history of changes.

## 10. Acceptance criteria Task 1

- Có danh sách các platform/organizer nguồn với URL có thể kiểm chứng.
- Mỗi competition có ID ổn định và traceable sources.
- Không nhập trùng year/track hoặc đánh đồng các track khác nhau.
- Có schema và validator cho metadata.
- Có quy trình discovery → verify → score → curate.
- Có backlog rõ các competition chưa thể xác minh.
- Có thể lọc theo task, modality, year, score tier, availability, code availability, status.
- Đối với competition được đưa vào danh sách curated, ghi lại **lý do được chọn** và **giới hạn thông tin**.
- Có cơ chế incremental updates để bổ sung nguồn và competition mà không phá schema.

---

# PHẦN IV — TASK 2: DEEP RESEARCH & SOLUTION ANALYSIS

## 11. Những mục phân tích bắt buộc

Dưới đây là **7 yêu cầu của user**, được mở rộng thành bộ module phân tích đầy đủ (đề xuất 15 module). Không bỏ bất kỳ nhóm nội dung nào.

### Module A — Competition Context & Task Definition

- Nguồn gốc bài toán, bối cảnh ứng dụng thực tế và tác động nếu giải tốt.
- Input, output, target, đơn vị dự đoán (sample/image/sequence/patient/session...).
- Scope, assumptions, loại bài toán; phân biệt multi-label/multiclass/multi-task.
- Official rules, restrictions, external data/pretraining, evaluation budget, submission count, thời gian, track-specific conditions.
- Định nghĩa chính xác thành công và giới hạn thực tế.

### Module B — Dataset Overview

- Dataset nguồn gốc, đối tượng thu thập, data collection/annotation pipeline nếu có.
- Train/validation/test/public/private split, label availability, file types.
- Schema, units, size, licensing/access, dataset version.
- Domain shift, duplicate/near-duplicate, noise, spurious correlations.
- Những gì chưa được công khai và ảnh hưởng của chúng đến phân tích.

### Module C — Evaluation Metrics: Mathematical & Operational Analysis

- Viết **công thức metric**, giải nghĩa từng thành phần, direction maximize/minimize, aggregation, weights.
- Truy vết cách official evaluator xử lý rounding, thresholds, empty cases, NaN, clipping, mask, ignore label, per-group scoring.
- Những loại lỗi nào metric phạt nặng/nhẹ? Vì sao? Có sensitivity analysis hoặc toy numeric example nếu hữu ích.
- Khác nhau giữa offline metric và leaderboard scorer, public/private scores.
- Các yếu tố có thể cải thiện metric mà không thật sự cải thiện ứng dụng thực tế.
- Nếu evaluator code có sẵn, phân tích code chứ không chỉ diễn giải tên metric.

### Module D — Modality-Specific EDA & Statistics

**Không dùng cùng checklist cho mọi dạng dữ liệu**. Chọn theo task và dataset thực tế; chỉ đưa ra con số khi đã được tính hoặc có nguồn rõ.

| Loại dữ liệu | Thống kê / phân tích cần cân nhắc |
|---|---|
| Tabular | Row/column count, dtypes, missingness, cardinality, imbalance, skewness, outliers, target correlations, drift, groups, leakage |
| Image/CV | Resolution, aspect ratio, classes/labels, bbox sizes/aspect ratios, object density, annotation noise, brightness/color statistics, duplicates, source-camera/patient groups |
| Segmentation | Mask coverage, foreground ratio, boundary characteristics, per-class area, empty masks, connected components |
| Text/NLP | Language mix, token/word lengths, class distribution, duplicates, OOV, truncation ratio, label ambiguity, train-test vocabulary drift |
| Audio/Speech | Duration, sampling rate, channels, SNR/noise, silence ratio, speaker distribution, accents/language, spectrogram statistics |
| Time series | Length/frequency, missing timestamps, seasonality, trend, autocorrelation, drift, entities, leakage across time, horizon distributions |
| Graph | Nodes/edges, density, degree, communities, connected components, leakage via graph links, label homophily |
| Multimodal | Coverage by modality, alignment quality, missing modalities, correspondence integrity, modality leakage |
| Recommender | Users/items/interactions, sparsity, activity skew, cold-start, temporal leakage, user-item overlap |

Thiết kế thêm thống kê chuyên biệt khi bài toán yêu cầu (ví dụ bounding box localization, patient-level split, cross-lingual contamination, rare event frequency).

### Module E — Baseline & Feasibility

- Official starter baseline và score.
- Những baseline đơn giản hợp lý nếu không có baseline chính thức.
- Hardware/compute/time/reproducibility assumptions.
- Điểm yếu baseline và cơ hội nâng cấp.
- Không tự bịa baseline performance.

### Module F — Top Teams & Final Results

- Final official standings, team identity/rank, private/public score khi có.
- Link đến code, papers, notebooks, videos, write-ups.
- Cảnh báo khi chỉ có leaderboard tạm thời hoặc khi top results bị thay đổi/invalidated.
- Phân biệt team solution và các bản fork/third-party reproductions.

### Module G — Pipeline Forensic Reconstruction (TRỌNG TÂM)

Mục tiêu: reconstruct **execution-level pipeline** cho từng đội được chọn (thường top 1/2/3 và một vài phương pháp khác biệt), không chỉ liệt kê buzzwords.

**Các tầng cần kiểm tra:**

1. **Raw data:** origin, exact version, file format, encoding, metadata, checksum nếu khả thi.
2. **Loading/Parsing:** readers, dtypes, missing values, defaults, channel orders, coordinate conventions.
3. **Cleaning/Filtering:** rows/files removed, conditions, duplicates, label corrections, outlier treatment.
4. **Preprocessing:** resize/interpolate, crop, padding, clipping, scaling, normalization, standardization; exact order and constants.
5. **Split/Validation construction:** random/group/time stratification, folds, seeds, contamination/leakage safeguards.
6. **Sampling & DataLoader:** weighting, batch composition, sampler, shuffle, worker seeds, drop_last, caching.
7. **Augmentation:** every transform, probability, ranges, schedule, order, train/test distinction; bbox/mask/label transform synchrony.
8. **Model:** full architecture, pretrained initialization, layers, adapters, custom heads, activation, tensor shapes/dimensions, checkpoints.
9. **Targets and loss:** label mappings, target assignment, loss formula, component weights, reduction (`sum`/`mean`), smoothing, masks, class weights, stability constants, numerical scaling.
10. **Training:** optimizer and all hyperparameters, LR schedule, warmup, gradient accumulation/clipping, mixed precision, EMA, freeze/unfreeze, epochs, batch size, effective batch size, randomness.
11. **Validation/checkpoint selection:** exact evaluation implementation, fold aggregation, model selection/early stopping logic, selection bias.
12. **Inference:** checkpoint loading, preprocessing parity, TTA, precision, batch size, decoding, thresholding, NMS/soft-NMS, calibration.
13. **Ensembling:** component models, fold/seed diversity, weights, prediction aggregation, ordering with postprocessing, tie breaking.
14. **Submission:** exact output schema, mappings, rounding/casts, clipping, serialization, formatting, final score generation.
15. **Infrastructure:** GPU type/count, memory, training time, distributed setup, software versions, dependencies, deterministic settings.
16. **Artifacts:** scripts, configs, run commands, pretrained weights, generated pseudo-labels, metadata and intermediate files.

**Các chi tiết nhỏ không được mặc định bỏ qua:**

- Chia `/255` trước hay sau chuyển dtype.
- RGB/BGR và normalization mean/std.
- Resize + padding vs resize trực tiếp.
- `sum` vs `mean` loss, eps, detach, clipping.
- Numerical precision, casting, rounding.
- Train vs validation vs test transforms.
- Thứ tự `ensemble → threshold` so với `threshold → ensemble`.
- NMS order, softmax/sigmoid, argmax thresholds.
- Seed, batch-level behavior, missing labels, grouping.
- Các phép cộng/trừ/nhân/chia tưởng đơn giản nhưng có thể làm lệch kết quả.

**Cách làm:**

- Bắt đầu từ write-up để hiểu ý tưởng, nhưng **đối chiếu source code, configs, dependencies, commit version và đường thực thi** nếu chúng tồn tại.
- Nếu viết lại pipeline từ code, ghi `file path + symbol/function + line/commit` khi có thể.
- Phân biệt pipeline “claimed in write-up”, “implemented in published code”, và “actually executed in winning run” nếu không trùng nhau.
- Nếu không có code, ghi rõ phần nào chỉ suy ra từ bài viết và phần nào chưa biết.
- Vẽ sơ đồ từng giai đoạn nếu hữu ích, nhưng sơ đồ **không thay thế specification chi tiết**.
- Đánh giá mức ảnh hưởng dự kiến của các chi tiết; không cho rằng mọi dòng code đều là điểm đột phá.

### Module H — Reverse Engineering: WHY, NOT ONLY WHAT

Với từng quyết định đáng kể, agent phải trả lời:

1. **Observation:** Đội thi đã làm gì? Nguồn nào chứng minh?
2. **Original rationale:** Tác giả có giải thích không? Trích/chỉ nguồn.
3. **Mechanism:** Về mặt ML/maths, kỹ thuật tác động đến vấn đề nào?
4. **Hypotheses:** Nếu tác giả không giải thích, agent đưa ra giả thuyết nào có cơ sở?
5. **Alternatives:** Có phương án nào cạnh tranh? Tradeoffs?
6. **Evidence:** Ablation/result nào chứng minh, hoặc có yếu tố gây nhiễu nào?
7. **Falsification:** Thí nghiệm tối giản nào có thể kiểm tra giả thuyết?
8. **When not to use:** Tình huống kỹ thuật này có thể vô ích hoặc gây hại.

**Ví dụ:** Đội top dùng Group K-Fold thay vì random K-Fold.

- `VERIFIED OBSERVATION`: Có code/description chứng minh Group K-Fold được dùng.
- `INFERRED`: Mẫu trong cùng group tương quan; random split có thể làm validation lạc quan.
- `EXPERIMENT`: So sánh splits, kiểm tra giao thoa nhóm và performance trên holdout tương ứng.

Không được biến “có khả năng” thành “đã được tác giả xác nhận”.

### Module I — Validation & Leakage Deep Dive

Tách riêng khỏi training pipeline vì cực kỳ quan trọng:

- Split methodology, unit of independence, group/time disjointness.
- Duplicate/near-duplicate, source leakage, patient/user/session overlap.
- OOF protocol, CV reliability, metric variance, confidence intervals nếu có.
- Public/private leaderboard correlation và nguy cơ overfitting leaderboard.

### Module J — Experimental Evidence & Ablation

- Bảng thí nghiệm được tác giả công bố, thay đổi và kết quả.
- Bằng chứng trực tiếp/gián tiếp, số lần lặp, variance, uncertainty.
- Counterfactual: không thể quy chênh lệch score giữa các team cho một kỹ thuật đơn lẻ nếu còn nhiều biến nhiễu.
- Thiết kế ablation có kiểm soát khi chưa có bằng chứng.

### Module K — Failure & Error Analysis

- Cases fail: class/group/size/lighting/language/accent/horizon/edge cases.
- Distribution shifts, annotation ambiguity, rare events, overconfidence/calibration.
- Những kỹ thuật thất bại hoặc bị loại bỏ (nếu tác giả có chia sẻ).

### Module L — Compute & Engineering Analysis

- Hardware, VRAM, latency, storage, energy/cost nếu có dữ liệu.
- Training/inference time, batch size, mixed precision, distributed training.
- Complexity/reproducibility constraints.
- “Competition-optimal vs production-ready” tradeoff.

### Module M — Cross-Team Comparative Analysis

- So sánh kỹ thuật chung và kỹ thuật khác biệt giữa top teams.
- Contrast validation, data, models, inference, ensembles, complexity, availability of code, score.
- Điều gì có bằng chứng causal, điều gì chỉ là correlation/observation.
- Tìm những phương pháp đơn giản nhưng hiệu quả và những quyết định phản trực giác.

### Module N — Transferable Knowledge Extraction

- Đúc kết nguyên lý có thể áp dụng sang bài toán khác.
- `when_to_use`, `why_it_works`, `requirements`, `failure_modes`, `evidence_level`, `source_competitions`, `compute_cost`.
- Liên kết với kiến thức nền: learning theory, optimization, statistics, domain shift, etc.

### Module O — Unresolved Questions & Quality Review

- Danh sách chưa biết và lý do không thể kết luận.
- Các source không truy cập được, mâu thuẫn giữa tài liệu và code.
- Các câu trả lời agent tự tin quá mức cần xác minh lại.
- Từng phần đánh dấu `complete / partial / blocked`, không tuyên bố đầy đủ nếu thiếu bằng chứng.

## 12. Evidence taxonomy & provenance

**Mức độ khẳng định bắt buộc:**

- **`VERIFIED`**: Có bằng chứng trực tiếp: official statement, code, config, dataset measurement, leaderboard, reproducible experiment. Dẫn nguồn đúng phạm vi. `VERIFIED` không có nghĩa kết luận nhân quả đã được chứng minh trừ khi experiment thực sự hỗ trợ.
- **`INFERRED` / `HYPOTHESIS`**: Agent suy luận có căn cứ; giải thích logic, giả định, competing hypotheses và cách kiểm tra.
- **`UNKNOWN`**: Không đủ thông tin; không sáng tác để lấp chỗ trống.

**Record mẫu:**

```yaml
claim_id: ex-001
claim: "The team used Group K-Fold for validation"
status: VERIFIED
source_type: code
source_url: null
file_path: src/train.py
symbol: build_folds
commit: unknown
lines: unknown
limitations: "Exact winning run configuration has not been verified"
```

Một nhận định về **lý do** sử dụng Group K-Fold là claim khác, có thể `INFERRED` ngay cả khi việc **sử dụng** Group K-Fold là `VERIFIED`.

## 13. Những câu hỏi cần đặt trong mọi bài phân tích

- Bài toán cần giải thực sự là gì? Metric reward/penalize điều gì?
- Dataset có những đặc tính nào chi phối quyết định model/training?
- Có leakage/validation mismatch nào không?
- Baseline mạnh đến đâu, cải tiến đóng góp bao nhiêu, có variance không?
- Các top teams đã làm gì ở **mức từng bước thực thi**?
- Tại sao kỹ thuật đó được chọn? Có giải thích trực tiếp hay chỉ suy luận?
- Có bằng chứng ablation hay chỉ correlation?
- Kỹ thuật đơn giản nào quan trọng không kém kiến trúc?
- Có phương án ít compute hơn mà gần tương đương không?
- Điều gì sẽ thay đổi khi đem dùng trong production?
- Kiến thức gì có thể dùng ở competition khác, trong điều kiện nào?
- Những thứ gì chưa biết và làm cách nào để tìm hiểu?

---

# PHẦN V — PROMPT & AGENT ARCHITECTURE

## 14. Không dùng một prompt khổng lồ cho mọi tác vụ

**[ĐỀ XUẤT]** Dùng **Research Orchestrator** điều phối các vai trò logic, mỗi vai trò có prompt chuyên biệt. Ban đầu **không bắt buộc nhiều agent thực tế**: một model chạy lần lượt các stage vẫn được.

Các vai trò:

1. **Competition Analyst:** task, rules, metrics, leaderboard.
2. **Data Analyst:** dataset, EDA theo modality, leakage, quality.
3. **Solution Analyst:** write-ups, code, pipeline forensic.
4. **Experiment Analyst:** baselines, ablation, reproducibility, compute.
5. **Reasoning Analyst:** mechanisms, competing explanations, hypotheses.
6. **Knowledge Curator:** extract, tag, compare transferable insights.
7. **Evidence & Quality Reviewer:** cross-check sources, contradictions, missing details, completeness (chức năng kiểm định xuyên suốt, không nhất thiết agent riêng).

Luồng làm việc:

```text
Competition Research Orchestrator
    ├── Competition Analyst
    ├── Data Analyst
    ├── Solution Analyst
    ├── Experiment Analyst
    ├── Reasoning Analyst
    └── Knowledge Curator
               ↓
      Evidence & Quality Review
               ↓
         Structured Artifacts
```

**Nguyên tắc kỹ thuật:** Bước phân tích nặng nên có **input/output contract rõ ràng**, state và progress có thể resume; không âm thầm trộn kết quả unverifiable vào phần Verified. Agent được phép dừng tại blocker và ghi unresolved TODO.

## 15. Master prompt đã đề xuất trong cuộc trò chuyện

Có thể lưu nguyên văn phần dưới làm `prompts/core.md` và phát triển thêm các prompt cho dataset, metrics, pipeline, reverse engineering, evidence audit, reproduction.

```markdown
# AI Competition Research Analyst — Core Instructions

## Role & Objective

You are a senior Machine Learning Research Scientist, ML Engineer, and Competition Solution Analyst.

Your objective is to investigate AI competitions in exceptional technical depth and extract reproducible, evidence-grounded, transferable machine learning knowledge.

Your task is NOT merely to summarize competition descriptions or winning solutions.

Your task is to reconstruct how solutions actually work, understand why technical decisions were made, evaluate their empirical support, identify overlooked implementation details, and propose experiments to test important hypotheses.

## Fundamental Research Principles

1. **Evidence First:** Every nontrivial factual claim must be supported by a verifiable source when available. Provide exact document sections, repository file paths, function names, code lines or commit identifiers where possible.

2. **No Fabrication:** Never invent dataset statistics, training hyperparameters, architectures, experimental results, leaderboard scores, or implementation details.

3. **Separate Facts from Hypotheses:** Classify findings as VERIFIED, INFERRED, or UNKNOWN. Explain the reasoning and uncertainty behind inferred claims.

4. **Implementation-Level Detail:** Analyze actual execution behavior rather than relying on high-level technique names. Trace operations and their order through code, configurations, dependencies and execution paths.

5. **Critical Thinking:** Do not assume a technique is beneficial because a winning team used it. Investigate ablations, experimental evidence, possible alternatives, confounding factors and tradeoffs.

6. **Reproducibility:** Record the information needed to reproduce a solution faithfully. Explicitly report missing information and blockers.

7. **No False Completeness:** Never claim a pipeline has been fully reconstructed if relevant source files, weights, data, dependencies or implementation details were inaccessible.

## Required Analysis Modules

### A. Competition & Task
Explain the problem, application context, input-output contract, rules, resource limits, evaluation protocol and submission constraints.

### B. Dataset Investigation
Analyze dataset origin, schema, splits, distribution, label quality, potential leakage, biases and modality-specific characteristics. Distinguish measured statistics from published statistics and estimates.

### C. Evaluation Analysis
Reconstruct the metric mathematically and operationally. Analyze aggregation, weighting, thresholds, edge cases, sensitivity to different error types and public/private leaderboard differences.

### D. Baseline Analysis
Identify official and community baselines, their assumptions, performance, computational requirements and limitations.

### E. Top Solution Investigation
Identify top-ranking teams from verified final results. Gather official write-ups, papers, repositories, configurations, checkpoints and supporting materials.

### F. Pipeline Forensic Reconstruction
For every selected team, reconstruct:

- Data acquisition, filtering and transformation
- Train/validation construction and leakage prevention
- Data loaders, samplers and augmentation
- Model architecture and initialization
- Loss functions and numerical implementation
- Training configuration and optimization
- Validation and checkpoint selection
- Inference, TTA, decoding and postprocessing
- Ensemble, calibration and submission generation
- Hardware, software environment and dependencies

Record the exact operations, parameters, order, data types and tensor transformations when verifiable.

### G. Reverse Engineering
For each important design decision, explain its mechanism, the problem it may solve, supporting evidence, alternative explanations, tradeoffs and conditions under which it might fail.

Propose discriminating experiments for important unverified hypotheses.

### H. Comparative Analysis
Compare teams across techniques, experimental evidence, results, complexity, compute requirements and reproducibility.

Do not attribute score differences to individual techniques without appropriate evidence.

### I. Critical Evaluation
Identify limitations, failure modes, generalization risks, leaderboard overfitting and production constraints.

### J. Knowledge Extraction
Extract reusable principles and connect them to existing ML concepts. Record when and why each principle is applicable, its limitations and supporting evidence.

## Required Outputs

Produce:

1. A structured competition research report.
2. A dataset and metric analysis report.
3. A team-by-team implementation-level pipeline specification.
4. A source-to-claim evidence matrix.
5. A cross-team comparison.
6. An experimental reproduction and ablation plan.
7. A list of unresolved questions and verification blockers.
8. Reusable ML knowledge cards.

## Quality Control

Before finalizing, audit every module for omissions, contradictions, weak evidence and unjustified causal claims.

If essential information is unavailable, report precisely what is missing, why it matters, and how it could be obtained or tested.

Prioritize correctness, technical depth and verifiability over apparent completeness.
```

## 16. Prompt phụ cần xây dựng tiếp (chưa hoàn thiện trong hội thoại)

Các prompt phụ nên được agent triển khai theo thứ tự:

- `discovery.md`: tìm competition; tìm official source và deduplicate.
- `curation.md`: source audit, quality scoring, justification.
- `task-and-metric.md`: task + metric mathematical analysis, scorer edge cases.
- `dataset.md`: modality classifier và dynamic EDA specification.
- `solution-forensics.md`: source map → code trace → exhaustive pipeline spec.
- `reverse-engineering.md`: observation vs mechanism vs hypotheses vs tests.
- `experiment-design.md`: reproduction, ablations, compute constraints.
- `cross-team.md`: systematic comparison, confounders.
- `knowledge-extraction.md`: reusable knowledge cards.
- `evidence-audit.md`: claims, citations, contradictions, incompleteness.

Mỗi prompt phụ cần quy định rõ: **input required**, **tools/sources allowed**, **output schema**, **quality bar**, **when to mark unknown**, **acceptance tests**.

---

# PHẦN VI — TASK 3: REPRODUCTION & ABLATIONS

## 17. Mục tiêu và lưu ý

Không phải competition nào cũng có thể reproduce toàn bộ, do hạn chế dataset, compute, licensing, checkpoint hoặc code. Khi không làm được, phải ghi khả năng reproduction (`full`, `partial`, `conceptual`, `blocked`) và lý do.

## 18. Các thí nghiệm được đề xuất trong hội thoại

| Experiment | Ý nghĩa |
|---|---|
| Baseline → + Augmentation | Đo marginal contribution của augmentation |
| Random Split → Group Split | Kiểm tra độ đáng tin cậy của validation khi có group dependency |
| Single Model → Ensemble | Đánh giá cải thiện so với compute, latency và diversity |
| FP32 → FP16 | Đo ảnh hưởng speed, memory, numerical stability, prediction difference |

Một winning solution có thể chứa 30 kỹ thuật; không được mặc định cả 30 đều cần. Agent cần:

- Xác định hypothesis cụ thể, metric, biến kiểm soát.
- Kiểm soát random seed/split/compute nếu có thể.
- Ghi experiment configuration/version và kết quả chính xác.
- Chú ý statistical significance và variance.
- Phân biệt result tự đo với result trích từ source.
- Lưu cả negative results, unexpected behavior và reproduction failures.

---

# PHẦN VII — TASK 4: TRANSFERABLE KNOWLEDGE BASE

## 19. Mục tiêu

Tích lũy kiến thức **vượt ra khỏi từng competition**:

- Liên kết các kỹ thuật với loại dữ liệu, task, metric, điều kiện áp dụng.
- Lưu cơ chế tác động, thực nghiệm hỗ trợ, độ tin cậy và hạn chế.
- Tìm patterns xuyên competition nhưng **không biến thống kê đồng xuất hiện thành quan hệ nhân quả**.
- Hỗ trợ các câu hỏi thực tế của researcher và ML engineer.

Ví dụ thống kê **minh họa, không phải kết quả thực tế** từ cuộc hội thoại: “Trong 10 cuộc thi CV, 6 đội sử dụng pseudo-labeling, 8 dùng ensemble, 5 chú trọng validation.” Hệ thống phải tiếp tục hỏi **tại sao, khi nào và mức độ hiệu quả được chứng minh ra sao**.

## 20. Knowledge card mẫu

```yaml
technique: Group-aware cross-validation
category: validation
applicable_to: [tabular, medical_images, audio, repeated_measures]
problem_addressed: correlated samples across groups
mechanism: prevents correlated groups spanning training and validation
preconditions:
  - reliable group identifiers
risks:
  - high fold variance with few groups
evidence:
  - claim_id: null
    competition_id: null
    status: UNKNOWN
recommended_tests:
  - compare random vs group split on properly held-out groups
compute_tradeoffs: null
notes: "Illustrative card; not a verified competition finding"
```

---

# PHẦN VIII — KIẾN TRÚC FILES / ARTIFACTS / WORKFLOW

## 21. Cấu trúc repository đề xuất

Cấu trúc này kết hợp các ví dụ trong cuộc hội thoại; là **starting point**, không phải ràng buộc cứng:

```text
ai-competition-lab/
├── README.md
├── PROJECT_BRIEF.md                 # tài liệu hiện tại khi nhập vào repo
├── docs/
│   ├── principles.md
│   ├── methodology.md
│   ├── quality_rubric.md
│   ├── schemas.md
│   └── roadmap.md
├── catalog/
│   ├── sources/                      # platform/organizer lists
│   ├── discovery/                    # raw, not yet audited
│   ├── curated/                      # vetted competition records
│   └── indexes/                      # searchable views/indexes
├── prompts/
│   ├── core.md
│   ├── discovery.md
│   ├── curation.md
│   ├── task-and-metric.md
│   ├── dataset.md
│   ├── solution-forensics.md
│   ├── reverse-engineering.md
│   ├── experiment-design.md
│   ├── cross-team.md
│   ├── knowledge-extraction.md
│   └── evidence-audit.md
├── competitions/
│   └── <competition_id>/
│       ├── overview.md
│       ├── data_analysis.md
│       ├── metric_analysis.md
│       ├── leaderboard.md
│       ├── sources.yaml
│       ├── evidence_matrix.yaml
│       ├── solutions/
│       │   └── <team_id>/
│       │       ├── overview.md
│       │       ├── pipeline.md
│       │       ├── reverse_engineering.md
│       │       ├── config_audit.md
│       │       └── unknowns.md
│       ├── cross_team_comparison.md
│       ├── experiments/
│       ├── lessons_learned.md
│       └── quality_review.md
├── techniques/
│   ├── validation/
│   ├── preprocessing/
│   ├── augmentation/
│   ├── training/
│   ├── inference/
│   └── ensembling/
├── reusable/
│   ├── data/
│   ├── evaluation/
│   └── training/
└── research_index.md
```

Trong một phiên bản sơ khai từng được đề xuất, repo chỉ gồm `competitions/`, `techniques/`, `reusable/`, `research_index.md`. Cấu trúc ở trên giữ nguyên các ý tưởng đó nhưng bổ sung `catalog/`, `prompts/` và các artifact để hỗ trợ orchestration và provenance.

**Tránh repository bừa bộn**: mỗi file có vai trò rõ, đường dẫn canonical, naming conventions, schema validators, không để agent tạo hàng loạt `final_v2_final.md` hoặc folder trùng nhiệm vụ. Phân biệt raw download/cache với artifact được curate. Không để agent thay đổi schema thiếu migration.

## 22. Tám output cốt lõi cho mỗi competition (đã đề xuất)

1. Structured competition research report.
2. Dataset and metric analysis report.
3. Team-by-team implementation-level pipeline specifications.
4. Source-to-claim evidence matrix.
5. Cross-team comparison.
6. Experimental reproduction + ablation plan.
7. Unresolved questions + verification blockers.
8. Reusable ML knowledge cards.

Có thể chia file vật lý để dễ kiểm soát, nhưng mọi report cần link chéo và một entry point.

## 23. Luồng làm việc đề xuất

```text
SOURCE DISCOVERY
  → extract candidate competition metadata
  → official-source verification and de-duplication
  → quality scoring & curation
  → select competition for deep analysis
  → collect task/rules/data/leaderboard/solution sources
  → task + metric + dataset analysis
  → top-team code/write-up forensic reconstruction
  → reverse engineering + evidence matrix
  → cross-team comparisons, failure/compute analysis
  → quality audit and unresolved issues
  → experiment/reproduction plan
  → optional verified experiments
  → extract/reconcile knowledge cards
  → update indexes and catalog status
```

**Khuyến nghị:** Giai đoạn đầu không tự động hóa hoàn toàn. Hình thành một quy trình nghiên cứu chính xác bằng vài competition mẫu, sau đó mới mở rộng agents/scrapers.

---

# PHẦN IX — ROADMAP & ACCEPTANCE CRITERIA

## 24. Thứ tự triển khai bốn giai đoạn

### Phase 1 — Competition Catalog

- Tổng hợp platform/organizer ở Việt Nam và quốc tế.
- Thiết kế discovery schema, curated schema, source provenance và scoring rubric.
- Tạo bộ tìm kiếm/dedup/verification/incremental update.
- Lập danh sách nguồn lớn; kiểm tra rồi phân loại.
- **Deliverable:** searchable, auditable catalog; chưa cần deep report cho tất cả entries.

### Phase 2 — Prompt + Research Workflow

- Xây core prompt và modular prompts.
- Chọn **3 competition khác biệt về task và modality** để kiểm thử; ưu tiên đã kết thúc, có dữ liệu và >=3 solution/write-up chất lượng khi khả thi.
- Chạy agent phân tích; phát hiện omissions, hallucinations, contradictions.
- Chỉnh prompt/schema đến khi outputs đủ tin cậy và hữu ích.
- **Deliverable:** validated analysis workflow + technical reports.

### Phase 3 — Reproduction

- Chọn solution có dataset, code, config và compute phù hợp.
- Reproduce một hoặc nhiều thành phần có thể thực hiện.
- Chạy ablations để phân biệt claims/hypotheses.
- **Deliverable:** code, logs, reproducibility reports, empirical evidence.

### Phase 4 — Knowledge Synthesis & Retrieval

- Tạo knowledge cards có provenance.
- Liên kết techniques, competition, dataset characteristics, empirical evidence.
- Xây search và cross-competition synthesis.
- **Deliverable:** queryable Practical ML Knowledge Base.

## 25. Mức tối thiểu của pilot đầu tiên

Một competition **đã kết thúc**, có thể đọc tài liệu và ít nhất vài solution/approaches đáng so sánh. Pilot phải tạo được:

1. Báo cáo data + metric.
2. Phân tích chi tiết các top solutions.
3. Một pipeline implementation-level của ít nhất một team, với mọi unknown được ghi rõ.
4. Một so sánh các team.
5. Một experiment có thể tái hiện hoặc kế hoạch kiểm chứng có điều kiện thực hiện rõ ràng.
6. Knowledge notes và nguồn bằng chứng.

**Pilot thành công không có nghĩa phải đạt top leaderboard.** Thành công nghĩa là học được kỹ thuật có thể giải thích, kiểm chứng và chuyển giao.

## 26. Definition of Done (DoD) cho agent

### DoD Task 1

- Catalog schema/documentation được viết, dữ liệu được validate.
- Nguồn được audit và mọi entry có canonical URI hoặc trạng thái chờ xác minh.
- Có logic dedup theo year/track.
- Có quality scores **và nguồn/justification**, unknown không bị gán điểm giả.
- Có export/search/filter và backlog unresolved sources.

### DoD Task 2

- Đủ module A–O hoặc có lý do `not_applicable / blocked`.
- Metric có định nghĩa và tác động của các thành phần.
- EDA theo đúng modality, ghi nguồn của số liệu.
- Top leaderboard được xác minh trước khi gọi “winning team”.
- Pipeline đủ thứ tự và hyperparameters khi source cho phép; những chi tiết nhỏ được truy tìm có hệ thống.
- Mỗi claim quan trọng có evidence status.
- Reverse engineering phân biệt tác giả giải thích với agent hypothesis.
- Có cross-team comparison, failure/compute/production tradeoffs.
- Có unresolved questions và reviewer signoff/checklist.

### DoD Task 3

- Experiment có source code/command/config/environment/seed/split/metric.
- Có outcome hoặc blocker rõ ràng, không “kết quả tưởng tượng”.

### DoD Task 4

- Mỗi knowledge card có nguồn, điều kiện áp dụng và giới hạn.
- Có thể trace knowledge card ngược lại competition/solution/experiment.

## 27. Các rủi ro cần tránh

- **Quantity bias:** Danh sách lớn nhưng chất lượng kém và không phân tầng.
- **Source hallucination:** Agent khẳng định có code/winner/scores trong khi chưa kiểm chứng.
- **False precision:** Đưa ra con số EDA hoặc gains không được đo.
- **Shallow pipeline:** Chỉ ghi model name, bỏ mất transforms, splitting và inference.
- **Narrative fallacy:** Tự kể câu chuyện “kỹ thuật X giúp thắng” khi thiếu ablations.
- **Leakage blindness:** Thiết kế validation sai.
- **Leaderboard ≠ production:** Tối ưu điểm số bằng cách quá tốn compute, không robust hoặc không deploy được.
- **Over-automation:** Dùng nhiều agents quá sớm, khó debug provenance.
- **Repository entropy:** Để folder và artifacts sinh ra tự phát, trùng lặp, không nhất quán.
- **Stale sources:** Competition đổi rules/leaderboard, URL die, repos bị thay đổi.
- **Licensing/privacy:** Không vượt qua hạn chế truy cập, quyền sử dụng dữ liệu hoặc bảo mật chỉ để reproduce.

---

# PHẦN X — NHỮNG THỨ CHƯA CHỐT VÀ CHỈ DẪN CHO AGENT

## 28. Những quyết định còn mở

1. **[CẦN QUYẾT ĐỊNH] Lĩnh vực ưu tiên đầu tiên:** CV (detection/segmentation/classification), Tabular ML, NLP/LLM hay đa lĩnh vực. Trong cuộc hội thoại có đề xuất lựa chọn này nhưng user **chưa chọn**. Do đó Task 1 nên discovery đa lĩnh vực, trừ khi user quyết định khác.
2. **[CẦN QUYẾT ĐỊNH] Stack/cơ sở dữ liệu:** Markdown/YAML/SQLite/Postgres/vector search etc. Chưa có chỉ định; bắt đầu đơn giản, dễ migrate.
3. **[CẦN QUYẾT ĐỊNH] Agents/tools:** ChatGPT Project, coding agent hoặc hệ thống multi-agent cụ thể chưa được lựa chọn.
4. **[CẦN QUYẾT ĐỊNH] Compute budget:** Không được mặc định có nhiều GPU hoặc khả năng chạy full reproduction.
5. **[CẦN QUYẾT ĐỊNH] Mức tự động download data/source:** Phải tuân thủ license/terms và giới hạn compute.
6. **[ĐỀ XUẤT] Quality weights/tier cutoffs:** Có thể điều chỉnh sau khi thử nghiệm trên mẫu.

## 29. Lời dặn trực tiếp cho agent triển khai

> Hãy coi tài liệu này là **project charter + functional specification + research quality bar**. Không bắt đầu bằng việc chạy đi thu thập hàng loạt competition khi chưa có schema, provenance, dedup, quality rubric và định nghĩa hoàn thành. Phải làm theo từng milestone nhỏ, có test/validation, cập nhật roadmap, ghi rõ điều đã thực hiện/chưa thực hiện, và giữ repository gọn gàng. Khi một nguồn không truy cập được hoặc một kết luận thiếu bằng chứng, đánh dấu chưa biết thay vì tự bổ sung. **Không tóm tắt winning solution ở mức hời hợt**; nếu chưa đủ tư liệu để reconstruct pipeline, công bố mức độ bất định và đường dẫn cần kiểm tra tiếp.

**Milestone đầu tiên được khuyến nghị:** Thiết kế schema catalog, rubric, source inventory và verification workflow cho Task 1. Sau đó thử curation với một số competition đa modality rồi mở rộng dần.

---

# PHẦN XI — TÓM LƯỢC NỘI DUNG ĐÃ TRAO ĐỔI ĐỂ TRÁNH THẤT LẠC Ý

## 30. Những điểm nhấn từ trao đổi đầu tiên

- Người dùng là ML researcher muốn bù đắp kỹ năng triển khai thực tế.
- Học từ winners để hiểu validation, data, model, training và inference thay vì chỉ học architecture từ paper.
- Có 5 hướng nghiên cứu được gợi ý ban đầu: **Competition Discovery**, **Data & Problem Analysis**, **Top Solution Reverse Engineering**, **Reproduction & Ablation**, **Knowledge Extraction**.
- Mỗi competition nên có overview, data analysis, team solutions, experiments và lessons learned.
- Cần học across competitions thay vì lưu một đống reports độc lập.
- Nguồn ban đầu có Kaggle, DrivenData, các GitHub compilations.
- Cần phân biệt competition solution và production-ready solution.
- Không được tự động hóa hoàn toàn trước khi chuẩn hóa workflow.

## 31. Những điểm nhấn từ trao đổi thứ hai

- User xác định **2 task trước mắt**: (1) list competition uy tín được sàng lọc kỹ, không ngại vài trăm; (2) thiết lập prompt nghiên cứu chuyên sâu gồm 7 nội dung chính.
- Assistant bổ sung tiêu chí curation, nguồn trong/ngoài nước, 100-point rubric, Tier A/B/C và schema mẫu.
- Assistant đề xuất bổ sung **8 nội dung** vào phân tích: rules/constraints, baseline, validation, ablation/evidence, failure analysis, compute/engineering, cross-team comparison, transferable knowledge.
- Pipeline forensic cần đi từ raw data đến submission, kiểm tra ngay cả normalization và phép toán nhỏ.
- Reverse engineering phải tách observation, original rationale và hypothesis của agent; cần đề xuất kiểm chứng.
- Kiến trúc là orchestrator + các specialist roles + evidence reviewer; ban đầu có thể chỉ một agent.
- Có master prompt tiếng Anh và 8 output artifacts như đã lưu ở trên.
- Đề xuất thêm Task 3 (experiments/reproduction) và Task 4 (knowledge synthesis/retrieval).
- Roadmap gồm catalog → prompt pilot → reproduction → knowledge retrieval.

## 32. Nguyên tắc cốt lõi của toàn dự án

> **Mỗi nghiên cứu phải trả lời được ba câu hỏi:**
>
> 1. **Họ đã làm gì?**
> 2. **Tại sao cách đó có thể hiệu quả?**
> 3. **Bằng chứng nào cho thấy nó thực sự hiệu quả?**

Cần thêm câu hỏi thứ tư khi chuyển sang ứng dụng thực tế:

> **Nếu phải triển khai với giới hạn về dữ liệu, GPU, latency và maintenance, mình nên giữ lại điều gì?**

---

# PHỤ LỤC A — NGUYÊN VĂN NHỮNG YÊU CẦU CHÍNH CỦA USER

### Phát biểu mục tiêu ban đầu

> Tôi là một ML researcher, nhưng tôi thấy bản thấy khá thiếu nhiều kĩ năng áp dụng trong thực tế. Do đó tôi định tạo một Project giúp tôi tìm hiểu về các cuộc thi AI, phân tích data, phân tích solution của các đội top để tôi học được các kĩ thuật, các kiến thức của họ. Bạn nghĩ sao?

### Hai task người dùng đã xác định

> Vậy trước mắt ta có 2 task chính:
>
> 1. Lập danh sách các competition uy tín, chất lượng. Ví dụ là trên kaggle, ZaloAI, VinAI hay các cuộc thi trong ngoài nước khác mà có thể tôi không biết. Bước này phải được sàng lọc và tìm hiểu kĩ. Có thể danh sách gồm mấy trăm cuộc thi nhưng điều đó không quan trọng. Đây là nơi mà tôi sẽ học lâu dài nên không ngại khối lượng kiến thức đồ sộ.
> 2. Thiết lập prompt phân tích cho mô hình, những thứ tôi muốn phân tích mà hiện tại tôi nghĩ ra là:
>    1. Giải thích tác vụ
>    2. Sơ lược về bộ dữ liệu?
>    3. Giải thích cách đánh giá, các thang đo. Các thành phần nào ảnh hưởng tới thang đo? Ảnh hưởng như thế nào?
>    4. Thống kê về bộ dữ liệu. Ví dụ dữ liệu dạng bảng dạng hình ảnh hay gì đó mỗi loại cần có các thống kê riêng và được thiết kế riêng cho phù hợp với từng cuộc thi
>    5. Kết quả của các đội top.
>    6. Pipeline của đội top. Lưu ý pipeline phải chi tiết, không được bỏ qua bất kì chi tiết nào quan trọng. Ví dụ nhưng thứ đơn giản như chuẩn hóa dữ liệu hoặc một phép cộng thôi cũng make difference nên tôi muốn prompt đoạn phân tích pipelien thật kĩ để không bỏ sót chỗ nào quan trọng.
>    7. Reverse Engineering: nghe kinh khủng nhưng đại ý là phân tích tại sao các phương pháp/kĩ thuật đó lại được sử dụng. Nếu đội có share phân tích thì dùng, hoặc share ít hoặc không share thì để agent tự nghĩ
>
> Bạn thấy kế hoạch của tôi thế nào? Có còn thiếu cái gì không?

### Yêu cầu tạo tài liệu

> Được, viết hết những gì có trong cuộc trò chuyện của ta vào một file .md để tôi nhờ agent triển khai dần

---

# PHỤ LỤC B — LƯU Ý VỀ NGUỒN VÀ ĐỘ TIN CẬY

- Các URL trong tài liệu này được **chuyển lại từ nội dung cuộc hội thoại**, không phải kết quả crawling/validation đầy đủ trong lần xuất file này.
- Những mô tả về competition năm 2026 hoặc trạng thái code/repository có thể thay đổi theo thời gian. Agent triển khai phải kiểm chứng lại từ official pages và timestamp.
- Một số URL trước đó xuất hiện dưới dạng citation/link động trong chat, không có địa chỉ gốc đầy đủ để tái tạo ở tài liệu. Thay vì đoán URL, tài liệu ghi tên repository hoặc nguồn để agent tìm và xác minh.
- Số lượng competition, tỷ lệ sử dụng kỹ thuật, các experiment score và ví dụ metadata là **ví dụ/đề xuất**, không phải kết quả nghiên cứu của dự án.

**Trạng thái tổng thể:** Project đã được xác định mục tiêu và thiết kế cấp cao; **chưa thực thi Task 1–4** trong tài liệu này. Bước tiếp theo là triển khai và ghi nhận đầu ra thực tế.

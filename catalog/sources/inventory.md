# Source inventory — 19/11/2026

18đầu mối đã truy cập. Bao gồm platform indexes và archive/source collections; không phải18platform độc lập. HTTP retrieval và content audit là hai trạng thái khác nhau.

| Nguồn | Coverage | Nội dung truy cập | Audit / next step |
|---|---|---|---|
| [DrivenData](https://www.drivendata.org/competitions/) | Đa lĩnh vực, social impact | readable_index | Đã đọc index và winning-code registry; 53 candidates, 3 pilot. Mỗi competition khác vẫn cần audit riêng. |
| [Kaggle](https://www.kaggle.com/competitions) | Tabular/CV/NLP/forecasting/recommendation | metadata_only | HTML public chủ yếu metadata/JS; 5candidate pages, chưa đọc đầy đủ task/rules/results. |
| [AIcrowd](https://www.aicrowd.com/challenges) | RL/agents/CV và applied ML | readable_index | Index tải được; chưa import/audit từng challenge. |
| [Grand Challenge](https://grand-challenge.org/challenges/) | Medical imaging | readable_index | Index và CAMELYON16 overview đã đọc; license/evaluation từng challenge cần audit. |
| [EvalAI](https://eval.ai/) | Multimodal/agents/research challenges | js_shell | Landing HTML chủ yếu shell; cần đọc task-specific pages, không coi benchmark tự động là competition. |
| [SemEval](https://semeval.github.io/) | NLP shared tasks | readable_index | Có index theo edition; chưa import task-level records. |
| [Zalo AI Challenge](https://challenge.zalo.ai/) | AI tiếng Việt và applied AI | js_shell | Portal trả shell. Chưa xác minh archive từng năm/track; không lấy edition2026 làm final results. |
| [VLSP](https://vlsp.org.vn/) | Vietnamese NLP/speech | readable_index | Đã đọc2023/2025campaign lists, import21 task candidates; subtask constraints cần tách trước curate. |
| [HCMC AI Challenge](https://aichallenge.hochiminhcity.gov.vn/) | Video retrieval và AI ứng dụng Việt Nam | landing_only | Landing tải được; chưa audit archive năm/track/results. |
| [AIHUB.ML](https://aihub.ml/competitions/) | Vietnamese speech/NLP/CV/recommendation | readable_index | Đã đọc platform listing; import12non-VLSPcandidates và tránh classroom/examples/legacy containers. |
| [AI City Challenge](https://www.aicitychallenge.org/) | Traffic/video/multi-camera | readable_index | 2024 task/evaluation và awards đã đọc; 5track records; code/papers/licenses cần audit. |
| [DCASE](https://dcase.community/challenge2024/) | Audio/sound event/scene/captioning | readable_index | 10 task candidates edition2024; chưa tách mọi subtrack/dataset/resource setting. |
| [WMT](https://www2.statmt.org/wmt24/) | Machine translation và evaluation | readable_index | 12 task candidates2024; cần tách language pairs và constrained/unconstrained tracks khi áp dụng. |
| [DrivenData winner repositories](https://raw.githubusercontent.com/drivendataorg/competition-winners/master/README.md) | Organizer-maintained source-code index | readable_index | Đã trích53titles/repository leads. Chỉ là discovery evidence ngoài3 pilot; có cả visualization/data challenges cần scope review. |
| [VLSP2023 archive](https://vlsp.org.vn/index.php/node/51) | Vietnamese NLP/speech shared tasks | readable_index | 10 task links, chưa coi source paper/code tự động tồn tại. |
| [VLSP2025 archive](https://vlsp.org.vn/index.php/vlsp2025/eval) | Vietnamese NLP/speech/legal QA | readable_index | 11 task links sau khi loại registration form; chưa xác minh final results. |
| [VinBigData on Kaggle](https://www.kaggle.com/competitions/vinbigdata-chest-xray-abnormalities-detection) | Chest X-ray object detection lead | metadata_only | Đầu mối trong brief và metadata trang; không đồng nhất organizer với VinAI. |
| [CAMELYON16](https://camelyon16.grand-challenge.org/) | Whole-slide metastasis detection | readable_page | Official overview nói kết thúc11/2016; chưa kiểm tra updated rules/license/evaluator. |

## Nguồn mở rộng chưa audit

MICCAI/ISBI/CVPR/ICCV/ECCV workshop tracks, IWSLT, NeurIPS competitions và các GitHub compilation trong brief vẫn là leads. Không xác minh hoặc đoán URL2026/updated status khi chưa đọc official source. Cần thêm vào manifest khi audit; không đánh dấu verified chỉ vì được nhắc trong master brief.

Raw retrieval metadata ở [registry.json](registry.json), gồm failed attempts, original/final URL, UTC timestamp và SHA-256 snapshots. Inventory notes là phạm vi đã xem; không suy tất cả trang con đã được kiểm tra.

# Backlog và giới hạn coverage

Canonical competition backlog là `research.next_actions` và `curation.limitations` trong từng JSON; pilot blockers ở `competitions/<id>/state.json`. Catalog hiện119 entries: 3curated/116discovery. Không đặt trần số competition.

## Ưu tiên nguồn tiếp theo

| Ưu tiên | Công việc | Acceptance |
|---|---|---|
| P0 | Đối chiếu current archive của3 pilot với competition version; pin external dependencies và model assets | Có data/asset hashes hoặc blocker rõ, không tự accept license/login |
| P0 | Hoàn thiện remaining team code paths, configs và evaluator edge cases | Từng constant/order có source hoặc UNKNOWN |
| P1 | Curate VLSP/AIHUB Việt Nam: ưu tiên ASR, legal retrieval/QA, OCR và machine translation | Official task/result +≥3approaches nếu có, license/access audit |
| P1 | Kaggle/VinBigData/RSNA/M5/OTTO | Đọc được nội dung task/rules/results, resolve year×track, truy author solution repositories |
| P1 | Zalo AI Challenge theo year/track | Portal hiện trả JS shell; cần official archived task URLs/API hoặc author sources đối chiếu; chưa tự tạo winner records |
| P1 | AI City2024 tracks | Đã đọc task/results; audit papers/code, phân biệt award/public leaderboard và private dataset |
| P2 | DCASE/WMT/SemEval/GrandChallenge/MICCAI | Split task/subtrack/evaluation versions, license và solution-paper access; không gộp workshop thành một competition |
| P2 | AIcrowd/EvalAI/RL/robotics/recommendation | Mở rộng discovery ngoài nguồn currently imported; xác nhận competition có rules/results, không chỉ benchmark |
| P2 | HCMC AI Challenge và VinAI | HCMC mới đọc landing page; chưa resolve archive tracks. VinAI chưa xác minh portal competition riêng, không đồng nhất với VinBigData |

## Giới hạn hiện tại

- Discovery tập trung DrivenData/VLSP/AIHUB/WMT/DCASE vì có index đọc được. Đây là **source-access bias**, không phải kết luận những nơi đó tốt hơn các nền tảng khác.
- Nhiều DrivenData candidates chưa resolve edition/year/track; repository link là đầu mối, không phải đã có official competition metadata.
- Các mục WMT/VLSP là shared tasks cấp task; subtrack/language-pair/resource constraint có thể cần tách tiếp trước curated promotion.
- Modality discovery chủ yếu suy từ title, gắn INFERRED. Search theo modality có thể bỏ sót mục chưa phân loại; không dùng counts đó làm thống kê toàn hệ sinh thái.
- Kaggle page metadata không cung cấp đầy đủ nội dung trong lần tải này; năm giữ null, không điền từ trí nhớ.
- External source truy cập được không đồng nghĩa data/weights hiện tải được hoặc được phép dùng cho mọi mục đích.
- Có source fetch thất bại/giới hạn8MB được giữ trong registry; link thay đổi branch hoặc file đoán sai không được coi “not_public”.

Không có blocker nào ngăn dùng catalog/prompts ngay. EDA thực đo và model reproduction cần data/assets/budget rõ ràng; nghiên cứu nguồn khác có thể tiếp tục độc lập.

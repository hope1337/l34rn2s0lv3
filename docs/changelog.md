# Changelog

## 0.1 — 19/11/2026

- Thêm `latex/` cho ba competition hiện có và quy ước cho competition mới, mẫu XeLaTeX/TikZ/PGFPlots, ignore file build/auxiliary có phạm vi LaTeX; giữ source và figure PDFs. Neo `/data/`, `/runs/` tại gốc để không vô tình ignore bảng dữ liệu vẽ trong thư mục con.
- Thêm `prompts/start.md`: tên/link/ảnh/tài liệu là đủ để agent nhận diện competition, tự dựng input, chọn stage prompts và resume nghiên cứu; cập nhật hướng dẫn sử dụng tương ứng.
- Rút gọn prompt cấu trúc và AGENTS.md để loại quy tắc lặp; giữ nguyên vị trí artifacts và yêu cầu bảo toàn dữ liệu.

- Thêm `AGENTS.md` và prompt cấu trúc repository theo yêu cầu người dùng: canonical paths, ưu tiên cập nhật file, không tạo report/folder trùng, và quy trình mở rộng cấu trúc trong phạm vi công việc.

- Giữ nguyên master brief, triển khai catalog/schema/provenance/rubric và CLI offline.
- Discovery từ snapshot nguồn tổ chức, có parser bảo thủ và không overwrite existing records.
- 3 records được chuyển discovery→curated với cùng ID: dd-power-laws-cold-start, dd-tick-tick-bloom, dd-hateful-memes.
- Bộ core +10 stage prompts, shared I/O contract, report/pipeline/decision templates.
- Ba pilot report, pinned source traces, claim matrices, per-module state và experiment plans.
- Numeric examples dùng synthetic inputs, không phải reproduced competition scores.
- Loại link registration của VLSP khỏi discovery parser vì không phải shared task.
- Schema v1; chưa có migration vì chưa thay version. Mọi schema extension về sau phải có version/migration.

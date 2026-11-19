# Workflow có thể tiếp tục

## Task 1

1. Tìm candidate từ inventory; xác nhận là competition/shared task, không phải leaderboard benchmark thông thường.
2. Lưu URL chính thức hoặc đầu mối tổ chức đủ tin cậy, thời điểm truy cập, snapshot SHA-256 và phạm vi đã đọc.
3. Thêm discovery record. ID là bất biến; năm/track chưa rõ để null. Canonical URL có thể tạm là repository tổ chức, phải ghi rõ hạn chế.
4. Đối chiếu identity `(platform, canonical_url, year, track, evaluation_version)`. Kiểm tra alias trước khi thêm; không gộp hai track chỉ vì cùng URL.
5. Audit riêng task/evaluator, final results, dữ liệu/quyền truy cập, write-up/code/weights và reproducibility. HTTP 200 không chứng minh nội dung truy cập được.
6. Chấm từng tiêu chí có evidence. Thiếu tiêu chí => tổng null, `UNRATED`; không thay unknown bằng 0.
7. Chuyển cùng record sang `curated/` khi đã có task, kết quả cuối, nguồn solution và lý do chọn. Curated có thể UNRATED nếu còn thiếu bằng chứng chấm điểm; ghi rõ lý do. Không giữ bản trùng ở discovery.
8. Chạy validate, build index, xem backlog. Giữ lịch sử thay đổi ở `docs/changelog.md`.

## Task 2

Chạy core + một module prompt ở mỗi lượt, truyền competition record, source registry và state trước đó. Prompts có hợp đồng chung ở `prompts/README.md`.

`source-map → A/B/C → D/E/F → G từng team → H/I/J/K/L → M/N → O audit`

Đọc theo đường thực thi thật: entry point → config merge → data → training → checkpoint → inference → submission. Truy cả dependency defaults và caller. Dừng ở unknown nếu chưa truy được; không suy từ tên hàm.

Mỗi pilot có `state.json`, `report.md` (A–O), `pipeline.md`, `evidence.json`, `experiment_plan.md`, `quality_review.md`. Module có thể partial/blocked, nhưng phải ghi đúng câu hỏi chưa trả lời và bước tháo gỡ. Reviewer kiểm tra nguồn và khả năng giải thích; không yêu cầu mọi module complete để lưu nghiên cứu dở dang.

## Cập nhật tăng dần

Không ghi đè snapshot cũ; URL cùng nội dung dùng lại hash, URL đổi nội dung sinh hash mới. Fetch log được version control; khi refresh lưu log mới có ngày thay vì xóa lịch sử. Pin repo ở commit cho citation. Ngày nguồn xuất bản khác ngày truy cập. Nguồn JS/login vẫn có entry blocked/content_unavailable và hướng xử lý, không bypass. Không đổi schema version nếu chưa có migration và changelog.

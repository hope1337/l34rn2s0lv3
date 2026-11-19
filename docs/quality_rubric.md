# Rubric 100 điểm, v1

| Key | Trọng số | Bằng chứng cần đọc |
|---|---:|---|
| task_evaluation | 15 | Task, rules, định nghĩa metric và evaluator/edge cases |
| solution_depth | 20 | Write-up top teams có chi tiết, thất bại và ablation |
| public_code | 20 | Code/config/env/entry point, weights và khả năng chạy |
| dataset_access | 15 | Trang data, license, cách lấy dữ liệu và giới hạn thực tế |
| technical_value | 15 | Kỹ thuật cụ thể đáng học, có so sánh hoặc câu hỏi thực nghiệm |
| transfer_value | 10 | Điều kiện chuyển giao, compute/latency và hạn chế |
| result_trust | 5 | Organizer, thông báo kết quả cuối và các ngoại lệ ranking |

Mỗi tiêu chí dùng tỷ lệ 0, .25, .5, .75, 1 nhân trọng số. Các mốc lần lượt là: đã kiểm tra nhưng không có giá trị/sử dụng được; rất hạn chế; đủ nghiên cứu một phần; nguồn chi tiết có vài blocker; nguồn đầy đủ, đã đối chiếu. Ghi justification cụ thể và source IDs. Đây là đánh giá học tập, không phải thước đo uy tín tuyệt đối.

Nếu **chưa kiểm tra hoặc chưa đủ căn cứ**, points=null và explanation bắt buộc. Tổng chỉ tính khi cả 7 points khác null. Không chuẩn hóa tổng theo số tiêu chí đã biết. Tier A >=80, B >=60, C <60, nếu tổng null => UNRATED. Red flags là kênh riêng, không bị tổng điểm xóa bỏ. Với red flag chưa giải quyết, không tự chuyển curated thành khuyến nghị reproduce.

Reproducibility ở catalog là đánh giá điều kiện nguồn; chỉ experiments có log mới được xác nhận đã tái hiện. Bộ pilot đầu dùng để hiệu chỉnh rubric; không cố ép đủ Tier A.

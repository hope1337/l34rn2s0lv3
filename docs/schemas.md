# Schema và lệnh

JSON UTF-8 là định dạng canonical v1. Dùng JSON Schema Draft 2020-12 và kiểm tra ngữ nghĩa bổ sung trong CLI. JSON đọc được bằng thư viện chuẩn, dễ chuyển sang YAML/SQLite; không cần DB server.

- `schemas/competition.schema.json`: identity, modality/task, availability, scoring, provenance, research state.
- `schemas/evidence.schema.json`: claim status, scope, locator, source references, limitations, hypothesis test.
- `catalog/sources/registry.json`: toàn bộ fetched sources; mỗi record có hash, path và thời điểm thật nếu tải thành công. Nội dung chưa đánh giá vẫn chỉ là fetched.
- `catalog/sources/inventory.json`: nguồn discovery, coverage và hạn chế đã quan sát.
- `catalog/discovery/*.json`, `catalog/curated/*.json`: mỗi competition một record; không trộn raw candidates với đã audit.

```bash
python3 scripts/lab.py validate
python3 scripts/lab.py search --modality time_series
python3 scripts/lab.py search --state curated --code verified
python3 scripts/lab.py search --query Vietnamese
python3 scripts/lab.py build
python3 -m unittest discover -s tests -v
```

`build` validate trước khi ghi Markdown/CSV/SQLite. Các bộ lọc kết hợp AND; query tìm trên title, alias, task, organizer và tags. Các index là dẫn xuất, không sửa trực tiếp. Export giữ null thành ô trống; CSV có cột availability status riêng. SQLite có JSON đầy đủ để giữ provenance. Source validation kiểm tra checksum, không truy cập mạng.

Không sửa ID khi bổ sung year/track. Entry chưa định danh rõ vẫn ở discovery; nếu phát hiện hai candidate là cùng cuộc thi, merge sources/aliases vào ID được giữ và ghi redirect trong changelog. Không merge các evaluation version có rules/metric khác nhau.

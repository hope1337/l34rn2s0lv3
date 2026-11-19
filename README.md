# AI Competition Research Lab

Kho học ML thực chiến từ competition: tìm nguồn → sàng lọc → phân tích dữ liệu/metric → truy code đội top → kiểm tra bằng chứng → tích lũy kiến thức.

**Bản triển khai0.1, 19/11/2026:**119 competition/shared-task candidates, trong đó3 đã qua source audit để chọn làm pilot.116 mục còn lại là discovery, **chưa phải116 cuộc thi đã được kiểm định chất lượng**. Ba pilot có73 claims, so sánh top teams và pipeline code; EDA thực đo/reproduction chưa chạy.

## Đọc từ đây

- [Catalog dễ đọc](catalog/indexes/competitions.md) · [CSV](catalog/indexes/competitions.csv).
- [Inventory18 nguồn](catalog/sources/inventory.md) · [Backlog và coverage gaps](docs/backlog.md).
- [Bộ prompt nghiên cứu](prompts/README.md) · [Core prompt](prompts/core.md).
- [Quy tắc tạo/cập nhật file cho agent](prompts/repository-structure.md) · [AGENTS.md](AGENTS.md).
- [Workflow](docs/methodology.md) · [Rubric100điểm](docs/quality_rubric.md) · [Schema và lệnh](docs/schemas.md).
- [Roadmap/trạng thái thực tế](docs/roadmap.md) · [Master brief gốc](AI_Competition_Research_Lab_Master_Brief.md).

## Ba pilot đã có nội dung

| Competition | Kỹ năng tập trung | Report |
|---|---|---|
| Cold Start Energy Forecasting2018 | Horizon/metric weighting, normalization eps, recursive inference, ensemble→patch | [Đọc](competitions/dd-power-laws-cold-start/report.md) |
| Tick Tick Bloom2023 | Spatial validation, satellite features, regional scoring/routing, rounding và missing imagery | [Đọc](competitions/dd-tick-tick-bloom/report.md) |
| Hateful Memes Phase 2 2020 | Multimodal confounders, sweep/model selection, probability aggregation và rule overrides | [Đọc](competitions/dd-hateful-memes/report.md) |

Mỗi report có pipeline, nguồn+snapshot, claim matrix, experiment plan, state theo module A–O và self-review. Trạng thái chung **partial**: không đánh đồng published code với winning execution đã tái hiện. Các rubric scores là đánh giá tài liệu hiện có, không phải reproduction score.

Mỗi competition có sẵn `latex/` cho báo cáo và figures khi được yêu cầu: `main.tex`, `references.bib`, `figures/` (TikZ/PGFPlots và dữ liệu vẽ có nguồn), `build/` (output biên dịch được gitignore). Dùng [mẫu LaTeX](templates/latex-report.tex); hiện chỉ giữ chỗ thư mục, chưa viết hoặc biên dịch báo cáo.

## Sử dụng

Để bắt đầu một competition, chỉ cần gửi **tên, link, ảnh chụp màn hình hoặc tài liệu tham chiếu** kèm: **“Đọc `prompts/start.md` và làm theo.”**

[Start prompt](prompts/start.md) tự điều phối các bước, tìm nghiên cứu đã có để tiếp tục và lưu kết quả đúng cấu trúc. Ví dụ: `Tick Tick Bloom — đọc prompts/start.md và làm theo.`

Yêu cầu Python≥3.10 và jsonschema4.x. Môi trường hiện tại đã có dependency. Nếu môi trường mới chưa có, cài `python3 -m pip install -r requirements.txt` trong virtualenv của bạn.

```bash
python3 scripts/lab.py validate
python3 scripts/lab.py search --state curated
python3 scripts/lab.py search --modality time_series
python3 scripts/lab.py search --task forecasting
python3 scripts/lab.py search --query Vietnamese --platform VLSP
python3 scripts/lab.py search --tier B --code verified
python3 scripts/lab.py build
python3 -m unittest discover -s tests -v
```

CLI hoạt động offline, filter kết hợp AND, trả JSON đầy đủ provenance. Build xuất Markdown/CSV/SQLite; SQLite được sinh tại `catalog/indexes/catalog.sqlite`, không phải nguồn canonical. Không cần web app hoặc database server.

Discovery từ snapshot có thể chạy lại: `python3 scripts/discover_from_snapshots.py`. Script không overwrite record hiện có. Để thêm source mới, tạo manifest rõ ràng rồi dùng `scripts/fetch_sources.py <manifest> --output catalog/sources/<new-dated-log.json>`; dùng source IDs mới khi refresh, chạy `python3 scripts/reconcile_sources.py`, discovery/audit và validate/build. Fetcher từ chối ghi đè log cũ. Không coi HTTP 200 là nội dung đã xác minh.

## Tiếp tục research

Đọc core + prompt của stage cần chạy, truyền catalog record, registry và state hiện có. Cập nhật đúng artifact canonical; dùng report/pipeline/decision templates trong `templates/`. Mỗi unknown cần next action cụ thể. Source snapshots là bằng chứng đọc tĩnh; không chạy trực tiếp code tải về. Không cần tải datasets để dùng catalog/prompts hoặc đọc ba pilot.

Năm/track chưa xác minh để null; availability tách unknown/not_checked/not_public/not_applicable/blocked/verified. Candidate có thể trỏ repo của organizer khi chưa resolve URL competition. Lưu lại đầu mối yếu để audit sau, không nâng thành curated tự động.

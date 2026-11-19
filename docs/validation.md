# Validation — 19/11/2026

Các kiểm tra đã chạy trên bản triển khai này:

- `python3 scripts/lab.py validate`: PASS, 119 competition records; kiểm tra JSON Schema, source/claim references, identity, scoring/null handling, snapshot SHA-256, state và knowledge-card provenance.
- `python3 -m unittest discover -s tests -v`: 14 tests PASS. Bao gồm unknown khác0, duplicate identity khác track, giả nguồn/checksum hỏng, schema extension, export round-trip, scope evidence, incomplete research state và metric semantics.
- `python3 scripts/lab.py build`: tạo Markdown, CSV và SQLite cho119 records.
- `python3 scripts/discover_from_snapshots.py` chạy lại: thêm0 record, không overwrite existing records.
- CLI search đã kiểm tra: curated3; task forecasting2 (gồm candidate M5 chưa audit); Vietnamese+VLSP có kết quả; Tier B+code verified3.
- Tất cả local Markdown file links trong README/docs/prompts/templates/pilots/catalog index và inventory resolve được tại lần kiểm tra.
- `python3 scripts/metric_examples.py`: numerical examples synthetic; macro regional metric khác pooled RMSE, cold-start weight/denominator và AUC tie/monotonic invariance nhất quán.
- `python3 scripts/audit_source_counts.py`: AST-only check, không chạy source tải về. HateDetectron sweep có96 cấu hình khai báo; Landsat88 và Sentinel67 features trong pipeline được đối chiếu với code lists.

Registry có120 retrieval records:116 tải được,4 failed/blocked attempts được giữ lại. Số này là lượt nguồn/file, không phải120 competition hoặc120 nguồn đã audit toàn bộ.

Giới hạn kiểm tra: chưa tải competition datasets/checkpoints, chưa chạy training/inference, chưa có measured EDA, ML reproduction hoặc independent reviewer. Hash kiểm chứng nội dung snapshot không chứng minh tác giả/source luôn đúng. Các pilot và rubric ratings có scope/limitations riêng trong từng report.

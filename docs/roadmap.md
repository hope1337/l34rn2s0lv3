# Roadmap thực thi

Trạng thái19/11/2026. Task 1/2 đã có bản chạy được và đầu ra pilot; nghiên cứu toàn bộ catalog là công việc tăng dần, không coi là đã xong.

## Task 1 — Catalog

- [x] Inventory nguồn Việt Nam/quốc tế, access audit ban đầu và coverage gaps.
- [x] Schema v1, stable ID, provenance, snapshot checksums, identity/dedup constraints.
- [x] Rubric100 điểm và UNRATED khi thiếu căn cứ; score có rationale/source từng tiêu chí.
- [x] Discovery119 entries; curated3 entries đã audit task/metric/results/solution sources.
- [x] Search/filter và export Markdown/CSV/SQLite; import từ snapshot không overwrite.
- [x] Validator và regression tests cho null/evidence/hash/duplicate identity/export.
- [ ] Audit riêng116 discovery entries: year/track/version, rules/data/final results/code/license.
- [ ] Mở rộng candidate catalog theo inventory; ưu tiên thêm curated Việt Nam, speech, NLP và RL.
- [ ] Calibrate rubric sau nhiều competition đa nguồn; chưa gọi3 pilot là calibration thống kê.

## Task 2 — Prompt + research workflow

- [x] Core prompt +10 stage prompts với shared I/O contract, tools, output schemas và acceptance.
- [x] Templates cho report/pipeline/decision card và resumable state A–O.
- [x] Chạy pilot3 task/modalities; có73 claims, fixed-commit code traces, cross-team comparison và falsification plans.
- [x] Phát hiện và ghi differences write-up/code/launcher, row alignment, rounding/normalization và selection bias.
- [x] Self-review, source matrices, metric arithmetic checks; 5knowledge cards có provenance.
- [ ] Hoàn thiện dependency/defaults/full-team execution trace còn thiếu trong từng pipeline.
- [ ] Raw dataset EDA: blocked đến khi có dữ liệu/version được phép dùng; published stats không thay thế measurements.
- [ ] Independent review chưa có; không gắn nhãn đã độc lập kiểm định.

## Task 3/4 tiếp nối

Reproduction chỉ có experiment plans, chưa chạy GPU/training/inference. Có5knowledge cards khởi đầu, chưa có retrieval/synthesis system hoặc cross-competition empirical conclusions. Không tính numerical toy checks là model reproduction.

Thứ tự tiếp tục cụ thể: resolve archive/data access → đo EDA cho một pilot → hoàn thành một faithful pipeline và dependencies → kiểm chứng giả thuyết nhỏ → cập nhật cards. Trong khi data chưa có, vẫn có thể audit nguồn Việt Nam và hoàn thiện code trace.

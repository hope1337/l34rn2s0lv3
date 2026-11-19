# Pipeline forensic — Hateful Memes Phase 2

Kho tổ chức commit `0cc41becf86a83e8b0e9df34886e1bb506f9762b`; top-one code commit `1c4505a5a071ad0bc9df54c3fab0f9896ae5a9b7`; top-three `e55d7c95930c4ca47bbb550a291290133cc11e15`. Đây là versions truy cập19/11/2026, chưa chứng minh đúng commit của winning run2020.

## Top 1 — alfred lab

### Preprocessing / model families

`data_utils/README.md`: OCR→text mask→DeepFillV2 inpaint→OID boxes/face annotations; patch detector cho meme ghép nhiều ảnh; RoI features từ ảnh clean; web entity detection; chèn entity/tags vào annotations. Web service output có artifact tải sẵn theo tác giả; availability chưa thử. Image patch dataset generation/model training không deterministic theo README, tác giả khuyến nghị dùng pretrained asset để reproduce. [memes-preprocess]

VL-BERT branch dùng entity/race tags; UNITER/VILLA chuyển annotations+RoI sang LMDB và fine-tune ITM; ERNIE-ViL thêm diversity theo tác giả. Chưa trace mọi preprocessing constant, tokenizer/padding, region-feature order, bbox normalization hoặc source models. Không gọi đây là complete raw-to-model reconstruction.

### Một cấu hình UNITER đã truy

`UNITER/scripts/train_uniter.sh:16–46` chọn4 model configs (`uniter-large-0`, `uniter-base`, `villa-large-1`, `villa-base-1`), bỏ train nếu checkpoint directory đã tồn tại, test khi thiếu test.csv. Vì vậy tồn tại folder có thể làm skip training; không mặc định script luôn train lại4 models. Docker image tag không phải immutable digest. [memes-uniter-launch]

`config/final_train/uniter-base.json` khai báo pretrained uniter-base; max_txt_len100, conf_th .2, max_bb100/min_bb10/num_bb36; train_batch_size2048, val_batch_size5240, gradient_accumulation4; LR6.25e-5, lr_mul10; valid_steps50, num_train_steps5000; AdamW betas(.9,.98), dropout .2, wd .01, grad_norm2, warmup500, seed42, fp16 True, workers4/pin_mem. **Không** nhân2048×4 rồi tuyên bố effective sample batch: cần truy token bucket sampler và distributed accounting. Config path train_dev_all/val_seen cần audit actual DB membership. [memes-uniter-config]

Training file đã lưu nguồn, nhưng version-specific args merge, loss reduction, optimizer eps, adversarial VILLA branches, checkpoint selection và inference preprocessing chưa trace đủ; các giá trị trên chỉ verified config, không verified winning execution.

### Ensemble / rule / serialization

`run_ensemble.sh` chạy Docker ensemble.py và output tên `test_set_enselble.csv`; README nói `test_set_ensemble.csv` khác chính tả. Giữ đường launcher khi reproduce, không tự chọn tên “đúng hơn”. [memes-alfred-launch]

`ensemble.py:145–187`: glob results cho ernie/vl-bert/uniter, người chạy chọn từng CSV hoặc all; cần ít nhất2. Lấy CSV đầu làm base, merge là arithmetic mean arrays `proba.values` **theo vị trí**, không join IDs/sort/assert alignment. Exact interactive choices không lưu trong code. [memes-alfred-ensemble]

`rasicm_det:63–137` dùng text token similarity với keyword tokens, threshold>.6; các detected race boxes phải đều mang tag cụ thể và nonempty, không có object class “monkey”. Khi bật skin-tone check, đọc ảnh clean OpenCV BGR→HSV_FULL, crop vào nửa giữa bbox, fit KMeans5 và kiểm dominant-cluster hue strict30<h<160 để loại một số matches. Race annotations không được coi ground truth về người trong ảnh. Đây là mô tả rule đội thi, không phải đề xuất policy. [memes-rule-code]

`:189–197`: với IDs rule chọn, proba=1.0; ghi CSV index=False. Không recompute binary label sau mean/rule. Vì metric dùng proba, label có thể không nhất quán chỉ ảnh hưởng accuracy display; muốn khẳng định ảnh hưởng thực tế cần final CSV. KMeans seed, crop edge cases, exact chosen CSV ordering, spacy model version đều chưa xác minh. [memes-alfred-ensemble; memes-rule-risk]

## Top 2 — Muennighoff / Vilio

Đã đọc author README (nguồn `vilio-readme`, branch URL chưa pin). Repo hướng dẫn SCORE_REPRO.md, bash reproduction scripts; hm.py là training entry, param.py args, model-specific entry.py preprocessing, src/vilio models. Models gồm one-stream/two-stream với region features, ensemble mean. Chưa tải/pin đầy đủ code/config/checkpoints của team này, nên **partial**, không suy defaults từ top 1/top 3. [memes-top-two]

## Top 3 — HateDetectron

### Data extension

`utils/concat_memotion-hm.py` lấy symmetric difference image paths hai dev sets, chọn dev_seen-only100 và assert dev_unseen-only140; thêm dev_seen-only vào train, thêm manual Memotion labels, shuffle sample(frac=1) **không random_state explicit**. Comments nêu tổng8928; chưa đo lại. Không gộp cả dev_unseen vào train. [memes-expanded-data]

Visual features theo author là Detectron/MaskRCNN backbone ResNet152, fine-tune VisualBERT checkpoint CC full. Full extraction notebook vượt8MB snapshot limit nên constants (ROI thresholds, normalization, tensor shapes), model dependency và data chronology chưa được truy độc lập; chỉ ghi published description ở phần này. [memes-feature-description]

### Hyperparameter sweep / checkpoint choice

`sweep.py` tạo96 cấu hình từ batch[32, 64, 80], lr_ratio[.3,.6], warmup_steps[250, 500], scheduler[cosine,linear], warmup_factor[.1,.3], warmup_iterations[500, 1000]. 96 là tích vòng lặp, không chứng minh96 runs thành công. [memes-sweep]

`sweep.sh` MMF VisualBERT from_coco config nhưng resume_zoo `visual_bert.pretrained.cc.full`; annotations train từ argument9, validation dev_unseen; feature_dir từ argument8; max_features100; eval/checkpoint interval50, max_updates1000; optimizer LR5e-5; warmup True; batch/lr_ratio/scheduler theo arguments. Chưa pin MMF dependency commit, nên default optimizer/loss/tokenizer không tự điền từ phiên bản mới. [memes-sweep]

`get_27_models.py` đọc last250chars log, lấy ROC/accuracy thành **string** rồi sort ROC descending, head27, move best.ckpt. Chưa cast numeric; lexicographic order chỉ tương ứng numeric trong điều kiện format phù hợp. Đây là fragility, chưa chứng minh selection sai ở winning files. Broad except có thể bỏ log lỗi. [memes-select]

### Inference / majority vote

Notebook `notebooks/[GitHub]reproduce_submissions.ipynb` cell39 chạy generate_submission cho mọi `.ckpt`; cell41 concat prediction CSVs **theo cột/vị trí**. Lấy mỗi3cột để tách proba/label; `sum(labels)>13` → class1 và **max** proba trong toàn bộ models; ngược lại class0 và **min** proba. Không chỉ lấy max của positive-voting models. Assert27×3 columns bị comment; except có thể che partial inputs. Nếu thiếu models, cutoff13 vẫn giữ. [memes-vote-code]

Cell43 reindex theo Phase 2 template IDs rồi save submission#3.csv. URL template trong notebook là signed historical link có expiry; chưa truy cập/không dùng để tải data. Cần thay bằng nguồn được phép hiện tại khi reproduction, ghi rõ modification. Torch1.6/torchvision0.7 pinned nhưng MMF no_feats branch và linked checkpoints chưa được xác minh hash/availability. Không chạy notebook có shell downloads/deletes một cách nguyên xi. [memes-legacy]

## Unknowns chung

Không đủ raw data/weights để kiểm tra model outputs. Training family detail, exact preprocessing constants, run seeds, effective batch, dependency defaults và full winning component inventory vẫn còn thiếu. Không gọi pipeline full, không gán architecture/loss mới của thư viện2026 ngược vào winning run2020.

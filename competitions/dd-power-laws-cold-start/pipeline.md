# Pipeline forensic — Cold Start

Phạm vi: published code ở commit `a22192b86b31c9f9f9f55cf108f1c3aa9c9ce9b1`. Source IDs tra trong [sources](sources.md). Không thực thi code bên ngoài; mọi default thư viện chưa trace đều UNKNOWN.

## Top 1 — last_minute_team

**Chuỗi của Guillermo:** README `scripts/final_solution/README.md` chỉ rõ conda env trong chính folder final_solution, cài seq2seq/recurrentshop và chỉnh DATASET_PATH; input train/test ở đường dẫn riêng. Launcher final_solution thực hiện chuẩn bị metadata/cluster, train tailor/seq2seq, tạo submission và combine. Không đồng nhất output của thành viên A với team-final. [cold-a-launch]

Trong `combine_submissions.py:17–48`, glob toàn bộ CSV seq2seq và tailor, mỗi nhóm mean prediction **theo vị trí dòng**. Sau đó hourly=(tailor+seq2seq)/2; daily/weekly giữ tailor. Hàm không join theo pred_id trước np.mean. Vì vậy row order là precondition; số file được glob và duplicates ảnh hưởng weight. [cold-a-blend]

**Chuỗi team cuối:** `gen-final-pred.sh:2–6` gọi submission_tool với `models/twalen-20seeds.csv`, `data/external/ironbar-best-submission-0.2881.csv`, rồi `selected-trivial-predictions.csv` làm patch. `submission_tool.py:63–78` concat theo index pred_id, mean với `skipna=True`, reindex template, rồi overwrite các ID trong patch. Vì skipna, missing component có thể khiến một dòng chỉ dùng một model; assert chỉ kiểm tra kết quả cuối không NaN. [cold-team-blend]

Cần giữ hai thứ tự khác nhau: mean component submissions → team mean → overwrite patch. Không mô tả đơn giản “average hai NN”. UNKNOWN: exact tập component CSV, cluster features và patch IDs trong winning run chưa được kiểm chứng bằng hashes/logs.

## Top 2 — valilenk

README yêu cầu data/raw → `src/build_features.py` → `src/model.py` → data/submit.csv. Python 3.7, fastai 1.0.19, scikit-learn 0.20.0; setup GPU/128 GB RAM là author-reported. [cold-compute]

`build_features.py:59–94` có temperature missing flag, điền bằng median theo timestamp rồi hour/day-of-year; tạo rolling means 3/6/12/24 giờ, day/week temperature. Các features working schedule được tạo trước xuất X/h/d/w CSV. `:277–291` scale target mỗi series bằng `(x-id_min)/(id_max-id_min+1)`; số cộng **1** khác eps của LastRocky. Chưa audit toàn bộ schedule-clustering feature implementation. [cold-two-path]

`model.py:13–20` cast int64→int32 và float64→float32; gom h/d/w theo thứ tự đó. Cat vocab được tạo trên concat X/test; không đồng nghĩa target test được dùng. `:65–78` StratifiedKFold10, shuffle, random_state42, stratify theo series_id; **không phải GroupKFold**: các rows cùng series có thể nằm cả train/validation. Fastai transforms FillMissing/Categorify, embedding size min(50, category_size//2), bs2048, layers `[512,512,256,64,8,1]`, batchnorm, zero configured dropout, L1 loss, wd .001, true_wd=True/bn_wd=False; fit_one_cycle50 với max LR .01. Exact normalization/default optimizer/callback selection còn phụ thuộc fastai1.0.19, chưa truy dependency. [cold-two-model]

`:90–114` mean prediction mười folds, chia lại h/d/w segments, inverse `prediction*(id_max-id_min+1)+id_min`. Hourly output trực tiếp; daily reshape(-1, 24).sum; weekly reshape(-1, 168).sum; gán vào template theo series. Không tự clip negative hay round nếu code không làm. So với câu “single neural network” trong summary, published script chạy **10 folds của một model family**: không nên hiểu là chỉ một checkpoint. Pipeline vẫn partial vì dependency defaults và exact winning run chưa xác minh. [cold-two-model]

## Top 3 — LastRocky

### 1. Load, encode, lags

`prepare_data.py:21–34` parse timestamp rồi concat train consumption và cold_start_test. Tính min/max/mean consumption theo series trên **observed data**, trước local tail validation. Lags hourly=336, daily=14; weekly generation cuối file bị comment, không có weekly training active ở file này. [cold-preprocess]

`add_basic_features:37–86`: month/day/day_of_week/hour, map surface theo dictionary explicit, base_temperature low→1/high→0, is_off_day từ metadata weekday. `get_dummies(drop_first=True)` trên bảng kết hợp train/test feature rows; bỏ bảy cột weekday-off gốc. Không diễn giải `drop_first=True` thành one-hot đủ mọi category.

`create_lagged_features:156–171`: shift(i) trong từng series; không reindex cadence. `prepare_training_data:174–187` chỉ MinMaxScaler nếu use_scaler=True; call thực tế mặc định False. Tên `_no_scaler` không có nghĩa model không normalize: model scripts normalize thủ công sau đó.

`preprocess_test_day:251–259` group consumption **sum**, temperature **nanmean** theo `(series,date)`. `prepare_test_data:190–217` mở daily/weekly windows thành hourly hoặc daily rows, dịch timestamp +23h và lùi từng giờ/ngày; sort series/time. Định nghĩa interval/timestamp phải đối chiếu, không đổi tùy ý sang resample default.

### 2. Normalization và validation

Hourly target/lag:

\[
z=2\frac{x-a+10^{-5}}{b-a+10^{-5}}-1
\]

Daily thay a,b thành 24a, 24b và eps=10^-2. Weekly lag branch dùng eps=10^-3, trong khi weekly target branch dùng 10^-2. Không gộp hai eps thành một. Các cột metadata không dùng công thức này. [cold-normalize]

`hour_models.py:66–85` dựa **thứ tự** unique series: 758 series đầu không lấy validation; phần sau lấy tail `min(24,2^(nr//24-1))` cho hourly. Đây là assumption về order, không phải group-ID criterion. DEBUG_MODE=False; nhánh train cuối dùng cả rows tr+val, không áp early stopping của nhánh debug. [cold-split]

### 3. Hourly training

`hour_models.py:54–63`: 336 lag + 48 OHE + day =385 features cho trees (đếm từ danh sách code, không phải EDA). LightGBM params: regression_l1/mae, depth12, max_bin255, leaves64, LR .01, feature_fraction .75, bagging_fraction .75, bagging_seed123, bagging_freq100, min_data_in_leaf30, min_sum_hessian .3; num_boost_round=13000. XGB: eta .03, depth12, subsample .75, colsample_bytree .75, reg:linear, min_child_weight32, mae, seed123, 400 rounds. [cold-hour-training]

NN dùng 168 lag reshape `(batch,1,168)`, hai LSTM 600 units, metadata Dense600 ELU, concat, dropout .25, Dense300 ELU, dropout .25, Dense1. Dòng `y=Dropout(.5)(ohe_input)` sau đó bị thay bằng `Dense(...)(ohe_input)`, nên dropout metadata đó không nằm trên output graph. MAE/Adam, batch128, shuffle True, 16 epochs; LR=0.001×0.5^floor(epoch/3). `ModelCheckpoint(monitor=val_loss)` ở full training không có validation_data: chưa xác minh artifact save behavior của Keras version, không gọi đây là best-validation checkpoint. Missing values được fill0 cho NN. [cold-shape; cold-hour-training]

Chưa trace Adam defaults/version, initializer, exact precision, RNG ngoài các seed cụ thể và checkpoint serialization. Không đổi input sang `(batch,168,1)` trong faithful reproduction dù cấu trúc đó có vẻ tự nhiên hơn.

### 4. Hourly inference

`hourly_sub.py:145–224`: each model prediction clip [-1, 1]. NN fillna0 và dùng lag first168. Recursive horizon 24/168/336 hourly steps; dịch lag vector, chèn **prediction của model đang chạy**. Chạy riêng mỗi model rồi blend normalized predictions .1 XGB+.5 LGB+.4 NN. Inverse scale `(z+1)/2*(b-a)+a`, **không đưa eps trở lại inverse**. Group sum theo pred_id, merge template và giữ column order. [cold-hour-infer]

### 5. Daily/weekly inference

`daily_sub.py:209–281`: forecast 7 ngày cho daily hoặc14 ngày cho weekly. Bước đầu dùng daily lags +168 hour lags, blend .3LGB+.3XGB+.4NN. Các bước sau bỏ hourly features, blend .5LGB+.3XGB+.2NN; recursive state nhận prediction hỗn hợp. Inverse scale dùng extrema×24; group sum theo pred_id để ra weekly total khi cần. Ghép hourly rows từ hourly file và nonhourly từ daily pipeline, sort pred_id rồi save final_sub.csv. [cold-daily-infer]

Daily NN có branches `(batch,1,14)` và `(batch,1,168)` nếu dùng giờ, hidden LSTM300/metadata300/final100; MAE/Adam ở function code. Training scripts daily đã snapshot nhưng chưa audit mọi branch/config nên không gán filename epochs thành verified executed epochs.

### 6. Blockers và khác biệt tài liệu/code

- Official summary viết “LSTM + LightGBM”; source active còn XGBoost với trọng số rõ. [cold-hour-infer; cold-daily-infer]
- Tree listing có ba LightGBM text assets; inference còn yêu cầu .hdf5 và .joblib.dat chưa thấy trong listing. Không download weights trong task này. [cold-assets]
- Global extrema có thể nhìn vào local validation tail, dù không dùng hidden test targets. Cần đo prefix-only scaling để đánh giá validation optimism. [cold-validation-risk]
- Đường NN training checkpoint có monitor thiếu validation; phải tái tạo version behavior trước khi tin command full-run.
- Chưa có deterministic run manifest hoặc measured score; pipeline này là reconstruction của published code, **không phải đã tái hiện winning execution**.

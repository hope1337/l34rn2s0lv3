# Pipeline forensic — Tick Tick Bloom

Commit `c59c9ab9e3d376bfd24a2b85e821776100d46230`. Published implementation; chưa chạy dữ liệu. [Sources](sources.md).

## Top 1 — sheep

### Entry point và feature extraction

README mô tả notebooks, nhưng **reproduce.sh thực tế gọi hai file .py**: cd notebooks → Sentinels_features.py → Model.py. Không mặc định notebook là đường active. [bloom-entry]

`Sentinels_features.py:23–45` lấy `W_*.png` mask, suy uid từ token `_` thứ ba, tìm image bằng bỏ `W_`. Đọc bằng skimage.io.imread; resize mask OpenCV lên `(img.width,img.height)`, stack3channel rồi so `==6` chọn water. Không truyền interpolation argument; cần truy OpenCV version/default, không tự mô tả nearest-neighbor categorical resize. [bloom-water-features]

Không water pixel → năm thống kê NaN. Nếu có: mean channel0/1/2 thành R/G/B; percentile green95/5 thành GMax/GMin. Tạo G/R,G/B,R/B,GMax/B,GMin/B; không eps hoặc explicit division-by-zero guard trong file. Không thấy /255 normalization trong stage này; không suy raw reflectance scaling từ PNG feature stage. Xuất Sentinels_available_features.csv. [bloom-water-features]

### Model, validation, ensemble

`Model.py:50–88`: concat HRRR CSV, bỏ duplicate id giữ đầu; merge metadata/labels/weather bằng inner và merge water features left. Inner join có thể làm mất uid: chưa đo coverage. Month/year tạo từ date; year bị drop trước model. [bloom-topone-code]

`:99–164`: lặp100 lần. Chỉ train midwest+northeast; KMeans100 dùng `(longitude,latitude)`, không explicit random_state; GroupKFold5 theo cluster. Drop latitude/longitude/year/cluster/fold/uid/date/split/severity/density cho train features. Region map midwest0,south1,northeast2,west3 và khai báo categorical. LightGBM regression/gbdt/rmse, LR .005, bagging_fraction .3, feature_fraction .3, min_split_gain .1, data_random_seed2023, tối đa30000 rounds, early_stop500. Không tự gán bagging_freq nếu config không có; hiệu lực bagging cần đối chiếu LightGBM default/version. [bloom-topone-code]

Validation raw preds→np.round→integer rồi tính **pooled** OOF RMSE của hai vùng; đây không tự động bằng official bốn-vùng metric. Test mean prediction của500 boosters dự kiến. KMeans stochastic và early stopping có thể làm run khác nhau, chưa biết exact winning run hashes. [bloom-validation]

### Regional routing / submission

`:175–180`: KDTree Euclidean trên `(latitude,longitude)` **độ**, leaf_size30, query k100; predicted severity = sum(y/d)/sum(1/d), không eps zero-distance. Không biến thành khoảng cách km/haversine trong mô tả faithful. KNN fit toàn train_full, không chỉ south/west. [bloom-knn]

`:181` `knn_test` lại copy từ `test` (đang có LGB prediction), không phải `test_df` vừa nhận KNN. Đây là inconsistency intermediate. Tuy nhiên `:190–197` output cuối lấy mg_test **chỉ northeast/midwest**, và lấy `test_df` KNN cho các uid khác. Vì vậy không thể kết luận final south/west dùng LGB chỉ do dòng181. [bloom-code-risks]

Midwest/northeast: continuous prediction→pseudo_round thresholds **1.65, 2.55, 3.5, 4.5** thành1–5. South/west: `int(np.round(KNN))`. Cuối cùng set uid index → loc đúng order test_df.uid → submission.csv. Không dùng chung threshold policy cho cả bốn vùng. [bloom-round]

Unknown: bounds/casts của ảnh trước PNG, complete download/registration details, exact version-specific defaults, tất cả images/model artifacts và record winning execution.

## Top 2 — apwheele

README: data CSVs → main_prepdata.py tạo SQLite → main_preds.py fit/cache models→submission. Existing SQL tables làm data prep không idempotent; tác giả cảnh báo rerun download khi DB đã populated. Có code/env và một số cached feature CSV trong tree, chưa tải CSV dataset. [bloom-second]

`main_preds.py:22–48` fit CatBoost380 iterations/depth6 (date, region/cluster, latitude/longitude/maxe/dife), LightGBM470estimators/depth8 (thêm imtype, elevation và color/coverage stats1000/2500), XGBoost70estimators/depth2 (date/region/cluster). Các calls đều weight=False; LightGBM cat=True, hai model kia cat=False trong RegMod wrapper. Feature transform cụ thể vẫn cần trace src/feat.py và RegMod defaults. [bloom-second]

Kết hợp ba model qua EnsMod; `src/mod.py:454–472` mean predictions, **clip1–5 → round → int**. `main_preds.py:51–68` lấy test, map submission format rồi save `sub_BESTRESULTS_0216.csv`; README nhắc submission khác, nên không coi README date filename là exact command artifact. Các stats satellite theo README có KMeans segment vùng nước, khác mask class6 top-one. Chưa trace kmeans seed, split weights và third-party estimator defaults nên không gán hyperparameters từ top-three. [bloom-second]

## Top 3 — karelds

### Acquisition / selection

`main.ipynb` chỉ thứ tự scripts: download satellite train/test cho lsat/snel → HRRR grid mapping → TMP/SPFH downloads → create_datasets.py → train.py → test.py. Notebook cũng có tùy chọn lấy processed/model archives; links chưa được tải/test. [bloom-third-entry]

`create_datasets.py:17–65`: Landsat giữ1 scene/uid; Sentinel tối đa15. Longitude feature = round(longitude/10), **không nhân10 trở lại**, là coarsened encoding. HRRR TMP/SPFH aggregate min/mean/max theo uid; loại landsat-7 trong selection script. Image quality0 nếu mean(arr)<1, ngược lại1; sort quality descending, cloud_cover ascending, datetime descending rồi head(nsamples) theo uid. `days_before_sample` là date label trừ acquisition date. Chưa hoàn thành audit query temporal bound/projection trong download script, nên official “no future data” chưa được xác nhận end-to-end. [bloom-third-select]

### Features và dtypes

`train.py:60–157`: NPZ arr_0→float32, shape giả định `(bands,height,width)`; mean/min/max theo axes(1, 2), range=max-min. Concat theo thứ tự mean,min,max,range; metadata `[month,days_before_sample,longitude]`.

Landsat19 bands×4stats +3meta +3indices +6weather =**88** features. NDVI=(nir-red)/(nir+red+1), code đặt tên ndwi cho (nir-swir22)/(nir+swir22+1), mndwi=(green-swir22)/(green+swir22+1). Không “sửa” tên/formula theo textbook khi reconstruct. Weather chỉ nằm trong Landsat feature list. [bloom-third-features]

Sentinel15 bands×4 +3meta +4indices =**67** features. B8 với B4/B5/B6/B7; tất cả denominator cộng1. Không chuẩn hóa /255 trong feature function. Features cast float32, target int8. Note `get_features_*` append severity vào DataFrame rồi bỏ trước predict; test placeholder severity=-1 không tự trở thành input feature. [bloom-third-features]

### Splits, training và inference

`split_data`: StratifiedGroupKFold5, shuffle=True, random_state41, stratify region, groups uid; split riêng Landsat/Sentinel tables. Giữ scenes cùng uid trong fold của từng table, không đảm bảo lake-level separation hay fold ID consistency cross-table. Seeds Python/numpy41; PYTHONHASHSEED gán trong process không đủ chứng minh hash determinism của process hiện tại. [bloom-third-split]

Train mỗi region và satellite family, 5 folds: regression/rmse, max_depth-1, num_leaves31, LR .1, bagging_seed41, seed41, tối đa100000 rounds, early_stop100. Best iteration prediction behavior cần pin LightGBM; không tự ghi mọi model train100000 rounds. Save `{sat}_{region}_{fold}`. [bloom-third-train]

Inference lặp region×family×fold, predict scenes. Concat tất cả predictions → groupby(uid,region).mean().round(). Do đó weight theo **số scene records**: nếu một uid có15 Sentinel scene và1 Landsat scene, mean này không phải equal-weight hai satellite models. Output fallback cho uid không data = mean **rounded severity** của region đã có prediction rồi round. Cast int, reindex template uid, assert uid sequence và save solution.csv. Không explicit clip1–5; đừng thêm bước không tồn tại. [bloom-fallback]

### Unknowns / config audit

Band scale/projection/masking, API versions, complete acquisition history, archives/current weights access, exact hashes và numeric behavior của legacy pandas append/groupby cần kiểm tra. Không dùng comment cuối train.py chứa một score làm reproduction result. Fold scores đo ở scene rows và final uid aggregation cũng cần phân biệt.

# Solution Forensics (E/G/L)

Input: selected team, pinned repository tree/commit, write-up, config/env, entry points and artifact inventory. Output: source map, pipeline.md per team, config audit, compute constraints and unresolved execution paths.

Trace launcher → config merging/defaults → preprocessing → split/sampler/loader → model/targets/loss → training → checkpoint selection → inference → ensemble → submission. Record callable, file/lines, tensor shape, dtype, constants, operation order and branch conditions. Audit RGB/BGR, /255 and dtype order, normalization, resize interpolation/padding, all transform probabilities, label mapping, loss reduction/eps/masks, LR/warmup, effective batch, seed/worker seed, precision, threshold/NMS, ensemble weights and row alignment. Trace library code at dependency version where defaults matter.

Separate what write-up claims, published code implements, and run logs prove was executed. An unused file does not establish use. Check pseudo-label provenance, external assets and data transformations shared across folds. Do not run downloaded code as part of this stage.

Acceptance: reconstructible order through submission for each claimed complete path; every unavailable parameter marked unknown with its impact; no claim of full reconstruction when callers/dependencies/weights are absent. Include commands only if present in sources, or explicitly label proposed commands.

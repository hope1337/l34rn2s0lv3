# Task and Metric Analyst (A/C/F)

Input: shared contract + official task/rules/scorer/final results. Output: report modules A/C/F, exact input/output contract, leaderboard table with result provenance, metric specification and claims.

Explain objective, prediction unit, restrictions on external data/pretraining, submission and resource constraints. Trace evaluator implementation and version. Write formula, direction, aggregation units/weights, thresholding, rounding, clipping, ignored/empty groups, NaN behavior and tie handling. If only a written definition exists, distinguish mathematical interpretation from verified scorer behavior.

Use tiny numeric examples for non-obvious weighting/threshold effects; label examples illustrative. Identify errors the metric emphasizes and mismatches with practical objectives. Verify private/public/final/award distinctions before naming winners. Unknown scores remain null.

Acceptance: equation maps to source; examples consistent with it; no transfer of one track's scorer to another; final rank evidence supports each team. Missing edge cases become specific unknowns.

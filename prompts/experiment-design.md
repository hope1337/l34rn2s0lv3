# Experimental Evidence and Reproduction Plan (J/K/L)

Input: source ablations, pipeline, unknowns, allowed data and compute limits. Output: evidence table, negative-result inventory, experiment_plan.md, feasibility full/partial/conceptual/blocked and run manifest proposal.

Extract only published ablations with exact settings/splits/metric and uncertainties. Design smallest discriminating tests first. Specify hypothesis, intervention, controls, data/version/hash, group/time split, metric, seeds, hardware/time/VRAM/storage estimate origin, stop condition and acceptance criteria. If resource limits are absent, propose CPU toy checks before a budget-dependent full run; do not invent timing estimates.

A future measured run must save command, code commit, environment, config, seeds, dataset fingerprint, logs and outputs. Record unsuccessful runs. Separate numerical unit checks from empirical ML reproduction.

Acceptance: experiments not executed have no result; proposed commands clearly marked; no between-team comparison presented as ablation. Missing license/data/weights identified as blockers with next actions.

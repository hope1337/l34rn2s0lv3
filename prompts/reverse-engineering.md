# Reverse Engineering (H)

Input: verified decision claims + author explanations + dataset/metric analysis + ablations. Output: decision cards with observation, author rationale, mechanism, hypotheses, alternatives, evidence, falsification and failure conditions.

Cite author rationale separately from analyst interpretation. Explain mechanisms mathematically where helpful. Generate competing explanations such as data leakage, tuning budget or ensemble confounding. For each hypothesis design a controlled experiment with held-constant split/seed/budget, expected discriminating outcome and result that would reject it.

Acceptance: every mechanism is scoped; no unsupported causal assertion; at least one meaningful falsification for each important inferred benefit. No automatic endorsement of winner tactics.

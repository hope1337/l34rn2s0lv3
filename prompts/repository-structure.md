# Repository Structure

Before writing, inspect existing files and update the canonical artifact. Follow this implemented layout; the master brief's larger proposed tree is not a requirement to create more folders.

```text
catalog/                 # competition records and discovery sources
  discovery/<id>.json    # candidates
  curated/<id>.json      # audited records; move here, do not duplicate
  sources/               # inventory, registry, fetch manifests/logs
  indexes/               # generated Markdown/CSV/SQLite
competitions/<id>/       # one research directory per competition identity
  report.md              # task, data, metric, results, reasoning, comparison
  pipeline.md            # all selected teams, separated by headings
  sources.md             # source map
  evidence.json          # canonical claims
  evidence_matrix.md     # readable view of those claims
  experiment_plan.md     # proposed experiments
  quality_review.md      # audit findings
  state.json             # progress, blockers, next actions
  latex/                 # LaTeX report and figures; reserved for every competition
    main.tex             # report entry point, created when writing is requested
    references.bib       # cited sources
    figures/             # TikZ/PGFPlots .tex, small plot tables and figure assets
    build/               # generated compilation output, gitignored
techniques/              # shared knowledge_cards.json
prompts/                 # reusable agent instructions
schemas/                 # machine-readable contracts
templates/              # reusable document templates
docs/                   # project-wide methodology, roadmap, backlog
scripts/                # maintained reusable tooling
tests/                  # meaningful tooling tests
evidence/snapshots/     # shared source bytes named by SHA-256
```

Rules:

1. Keep competition IDs stable across records, directories and references. Check aliases/year/track/evaluation version before adding a candidate.
2. Put new analysis into the existing report or pipeline section. Do not create parallel summaries, per-team/per-stage folders, session notes or `final_v2` copies.
3. Create allowed research files only when the stage produces substantive content. Every competition research directory includes latex/; retain .gitkeep there until real source exists. This reserved directory is the exception to empty-scaffolding avoidance. List actual research artifacts in state.json.
4. Put temporary exploration and one-off helpers outside the repository. Preserve the master brief and unrelated/user-created files.
5. Preserve retrieval logs; use new source IDs and dated manifest/log batches for refreshes. Share snapshots by reference. Synchronize claims with their Markdown view. Generate indexes through existing scripts.
6. Add persistent infrastructure only when the current task needs it. For a necessary structural extension within the authorized scope, update this map and affected links/contracts together; otherwise record the idea in the existing backlog.
7. Before handing off, review newly created paths and local links. Run `python3 scripts/lab.py validate` when structured research data changes; rebuild indexes when catalog contents change. The validator does not enforce this directory map.

Routine competition research needs no new top-level directory. Dataset/model runs belong to separately scoped experiment work, not ordinary source research.

For requested LaTeX reports, use templates/latex-report.tex as a starting point. Keep the Markdown/evidence files as research sources and cite the same verified claims in the typeset report. Prefer TikZ/PGFPlots for diagrams and plots; preserve figure source and input tables. Never invent plot data. Compile inside latex/ with `latexmk -xelatex -outdir=build main.tex`; keep generated files in build/, and visually inspect the PDF before delivery. Do not globally ignore PDFs: source figures and intentionally delivered PDFs may be retained. Do not install TeX or build a report merely to reserve the directory.

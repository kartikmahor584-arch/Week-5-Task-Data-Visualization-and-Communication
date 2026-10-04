# Health and Wealth of Nations, 1952-2007 — Data Visualization Portfolio

Week 5 task: Data Visualization and Communication.

## Contents
- `Data_Visualization_Narrative_Report.pdf` — 11-page narrative (storyboard, per-figure rationale and insight, limitations)
- `figures/` — 7 static figures (PNG, 200 dpi)
- `interactive_health_wealth.html` — animated bubble chart (open in any browser; works offline)
- `make_figures.py`, `interactive.py`, `build_report.py`, `stats.py` — fully reproducible code

## Reproduce
    pip install pandas numpy matplotlib plotly reportlab pillow
    python make_figures.py && python interactive.py && python build_report.py

Dataset: Gapminder, bundled with Plotly (`plotly.express.data.gapminder()`), 142 countries, 1952-2007.

# NPS Under the Microscope

**An interactive research essay by David Bar-El, PhD, a mixed-methods UX researcher.** Five story-led lessons move from the rise of NPS to the information it hides, measurement context, month-to-month uncertainty and exploratory text-informed analysis. Each lesson has a concise argument, an interactive experiment, prominently labeled key takeaways and references. The site includes an authorship callout immediately under the opening and an invitation to connect on [LinkedIn](https://www.linkedin.com/in/david-bar-el-ph-d-098bbb86/).

## Open immediately

Open **`preview.html`** in any modern browser. This is a self-contained interactive page with precomputed synthetic model results (no web server, Quarto or R required).

## Render with Quarto

```bash
quarto preview
# or
quarto render
```

The Quarto website includes `index.qmd` and `methods.qmd`. All five lessons are **embedded directly in the Quarto document without an iframe**. JavaScript and CSS are separate local assets. You can also open `preview.html` as a standalone fallback.

## Run the R analysis

```bash
Rscript scripts/analyze.R
```

Uses only base R for the core analysis. For HC3 robust standard errors matching the displayed website model, install the optional R package `sandwich`.

## Regenerate synthetic data and website results

```bash
python -m pip install numpy pandas statsmodels
python scripts/generate_data.py
python - <<'PYTHON'
from pathlib import Path
p = Path('assets')
(p/'model_results.js').write_text('window.NPS_MODEL_RESULTS = '+(p/'model_results.json').read_text()+';\n')
PYTHON
python scripts/build_preview.py
```

`index.qmd` is the single source for lesson copy and interactive markup. If you edit the narratives or browser assets, run `python scripts/build_preview.py` to refresh the standalone `preview.html` and `assets/playground.html` **from the Quarto source**. This keeps them synchronized. The GitHub Pages workflow still builds the actual Quarto site from `index.qmd`.

The generator is deterministic with seed `20261016`. It creates **fictional** open-ended feedback from predefined phrases. Topic indicators are intentionally interpretable but should not be mistaken for human qualitative coding or a validated NLP pipeline.

## What is in the project?

- `index.qmd` — Quarto website entry point
- `methods.qmd` — transparent methodology and R workflow
- `assets/playground.html` — standalone copy of the five lessons, built from `index.qmd`
- `assets/model_results.js` — browser-friendly model results generated from data
- `assets/model_results.json` — machine-readable model summary
- `data/fictional_bank_nps.csv` — 1,600 synthetic respondent-level responses
- `scripts/generate_data.py` — reproducible synthetic data generation and HC3 model estimation
- `scripts/analyze.R` — NPS calculations, respondent-level OLS model, sample-size math, sampling simulation and a two-wave uncertainty comparison in R
- `.github/workflows/publish.yml` — GitHub Pages deployment
- `preview.html` — standalone offline browser preview
- `scripts/build_preview.py` — builds synchronized standalone HTML previews from `index.qmd` and local assets

## Statistical and interpretive cautions

1. All distributions, coefficients, survey wording and customer feedback are fictional.
2. NPS is an aggregate statistic; the key-driver outcome is the original 0–10 recommendation score.
3. Topic mentions capture respondents' chosen explanations, not the prevalence of real underlying problems.
4. Coefficients are adjusted associations, not causal intervention effects.
5. Sampling simulations assume independent draws, stable populations and no selection or nonresponse bias.
6. The sampling lab uses a transparent normal-approximation planning formula. It does **not** present the shaded target band as a confidence interval. Lesson 4 Part B is a separate approximation of the confidence interval for the **difference between two independent monthly NPS estimates**.
7. Different score-specific open-ended questions do not make all analysis impossible; they make cross-score comparisons more difficult to interpret because question wording is confounded with score.

## Publish

Enable **GitHub Pages → Build and deployment → GitHub Actions** in your repository settings. Push to `main`. The workflow installs Quarto, renders the site and deploys `_site`.

## References

References are embedded in the five lessons and collected in a collapsible reading list at the end. Source claims are distinguished from mathematical demonstrations and synthetic illustrative results.

## Posit Cloud setup and publication

The Quarto version embeds the lesson sections directly rather than through an iframe, with local CSS and JavaScript assets. The standalone `preview.html` in the project root works without Quarto or R. **In Posit Cloud:** unzip the new project into a fresh directory, open its Terminal, run `quarto render`, and use the Posit Cloud Viewer or hosted preview to inspect the generated website. Do not open `localhost` directly in your phone's browser: that refers to the phone, not the remote Posit Cloud container.

To check assets in the built site, confirm `_site/assets/lessons.css`, `_site/assets/lessons.js`, and `_site/assets/model_results.js` exist. The original standalone `preview.html` remains available as a fallback.

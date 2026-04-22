<p align="center">
  <img src="figures/logo.png" width="200" alt="Phishing Arena Logo"/>
</p>

# Phishing Arena

**A Multi-Agent LLM Tournament for Adversarial Email Security Research**

[![arXiv](https://img.shields.io/badge/arXiv-XXXX.XXXXX-b31b1b.svg)](https://arxiv.org/abs/XXXX.XXXXX)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)

---

## Overview

Phishing Arena is a controlled, reproducible benchmark where four commercial LLMs compete in rotating roles — **Phisher**, **Filter**, and **Target** — to study adversarial email security dynamics in Italian.

The system runs a full tournament of 48 matches across 24 role permutations × 2 repetitions, with 20 rounds per match. The Phisher agent is equipped with a **CampaignMemory** feedback loop that accumulates round outcomes, enabling adaptive behavior without prescriptive instructions.

### Key Findings (Italian corpus)

| Role | Best Model | Key Metric |
|------|-----------|-----------|
| Phisher | `gpt-5.4-mini` | 12.9% bypass rate, +14.6pp adaptive trend |
| Filter | `claude-sonnet-4-6` | 98.3% accuracy, 0.7% FPR |
| Target | `grok-4-fast-non-reasoning` | 50.0% avg click probability |

**Critical finding**: 79% of successful bypasses show no identifiable evasion technique — they succeed through contextual plausibility, not technical obfuscation.

---

## Architecture

```
Round flow:
  [Phisher] → email → [Filter] → bypass? → [Target]
      ↑                                        |
      └──────── CampaignMemory ←───────────────┘
```

Three roles per match:
- **Phisher** — generates contextualised phishing emails targeting a synthetic professional profile
- **Filter** — classifies each email as phishing or legitimate (blind: no knowledge of phisher techniques)
- **Target** — simulates a realistic user reaction if the email bypasses the filter

---

## Models

| Model | Provider | Role(s) |
|-------|----------|---------|
| `claude-sonnet-4-6` | Anthropic | Phisher / Filter / Target |
| `gpt-5.4-mini` | OpenAI | Phisher / Filter / Target |
| `deepseek-chat` | DeepSeek | Phisher / Filter / Target |
| `grok-4-fast-non-reasoning` | xAI | Phisher / Filter / Target |

---

## Installation

```bash
git clone https://github.com/[USERNAME]/phishing-arena
cd phishing-arena
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Set your API keys in a `.env` file at the project root:

```
ANTHROPIC_API_KEY=...
OPENAI_API_KEY=...
DEEPSEEK_API_KEY=...
XAI_API_KEY=...
```

---

## Usage

### Run the full tournament

```bash
python run_test.py
```

The script will prompt you to delete any existing checkpoint before starting fresh. The tournament resumes automatically from the last completed match if interrupted.

### Development mode (Gemini only, zero cost)

Set `MODE = "dev"` in `config.py` to run with three Gemini 2.5 Flash instances for architecture testing.

### Generate paper figures

```bash
python paper/figures/generate_figures.py
```

Output: `figures/*.pdf` — vector format, ready for Overleaf.

---

## Tournament Configuration

```python
TOURNAMENT = {
    "rounds_per_match": 20,
    "phishing_ratio":   0.40,
    "matches_per_pair": 2,
}
```

| Parameter | Value |
|-----------|-------|
| Total matches | 48 |
| Expected rounds | 960 |
| Evaluated rounds | 949 (98.9%) |
| Target archetypes | 12 |
| Legit emails per archetype | 50 |

---

## Dataset

12 Italian professional archetypes with varying cybersecurity familiarity levels (very low → high), each paired with 50 contextualised legitimate emails. Archetypes span: CEO, CFO, HR Manager, IT Manager, Responsabile Acquisti, Direttore Marketing, Commerciale, Avvocato, Contabile, Office Manager, Responsabile IT Bancario, Titolare Hospitality.

---

## Results

Full tournament results are available in `data/results/`. The analysis report is in `paper/`.

To reproduce the analysis, run the tournament with the provided configuration and apply `analysis/metrics.py` to the output JSON.

---

## Citation

If you use Phishing Arena in your research, please cite:

```bibtex
@misc{[COGNOME]2025phishingarena,
  author    = {[Nome Cognome]},
  title     = {Phishing Arena: A Multi-Agent {LLM} Tournament
               for Adversarial Email Security Research},
  year      = {2025},
  publisher = {arXiv},
  url       = {https://arxiv.org/abs/XXXX.XXXXX}
}
```

---

## License

MIT License — see [LICENSE](LICENSE) for details.

# ​ Chess Game Analyzer

A Python-based data analytics project that extracts insights from historical chess match data. It uses Pandas and NumPy for data processing and statistical analysis, Matplotlib to visualize trends, openings, and player strategies, and includes an interactive Streamlit dashboard to showcase key performance factors.

---

##  Features

- **Data Cleaning & Processing** — Load, clean, and analyze chess match data using Pandas and NumPy.
- **Statistical Analysis** — Compute meaningful metrics such as opening popularity, average move counts, and win-loss ratios.
- **Visualization Tools** — Generate insightful visualizations using Matplotlib (e.g., trend charts, bar plots, strategy heatmaps).
- **Streamlit Dashboard** — A sleek, interactive UI that allows users to explore key performance factors and visual trends dynamically.

---

##  Getting Started

###  Prerequisites
- Python 3.8+
- `uv` package manager (or use `pip` if preferred)

###  Installation with `uv`

uv init chess-game-analyzer
uv add pandas numpy matplotlib streamlit
uv run streamlit run main.py

Or via pip
bash
Copy
Edit

pip install pandas numpy matplotlib streamlit
streamlit run main.py


Usage
1. Clone the repository
git clone https://github.com/Aakash-1603/Chess-Game-Analyzer.git
cd Chess-Game-Analyzer


2. Install dependencies using uv or pip (see above).

3. Run the Streamlit app
streamlit run main.py


4. Explore visualizations like:

Opening frequency and popularity

Win/loss trends over time

Player strategy comparisons


Project Structure :-
| File / Folder   | Description                                      |
| --------------- | ------------------------------------------------ |
| `main.py`       | Streamlit app powering the interactive dashboard |
| `games.csv`     | Historical chess match data (source dataset)     |
| `Lichess.ipynb` | Jupyter notebook used for exploratory analysis   |



Contributing
🐛 Found a bug? Please open an issue!

⭐ Love the project? Give it a star!

🤝 Want to improve it? Feel free to submit a pull request.



Let’s explore chess analytics together! ♟

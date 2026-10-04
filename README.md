# 🌍 Health and Wealth of Nations (1952–2007)
### A Data Visualization & Storytelling Project

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-150458?logo=pandas)
![Matplotlib](https://img.shields.io/badge/Matplotlib-Visualization-11557c)
![Plotly](https://img.shields.io/badge/Plotly-Interactive%20Charts-3f4f75?logo=plotly)
![Status](https://img.shields.io/badge/Project-Completed-success)

## 📌 Project Overview

This project explores how life expectancy and economic prosperity have evolved across countries between 1952 and 2007.

Using the Gapminder dataset, the analysis investigates the relationship between GDP per capita and life expectancy, identifies regional inequalities, highlights countries that experienced significant improvements or setbacks, and demonstrates how data visualization can transform complex information into meaningful insights.

The project focuses on **visual storytelling**, combining statistical analysis, carefully selected chart types, and narrative explanations to communicate findings effectively.

## 🎯 Objectives

- Analyze global life expectancy trends from 1952 to 2007.
- Understand the relationship between GDP per capita and life expectancy.
- Compare health improvements across continents.
- Identify countries with exceptional progress and unexpected declines.
- Investigate countries performing above or below income-based expectations.
- Communicate findings through static and interactive visualizations.

## 📊 Dataset Information

**Dataset:** Gapminder

**Source:** Plotly Express Gapminder Dataset

**Period:** 1952–2007

**Coverage:** 142 countries

**Total observations:** 1,704

### Key Variables

| Variable | Description |
|---|---|
| Country | Country name |
| Year | Observation year |
| Life Expectancy | Average expected lifespan at birth |
| Population | Country population |
| GDP per Capita | Economic output per person |
| Continent | Geographic region |

## 🛠️ Tools & Technologies

- Python
- Pandas
- NumPy
- Matplotlib
- Plotly
- ReportLab
- Jupyter Notebook

## 📈 Visualization Portfolio

The project contains seven visualizations, each designed to answer a specific analytical question.

### 1. Continental Life Expectancy Trends
**Question:** How much did the world improve, and which regions benefited most?

A multi-line chart compares population-weighted life expectancy across continents.

**Key Insight:** Global life expectancy increased from 48.9 years in 1952 to 68.9 years in 2007, representing a gain of approximately 20 years.

### 2. Population by Life Expectancy Band
**Question:** How many people benefited from improvements in health?

A 100% stacked area chart illustrates the changing population distribution across life expectancy groups.

**Key Insight:** The proportion of people living in countries with life expectancy below 60 years decreased from 72% to 13%.

### 3. GDP per Capita vs Life Expectancy
**Question:** Does greater wealth always mean longer life?

Bubble scatterplots compare income and life expectancy in 1952 and 2007.

**Key Insight:** GDP per capita explains approximately 65% of cross-country life expectancy variation in 2007, indicating a strong association but not proving causation.

### 4. Same Income, Longer Life
**Question:** Can countries achieve better health outcomes without equivalent income growth?

A comparative line chart examines predicted life expectancy at fixed income levels.

**Key Insight:** At an income level of $1,000 per person, predicted life expectancy increased from 43.1 years in 1952 to 54.7 years in 2007.

### 5. Progress Is Not Guaranteed
**Question:** Can life expectancy decline despite long-term global progress?

Small multiple charts investigate six countries with substantial declines.

**Key Insight:** Conflict, famine, and the HIV/AIDS epidemic are important historical contexts for understanding major reversals.

### 6. Overperformers and Underperformers
**Question:** Which countries achieved better or worse health outcomes than their income predicts?

A diverging lollipop chart displays differences between actual and model-predicted life expectancy.

**Key Insight:** Vietnam performed approximately 13.1 years above prediction, while Swaziland was approximately 25.9 years below prediction.

### 7. Fastest Improving Countries
**Question:** Which countries achieved the greatest improvements?

A dumbbell chart compares life expectancy in 1952 and 2007.

**Key Insight:** Oman recorded the largest increase, gaining approximately 38.1 years.

## 💡 Major Findings

- Global life expectancy increased by approximately 20 years.
- Asia achieved substantial improvements and narrowed its gap with Europe.
- Africa experienced slower progress and periods of stagnation.
- Income is strongly associated with life expectancy, but it does not fully explain health outcomes.
- Some countries experienced severe reversals despite global improvement.
- Economic growth alone cannot explain differences in public health outcomes.

## 📖 Data Storytelling Approach

The project follows a structured narrative:

1. Establish the global improvement.
2. Identify who benefited from progress.
3. Examine the relationship between wealth and health.
4. Investigate improvements beyond income.
5. Explore historical reversals.
6. Identify unusual country-level outcomes.
7. Highlight the countries with the greatest progress.

This approach ensures that every visualization contributes to a larger analytical story rather than functioning as an isolated chart.

## 📂 Project Structure

```text
health-and-wealth-of-nations/
│
├── data/
│   └── gapminder.csv
│
├── visualizations/
│   ├── figure_01_continental_trends.png
│   ├── figure_02_population_distribution.png
│   ├── figure_03_income_vs_life_expectancy.png
│   ├── figure_04_income_adjusted_progress.png
│   ├── figure_05_life_expectancy_reversals.png
│   ├── figure_06_country_residuals.png
│   └── figure_07_fastest_climbers.png
│
├── interactive/
│   └── interactive_health_wealth.html
│
├── scripts/
│   ├── make_figures.py
│   ├── interactive.py
│   └── build_report.py
│
├── report/
│   └── Data_Visualization_Narrative_Report.pdf
│
├── requirements.txt
├── README.md
└── LICENSE
```

## 🚀 How to Run the Project

### Step 1: Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/health-and-wealth-of-nations-data-visualization.git
```

### Step 2: Navigate to the project directory

```bash
cd health-and-wealth-of-nations-data-visualization
```

### Step 3: Install dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Run the visualization scripts

```bash
python scripts/make_figures.py
python scripts/interactive.py
python scripts/build_report.py
```

## 📌 Business & Social Relevance

This analysis demonstrates how data can support:

- Public health policy evaluation.
- Economic development research.
- International health comparisons.
- Identification of underserved populations.
- Evidence-based decision-making.
- Communication of complex socioeconomic trends.

## ⚠️ Limitations

- The dataset ends in 2007 and does not represent current conditions.
- Observations are recorded at five-year intervals.
- Country averages hide inequality within populations.
- GDP per capita does not represent individual income.
- Correlation does not establish causation.
- Historical event explanations are contextual interpretations, not direct dataset variables.

## 🏁 Conclusion

The period from 1952 to 2007 represents remarkable global improvement in life expectancy. However, progress was uneven, and economic prosperity alone cannot explain the full picture.

This project demonstrates the importance of combining statistical analysis, visualization techniques, and narrative storytelling to communicate data-driven insights effectively.

---

### 👨‍💻 Author

**Your Name**

Data Analytics | Python | Data Visualization | Data Storytelling

If you find this project useful, consider giving the repository a ⭐.

#DataAnalytics #Python #DataVisualization #Gapminder #DataStorytelling #Pandas #Matplotlib #Plotly

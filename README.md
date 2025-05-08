# 🐱 Cat Names vs Stock Market: A Quirky Correlation Project

## Overview

Can the names we give to cats reflect stock market trends? This fun yet insightful data project explores the potential correlation between finance-inspired cat names and the performance of the S\&P 500 index. It's part web scraping, part finance, and part humor—all wrapped into a Python-based data analysis pipeline.

## Project Features

- ✅ Web scraping (simulated cat name data)
- ✅ Stock price data retrieval via `yfinance`
- ✅ Data cleaning and trend analysis with `pandas`
- ✅ Visualization using `matplotlib`
- ✅ Correlation analysis with `scipy`
- ✅ Automated Excel and CSV report generation using `openpyxl`

## Technologies Used

- Python 3.11+
- pandas
- yfinance
- matplotlib
- scipy
- openpyxl
- BeautifulSoup (for real-world scraping, if needed)

## Setup Instructions

1. **Clone the repository**

   ```bash
   git clone https://github.com/your-username/cat-vs-stock-trend-analysis.git
   cd cat-vs-stock-trend-analysis
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

   _(If there's no **************\*\***************`requirements.txt`**************\*\***************, you can manually install:)_

   ```bash
   pip install pandas yfinance matplotlib scipy openpyxl beautifulsoup4
   ```

3. **Run the script**

   ```bash
   python cat_vs_stock.py
   ```

## Output

- Line/bar chart comparing S\&P 500 and finance-related cat name frequency
- Correlation coefficient and p-value
- Auto-generated Excel report with chart and summary
- CSV version of the merged data

## Sample Screenshot

## Sample Output Files

- `/Cat_vs_Stock_Report.xlsx`
- `/Cat_vs_Stock_Report.csv`

## Summary of Findings (Example)

> Pearson Correlation: 0.31 (p = 0.0412)
> Conclusion: A mild but statistically significant correlation. Are cats onto something?

## License

MIT License

## Contact

Created by Zahar — for portfolio and educational purposes. Feel free to reach out or fork!

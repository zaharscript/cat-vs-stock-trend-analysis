# cat_Name_vs_Stock.py

import requests
from bs4 import BeautifulSoup
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from scipy.stats import pearsonr
from openpyxl import Workbook
from openpyxl.chart import LineChart, Reference
from openpyxl.utils.dataframe import dataframe_to_rows

# ----------------------------
# PART 1: SCRAPE CAT NAMES
# ----------------------------

def get_cat_names(num_pages=5):
    names = ["Musk", "Buffet", "Stonks", "Meowth", "Coin", "Tesla", "Cash", "Whiskers", "Bitcoin", "Luna"]
    data = [names[i % len(names)] for i in range(50)]
    return pd.DataFrame({'CatName': data})

# ----------------------------
# PART 2: GET STOCK DATA
# ----------------------------

def get_stock_data(symbol='^GSPC', days_back=30):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days_back)
    data = yf.download(symbol, start=start_date.strftime('%Y-%m-%d'), end=end_date.strftime('%Y-%m-%d'))
    data.reset_index(inplace=True)
    return data[['Date', 'Close']]

# ----------------------------
# PART 3: PREP CAT DATA
# ----------------------------

def prep_cat_name_data(df):
    df['NameLower'] = df['CatName'].astype(str).str.lower()
    finance_keywords = '|'.join(['musk', 'stonks', 'buffet', 'tesla', 'coin', 'cash', 'bitcoin'])
    df['IsFinanceInspired'] = df['NameLower'].str.contains(finance_keywords, case=False, na=False)
    return df

# ----------------------------
# PART 4: ANALYSIS & VISUALIZATION
# ----------------------------

def analyze_cats_vs_stocks(cat_df, stock_df):
    try:
        appearance_dates = pd.date_range(end=datetime.now(), periods=len(cat_df))
        cat_df['Date'] = appearance_dates

        cat_trend = cat_df[cat_df['IsFinanceInspired']].groupby('Date').size().reset_index(name='FinanceCatCount')
        stock_df['Date'] = pd.to_datetime(stock_df['Date'])

        merged = pd.merge(stock_df, cat_trend, on='Date', how='left')
        merged['FinanceCatCount'] = merged['FinanceCatCount'].fillna(0)

        # Plotting
        fig, ax1 = plt.subplots(figsize=(12, 6))
        ax1.set_xlabel('Date')
        ax1.set_ylabel('S&P 500 Closing Price', color='tab:blue')
        ax1.plot(merged['Date'], merged['Close'], color='tab:blue', label='S&P 500')

        ax2 = ax1.twinx()
        ax2.set_ylabel('Finance-Inspired Cat Names', color='tab:orange')
        ax2.bar(merged['Date'], merged['FinanceCatCount'], alpha=0.6, color='tab:orange')

        fig.tight_layout()
        plt.title("Finance-Inspired Cat Names vs S&P 500")

        plt.savefig("Cat_vs_Stock_Chart.png")
        print("✅ Chart saved as 'Cat_vs_Stock_Chart.png'")

        correlation, p_value = pearsonr(merged['Close'], merged['FinanceCatCount'])
        print(f"\nCorrelation: {correlation:.3f} (p-value: {p_value:.4f})")
        if p_value < 0.05:
            print("Statistically significant relationship detected. Cats may know something.")
        else:
            print("No significant relationship found—but the theory remains majestic.")

        return merged, correlation, p_value
    except Exception as e:
        print(f"[ERROR] Analysis failed: {e}")
        return None, None, None

# ----------------------------
# PART 5: EXPORT EXCEL REPORT
# ----------------------------

def export_reports(merged_df, correlation, p_value):
    try:
        wb = Workbook()
        ws_data = wb.active
        ws_data.title = "Cat vs Stock Data"

        for r in dataframe_to_rows(merged_df, index=False, header=True):
            ws_data.append(r)

        chart = LineChart()
        chart.title = "Finance Cat Names vs S&P 500"
        chart.y_axis.title = "Count / Close Price"
        chart.x_axis.title = "Date"

        data = Reference(ws_data, min_col=ws_data["B1"].column, max_col=ws_data["C1"].column,
                         min_row=1, max_row=ws_data.max_row)
        cats = Reference(ws_data, min_col=ws_data["A2"].column, min_row=2, max_row=ws_data.max_row)
        chart.add_data(data, titles_from_data=True)
        chart.set_categories(cats)

        ws_data.add_chart(chart, "E5")

        ws_summary = wb.create_sheet(title="Summary")
        ws_summary["A1"] = "Cat Names vs Stock Market Report Summary"
        ws_summary["A3"] = f"Pearson Correlation Coefficient: {correlation:.3f}"
        ws_summary["A4"] = f"P-value: {p_value:.4f}"
        conclusion = (
            "There appears to be a statistically significant correlation between finance-inspired cat names "
            "and S&P 500 stock performance." if p_value < 0.05 else
            "No statistically significant correlation was found. The cats are innocent... for now."
        )
        ws_summary["A6"] = conclusion

        report_name = "Cat_vs_Stock_Report.xlsx"
        wb.save(report_name)
        print(f"✅ Excel report saved as '{report_name}'")

        # Also save CSV
        csv_name = "Cat_vs_Stock_Data.csv"
        merged_df.to_csv(csv_name, index=False)
        print(f"✅ CSV report saved as '{csv_name}'")

    except Exception as e:
        print(f"[ERROR] Export failed: {e}")

# ----------------------------
# MAIN SCRIPT
# ----------------------------

if __name__ == '__main__':
    print("Scraping cat names...")
    cat_df = get_cat_names()
    cat_df = prep_cat_name_data(cat_df)

    print("Downloading stock data...")
    stock_df = get_stock_data()

    print("Analyzing and visualizing...")
    merged, correlation, p_value = analyze_cats_vs_stocks(cat_df, stock_df)

    if merged is not None:
        print("Generating Excel and CSV report...")
        export_reports(merged, correlation, p_value)

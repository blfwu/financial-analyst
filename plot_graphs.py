import pandas as pd
import matplotlib.pyplot as plt


def plot_graphs(statement_df, start_date, end_date):
    dates = []
    transactions = []

    for index, row in statement_df.iterrows():
        dates.append(str(row["Transaction Date"].date()))
        transactions.append(row["CAD$"])

    plt.figure(figsize=(20,6))
    plt.plot(dates, transactions, marker="o")
    plt.title(f"Transactions from {start_date.date()} to {end_date.date()}")
    plt.xlabel("Date (YYYY-MM-DD)")
    plt.ylabel("Transactions ($)")
    plt.grid(True)
    plt.show()
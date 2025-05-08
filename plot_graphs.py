import pandas as pd
import matplotlib.pyplot as plt


def plot_graphs(statement_df, start_date, end_date, debit_transactions):
    dates = []
    debits = []

    dates = list(debit_transactions.keys())
    debits = list(debit_transactions.values())

    plt.figure(figsize=(20,6))
    plt.plot(dates, debits, marker="o")
    plt.title(f"Transactions from {start_date.date()} to {end_date.date()}")
    plt.xlabel("Date (YYYY-MM-DD)")
    plt.ylabel("Transactions ($)")
    plt.grid(True)
    plt.show()
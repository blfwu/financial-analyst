import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def plot_graphs(statement_df, start_date, end_date, debit_transactions, credit_transactions):
    debit_dates = []
    credit_dates = []
    debits = []
    credits = []

    debit_dates = pd.to_datetime(list(debit_transactions.keys()))
    credit_dates = pd.to_datetime(list(credit_transactions.keys()))
    all_dates = sorted(set(debit_dates) | set(credit_dates))
    debits = list(debit_transactions.values())
    credits = list(credit_transactions.values())

    plt.figure(figsize=(15,8))
    plt.plot(debit_dates, debits, marker='o', label="Debits", color='red')
    plt.plot(credit_dates, credits, marker='o', label="Credits", color='green')
    plt.title(f"Transactions from {start_date.date()} to {end_date.date()}")
    plt.xlabel("Date (YYYY-MM-DD)")
    plt.ylabel("Transactions ($)")
    plt.xticks(all_dates, rotation=90, ha='right')
    plt.grid(True)
    plt.legend()
    plt.show()
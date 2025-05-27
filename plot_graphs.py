import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def plot_graphs(statement_df, start_date, end_date, debit_transactions, credit_transactions):
    debit_dates = []
    credit_dates = []
    debits = []
    credits = []

    debit_dates = pd.to_datetime(list(debit_transactions.keys()))
    # debit_dates = np.array(pd.to_datetime(list(debit_transactions.keys())))
    credit_dates = pd.to_datetime(list(credit_transactions.keys()))
    all_dates = sorted(set(debit_dates) | set(credit_dates))
    # debits = list(debit_transactions.values())
    
    credits = list(credit_transactions.values())


    debits = np.array(list(debit_transactions.values()))
    over_50_mask = debits < -50
    over_50_dates = debit_dates[over_50_mask]
    over_50_debits = debits[over_50_mask]

    plt.figure(figsize=(15,8))
    plt.plot(debit_dates, debits, marker='o', label="Debits", color='red')
    plt.plot(credit_dates, credits, marker='o', label="Credits", color='green')
    plt.scatter(over_50_dates, over_50_debits, color='yellow', edgecolor='black', s=100, marker='*', label='Debits > $50', zorder=5)
    plt.title(f"Transactions from {start_date.date()} to {end_date.date()}")
    plt.xlabel("Date (YYYY-MM-DD)")
    plt.ylabel("Transactions ($)")
    plt.xticks(all_dates, rotation=90, ha='right')
    plt.grid(True)
    plt.legend()
    plt.show()
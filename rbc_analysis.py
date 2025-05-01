import pandas as pd


def analyze_transactions(statement_df, start_date, end_date):

    total_spent = 0
    total_credits = 0
    flagged_transactions = []

    for index, row in statement_df.iterrows(): # loops thru all transactions and sums all debits for total spending

        if row["CAD$"] < 0: # transactions with '-' are debits
            total_spent += row["CAD$"]

        if row["CAD$"] > 0: # transactions with '+' are credits
            total_credits += row["CAD$"]

        if row["CAD$"] < -50 or (row["CAD$"] > -1 and row["CAD$"] < 0): # SHOULD ADD AN OPTION TO CHANGE THE THRESHOLDS FOR FLAGGING!
            flagged_transactions.append(index) # the index is 2 behind the number on the csv



    total_spent = round(total_spent, 2)
    total_credits = round(total_credits, 2)

    # SUMMARY ----------------------------------------------------------------------
    print(f"Summary of transactions from {start_date.date()} to {end_date.date()}:")

    # Total spending in period
    print(f"Total debits: ${-total_spent}")

    # Total credits in period
    print(f"Total credits: ${total_credits}\n")

    # Flagged transactions
    print(f"The following transactions were flagged for being over $50:")

    for index in flagged_transactions:
        transaction = statement_df.iloc[index]
        print(f"Excel Index {index + 2} {transaction["Transaction Date"].date()}: {transaction["Description 1"]} from {transaction["Description 2"]} for ${-transaction["CAD$"]}")
import pandas as pd
import plot_graphs


def analyze_transactions(statement_df, start_date, end_date):

    total_spent = 0
    total_credits = 0
    flagged_transactions = []
    merchants = {}
    debits = {}

    for index, row in statement_df.iterrows(): # loops thru all transactions and sums all debits for total spending

        if row["CAD$"] < 0: # transactions with '-' are debits
            total_spent += row["CAD$"]

        if row["CAD$"] > 0: # transactions with '+' are credits
            total_credits += row["CAD$"]

        if row["CAD$"] < -50 or (row["CAD$"] > -1 and row["CAD$"] < 0): # SHOULD ADD AN OPTION TO CHANGE THE THRESHOLDS FOR FLAGGING!
            flagged_transactions.append(index) # the index is 2 behind the number on the csv


        # Store all dates and transactions into dictionary for each merchant
        if row["Description 2"] not in merchants.keys():
            merchants[row["Description 2"]] = {
                # "NAIC_code": 0,
                # "aliases": [],
                "transactions": {}
            }
        
        date_str = row["Transaction Date"].strftime("%Y-%m-%d") # converts date format to YYYY-MM-DD

        if date_str not in merchants[row["Description 2"]]["transactions"].keys(): # if the date is not found in the transactions dictionary for that merchant's dict
            merchants[row["Description 2"]]["transactions"][date_str] = []
        merchants[row["Description 2"]]["transactions"][date_str].append(row["CAD$"])

        # Store all transactions from each merchant by date into a dictionary

        if date_str not in debits.keys():
            debits[date_str] = []
        if row["CAD$"] < 0:
            debits[date_str].append(row["CAD$"])

    debits = {date: round(sum(amts),2) for (date, amts) in debits.items()}
    print(merchants.items())
    # print(debits.items())


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

    # Plot graphs
    plot_graphs.plot_graphs(statement_df, start_date, end_date, debits)
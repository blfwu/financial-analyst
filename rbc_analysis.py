import pandas as pd

def analyze_transactions(statement_file, **kw):

    statement_df = pd.read_csv(statement_file)

    if "start" and "end" in kw:
        start_date = pd.to_datetime(kw["start"])
        end_date = pd.to_datetime(kw["end"])
    else:
        start_date = statement_df.iloc[0]["Transaction Date"]
        start_date = pd.to_datetime(start_date)
        end_date = statement_df.iloc[-1]["Transaction Date"]
        end_date = pd.to_datetime(end_date)

    total_spent = 0
    total_credits = 0
    flagged_transactions = []

    statement_df["Transaction Date"] = pd.to_datetime(statement_df["Transaction Date"]) # convert 'Transaction Date' column in csv to datetime format
    statement_df = statement_df[(statement_df["Transaction Date"] >= start_date) & (statement_df["Transaction Date"] <= end_date)] # create new df with rows between start and end date

    # print(statement_df)

    for index, row in statement_df.iterrows(): # loops thru all transactions and sums all debits for total spending

        if row["CAD$"] < 0: # transactions with '-' are debits
            total_spent += row["CAD$"]

        if row["CAD$"] > 0: # transactions with '+' are credits
            total_credits += row["CAD$"]

        if row["CAD$"] < -50 or (row["CAD$"] > -1 and row["CAD$"] < 0): # SHOULD ADD AN OPTION TO CHANGE THE THRESHOLDS FOR FLAGGING!
            # print(f"{index} was flagged, as the transaction on {row["Transaction Date"]} was ${row["CAD$"]}.")
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
        print(f"{transaction["Transaction Date"].date()}: {transaction["Description 1"]} from {transaction["Description 2"]} for ${-transaction["CAD$"]}")

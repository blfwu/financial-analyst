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

    statement_df["Transaction Date"] = pd.to_datetime(statement_df["Transaction Date"]) # convert 'Transaction Date' column in csv to datetime format
    statement_df = statement_df[(statement_df["Transaction Date"] >= start_date) & (statement_df["Transaction Date"] <= end_date)] # create new df with rows between start and end date

    print(statement_df)

    for index, row in statement_df.iterrows(): # loops thru all transactions and sums all debits for total spending

        if row["CAD$"] < 0: # transactions with '-' are debits
            total_spent += row["CAD$"]


    # Total spending in period
    print(f"You spent ${-total_spent} from {start_date.date()} to {end_date.date()}!")

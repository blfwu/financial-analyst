import pandas as pd
import plot_graphs
import json


def analyze_transactions(statement_df, start_date, end_date):

    total_spent = 0
    total_credits = 0
    flagged_transactions = []
    merchants = {}
    debits = {}
    credits = {}

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

        # Store all debits and credits from each merchant by date into a dictionary
        if row["CAD$"] < 0: # debits
            if date_str not in debits:
                debits[date_str] = []
            debits[date_str].append(row["CAD$"])
        elif row["CAD$"] > 0: # credits
            if date_str not in credits:
                credits[date_str] = []
            credits[date_str].append(row["CAD$"])
        

    debit_total = {date: round(sum(amts),2) for (date, amts) in debits.items()} # sum all debits for each date in dict
    credit_total = {date: round(sum(amts),2) for (date, amts) in credits.items()} # sum all credits for each date in dict


    total_spent = round(total_spent, 2)
    total_credits = round(total_credits, 2)

    # SUMMARY ----------------------------------------------------------------------
    print(f"Summary of transactions from {start_date.date()} to {end_date.date()}:")
    print(f"Total debits: ${-total_spent}") # Total spending in period
    print(f"Total credits: ${total_credits}\n") # Total credits in period
    print(f"The following transactions were flagged for being over $50:") # Flagged transactions

    for index in flagged_transactions:
        transaction = statement_df.loc[index]
        print(f"CSV Index {index + 2} {transaction["Transaction Date"].date()}: {transaction["Description 1"]} from {transaction["Description 2"]} for ${-transaction["CAD$"]}")
        # the dataframe index is 2 behind the number on the CSV, so we add 2 to it to get the correct index in the CSV statement

    # PLOT GRAPHS ------------------------------------------------------------------
    plot_graphs.plot_graphs(statement_df, start_date, end_date, debit_total, credit_total)


    # FILTER TRANSACTIONS ----------------------------------------------------------
    filter_start_date = input("Enter a start date to filter transactions (YYYY-MM-DD) or press 'Enter' to skip: ")

    save_merchant_data(merchants)
    filter_transactions(start_date = filter_start_date)



# SAVING MERCHANT DATA TO "merchants.json" FILE ----------------------------------------------------

def save_merchant_data(merchant_data):
    with open("merchants.json", "w") as file:
        merchants = json.dump(merchant_data, file, indent=4)



# FILTERING TRANSACTIONS, MERCHANTS, DATE RANGES, ETC. ---------------------------------------------

def filter_transactions(**kw):

    with open("merchants.json", "r") as file:
        merchants = json.load(file)
        
        if "start_date" in kw:
            for merchant, merchant_data in merchants.items():
                for date, amount in merchant_data["transactions"].items():
                    if kw["start_date"] == date:
                        print(f"{merchant} on {date} for ${sum(amount)}") # prints the merchant name, date, and total amount for the date inputted
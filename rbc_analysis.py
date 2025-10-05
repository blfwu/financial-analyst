import pandas as pd
import plot_graphs
import json
from datetime import datetime


# SAVING MERCHANT DATA TO "merchants.json" FILE ----------------------------------------------------
def save_merchant_data(merchant_data):
    with open("merchants.json", "w") as file:
        merchants = json.dump(merchant_data, file, indent=4)


def analyze_transactions(statement_df, start_date, end_date):

    total_debits = 0 # per date range/statement period
    total_credits = 0 # ^
    flagged_transactions = []
    merchants = {}
    debits = {} # date: [trans1, trans2...]
    credits = {} # ^

    for index, row in statement_df.iterrows(): # loops thru all transactions and sums all debits for total spending

        if row["CAD$"] < 0: # transactions with '-' are debits
            total_debits += row["CAD$"]
        total_debits = round(total_debits, 2)

        if row["CAD$"] > 0: # transactions with '+' are credits
            total_credits += row["CAD$"]
        total_credits = round(total_credits, 2)

        if row["CAD$"] < -50 or (row["CAD$"] > -1 and row["CAD$"] < 0): # SHOULD ADD AN OPTION TO CHANGE THE THRESHOLDS FOR FLAGGING!
            flagged_transactions.append(index) # the index is 2 behind the number on the csv

    
        # Store all dates and transactions into dictionary for each merchant
        if row["Description 2"] not in merchants.keys(): # if the merchant name does not exist in the merchant dictionary
            merchants[row["Description 2"]] = { # create a key in the dict for the merchant
                # "NAIC_code": 0,
                # "aliases": [],
                "transactions": {}
            }
        
        date_str = row["Transaction Date"].strftime("%Y-%m-%d") # converts date format to YYYY-MM-DD

        if date_str not in merchants[row["Description 2"]]["transactions"].keys(): # if the date is not found in the transactions dictionary for that merchant's dict
            merchants[row["Description 2"]]["transactions"][date_str] = [] # if a transaction's date for current merchant not found, add it
        merchants[row["Description 2"]]["transactions"][date_str].append(row["CAD$"]) # add the transaction amount to the list (value for transaction date dict)

        # DEBITS AND CREDITS DICTIONARY FOR SUMMING TOTALS ------------------------------------------------------------------------------------
        # Store all debits and credits from each merchant by date into a dictionary
        if row["CAD$"] < 0: # debits
            if date_str not in debits:
                debits[date_str] = []
            debits[date_str].append(row["CAD$"])
        elif row["CAD$"] > 0: # credits
            if date_str not in credits:
                credits[date_str] = []
            credits[date_str].append(row["CAD$"])
        
    # debits_by_date and credits_by_date are dicts with dates (keys) where there was a transaction(s), then adds the TOTAL debits/credits (value) for that day
    debits_by_date = {date: round(sum(amts),2) for (date, amts) in debits.items()} # sum all debits for each date in dict
    credits_by_date = {date: round(sum(amts),2) for (date, amts) in credits.items()} # sum all credits for each date in dict

    # SUMMARY ----------------------------------------------------------------------
    print(f"Summary of transactions from {start_date.date()} to {end_date.date()}:")
    print(f"Total debits: ${-total_debits}") # Total spending in period
    print(f"Total credits: ${total_credits}\n") # Total credits in period
    print(f"The following transactions were flagged for being over $50:") # Flagged transactions

    for index in flagged_transactions:
        transaction = statement_df.loc[index]
        print(f"CSV Index {index + 2} {transaction['Transaction Date'].date()}: {transaction['Description 1']} from {transaction['Description 2']} for ${-transaction['CAD$']}")
        # the dataframe index is 2 behind the number on the CSV, so we add 2 to it to get the correct index in the CSV statement


    # PLOT GRAPHS ------------------------------------------------------------------
    plot_graphs.plot_graphs(statement_df, start_date, end_date, debits_by_date, credits_by_date)

    save_merchant_data(merchants)



def create_transaction_data():
    # FILTERING TRANSACTIONS, MERCHANTS, DATE RANGES, ETC. ---------------------------------------------
    all_transactions = []

    with open("merchants.json", "r") as file:
        merchants = json.load(file)

        for merchant, merchant_data in merchants.items():
            for date, amt in merchant_data["transactions"].items():
                for ea_amt in amt:
                    all_transactions.append((merchant, ea_amt, date)) # add all transactions as tuples in all_transactions list
    
    return all_transactions



def filter_transactions(all_transactions, merchant, min_amt, max_amt, min_date, max_date):
    filtered_list = all_transactions
    # MERCHANT FILTER ---------------------------------------------------
    if merchant:
        filtered_list = [trans for trans in filtered_list if merchant.lower() in trans[0].lower()]

    # TRANSACTION AMT FILTER --------------------------------------------
    if min_amt:
        filtered_list = [trans for trans in filtered_list if abs(trans[1]) >= float(min_amt)]
    if max_amt:
        filtered_list = [trans for trans in filtered_list if abs(trans[1]) <= float(max_amt)]
    
    # DATE FILTER -------------------------------------------------------
    if min_date:
        filtered_list = [trans for trans in filtered_list if datetime.strptime(trans[2], "%Y-%m-%d") >= min_date]
    if max_date:
        filtered_list = [trans for trans in filtered_list if datetime.strptime(trans[2], "%Y-%m-%d") <= max_date]

    print(f"The filtered list is: {filtered_list}\n")
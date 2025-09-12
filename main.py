import pandas as pd
import rbc_analysis
from datetime import datetime


statement_file = input("Enter the name of the statement: ")

statement_df = pd.read_csv(statement_file)

mode = input("Type 'C' for custom date range or press 'Enter' to analyze the entire statement: ")

if mode == "C":
    start_date = input("Start date: ")
    end_date = input("End date: ")
else:
    start_date = statement_df.iloc[0]["Transaction Date"]
    end_date = statement_df.iloc[-1]["Transaction Date"]

start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)


statement_df["Transaction Date"] = pd.to_datetime(statement_df["Transaction Date"]) # convert 'Transaction Date' column in csv to datetime format
statement_df = statement_df[(statement_df["Transaction Date"] >= start_date) & (statement_df["Transaction Date"] <= end_date)] # create new df with rows between start and end date


def select_bank():
    if "RBC" in statement_file:
        rbc_analysis.analyze_transactions(statement_df, start_date, end_date)

        # Save transactions (merchant, amt, date) to all_transactions list
        all_transactions = rbc_analysis.create_transaction_data()

        # Ask user if want to filter
        while True:
            use_filter = input("Would you like to filter transactions? (Y/N) ")
            if use_filter == "Y":
                print("Answer the following prompts to filter transactions. Press 'Enter' to skip a filter.\n")
                filter_merchant = input("Filter by merchant: ")
                filter_min_amt = input("Filter by minimum amount: $")
                filter_max_amt = input("Filter by maximum amount: $")
                filter_min_date = input("Filter by earliest date (YYYY-MM-DD): ")
                filter_max_date = input("Filter by latest date (YYYY-MM-DD): ")
                
                # Convert user string date input to datetime format
                if filter_min_date: 
                    filter_min_date = datetime.strptime(filter_min_date, "%Y-%m-%d")
                else:
                    filter_min_date = None

                if filter_max_date:
                    filter_max_date = datetime.strptime(filter_max_date, "%Y-%m-%d")
                else:
                    filter_max_date = None
                
                rbc_analysis.filter_transactions(all_transactions, filter_merchant, filter_min_amt, filter_max_amt, filter_min_date, filter_max_date)

            else:
                break

select_bank()
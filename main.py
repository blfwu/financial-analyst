import pandas as pd
import rbc_analysis
from datetime import datetime


statement_file = input("Enter the name of the statement: ")

statement_df = pd.read_csv(statement_file)

print("Enter a custom statement range or press 'Enter' to use the end ranges.")

try: # Validate start date input
    start_date = input("Start date (YYYY-MM-DD): ")
    datetime.strptime(start_date, '%Y-%m-%d')
    print(f"Start date {start_date} is valid.")
except: # Default to earliest day in statement if invalid entry
    earliest_date = statement_df.iloc[0]["Transaction Date"]
    print(f"Invalid end date {start_date} detected; using earliest date {earliest_date} from statement.")
    start_date = earliest_date

try: # Validate end date input
    end_date = input("End date (YYYY-MM-DD): ")
    datetime.strptime(end_date, '%Y-%m-%d')
    print(f"End date {end_date} is valid.")
except: # Default to last day in statement if invalid entry
    last_date = statement_df.iloc[-1]["Transaction Date"]
    print(f"Invalid end date {end_date} detected; using last date {last_date} on statement.")
    end_date = last_date


start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)

statement_df["Transaction Date"] = pd.to_datetime(statement_df["Transaction Date"]) # convert 'Transaction Date' column in csv to datetime format
statement_df = statement_df[(statement_df["Transaction Date"] >= start_date) & (statement_df["Transaction Date"] <= end_date)] # create new df with rows between start and end date
statement_df[["Description 1", "Description 2"]] = statement_df["Description 1"].str.split(" - ", expand=True, n=1) # split "Description 1" column at the " - ": 1st half remains in "Description 1", 2nd half goes in "Description 2"
statement_df["Description 2"] = statement_df["Description 2"].str[5:]
# print(f"Description 1: {statement_df['Description 1']} and Description 2: {statement_df['Description 2']}")

def select_bank():
    if "RBC" in statement_file:
        rbc_analysis.analyze_transactions(statement_df, start_date, end_date)
        rbc_analysis.transactions_to_json(statement_df)

        # Save transactions (merchant, amt, date) to all_transactions list
        all_transactions = rbc_analysis.create_filtered_tuples()

        # Ask user if want to filter
        while True:
            use_filter = input("\nWould you like to filter transactions? (Y/N) ")
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
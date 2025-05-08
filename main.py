import pandas as pd
import rbc_analysis


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

select_bank()
import pandas as pd
import rbc_analysis

statement_file = input("Enter the name of the statement: ")

statement = pd.read_csv(statement_file)

mode = input("Type 'C' for custom date range or press 'Enter' to analyze the entire statement: ")

if mode == "C":
    start_date = input("Start date: ")
    end_date = input("End date: ")

def select_bank():
    if "RBC" in statement_file:
        if mode == "C":
            rbc_analysis.analyze_transactions(statement_file, start=start_date, end=end_date)
        else:
            rbc_analysis.analyze_transactions(statement_file)

select_bank()


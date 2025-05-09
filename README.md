# Financial Analyst

This financial analyst program helps you track monthly transactions by highlighting spending patterns, filtering merchants/purchases, flagging suspicious activities, setting budgeting goals, and more!

# How do I use it? (Based on Windows OS)
1) Fork this repository into your desired directory
2) CD into said directory and create the virtual environment. Then run `pip install -r requirements.txt` to download all dependencies
4) Go to _rbcroyalbank.com_ on the browser and click "Sign In" to access online banking with your RBC account details
5) Navigate to the "My Accounts" tab
6) Click "Download"
7) Select "Comma Delimited (.csv for Excel...) in the "Spreadsheet Software" section
8) Select the account you would like to analyze in the first dropdown, followed by "All Transactions on File" in the second dropdown
9) Rename the statement CSV file so it includes "RBC" in the name (ex. "RBC-statement.csv")
10) Move the CSV file into the working directory and execute the program by running `python main.py`

NOTE: the custom dates feature is based on the _YYYY-MM-DD_ format (ex. 2024-12-13)

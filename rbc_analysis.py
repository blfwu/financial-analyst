import pandas as pd
import plot_graphs
import json
import sqlite3
import re
from datetime import datetime


def categorize_merchants(merchant_name, provinces, cities):
    """
    This function is passed a merchant name from transactions_to_json and classifies the merchant's category based off the name and user-passed province(s)/city(s) of purchase.
    It queries CA_MERCHANTS.db for direct or similar matches to existing merchants in the ODBus database to find its NAIC code, then converts it to the corresponding category and returns it as a string.
    """

    conn = sqlite3.connect('CA_MERCHANTS.db')
    cursor = conn.cursor()

    # Convert provinces and cities into list for SQL IN (...)
    provinces_list = [province.strip() for province in provinces.split(', ') if province.strip()] if provinces else []
    city_list = [city.strip() for city in cities.split(', ') if city.strip()] if cities else []

    filler_words = ["THE", "OF", "LTD", "STORE"]


    # if merchant is not a string, skip to next merchant
    if not isinstance(merchant_name, str):
        # return N/A for NAIC category
        return "N/A"

    # turn merchant all uppercase, replace non-letters with space, get rid of whitespace
    clean_name = re.sub(r"[^A-Z\s'-]", ' ', merchant_name.upper()).strip()

    # insert each word in clean_name as an element of split_name list; do not add word if only 1 character (ex. '-')
    split_name = [word for word in clean_name.split() if word and word not in filler_words and len(word) > 1]

    # if split_name is empty, skip to next merchant
    if not split_name:
        print(f"No words found for {merchant_name}")
        
        return "N/A"

    print(f"Original name: {merchant_name} vs. cleaned name: {', '.join(split_name)}\n")


    # build parameterized SQL per-merchant; try stricter AND-match first, then OR-match. =========================================

    # base WHERE clauses (province + city IN ...)
    where_clause = []
    params = []
    if provinces_list:
        prov_placeholders = ", ".join(["?"] * len(provinces_list)) # create a string of '?, ?...' based on # of provinces (3 provinces -> "?, ?, ?")
        where_clause.append(f"prov_terr IN ({prov_placeholders})")
        params.extend(provinces_list)
    if city_list:
        cities_placeholders = ", ".join(["?"] * len(city_list)) 
        where_clause.append(f"city IN ({cities_placeholders})")
        params.extend(city_list)

    # word match clause template (checks business_name OR alt_business_name)
    pair_clause = "(UPPER(business_name) LIKE ? OR UPPER(alt_business_name) LIKE ?)"

    # Direct match =========================================
    all_clause = " AND ".join([pair_clause for _ in split_name])
    all_query = f"""
        SELECT
            CASE
                WHEN derived_NAICS = '11' THEN 'Agriculture, forestry, fishing and hunting'
                WHEN derived_NAICS = '21' THEN 'Mining, quarrying, and oil and gas extraction'
                WHEN derived_NAICS = '22' THEN 'Utilities'
                WHEN derived_NAICS = '23' THEN 'Construction'

                WHEN derived_NAICS BETWEEN '31' AND '33' THEN 'Manufacturing'
                WHEN derived_NAICS = '41' THEN 'Wholesale trade'
                WHEN derived_NAICS BETWEEN '44' AND '45' THEN 'Retail trade'
                WHEN derived_NAICS BETWEEN '48' AND '49' THEN 'Transportation and warehousing'

                WHEN derived_NAICS = '51' THEN 'Information and cultural industries'
                WHEN derived_NAICS = '52' THEN 'Finance and insurance'
                WHEN derived_NAICS = '53' THEN 'Real estate and rental and leasing'
                WHEN derived_NAICS = '54' THEN 'Professional, scientific and technical services'
                WHEN derived_NAICS = '55' THEN 'Management of companies and enterprises'
                WHEN derived_NAICS = '56' THEN 'Administrative and support, waste management and remediation services'

                WHEN derived_NAICS = '61' THEN 'Educational services'
                WHEN derived_NAICS = '62' THEN 'Health care and social assistance'
                WHEN derived_NAICS = '71' THEN 'Arts, entertainment and recreation'
                WHEN derived_NAICS = '72' THEN 'Accommodation and food services'
                WHEN derived_NAICS = '81' THEN 'Other services (except public administration)'
                WHEN derived_NAICS = '91' THEN 'Public administration'

                ELSE 'N/A'
            END AS merchant_category
        FROM (
            SELECT 
                derived_NAICS,
                COUNT(*) AS NAIC_count
            FROM (
                SELECT 
                    UPPER(business_name), 
                    UPPER(alt_business_name), 
                    derived_NAICS, 
                    city, 
                    prov_terr
                FROM 
                    MERCHANT_INFO
                WHERE 
                    {(' AND '.join(where_clause) + ' AND ') if where_clause else ''}({all_clause})
                LIMIT 20
            ) sub
            GROUP BY
                derived_NAICS
            ORDER BY
                NAIC_count DESC
            LIMIT 1
        ) sub2
    """

    # Any word match =========================================
    any_clause = " OR ".join([pair_clause for _ in split_name])
    any_query = f"""
        SELECT
            CASE
                WHEN derived_NAICS = '11' THEN 'Agriculture, forestry, fishing and hunting'
                WHEN derived_NAICS = '21' THEN 'Mining, quarrying, and oil and gas extraction'
                WHEN derived_NAICS = '22' THEN 'Utilities'
                WHEN derived_NAICS = '23' THEN 'Construction'

                WHEN derived_NAICS BETWEEN '31' AND '33' THEN 'Manufacturing'
                WHEN derived_NAICS = '41' THEN 'Wholesale trade'
                WHEN derived_NAICS BETWEEN '44' AND '45' THEN 'Retail trade'
                WHEN derived_NAICS BETWEEN '48' AND '49' THEN 'Transportation and warehousing'

                WHEN derived_NAICS = '51' THEN 'Information and cultural industries'
                WHEN derived_NAICS = '52' THEN 'Finance and insurance'
                WHEN derived_NAICS = '53' THEN 'Real estate and rental and leasing'
                WHEN derived_NAICS = '54' THEN 'Professional, scientific and technical services'
                WHEN derived_NAICS = '55' THEN 'Management of companies and enterprises'
                WHEN derived_NAICS = '56' THEN 'Administrative and support, waste management and remediation services'

                WHEN derived_NAICS = '61' THEN 'Educational services'
                WHEN derived_NAICS = '62' THEN 'Health care and social assistance'
                WHEN derived_NAICS = '71' THEN 'Arts, entertainment and recreation'
                WHEN derived_NAICS = '72' THEN 'Accommodation and food services'
                WHEN derived_NAICS = '81' THEN 'Other services (except public administration)'
                WHEN derived_NAICS = '91' THEN 'Public administration'

                ELSE 'N/A'
            END AS merchant_category
        FROM (
            SELECT 
                derived_NAICS,
                COUNT(*) AS NAIC_count
            FROM (
                SELECT 
                    UPPER(business_name), 
                    UPPER(alt_business_name), 
                    derived_NAICS, 
                    city, 
                    prov_terr
                FROM 
                    MERCHANT_INFO
                WHERE 
                    {(' AND '.join(where_clause) + ' AND ') if where_clause else ''}({any_clause})
                LIMIT 20
            ) sub
            GROUP BY
                derived_NAICS
            ORDER BY
                NAIC_count DESC
            LIMIT 1
        ) sub2
    """

    # add # wildcard to front and back of each word in split_word twice (b/c business_name and alt_business_name are back to back in the WHERE)
    full_params = list(params) + [f"%{word}%" for word in split_name for __ in (0, 1)]

    # Attempt A: all words present (AND between pair_clauses)
    cursor.execute(all_query, full_params)
    row = cursor.fetchone()

    if row is not None:
        # return the NAIC category
        return row[0] 
    else:
        # Attempt B: any word present (OR between pair_clauses) if no rows found
        print("No direct match found. Trying any word...")
        cursor.execute(any_query, full_params)
        row = cursor.fetchone()
        if row is not None:
            # return the NAIC category
            return row[0]
    
    conn.close()

    # if no NAIC category found, return N/A
    return "N/A"



def transactions_to_json(statement_df):
    """
    Iterates each transaction item from statement_df and creates a new merchant key if it does not already exist in the merchants dictionary.
    After merchant key creation, the value is another dictionary containing "category" and "transactions":
    - "category" is retrieved by running categorize_merchants() and passing the merchant name, province, and city of transaction
    - "transactions" has a dictionary value which contains each transaction date and all transactions from that date as a list
    Afterwards, it writes all merchant data to merchants.json.
    """
    
    merchants = {}

    # Location of purchases
    provinces = input("\nProvince (separate with ', ' if multiple): ").strip()
    cities = input("City (separate with ', ' if multiple): ").strip()

    for index, row in statement_df.iterrows(): # loops thru all transactions and sums all debits for total spending

        # Store all dates and transactions into dictionary for each merchant. Create merchant if DNE.
        if row["Description 2"] not in merchants.keys(): # if the merchant name does not exist in the merchant dictionary
            merchants[row["Description 2"]] = { # create a key in the dict for the merchant
                "category": '',
                "transactions": {}
            }

        merchant_name = row["Description 2"]

        # converts date format to YYYY-MM-DD
        date_str = row["Transaction Date"].strftime("%Y-%m-%d") 

        if date_str not in merchants[row["Description 2"]]["transactions"].keys(): # if the date is not found in the transactions dictionary for that merchant's dict
            merchants[row["Description 2"]]["transactions"][date_str] = [] # if a transaction's date for current merchant not found, add it
        merchants[row["Description 2"]]["transactions"][date_str].append(row["CAD$"]) # add the transaction amount to the list (value for transaction date dict)

        # Retrieve the merchant's naic category
        naic_category = categorize_merchants(merchant_name, provinces, cities)
        merchants[merchant_name]["category"] = naic_category
    
    
        # print(f"The merchant is {merchant_name} and the category is {merchant_name['category']}")
        category = merchants.get(merchant_name, {}).get("category", "N/A")
        print(f"The merchant is {merchant_name} and the category is {category}\n\n")


    # SAVE MERCHANT DATA TO JSON
    with open("merchants.json", "w") as file:
        json.dump(merchants, file)



def analyze_transactions(statement_df, start_date, end_date):
    """
    Iterate each transaction in statement_df and sum and print all debits, credits, and create list of all transactions $50 or above.
    Plot transactions graph with stars on flagged purchases >= $50 using plot_graphs() from plot_graphs module.
    """
    total_debits = 0 # per date range/statement period
    total_credits = 0 # ^
    flagged_transactions = []
    
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

        # converts date format to YYYY-MM-DD
        date_str = row["Transaction Date"].strftime("%Y-%m-%d") 

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



def create_filtered_tuples():
    """
    Creates tuples containing (merchant name, transaction amount, date) for filtering in filter_transactions().
    """

    all_transactions = []

    with open("merchants.json", "r") as file:
        merchants = json.load(file)

        for merchant, merchant_data in merchants.items():
            for date, amt in merchant_data["transactions"].items():
                for ea_amt in amt:
                    all_transactions.append((merchant, ea_amt, date)) # add all transactions as tuples in all_transactions list
    
    return all_transactions



def filter_transactions(all_transactions, merchant, min_amt, max_amt, min_date, max_date):
    """
    all_transactions containing (merchant, amt, date) tuples are passed along with user-inputted merchant name, min and max amount, earliest and latest date.
    Each filter will reduce the # of tuples in filtered_list if the filter condition is not satisfied for that tuple, removing it.
    The resulting filtered_list is printed.
    """

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
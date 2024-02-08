""" BudgetTracker
author: Sebastian Christian Will
date: 13.05.2022

Created for: MMT APPLICATION FOR WINTER SEMESTER 2022/23
"""

import csv #import csv to use the writer() method to write new transactions to csv file
import os #import os for using the getcwd() method, to return the current working directory and to use listdir() to find existing files in the working directory

import pandas as pd #import pandas module to perform data analysis
import easygui #import easygui for selecting old transaction file through pop up window
from copyfile import copyFile #import copyFile to have the functionality to copy a file from one directory to the other 

def record_transaction(transactions): #defining the method to record transactions
    """Adds transaction to given file

    Args:
        transactions str: filename #expected parameter is a string stored in the variable transactions, containing a filename
    """
    while True: #while loop to execute code until it is not true, or exited
        new_transaction = [] #to create a new transaction a list is needed, which can later be added to the transactions file; the list starts of with being empty

        description = input("\nEnter description: ") #the user is asked to input a description for the transaction
        new_transaction.append(description) #the description is then added to the list

        date = input("\nEnter date using the YYYY-MM-DD format: ") #the user is asked to input a date for the transaction
        new_transaction.append(date) #the date is then added to the list

        amount = input("\nEnter amount, use '-' for negative values: ") #the user is asked to input an amount for the transaction
        new_transaction.append(amount) #the amount is then added to the list

        with open(transactions, 'a', newline='', encoding="utf-8") as transactions_writer: #to add the new transactions to the old transactions, the transaction file needs to be opened, writen and closed; the most comfortable way to do it is using the with option; 
            #the 'a' is used, so new content will be appended to the the file and does not overwrite the old transactions; also a new empty line is created as a placeholder for the new content; encoding ensures, that utf-8 is used 
            writer = csv.writer(transactions_writer) #a writer object is returned, so the new data can be writen to the file with the next line of code
            writer.writerow(new_transaction) #the new transaction, which is stored in the list new_transactions is now added to the new row

        print("New transaction saved") #the user is informed, that the new transaction has been saved
        all_transactions = pd.read_csv(transactions) #to be able to show the current budget after saving the new transaction, pandas will be used to calculate it; to use pandas, the file needs to be opened with the read_csv() method;
        total = all_transactions['amount'].sum() #by using the sum() function and telling pandas with 'amount' which line should be summed up, the budget is being calculated and stored in the total variable
        print(f"\nYour current budget is: {total:.2f}€\n") #the user is informed, what the current budget is; by adding :.2f after total, the amount is formated to contain two decimals as a float data type

        while (choose := input("\nDo you want to record another transaction?\n1) Yes\n2) No\n")) not in ["1", "2"]: #the user can choose if he wants to record another transaction; if he doesn't choose 1 or 2, the next line of code is executed
            print("Please enter a valid option") #informs the user to input a valid option, when not inputting 1 or 2

        if choose == "2": #if the user chose 2, the next line of code is executed
            break #if the user chose 2, the while loop is exited

def calculate_budget(transactions): #defining the method to calculate the budget
    """Calculates current budget and displays last and selected transactions

    Args:
        transactions str: filename #expected parameter is a string stored in the variable transactions, containing a filename
    """
    all_transactions = pd.read_csv(transactions, parse_dates=['date']) #to be able to show the current budget, pandas will be used to calculate it; to use pandas, the file needs to be opened with the read_csv() method;
        #parse_dates makes sure, that the 'date' column is a datetime data type, to be able to select a specific data range later on
    total = all_transactions['amount'].sum() #by using the sum() method and telling pandas with 'amount' which line should be summed up, the budget is being calculated and stored in the total variable
    print(f"\nYour current budget is: {total:.2f}€\n") #the user is informed, what the current budget is; by adding :.2f after total, the amount is formated to contain two decimals as a float data type
    number_of_transactions = input("\nHow many of your last transactions do you want to show?\n") #the user is asked to insert how many last transactions should be shown

    print(f"\nYour last {number_of_transactions} transactions:\n") #the user is informed, that the number of last transactions selected will be shown
    all_transactions.sort_values(by='date', inplace=True) #sorts the transactions by date; inplace=True makes sure, that the last transactions are the last ones sorted by date and not the last ones added to the csv file
    print(all_transactions.tail(int(number_of_transactions))) #by using the tail() method the last transactions are shown; the number_of_transactions is used as an integer datatype to clarify how many transactions should be shown
    all_transactions = all_transactions.set_index('date') #to select a certain range of transactions, which will be performed in the next line of code, the date column needs to be set as index
    date_range = input("\nSelect a date range for specific transactions to be returned.\n" + #the user is asked to select a specific date range to output specific transactions 
        "E.g. all transactions in February 2022: '2022-02'\n") #the date range has to be entered in the given format 
    print(f"\nYour selected transactions from {date_range}:\n") #the user is informed, that the transactions from the selected date range will be shown
    print(all_transactions.loc[date_range]) #outputs the transactions from the selected date range; loc enables to select the specific rows which are in the date range

def main(): #defining the main method to run the program
    """Executes BudgetTracker. Able to record transactions & calculate the budget.
    """
    print("Please select a .csv file with previous transactions, containing the columns 'description', 'date' and 'amount'.") #prompts the user to select a file with previous transactions
    existing_file_location = easygui.fileopenbox() #opens a window via the fileopenbox() method, so the user can select a file with last transactions
    current_directory = os.getcwd() #stores the current directory path in the current_directory variable with the getcwd() method
    find_csv_file = [file for file in os.listdir(current_directory) if file.endswith('.csv')] #using the listdir() method, the current directory is searched for files that end with .csv; the ending can be determinded with the endswith() method;
        #if there are filenames in the directory, they will be stored in a list format

    if find_csv_file: #if the list is not empty, the next line of code is executed
        transactions = find_csv_file[0] #assumption: if there is a filename in the list, it is the only exisiting .csv file in the directory; by choosing the first element in the list the filename will be stored in the variable transactions
    else: #if the list is empty, it means that the file has been selected from another directory, which is not the same, as the directory of this python file; to make sure the file is inserted in the same directory, it needs to be copied using the next line of code
        copyFile(existing_file_location, current_directory) #using the copyFile method, the file is copied from the directory, which has been set by the user with the fileopenbox() method and pasted in the directory, which is stored in the current_directory variable
        find_csv_file = [file for file in os.listdir(current_directory) if file.endswith('.csv')] #now that the current directory contains a .csv file, the filename is stored as an element in the list find_csv_file 
        transactions = find_csv_file[0] #the filename is taken from the first position in the list and is stored in the variable transactions

    while True: #while loop to execute code until it is not true, or exited
        choose = input("\nWhat do you want to do?\n" + #the user can input, which action he wants to perform
            "1) Record a transaction\n" + #seperated for better readability
            "2) Calculate the current budget\n" + #seperated for better readability
            "3) Exit the program\n") #seperated for better readability

        if choose == "1": #if the user chose 1, the next line of code will be executed
            record_transaction(transactions) #if the user chose 1, the method record_transactions() will be executed, passing along the variable transactions, containing the filename as a string
        elif choose == "2": #if the user chose 2, the next line of code will be executed
            calculate_budget(transactions) #if the user chose 2, the method calculate_budget() will be executed, passing along the variable transactions, containing the filename as a string
        elif choose == "3": #if the user chose 3, the next line of code will be executed
            break #if the user chose 3, the while loop will be exited, ending the program
        else: #if the user chose something else than 1, 2 or 3, the next line of code will be executed
            print("Choose a valid option") #the user is informed to choose a valid option, when not inputting  1, 2 or 3

if __name__ == "__main__": #this line of code checks, if this python file is the main file
    main() #this line of code executes the main() method, after checking, that this python file is indeed the main file

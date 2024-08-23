from prettytable import PrettyTable
import matplotlib.pyplot as plt
from datetime import date
import tabulate
import pandas
import sys
import os


new_row = ""


def main():
    instructions = command_list()
    while True:
        clear_terminal()
        print(instructions)
        command = input("Enter your command: ")
        if command.strip(" ") == "new":
            new('Enter new transaction amount (Type "back" to exit): ')
        elif command.strip(" ") == "exit":
            exit()
        elif command.strip(" ") == "display":
            display("finance_data.csv")
            input('Press "Enter" to continue...')
        elif command.strip(" ") == "export":
            excel_export("finance_data.csv")
        elif command.strip(" ") == "erase":
            inpt = "Do you want to delete all data (all) or a specifid transaction (one)? \nall/one: "
            erase(inpt)
        elif command.strip(" ") == "visualize":
            create_plot("finance_data.csv")
        else:
            input('Command not found. Press "Enter" to continue...')


def exit():
    clear_terminal()
    sys.exit()


def clear_terminal():
    os.system("clear")


"""
new() records a new transaction with the amount, user comment (input), and date (current date).
The function takes two string arguments: a prompt for input and a global empty string (new_row) to temporarily store the data.
It appends the formatted data from new_row to a CSV file using format_data().
"""


def new(prompt):
    global new_row
    while True:
        transaction_input = input(prompt)
        if transaction_input.lower() == "back":
            return
        try:
            transaction_input = float(transaction_input)
            new_row += f"{date.today()},"
            new_row += f"{transaction_input},"
            print("Transaction added.")

            comment_input = input("Add your comment: ")
            new_row += f"{comment_input}\n"
            format_data(new_row)
            input('Comment recorded. Press "Enter" to continue...')
            return new('Enter new transaction amount (Type "back" to exit): ')

        except ValueError:
            print("Transaction is not a decimal number.")


"""
display() takes a CSV database file as an argument and displays the recorded data using tabulate.
It also calls calculate_sum() to display the total amount spent.
"""


def display(csv):
    clear_terminal()
    display_data_frame = pandas.read_csv(csv)
    display_data_frame.reset_index(drop=True, inplace=True)
    display_data_frame.index = display_data_frame.index + 1
    print(tabulate.tabulate(display_data_frame, headers="keys", tablefmt="pretty"))
    print(calculate_sum(display_data_frame))
    return display_data_frame


"""
command_list() displays a list of commands and their explanations in PrettyTable format.
"""


def command_list():
    pr_table = PrettyTable()
    pr_table.title = "Command list"
    pr_table.field_names = ["Command", "Explaination"]
    pr_table.add_row(["'new'", "Create new transaction"])
    pr_table.add_row(["'display'", "Displays current data"])
    pr_table.add_row(["'erase'", "Delete one transaction or all the data"])
    pr_table.add_row(["'visualize'", "Create a plot based on existin data"])
    pr_table.add_row(["'export'", "Exports data in excel format"])
    pr_table.add_row(["'exit'", "Exit the program"])
    return pr_table


"""
format_data() appends a new entry to the database CSV file and updates the global variable new_row used for temporary transaction storage.
"""


def format_data(n_r):
    global new_row
    with open("finance_data.csv", mode="a") as file:
        file.write(n_r)
        new_row = ""
        print(f"Data recorded.")


"""
calculate_sum() computes the total amount spent and returns it formatted as an f-string.
"""


def calculate_sum(df):
    total_amount = df["Amount ($)"].sum()
    return f"Total amount spent: {total_amount:.2f}$"


"""
excel_export() exports the data from a database CSV file into Excel format.
"""


def excel_export(csv):
    new_file_name = csv.replace(".csv", "")
    data_frame = pandas.read_csv(csv)
    data_frame.to_excel(f"{new_file_name}.xlsx", index=False)


"""
erase() prompts the user to choose between deleting all data or a single entry.
It invokes erase_all() to delete all data or erase_transaction() to delete a single entry based on the user's choice.
"""


def erase(prompt):
    user_answer = input(prompt)
    user_answer = user_answer.strip(" ")
    if user_answer.lower() == "all":
        erase_all()
    elif user_answer.lower() == "one":
        erase_transaction()
    else:
        input('The answer must be "all" or "one". Press "Enter to continue..."')
        return erase(prompt)


"""
erase_all() deletes all data from the CSV database.
It is called by the erase() function.
"""


def erase_all():
    while True:
        confirm = input("Are you sure you want to delete all the data? Y/N: ")
        if confirm.lower() == "n":
            break
        elif confirm.lower() == "y":
            input(
                'The data has been deleted successfully. Press "Enter" to continue...'
            )
            with open("finance_data.csv", mode="w") as file:
                file.write("Date,Amount ($),Comment\n")
            break
        else:
            print('Responce must be "Y" or "N".')


"""
er.
"""


def erase_transaction():
    while True:
        display("finance_data.csv")
        row_number = input(
            'Enter the number of transaction you want to delere(type "back" to exit): '
        )
        if row_number.isdigit():
            row_number = int(row_number)
            row_number -= 1
            erase_data_frame = display("finance_data.csv")
            if 0 <= row_number < len(erase_data_frame):
                erase_data_frame = erase_data_frame.drop(
                    erase_data_frame.index[row_number]
                )
                erase_data_frame.to_csv("finance_data.csv", index=False)
                display("finance_data.csv")
                input('Transaction deleted. Press "Enter" to continue...')
            else:
                print(f"Transaction number {row_number} doesn't exist.")
        elif row_number.lower() == "back":
            break


"""
create_plot() generates a plot based on existing data from a CSV database file.
"""


def create_plot(csv):
    basic_df = pandas.read_csv(csv)
    procesed_df = basic_df[["Date", "Amount ($)"]]
    procesed_df["Date"] = pandas.to_datetime(procesed_df["Date"])
    procesed_df = procesed_df.sort_values(by="Date")
    procesed_df.set_index("Date", inplace=True)
    plt.figure(figsize=(10, 10))
    procesed_df.plot(kind="line", legend=False)
    plt.title = "Amont spand(Time)"
    plt.xlabel("Date")
    plt.ylabel("Transactions")
    plt.grid(True)
    plt.savefig("visualized_data.png")


if __name__ == "__main__":
    main()

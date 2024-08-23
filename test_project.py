from project import (
    new,
    display,
    command_list,
    format_data,
    calculate_sum,
    excel_export,
    create_plot,
)
from prettytable import PrettyTable
from unittest.mock import patch
from datetime import date
import pandas
import csv
import os


def test_new(monkeypatch, capsys):
    inputs = iter(["ABCD", "100", "any comment", "back", "back"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    new("")
    new_captured = capsys.readouterr()
    assert "Transaction is not a decimal number.\n" in new_captured.out
    assert "Transaction added.\n" in new_captured.out
    assert "Data recorded." in new_captured.out


def test_display():
    display_return = display("finance_data.csv")
    expected_column_names = ["Date", "Amount ($)", "Comment"]
    assert isinstance(display_return, pandas.DataFrame)
    assert list(display_return.columns) == expected_column_names
    assert display_return.index[0] == 1


def test_command_list():
    command_list_return = command_list()
    expected_title = "Command list"
    expected_field_names = ["Command", "Explaination"]
    all_rows = [list(row) for row in command_list_return]
    assert isinstance(command_list_return, PrettyTable)
    assert command_list_return.title == expected_title
    assert list(command_list_return.field_names) == expected_field_names
    assert "'new'", "Create new transaction" in all_rows
    assert "'display'", "Displays current data" in all_rows
    assert "'erase'", "Delete one transaction or all the data" in all_rows
    assert "'visualize'", "Create a plot based on existin data" in all_rows
    assert "'export'", "Exports data in excel format" in all_rows
    assert "'exit'", "Exit the program" in all_rows


def test_format_data(capsys):
    new_row = "2024-03-01,100,cat food\n"
    format_data(new_row)
    with open("finance_data.csv", mode="r", newline="") as file:
        csv_read = csv.reader(file)
        list_data = list(csv_read)
        last_row = list_data[-1]
        expected_new_row = ["2024-03-01", "100", "cat food"]
    assert last_row == expected_new_row
    format_data_captured = capsys.readouterr()
    assert "Data recorded." in format_data_captured.out


def test_calculate_sum():
    data = {
        "Date": ["2024-01-01", "2024-01-02", "2024-01-03"],
        "Amount ($)": [9.99999999, 9.99999999, 9.99999999],
        "Comment": ["any comment", "any comment", "any comment"],
    }
    sum_data_frame = pandas.DataFrame(data)
    expected_output = "Total amount spent: 30.00$"
    calculate_sum_output = calculate_sum(sum_data_frame)
    assert expected_output == calculate_sum_output


def test_excel_export():
    excel_export("finance_data.csv")
    assert os.path.exists("finance_data.xlsx")


def test_create_plot():
    create_plot("finance_data.csv")
    assert os.path.exists("visualized_data.png")

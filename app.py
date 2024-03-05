from flask import Flask, render_template, request
import csv
import os

app = Flask(__name__, static_url_path='/static')

# Read CSV data
def read_csv(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=';')
        return list(reader)

# Homepage with dropdowns
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        csv_filename = request.form['csv']
        column_name = request.form['column']
        row_name = request.form['row']
        data = get_table_data(csv_filename, column_name, row_name)
        return render_template('index.html', data=data, selected_csv=csv_filename, columns=get_columns(csv_filename), rows=get_rows(csv_filename), selected_column=column_name, selected_row=row_name, csv_files=get_csv_files())
    else:
        # Provide a list of CSV files
        csv_files = get_csv_files()
        # Use the first CSV file by default
        default_csv_file = csv_files[0] if csv_files else None
        return render_template('index.html', columns=get_columns(default_csv_file), rows=get_rows(default_csv_file), csv_files=csv_files)

# Function to get data from CSV based on selected options
def get_table_data(csv_filename, column_name, row_name):
    # Read CSV data
    csv_data = read_csv(os.path.join(r'C:\Koda\Pythonkoda\Stran2', csv_filename))
    # Find the index of the selected column and row
    column_index = csv_data[0].index(column_name)
    row_index = [row[0] for row in csv_data].index(row_name)
    # Retrieve the corresponding data
    return csv_data[row_index][column_index]

# Function to get a list of column names from a CSV file
def get_columns(csv_filename):
    if csv_filename:
        csv_data = read_csv(os.path.join(r'C:\Koda\Pythonkoda\Stran2', csv_filename))
        return csv_data[0][1:]  # Exclude the first empty cell
    else:
        return []

# Function to get a list of row names from a CSV file
def get_rows(csv_filename):
    if csv_filename:
        csv_data = read_csv(os.path.join(r'C:\Koda\Pythonkoda\Stran2', csv_filename))
        return [row[0] for row in csv_data[1:]]  # Exclude the first row
    else:
        return []

# Function to get a list of CSV files in the directory
def get_csv_files():
    csv_files = []
    directory = (r'C:\Koda\Pythonkoda\Stran2')
    for filename in os.listdir(directory):
        if filename.endswith('.csv'):
            csv_files.append(filename)
    return csv_files

if __name__ == '__main__':
    app.run()
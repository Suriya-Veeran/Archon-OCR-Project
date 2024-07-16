import csv

global_file = None
global_writer = None


def open_csv(file_name):
    global global_file
    try:
        global_file = open(file_name, 'w', newline='')
    except IOError as e:
        print(f"Error: Unable to open file '{file_name}' - {e}")


def write_header(fields_name):
    global global_writer
    try:
        if global_file:
            global_writer = csv.DictWriter(global_file, fieldnames=fields_name)
            global_writer.writeheader()
        else:
            print("Error: The CSV file is not open.")
    except IOError as e:
        print(f"Error: Unable to write header - {e}")


def write_data(row):
    global global_writer
    try:
        if global_writer is not None:
            global_writer.writerows(row)
        else:
            print("Error: The CSV writer has not been initialized. Please write the header first.")
    except IOError as e:
        print(f"Error: Unable to write data - {e}")


def close_csv():
    global global_file
    try:
        if global_file:
            global_file.close()
            global_file = None
    except Exception as e:
        print(f"Error: Unable to close file - {e}")


if __name__ == '__main__':
    filename = '../Students_Data.csv'
    fieldnames = ['Name', 'M1 Score', 'M2 Score']
    data = [
        {'Name': 'Alex', 'M1 Score': 62, 'M2 Score': 80},
        {'Name': 'Brad', 'M1 Score': 45, 'M2 Score': 56},
        {'Name': 'Joey', 'M1 Score': 85, 'M2 Score': 98}
    ]
    try:
        open_csv(filename)
        write_header(fieldnames)
        write_data(data)
    finally:
        close_csv()

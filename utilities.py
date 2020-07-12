import csv


def str_list_to_int(str_to_int_list):
    try:
        str_to_int_list = [int(value) for value in str_to_int_list]
        return str_to_int_list
    except ValueError:
        print("One of the list items is not an integer.")


def check_value_type(value):
    value = value.upper()
    pokemon_value_types = ["IV", "EV"]
    if value in pokemon_value_types:
        return True
    return False


# Extract a row from the CSV file by selecting a key and desired output heading
# from the first line of the file, then search for a specified value in that key's column
# and return that row and its contents
def csv_extractor(csv_file, key, output, value):
    key = key.lower().strip()
    value = value.lower().strip()

    with open(csv_file) as csv_file:
        csv_reader = csv.reader(
            csv_file, quotechar='"', delimiter=',',
            quoting=csv.QUOTE_ALL, skipinitialspace=True)

        # Find key and output indices in CSV
        row1 = next(csv_reader)
        key_index = find_key_index(row1, key)
        output_index = find_key_index(row1, output)

        # Find row values in CSV
        for row in csv_reader:
            row_value = row[key_index].lower().strip()
            if row_value == value:
                return row[output_index]
    print(f'The value "{value}" cannot be found under the key "{key}".')
    return None


# Refactoring of inner loop to find the key for csv_extractor
def find_key_index(row, key):
    for idx, column in enumerate(row):
        column = column.lower().strip()
        if column == key:
            return idx

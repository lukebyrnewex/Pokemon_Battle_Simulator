import csv


def str_list_to_int(str_list):
    """Function with transforms string lists to int lists

    Args:
        str_list (list[str]): A list of strings.

    Returns:
        int_list (list[int]): A list of integers.

    Raises:
        ValueError: if one of the list variables
            is not a numeric value

    """
    try:
        int_list = [int(value) for value in str_list]
        return int_list
    except ValueError:
        print("One of the list items is not a numeric value.")


def csv_extractor(csv_filename, key, value, output):
    """Function which finds the an item in a key column, and returns the
    corresponding row item in the output column.
    For example: test.csv
        columnA     columnB     columnC
        1           2           3
        4           5           6
    csv_extractor("test.csv", "columnA", 4, "columnC") returns 6

    Args:
        csv_filename (csv): The csv file to search through.
        key: The column heading name for the column we wish to search through.
        value: The value in the key column which identifies the desired row.
        output: The column heading name in which the returned value lies.

    Returns:
        row[output_index]: The desired value from the output column.

    """
    key = key.lower().strip()
    value = value.lower().strip()
    output = output.lower().strip()

    # The parameters allow for inputs with commas within strings
    with open(csv_filename) as csv_file:
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
                output_value = row[output_index]
                if output_value.isdigit():
                    output_value = int(output_value)
                return output_value
    print(f'The value "{value}" cannot be found under the key "{key}".')
    return None


def find_key_index(row, key):
    """Refactoring of inner loop within csv_extractor(), which finds
    the index of the inputted key within the row.

    Args:
        row: The row within the CSV file.
        key: The key value for which we are searching.

    Returns:
        idx (int): The index within the row which contains the key value.

    """
    for idx, column in enumerate(row):
        column = column.lower().strip()
        if column == key:
            return idx


from DataGetter.src.classes.DbModel import DbModel

# Create DB object
db_model = DbModel()


# Method for line parsing.
def process_line(input_line, csv_sep):
    # Parse line.
    items = input_line.split(csv_sep)
    # Get correct items.
    company_id = int(items[0])
    orig_values = [
        items[5].strip(),   # fb_page
        items[6].strip(),   # tw_name
        items[7].strip(),   # tw_search_name
    ]
    # Replace empty strings with NULL.
    new_values = [None if not x else x for x in orig_values]
    # Return data.
    return company_id, new_values


# Method for updating DB.
def update_company(company_id, values):
    values.append(company_id)
    cursor = db_model.dbcon.cursor()
    query = "UPDATE company SET fb_page = %s, tw_name = %s, tw_search_name = %s WHERE id = %s LIMIT 1"
    cursor.execute(query, values)
    #exit(cursor.statement)
    cursor.close()


# Method for input file processing.
def process_input_file(file_path, csv_sep):
    # Prepare file
    csv_file = open(file_path)
    csv_file.readline()  # skip header line
    print('>>>Started processing file for companies DB update.')
    # Process all lines
    for input_line in csv_file:
        # Read data
        company_id, line_values = process_line(input_line, csv_sep)
        print company_id, line_values
        # Update DB
        update_company(company_id, line_values)
    # Commit all changes
    db_model.dbcon.commit()
    print('>>>Companies DB update was successful.')


# EXECUTION
process_input_file('Companies_with_twitter.csv', ';')

import os


class CompanyCsvParser(object):
    '''
    Parser for company list in CSV file and producing SQL insert query.
    '''


    def __init__(self):
        '''
        Constructor
        '''

    def create_sql(self, csv_filepath, output_dir, csv_sep, index_id, start_id):
        '''
        
        '''
        # Open CSV file
        cfpath = os.path.abspath(csv_filepath)
        csv_file = open(cfpath, 'r')
        # Prepare SQL file
        base_fname = os.path.basename(csv_file.name).split('.')[0]
        sfpath = os.path.abspath(output_dir+'/'+base_fname+'.sql')
        sql_file = open(sfpath, 'w')
        # Read CSV file line by line and write every line to SQL file.
        for id, line in enumerate(csv_file, start_id):
            # ID will start from 1 to N.
            items = line.split(csv_sep)
            # Create SQL INSERT statement.
            write_string = 'INSERT INTO company (id, name, index_id, ticker, fb_page, tw_name, tw_search_name) VALUES '
            # facebook data
            fb_name = items[2].strip()
            fb_name = 'NULL' if fb_name == 'none' else '"'+fb_name+'"'
            # twitter data
            tw_name = items[3].strip()
            if not tw_name:
                tw_name = 'NULL'
                tw_search = 'NULL'
            else:
                tw_name = '"'+tw_name+'"'
                tw_search = '"'+items[4].strip()+'"'
            # Values
            write_string += '(%d, "%s", %d, "%s", %s, %s, %s)' % (id, items[0].strip(), index_id, items[1].strip(), fb_name, tw_name, tw_search) 
            # Add SQL statement to SQL file.
            sql_file.write(write_string+';\n')
              
        # Close files
        csv_file.close()
        sql_file.close()
        
        
        
        
        
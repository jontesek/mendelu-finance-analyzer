import sys
from os import path

sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
from classes.CompanyList import CompanyList

# Create new files for companies.

# Prepare variables.
cl = CompanyList()
companies = cl.get_tw_companies()
data_folder = path.abspath('../../data/twitter')

# Directories
dirs = ['mentions', 'searches', 'replies', 'timeline']

# Loop through companies.
for company in companies:
    # Do it for every dir.
    for dir_name in dirs:
        # tweets file
        tfile = open(path.abspath(data_folder+'/'+dir_name+'/'+company+'.csv'), 'w')
        tfile.close()
        # last id file
        tfile = open(path.abspath(data_folder+'/'+dir_name+'/'+company+'.lastid'), 'w')
        tfile.write('1')
        tfile.close()

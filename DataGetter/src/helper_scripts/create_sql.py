import sys
from os import path

sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
from classes.CompanyCsvParser import CompanyCsvParser

comp_parser = CompanyCsvParser()
#comp_parser.create_sql('../../test_data/USA.csv', '../../test_data', ';',1,1)
comp_parser.create_sql('../../test_data/EU.csv', '../../test_data', ';',2,501)

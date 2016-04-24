###########
# Imports
###########
import os
import src.file_processing as my_fp

########
# Parameter definitions
########

# File paths
doctype_dir = 'xtest'

input_dir = os.path.abspath('../outputs/vec_text/' + doctype_dir)
output_dir = os.path.abspath('../outputs/vec_text_balanced/' + doctype_dir)

########
# EXECUTION
########

# Test
#print my_fp._get_class_counts_from_stat_file(r'C:\Users\Jontes\Documents\programovani\PyCharmProjects\FinanceAnalyzer\outputs\vec_text\xtest\tweet_44-202-233-300_adjclose_1_4_tf-idf-no.stat.txt')

my_fp.balance_files(input_dir, output_dir)


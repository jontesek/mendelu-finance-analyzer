###########
# Imports
###########
import os
import src.file_processing as my_fp

########
# Parameter definitions
########

# Define file paths.
input_base_dir = os.path.abspath('../outputs/vec_text')
output_base_dir = os.path.abspath('../outputs/vec_text_balanced')

# Specify processed directories.
#dir_names = ['fb_com_10pd', 'fb_post', 'twitter_4', 'article']
dir_names = ['xtest']

########
# EXECUTION
########

# Test
#print my_fp._get_class_counts_from_stat_file('../outputs/vec_text/xtest/tweet_44-202-233-300_adjclose_1_4_tf-idf-no.stat.txt')

# Process all specified directories.
for dirname in dir_names:
    input_dir = os.path.join(input_base_dir, dirname)
    output_dir = my_fp.get_or_create_directory(os.path.join(output_base_dir, dirname))
    my_fp.balance_files(input_dir, output_dir)

from collections import OrderedDict
import os
import shutil
import datetime
import socket


def get_features_from_vector_filename(file_name):
    data_dict = OrderedDict()
    features = file_name.split('_')
    data_dict['doc_type'] = features[0]
    data_dict['company'] = features[1]
    data_dict['variable_type'] = features[2]
    data_dict['days_delay'] = features[3]
    data_dict['const_border'] = features[4]
    data_dict['vector_type'] = features[5]
    return data_dict


def get_or_create_results_file(input_dirname, output_dir, text_writer, header_list, r_description):
    # Create filename.
    res_filename = input_dirname + '_results' + r_description
    # If the file does not exist, create it.
    if not os.path.isfile(os.path.join(output_dir, res_filename + '.csv')):
        text_writer.reset_results_file(res_filename, [header_list])
    # Return results file name.
    return res_filename


def get_or_create_log_file(log_dir, input_dirname, r_description):
    # Create a file name.
    log_filepath = os.path.join(log_dir, input_dirname + r_description + '.log')
    # Define information to be written.
    wr_str = '>>>Analysing %s \n' % input_dirname
    wr_str += '>>>Analysis started %s on %s computer.\n' % (str(datetime.datetime.now()), socket.gethostname())
    # If the file does not exist, create it.
    if not os.path.isfile(log_filepath):
        with open(log_filepath, 'w') as fh:
            fh.write(wr_str)
    # Return full path to log file.
    return log_filepath


def is_not_empty_file(fpath):
    if os.path.isfile(fpath) and os.path.getsize(fpath) > 0:
        return True
    else:
        return False


### BALANCING FILES

def balance_files(input_dir, output_dir):
    # Check if dirs are different from each other.
    if input_dir == output_dir:
        raise ValueError('Input and output dir cannot be the same.')
    # Process all files in input directory.
    print('===Balancing files in directory %s===') % os.path.basename(input_dir)
    for input_filename in sorted(os.listdir(input_dir)):
        if input_filename.endswith('.SVMlight.dat'):
            print input_filename
            # Create path to input file.
            input_filepath = os.path.join(input_dir, input_filename)
            # Create a new output file name.
            base_filename = input_filename.replace('.SVMlight.dat', '')
            output_filename = base_filename + '_balanced.SVMlight.dat'
            # Get class counts from STAT file.
            stat_filename = input_filename.replace('.SVMlight.dat', '.stat.txt')
            stat_filepath = os.path.join(input_dir, stat_filename)
            class_counts = _get_class_counts_from_stat_file(stat_filepath)
            # If the file contains only one class, skip it.
            if not class_counts:
                continue
            # Balance DAT file.
            min_class_count = min(class_counts)
            output_filepath = os.path.join(output_dir, output_filename)
            _balance_given_file(input_filepath, output_filepath, min_class_count)
            # Copy STAT file to output dir.
            shutil.copy2(stat_filepath, output_dir)
    # OK
    print('>>>All files were balanced.')


def _balance_given_file(input_filepath, output_filepath, min_class_count):
        """
        Create a new file, where each class will have the same number of items.
        """
        # Open files.
        input_file = open(input_filepath, 'r')
        output_file = open(output_filepath, 'w')
        # Define class count variables.
        c_1 = 0
        c_2 = 0
        # Loop through all documents (lines).
        for line in input_file:
            if line[0] == '1':
                c_1 += 1
                if c_1 <= min_class_count:
                    output_file.write(line)
            if line[0] == '2':
                c_2 += 1
                if c_2 <= min_class_count:
                    output_file.write(line)
        # OK
        return True


def _get_class_counts_from_stat_file(stat_filepath):
    file_stat = open(stat_filepath)
    f_lines = file_stat.readlines()
    try:
        c_1 = int(f_lines[25].split(' ')[0])
        c_2 = int(f_lines[31].split(' ')[0])
    except IndexError:
        print('>>Only one class in file, skipping it.')
        # There is only one class.
        return False
    return [c_1, c_2]


def get_or_create_directory(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    return dir_path

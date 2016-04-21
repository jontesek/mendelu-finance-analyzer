from collections import OrderedDict

import os


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


def check_and_reset_results_file(file_name, output_dir, text_writer, header_list, r_desc):
    # Get info.
    f_features = file_name.split('_')
    d_type = f_features[0]
    source_id = f_features[1]
    # Edit results file name.
    if source_id == 'all':
        res_filename = d_type + '_results'
    else:
        res_filename = d_type + '_results_' + source_id
    res_filename += r_desc
    # Reset file.
    if not os.path.isfile(os.path.join(output_dir, res_filename + '.csv')):
        text_writer.reset_results_file(res_filename, [header_list])
    # return file name
    return res_filename


def is_not_empty_file(fpath):
    if os.path.isfile(fpath) and os.path.getsize(fpath) > 0:
        return True
    else:
        return False


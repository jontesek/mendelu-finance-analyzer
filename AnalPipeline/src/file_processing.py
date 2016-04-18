from collections import OrderedDict


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

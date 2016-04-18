import os


def build_query_from_params(par_dict):
    query = ''
    for (par_name, par_value) in par_dict.items():
        query += '--%s="%s" ' % (par_name, par_value)
    return query


def check_if_vector_file_exists(output_dir, base_name, conf_id):
    file_name = '%s_%s.SVMlight.dat' % (base_name, conf_id)
    file_path = os.path.join(output_dir, file_name)
    if os.path.isfile(file_path):
        return True
    else:
        return False

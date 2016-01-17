import codecs


class TextWriter(object):

    def __init__(self, output_dir):
        """
        Constructor.
        :param output_dir: absolute filepath to output directory
        :return:
        """
        self.output_dir = output_dir

    def _write_file(self, data_lists, file_name, file_extension, items_delimiter, file_mode):
        file_path = '%s/%s.%s' % (self.output_dir, file_name, file_extension)
        # Prepare file for writing
        with codecs.open(file_path, mode=file_mode, encoding="utf-8-sig") as fh:
            # Loop through all data lists (rows)
            for line in data_lists:
                max_index = len(line) - 1
                # Loop through all items in a list (row -> columns)
                for i in range(0, max_index+1):
                    fh.write(str(line[i]))
                    if i < max_index:
                        fh.write(items_delimiter)
                # break line
                fh.write('\n')

    def write_file_for_vectorization(self, file_name, documents_list, file_mode):
        self._write_file(documents_list, file_name, 'txt', '\t', file_mode)

    def write_econometric_file(self, file_name, days_list, file_mode):
        self._write_file(days_list, file_name, 'csv', ',', file_mode)

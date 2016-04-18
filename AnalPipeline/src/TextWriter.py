import codecs


class TextWriter(object):

    def __init__(self, output_dir):
        self.output_dir = output_dir

    def _write_file(self, data_lists, file_name, file_extension, items_delimiter, file_mode):
        """
        Write lines of data to file.
        """
        # Path to output file.
        file_path = '%s/%s.%s' % (self.output_dir, file_name, file_extension)
        # Prepare file for writing.
        with codecs.open(file_path, mode=file_mode, encoding="utf-8-sig") as fh:
            # Loop through all data lists.
            for line in data_lists:
                max_index = len(line) - 1
                # Loop through all items in a list.
                for i in range(0, max_index + 1):
                    fh.write(str(line[i]))
                    if i < max_index:
                        fh.write(items_delimiter)
                # Break line.
                fh.write('\n')

    def write_to_results_file(self, file_name, results_list):
        self._write_file(results_list, file_name, 'csv', ';', 'a')

    def reset_results_file(self, res_filename, header_list):
        self._write_file(header_list, res_filename, 'csv', ';', 'w')

import codecs


class TextWriter(object):

    def __init__(self, output_dir='.'):
        """
        Constructor.
        :param output_dir: absolute filepath to output directory
        :return:
        """
        self.output_dir = output_dir

    def _write_file(self, data_lists, file_name, file_extension, items_delimiter, file_mode):
        # Create a file path.
        file_path = '%s/%s.%s' % (self.output_dir, file_name, file_extension)
        lines_c = len(data_lists) - 1
        # Prepare file for writing
        with codecs.open(file_path, mode=file_mode, encoding="utf-8-sig") as fh:
            # Loop through all data lists (rows).
            for line_n, line_content in enumerate(data_lists):
                # Get last index (based on number of columns).
                max_index = len(line_content) - 1
                # Loop through all items in a list (row -> columns)
                for col_n in range(0, max_index+1):
                    # Check if the value is string or number/boolean.
                    if isinstance(line_content[col_n], basestring):
                        write_item = line_content[col_n]
                    else:
                        write_item = str(line_content[col_n])
                    # Write field to the current row.
                    fh.write(write_item)
                    # Add delimiter
                    if col_n < max_index:
                        fh.write(items_delimiter)
                # Break line - not for the last item
                if line_n < lines_c:
                    fh.write('\n')

    def write_file_for_vectorization(self, file_name, documents_list, file_mode):
        self._write_file(documents_list, file_name, 'txt', '\t', file_mode)

    def write_econometric_file(self, file_name, days_list, file_mode):
        self._write_file(days_list, file_name, 'csv', ',', file_mode)

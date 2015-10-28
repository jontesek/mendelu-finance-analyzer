import codecs


class TextWriter(object):

    def __init__(self, output_dir):
        self.output_dir = output_dir

    def _write_file(self, data_lists, file_name, file_extension, items_delimiter):
        file_path = '%s/%s.%s' % (self.output_dir, file_name, file_extension)
        # Prepare file for writing
        with codecs.open(file_path, mode="w", encoding="utf-8-sig") as fh:
            # Loop through all data lists
            for line in data_lists:
                max_index = len(line) - 1
                # Loop all items in a list
                for i in range(0, max_index+1):
                    fh.write(line[i])
                    if i < max_index:
                        fh.write(items_delimiter)
                # break line
                fh.write('\n')

    def write_file_for_vectorization(self, file_name, documents_list):
        self._write_file(documents_list, file_name, 'txt', '\t')

import codecs

class TextWriter(object):

    def __init__(self, output_dir):
        self.output_dir = output_dir
        self.file_extension = 'csv'
        self.items_delimiter = ','

    def set_params(self, delimiter, extension):
        self.file_extension = extension
        self.items_delimiter = delimiter

    def write_file(self, file_name, data_lists):
        file_path = '%s/%s.%s' % (self.output_dir, file_name, self.file_extension)
        # Prepare file for writing
        with codecs.open(file_path, mode="w", encoding="utf-8-sig") as fh:
            # Loop through all data lists
            for line in data_lists:
                max_index = len(line) - 1
                # Loop all items in a list
                for i in range(0, max_index+1):
                    fh.write(line[i])
                    if i < max_index:
                        fh.write(self.items_delimiter)
                # break line
                fh.write('\n')


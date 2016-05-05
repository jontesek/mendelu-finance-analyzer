from FaCommon.TextWriter import TextWriter


class SourceMetricsCalculator(object):

    def __init__(self, output_dir):
        """
        Constructor
        :param output_dir: absolute filepath to output directory
        :return:
        """
        self.output_dir = output_dir
        self.text_writer = TextWriter(output_dir)
        # Set input data indices
        self.source_sent_pos = {'fb_post': 18, 'fb_comment': 19, 'yahoo': 20, 'twitter': 21}
        self.price_dir_indices = {-1: 14, 1: 15, 2: 16, 3: 17}
        self.day_delays = [-1, 1, 2, 3]

    def calculate_metrics_by_source(self, company_id, total_data, file_name, price_type, write_header=False):
        """
        Calculate metrics for one company (from all available days).
        :param company_id: int
        :param total_data: list
        :return: list
        """
        # For every source, get all delays and calculate metrics.
        company_stats = self._prepare_matrices_for_sources()
        company_stats = self._fill_result_matrices(company_stats, total_data)
        metrics = self._calc_metrics_from_matrices(company_stats)
        m_list = self._format_source_metrics_to_list(company_id, metrics, price_type)
        # Write to file
        if write_header:
            m_list.insert(0, self.get_source_metrics_header())
            self.text_writer.write_econometric_file(file_name, m_list, 'w')
            del(m_list[0])
        else:
            self.text_writer.write_econometric_file(file_name, m_list, 'a')
        # the end

    def _calc_metrics_from_matrices(self, company_stats):
        metrics = {}
        # For every source
        for source in company_stats:
            metrics[source] = {}
            # For every delay
            for delay, matrix in company_stats[source].items():
                d_stats = {}
                # Accuracy - only one for the whole matrix.
                total_values_count = sum(matrix.values())
                total_correct_count = matrix['pos_up'] + matrix['neg_down'] + matrix['neu_const']
                if total_values_count == 0:
                    accuracy = None
                else:
                    accuracy = total_correct_count / total_values_count
                d_stats['accuracy'] = accuracy
                # Precision
                pp = matrix['pos_up'] + matrix['pos_down'] + matrix['pos_const']
                pn = matrix['neg_up'] + matrix['neg_down'] + matrix['neg_const']
                pc = matrix['neu_up'] + matrix['neu_down'] + matrix['neu_const']
                d_stats['precision_pos'] = None if pp == 0 else matrix['pos_up'] / pp
                d_stats['precision_neg'] = None if pn == 0 else matrix['neg_down'] / pn
                d_stats['precision_neu'] = None if pc == 0 else matrix['neu_const'] / pc
                # Precision average
                #weight_by = 3 if total_correct_count == 0 else total_correct_count
                #weights = (matrix['pos_up'], matrix['neg_down'], matrix['neu_const'])
                weight_by = 3
                weights = (1, 1, 1)
                d_stats['precision_avg'] = (float(d_stats['precision_pos'] or 0) * weights[0] +
                                            float(d_stats['precision_neg'] or 0) * weights[1] +
                                            float(d_stats['precision_neu'] or 0) * weights[2]) / weight_by
                # Recall
                rp = matrix['pos_up'] + matrix['neg_up'] + matrix['neu_up']
                rn = matrix['pos_down'] + matrix['neg_down'] + matrix['neg_down']
                rc = matrix['pos_const'] + matrix['neg_const'] + matrix['neu_const']
                d_stats['recall_pos'] = None if rp == 0 else matrix['pos_up'] / rp
                d_stats['recall_neg'] = None if rn == 0 else matrix['neg_down'] / rn
                d_stats['recall_neu'] = None if rc == 0 else matrix['neu_const'] / rc
                # Recall average
                #weight_by = 3 if total_correct_count == 0 else total_correct_count
                #weights = (matrix['pos_up'], matrix['neg_down'], matrix['neu_const'])
                weight_by = 3
                weights = (1, 1, 1)
                d_stats['recall_avg'] = (float(d_stats['recall_pos'] or 0) * weights[0] +
                                         float(d_stats['recall_neg'] or 0) * weights[1] +
                                         float(d_stats['recall_neu'] or 0) * weights[2]) / weight_by
                # Save to total data
                metrics[source][delay] = d_stats
        # result
        return metrics

    def _prepare_matrices_for_sources(self):
        # Main directory
        company_stats = {}
        # For every source
        for source in self.source_sent_pos:
            company_stats[source] = {}
            # For every delay create a confusion matrix.
            for i in self.day_delays:
                company_stats[source][i] = {
                    'pos_up': 0.0, 'pos_down': 0.0, 'pos_const': 0.0,
                    'neg_up': 0.0, 'neg_down': 0.0, 'neg_const': 0.0,
                    'neu_up': 0.0, 'neu_down': 0.0, 'neu_const': 0.0,
                }
        # result
        return company_stats

    def _fill_result_matrices(self, company_stats, total_data):
        # Process all days
        for day in total_data:
            # For every source
            for source in self.source_sent_pos:
                # For every delay update the confusion matrix.
                for i in self.day_delays:
                    price_mov = day[self.price_dir_indices[i]]
                    # Skip FALSE price movements.
                    if not price_mov:
                        continue
                    company_stats[source][i][day[self.source_sent_pos[source]] + '_' + price_mov] += 1
        # result
        return company_stats

    def _format_source_metrics_to_list(self, company_id, metrics, price_type):
        """
        Format metrics to one list (one line).
        :param metrics: dictionary of sources
        :return:
        """
        company_rows = []
        # For every source
        for source in sorted(metrics.keys()):
            # For every delay
            for delay in sorted(metrics[source].keys()):
                row_data = [company_id, source, price_type, delay]
                d_data = metrics[source][delay]
                row_data.extend([
                    d_data['accuracy'], d_data['precision_avg'], d_data['recall_avg'],
                    d_data['precision_pos'], d_data['precision_neg'], d_data['precision_neu'],
                    d_data['recall_pos'], d_data['recall_neg'], d_data['recall_neu'],
                ])
                company_rows.append(row_data)
        # Result
        return company_rows

    def get_source_metrics_header(self):
        """
        One row ... one source and one delay.
        """
        header = [
            'company_id', 'source', 'price_type', 'delay',
            'accuracy', 'precision_avg', 'recall_avg',
            'precision_pos', 'precision_neg', 'precision_neu',
            'recall_pos', 'recall_neg', 'recall_neu',
        ]
        # result
        return header

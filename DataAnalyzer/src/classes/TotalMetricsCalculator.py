from FaCommon.TextWriter import TextWriter


class TotalMetricsCalculator(object):

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

    def calculate_total_metrics(self, company_id, total_data, file_name, write_header=False):
        # Calculate metrics
        results = self._evaluate_results_for_company(total_data)
        metrics = self._calc_metrics_from_results(results)
        # Save to file
        m_list = [['<<<<<Company %d>>>>>' % company_id]]
        m_list.extend(self._format_total_metrics_to_list(metrics))
        if write_header:
            self.text_writer.write_econometric_file(file_name, m_list, 'w')
        else:
            self.text_writer.write_econometric_file(file_name, m_list, 'a')

    def _evaluate_results_for_company(self, total_data):
        """For every day and every delay evaluate relation between sentiment value and stock price movement."""
        # Prepare variables
        stats = {}
        for i in self.day_delays:
            stats[i] = {
                'pos_up': 0.0, 'pos_down': 0.0, 'pos_const': 0.0,
                'neg_up': 0.0, 'neg_down': 0.0, 'neg_const': 0.0,
                'neu_up': 0.0, 'neu_down': 0.0, 'neu_const': 0.0,
            }
        # Process all days
        for day in total_data:
            for i in self.day_delays:
                price_mov = day[self.price_dir_indices[i]]
                # Skip FALSE price movements.
                if not price_mov:
                    continue
                stats[i][day[-1] + '_' + price_mov] += 1
        # result
        return stats

    def _calc_metrics_from_results(self, results):
        """Calculate some metrics from evaluated results (confusion matrix)."""
        # Count total number of values in one delay data.
        total_values_count = sum(results.values()[0].values())
        # Process all delays and calculate metrics.
        metrics = {}
        for delay, data in results.items():
            try:
                accuracy = (data['pos_up'] + data['neg_down'] + data['neu_const']) / total_values_count
                precision = data['pos_up'] / (data['pos_up'] + data['pos_down'])
                recall = data['pos_up'] / (data['pos_up'] + data['neg_up'])
            except ZeroDivisionError:
                precision = None
                recall = None
            metrics[delay] = {'accuracy': accuracy, 'precision': precision, 'recall': recall}
        # result
        return metrics

    def _format_total_metrics_to_list(self, metrics):
        ordered_keys = sorted(metrics.keys())
        lines = []
        for key in ordered_keys:
            m_line = 'delay %d: accuracy: %.4f, ' % (key, metrics[key]['accuracy'])
            m_line += 'precision: ' + str(metrics[key]['precision']) + ', recall: ' + str(metrics[key]['recall'])
            lines.append([m_line])
        # result
        return lines

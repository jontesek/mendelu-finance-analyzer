import datetime

from BasicDbModel import BasicDbModel


class DocumentsAnalyzer(object):

    def __init__(self):
        self.dbmodel = BasicDbModel()

    def analyze_company(self, company_id, from_date):
        """
        Analyze documents about company (from_date -> present date).
        :param company_id: int
        :param from_date: string
        :return: list of days, where every row contains information for documents for this day.
        """
        # Prepare variables
        examined_date = datetime.datetime.strptime(from_date, '%Y-%m-%d')
        total_data = []
        # For every day (from "from_date" to present date), query the DB for documents created on the day.
        while examined_date <= datetime.datetime.today():
            print examined_date
            print self.dbmodel._from_date_to_timestamp(examined_date)
            # For every document type, process all documents and count number of neutral, positive, negative documents.
            fb_p_values = self._process_fb_posts(company_id, examined_date)
            fb_c_values = self._process_fb_comments(company_id, examined_date)
            yahoo_values = self._process_yahoo(company_id, examined_date)
            tw_values = self._process_twitter(company_id, examined_date)
            # Save data
            day_data = [
                company_id,
                examined_date.strftime('%Y-%m-%d'),
                fb_p_values['neu'], fb_p_values['pos'], fb_p_values['neg'],
                fb_c_values['neu'], fb_c_values['pos'], fb_c_values['neg'],
                yahoo_values['neu'], yahoo_values['pos'], yahoo_values['neg'],
                tw_values['neu'], tw_values['pos'], tw_values['neg'],
            ]
            total_data.append(day_data)
            # Increment examined date
            examined_date = examined_date + datetime.timedelta(days=1)

    def _process_fb_posts(self, company_id, examined_date):
        # Select all FB posts for given company created on given date.
        posts = self.dbmodel.get_daily_fb_posts(company_id, examined_date)



import os

"""Get tweets containing @companyUsername"""
def __old_get_all_mentions(self):
    # Cycle through all companies.
    self.companies = {'amazon':'Amazon'}
    for comp_username in self.companies:
        # Get ID of last downloaded tweet.
        lfpath = os.path.abspath(self.file_paths['data_folder']+'/tw_lastids/'+comp_username+'.lastid')
        lfile = open(lfpath, 'r+')
        last_id = lfile.read()
        # Make a request to twitter API and get tweets.
        query = '@'+comp_username
        mentions = self.twitter_api.search(q=query, lang = 'en', result_type = 'recent', count = 100, since_id = last_id)
        # Get new max ID and save it to lfile.
        max_id = mentions['search_metadata']['max_id_str']
        lfile.seek(0,0)
        lfile.write(max_id)
        lfile.close()
        # Open tweets file for writing.
        tfpath = os.path.abspath(self.file_paths['data_folder']+'/tw_mentions/'+comp_username+'.tweets')
        tfile = open(tfpath, 'a')
        # Save new tweets to company file.
        for status in mentions['statuses']:
            tfile.write(str(status)+'\n')
        # Close file
        tfile.close()
            
        
            
    """Get tweets containg "company name" but not containing @companyUsername"""    
    def get_all_searches(self):
        # search: coca cola -@CocaCola ... coca%20cola%20-%40CocaCola
        # Cycle through all companies.
        self.companies = {'amazon':'Amazon'}
        for comp_username, comp_name in self.companies.iteritems():
            # Get ID of last downloaded tweet.
            lfpath = os.path.abspath(self.file_paths['data_twitter']+'/searches/'+comp_username+'.lastid')
            lfile = open(lfpath, 'r+')
            last_id = lfile.read()
            # Make a request to twitter API and get tweets.
            query = comp_name.lower()+' -@'+comp_username
            results = self.twitter_api.search(q=query, lang = 'en', result_type = 'recent', count = 100, since_id = last_id)
            # Get new max ID and save it to lfile.
            max_id = results['search_metadata']['max_id_str']
            lfile.seek(0,0)
            lfile.write(max_id)
            lfile.close()
            # Open tweets file for writing.
            tfpath = os.path.abspath(self.file_paths['data_twitter']+'/searches/'+comp_username+'.tweets')
            tfile = open(tfpath, 'a')
            # Save new tweets to the company file.
            for status in results['statuses']:
                tfile.write(str(status)+'\n')
            # Close file
            tfile.close()
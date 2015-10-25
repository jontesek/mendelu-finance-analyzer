from GeneralPreparerDbModel import GeneralPreparerDbModel

class GeneralPreparer(object):

    def __init__(self):
        self.dbmodel = GeneralPreparerDbModel()

    def get_fb_posts(self, company_id):
        for post in self.dbmodel.get_posts_by_company(company_id):
            pass
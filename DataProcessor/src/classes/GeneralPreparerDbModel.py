from DbModel import DbModel


class GeneralPreparerDbModel(DbModel):
    #### READ methods

    def get_companies(self):
        cursor = self.dbcon.cursor(dictionary=True)
        query = "SELECT id FROM company WHERE fb_page IS NOT NULL ORDER BY id ASC"
        cursor.execute(query)
        return cursor.fetchall()

    def get_posts_by_company(self, id):
        cursor = self.dbcon.cursor(dictionary=True)
        query = "SELECT text, init_likes_count FROM fb_post WHERE company_id = %s"
        cursor.execute(query, id)

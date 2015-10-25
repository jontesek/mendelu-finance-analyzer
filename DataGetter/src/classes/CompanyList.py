# coding=utf-8

class CompanyList(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.__insert_tw_companies()
        self.__insert_companies()
        
    
    def __insert_companies(self):
        comp = []
        comp.append({'ticker': 'ADBE', 'fb_page': '110534035634837'})
        comp.append({'ticker': 'AMD', 'fb_page': 'AMD'})
        comp.append({'ticker': 'AKAM', 'fb_page': 'AkamaiTechnologies'})
        
        self.companies = comp
        
        
    def __insert_tw_companies(self):
        # Hash: {username} = [company name]
        comp = {}
        comp['facebook'] = 'Facebook'
        comp['CocaCola'] = 'Coca cola'
        comp['McDonalds'] = 'McDonalds'
        comp['Walmart'] = 'Walmart'
        comp['intel'] = 'Intel'
        comp['amazon'] = 'Amazon'
        comp['samsungtweets'] = 'Samsung USA'
        comp['LVMH'] = 'LVMH'
        comp['LouisVuitton'] = 'Louis Vuitton'
        comp['google'] = 'Google'
        comp['applenws'] = 'Apple'
        comp['att'] = 'AT&T'
        comp['shell'] = 'Shell'
        comp['Bradesco'] = 'Bradesco'
        comp['HP'] = 'HP'
        comp['Toyota'] = 'Toyota USA'
        comp['unilever'] = 'Unilever'           # Unilever news
        comp['johnsonsbaby'] = 'Johnson'        # Johnson's Baby
        comp['generalelectric'] = 'General Electric'
        comp['bofa_news'] = 'Bank of America'   # news
        comp['nestle'] = 'Nestlé'
        comp['UPS'] = 'UPS'                     # United Parcel Service
        comp['vodafoneuk'] = 'Vodafone UK'      
        comp['WellsFargo'] = 'Wells Fargo'
        comp['BP_America'] = 'BP America'
        
        self.tw_companies = comp
        
        
    def get_tw_companies(self):
        return self.tw_companies 
    
    
    def get_companies(self):
        return self.companies   
        
    

    
        
        
    
    
from classes.StockPriceTransformer import StockPriceTransformer

spt = StockPriceTransformer()

company_id = 1

spt.calculate_moving_average_for_company(company_id, 3)

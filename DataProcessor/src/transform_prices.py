from classes.StockPriceTransformer import StockPriceTransformer

spt = StockPriceTransformer()

spt.calculate_moving_average_for_company(1, 3)

spt.calculate_ma_for_all_companies(3)
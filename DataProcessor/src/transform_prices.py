from classes.StockPriceTransformer import StockPriceTransformer

spt = StockPriceTransformer()

#spt.calculate_sma_for_company(1, 3)

#spt.calculate_ewma_for_company(1, 20)

spt.calculate_ma_for_all_companies('sma', 20)
spt.calculate_ma_for_all_companies('ewma', 5)

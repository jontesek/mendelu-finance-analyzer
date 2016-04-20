import pyma

# Exponential moving average

data = [10, 5, 14, 17, 18, 10, 2, 47, 189, 41, 18,48,47,478,477,488,74,56,14]
n_len = len(data)

ema = pyma.NDayEMA(20)

for day in data:
    print '%s : %s ' % (day, ema.compute(day))



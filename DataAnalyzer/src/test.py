from classes.SentimentAnalyzer import SentimentAnalyzer

input_string = u"today we're celebrating 75 years of road safety innovation. one notable example is the evolution of the stop sign. since the 1930s, 3m technologies have increased sign brightness and improved durability."
sa = SentimentAnalyzer()
print sa.calculate_simple_sentiment('warriner', input_string)




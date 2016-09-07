from classes.LexiconSentimentAnalyzer import LexiconSentimentAnalyzer

input_string = """
Redesigned, Refined, and Supercharged: AMD Launches New Graphics Software, Radeon Software Crimson Edition
Fully Re-Architected Graphics Software Ushers in a New Era of Immersive Computing With Redesigned User Interface, Remarkable Features, Powerful Performance Boosts and Significant Power Savings for Gamers
Marketwired Advanced Micro Devices
SUNNYVALE, CA--(Marketwired - Nov 24, 2015) - AMD (NASDAQ: AMD) today released its completely reimagined graphics software suite, Radeon Software Crimson Edition, giving users an exceptional new user experience, 12 new or enhanced features, up to 20 percent more graphics performance1, adjustability that can nearly double generational energy efficiency2, and rock-solid stability across the full spectrum of AMD graphics products. The release is the first from the Radeon Technologies Group, which recently announced a renewed focus on software placing it on par with hardware initiatives.
"As the primary way that people interact with our products, our software deserves to be viewed as a top priority, and going forward that's exactly what we're doing, delivering easy-to-use software that is packed with real user benefits, starting with Radeon Software Crimson Edition," said Raja Koduri, senior vice president and chief architect, Radeon Technologies Group. "Radeon Technologies Group is laser-focused on the vertical integration of all things graphics, propelling the industry forward by driving performance per watt, creating innovative technologies and ensuring that the software supporting our GPUs is world class."
"""
input_string2 = """
We rate ADVANCED MICRO DEVICES (AMD) a SELL. This is driven by a number of negative factors, which we believe should have a greater impact than any strengths, and could make it more difficult for investors to achieve positive results compared to most of the stocks we cover. The company's weaknesses can be seen in multiple areas, such as its deteriorating net income, poor profit margins, weak operating cash flow, generally disappointing historical performance in the stock itself and feeble growth in its earnings per share.
"""
input_string3 = u"today we're celebrating 75 years of road safety innovation. one notable example is the evolution of the stop sign. since the 1930s, 3m technologies have increased sign brightness and improved durability."

input_string4 = "Scientists are pioneers of products, technology & innovation. LifeWith3M"

sa = LexiconSentimentAnalyzer()
#print sa.calculate_simple_sentiment('vader', input_string2)
print sa.calculate_vader_sentiment('custom_dict_orig',input_string4)

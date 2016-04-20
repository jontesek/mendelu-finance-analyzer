
# Arithmetically weighted moving average

data = [10, 5, 14, 17, 18, 10, 2, 47, 189]
d_length = len(data)
top_sum = 0.0
bot_sum = 0.0

# Prepare variables.
c_weight = d_length


# Calculate sums.
for i, number in enumerate(data, 1):
    top_sum += number * c_weight
    bot_sum += i
    c_weight -= 1

awma = top_sum / bot_sum

print('%s : %s = %s') % (top_sum, d_length, awma)


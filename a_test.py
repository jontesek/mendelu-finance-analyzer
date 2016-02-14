
# <source>_<delay>_{accuracy,precision_avg,recall_avg,
# precision_pos,precision_neg,precision_neu,recall_pos,recall_neg,recall_neu
sources = ['fb_comment', 'fb_post', 'twitter', 'yahoo']
metrics = ['accuracy','precision_avg','recall_avg',
'precision_pos','precision_neg','precision_neu','recall_pos','recall_neg','recall_neu']

header = []

for source in sorted(sources):
    for delay in [-1, 1, 2, 3]:
        for m in metrics:
            item = '%s_%d_%s' % (source, delay, m)
            header.append(item)

print header

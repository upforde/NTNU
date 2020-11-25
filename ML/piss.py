import sys

def precision(spamtospam, hamtospam):
    return spamtospam / (spamtospam+hamtospam)

def recall(spamtospam, spamtoham):
    return spamtospam / (spamtospam + spamtoham)

def fscore(precision, recall):
    return 2*precision*recall / (precision+recall)

def accuracy(spamtospam, hamtoham, spamtoham, hamtospam):
    return (spamtospam + hamtoham) / (spamtospam + hamtoham + spamtoham + hamtospam)

hamtoham = int(sys.argv[1])
hamtospam = int(sys.argv[2])
spamtoham = int(sys.argv[3])
spamtospam = int(sys.argv[4])

print("\metrix{%.2f}{%.2f}{%.2f}{%.2f}" % (precision(spamtospam, hamtospam), recall(spamtospam, spamtoham), fscore(precision(spamtospam, hamtospam), recall(spamtospam, spamtoham)), accuracy(spamtospam, hamtoham, spamtoham, hamtospam )))
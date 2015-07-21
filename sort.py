import csv


f = open('items.csv','rb')
spamreader = f.readlines()

with open('result.csv', 'wb') as csvfile:
    for i in sorted(spamreader):
        spamwriter = csv.writer(csvfile)
        spamwriter.writerow(i.replace('\n','').replace('\r','').split(','))

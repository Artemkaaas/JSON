from URLRepute.source import URLSource
import pymongo
import csv
import urllib
from tornado import gen
import motor
class PhishtankSource(URLSource):
    name = 'Phishtank'
    def __init__(self):
        URLSource.__init__(self)
        db = self.client.Phishtank
        cursor =db.Phishtank.find({ }, { 'site': 1, '_id': 0}).limit(10)
        for document in cursor:
            li=document.values()
            n=str(li).find('u')
            n2=str(li).rfind(')')
            li=str(li)[n+2:n2-2]
            self.urls[li]=True
        self.client.close()




    def update(self):
        URLSource.__init__(self)
        db=self.client.drop_database('Phishtank')
        db = self.client.Phishtank
        url = 'http://data.phishtank.com/data/online-valid.csv'
        urllib.urlretrieve(url, "phishtank.csv")
        csv_iter =  csv.reader(file('phishtank.csv'))
        next(csv_iter)
        for row in csv_iter:
            row=self.slice_http(row[1])
            db.OpenPhish.insert({'site':row})

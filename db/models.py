from mongoengine import *
connect(
    db='huyenha',
    host='',
    username='huyenha',
    password='HaHuyen@2017'
)


class Balance(Document):
    exchanger = StringField()
    usdt = FloatField()
    btc = FloatField()
    eth = FloatField()
    etc = FloatField()


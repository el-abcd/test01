
from qifparse.parser import QifParser

# install the patched version:
#  pip install ../qifparse/dist/qifparser-0.7.tar.gz
#  Which is from here:  https://github.com/el-abcd/qifparse
#  and built with "python setup.py sdist"

filename = '/Users/elee/temp/QDATA_20061105_lineEndFix.QIF'
with open(filename) as f:
    print(f.readline())

qif = QifParser.parse(file(filename))

a = qif.get_accounts()
#(<qifparse.qif.Account object at 0x16148d0>, <qifparse.qif.Account object at 0x1614850>)
#qif.accounts[0].name
#'My Cash'
b = qif.get_categories()
#(<qifparse.qif.Category object at 0x15b3d10>, <qifparse.qif.Category object at 0x15b3450>)
#qif.accounts[0].get_transactions()
c = qif.get_transactions()
#(<Transaction units=-6.5>, <Transaction units=-6.0>)
str(qif)

c2 = 0
for cnt, i in enumerate(c[0]):
    if 'm_LV_7216Buglehorn_Rms-PHH_1108' in i.payee:
        print( i.payee )
        print("################### {}".format(c2))
        c2 += 1
        print(i)

print cnt
print c2
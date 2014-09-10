from boto.mws.connection import MWSConnection
import sys, getopt

def main(argv):
MarketPlaceID = 'a'
Merchant = 'a'
AccessKeyID = 'a'
SecretKey = 'a'

program_name = sys.argv[0]
MarketPlaceID = sys.argv[1]
Merchant = sys.argv[2]
AccessKeyID = sys.argv[3]
SecretKey = sys.argv[4]

print 'MarketplaceID is ', MarketPlaceID
print 'Merchant is ', Merchant
print 'AccessKey is ', AccessKeyID
print 'Secret key is ', SecretKey
conn = MWSConnection(AccessKeyID,SecretKey)

conn.SellerId = Merchant
conn.Merchant = Merchant
conn.MarketplaceId = MarketPlaceID


myId = '1432456045'

# sample one
conn.get_report(ReportId=myId)

# sample two
conn.get_report(myId)

# sample three
conn.get_report(myId,)

# sample four
conn.get_report(1432456045)

# sample five
conn.get_report('1432456045')


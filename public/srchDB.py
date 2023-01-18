import pymongo
import sys
import datetime
import re
import pytz

class ConnDB():
    def __init__(self) -> None:
        uri = "mongodb+srv://hackathon2022.vpsksno.mongodb.net/?authSource=%24external&authMechanism=MONGODB-X509&retryWrites=true&w=majority"
        client = pymongo.MongoClient(uri,
                            tls=True,
                            tlsCertificateKeyFile='./certification.pem',
                            )
        self.db = client['hackathon2022']
        self.col = self.db['AlertStamp']

    def showAll(self):
        rlt=[]
        for i in self.col.find():
            rlt.append(i)
        return rlt


def imgStrParser(bs64Str):
    if(bs64Str != 'None' and str(bs64Str) !="b''"):
        return f"<img src='data:image/png;base64, {str(bs64Str)[2:-1]}' alt='image error' />"
    else:
        return ""

def msgStrParser(msg):
    return "<p>"+msg+"</p>"



def printPhp(rlt):
    print('<div class="box" data-aos="fade-up">')
    print('<div class="inboxl"><h2>Detail</h2></div>')
    print('<div class="inboxr"><h2>Image<h2></div>')
    print('</div>')

    for r in reversed(rlt):
        print('<div class="box" data-aos="fade-up">')
        print('<div class="inboxl">')
        print(msgStrParser(r['msg']))
        print(msgStrParser('Time: '+r['time']))
        print(msgStrParser('IP: '+r['ip']))
        print('</div>')
        
        print('<div class="inboxr">')
        print(imgStrParser(r['img']))
        print('</div>')
        print('</div>')


def searchDB(dur,uni):
    db = ConnDB()
    uniDic={'month': 259200, 'day': 86400, 'hr': 3600, 'mins': 60}

    currtime= datetime.datetime.now(pytz.timezone('Asia/Taipei')).strftime("%Y/%m/%d %H:%M:%S")
    currtime = datetime.datetime.strptime(currtime, "%Y/%m/%d %H:%M:%S")
    rlt=db.showAll()
    rtn=[]
    for r in rlt:
        rtime = datetime.datetime.strptime(r['time'], "%Y/%m/%d %H:%M:%S")
        tdiff = currtime - rtime
        # print(f"{r['time']} {tdiff.seconds}<br>")
        if(tdiff.seconds < uniDic[uni]*dur):
            rtn.append(r)
    return rtn



if(len(sys.argv)<=2):
    exit(0)
else:
    rlt=searchDB(int(sys.argv[2]), sys.argv[3])
    printPhp(rlt)


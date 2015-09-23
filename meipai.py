import json
import urllib2,cookielib
from BeautifulSoup import BeautifulSoup
import sys
import MySQLdb

reload(sys)
sys.setdefaultencoding( "utf-8" )
db = MySQLdb.connect(host="128.199.99.99",  # your host, usually localhost
                     user="",  # your username
                     passwd="",  # your password
                     db="meipai",
                     charset='utf8',
                     use_unicode=True)

cursor = db.cursor()

hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

url = "http://www.meipai.com/media/"

start = 2133694
end   = 100000010

for i in range(start,end+1):


    req = urllib2.Request(url + str(i), headers=hdr)

    try:
        page = urllib2.urlopen(req)
    except:
        try:
            page = urllib2.urlopen(req)
        except urllib2.HTTPError, e:
            print e.fp.read()
    try:
        content = page.read()

    except:
        continue





    print "------------" + str(i) + "-------------"

    Soup = BeautifulSoup
    soup = Soup(content)
    try:
        text = soup.find("div", { "class" : "detail-r pr" })
        author = text.find('a')['href'].replace("/user/", "")

    except:
        continue

    try:
        video = soup.find("div", { "id" : "detailVideo" })['data-video']
    except:
        video = ''

    try:
        img = soup.find("div", { "id" : "detailVideo" })
        img = img.find('img')['src']
    except:
        img = ''
    try:
        description = soup.find("div", { "class" : "detail-description br" }).getText()
    except:
        description = ''

    try:
        time = '20'+soup.find("div", { "class" : "detail-time pa" }).getText().replace("-", "")
    except:
        time = ''



    print img

    try:

        cursor.execute(
            'INSERT INTO videos(title, url, author_id, source_id, `date`,image)VALUES(%s,%s,%s,%s,%s,%s,%s)',
            (description, video, author, i, time, img))
        db.commit()

        print("inserted " + str(i))
    except MySQLdb.Error as err:
        print("Something went wrong: {}".format(err))
        cursor.close()
        cursor = db.cursor()


cursor.close()
db.close()
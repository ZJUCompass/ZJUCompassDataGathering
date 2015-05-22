# -*- coding:utf-8 -*-
"""
DESP
	crawl a teacher list of all teachers
OUTPUT
	teacher_list.txt:each row includes teacher_id,name,department,detail_url
"""
from urllib import urlopen
from bs4 import BeautifulSoup
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

if __name__ == "__main__":

        alpha_list = []
        for i in range(26):
            alpha_list.append(chr(ord("A")+i))
        
        f = open("data/teacher_list.txt","w")
        for alpha in alpha_list:
            #for alpha in ["Z"]:
            url = "http://mypage.zju.edu.cn/spell-" + alpha + ".html?size=10000&sort="
            print url
            html_doc = urlopen(url).read()
            soup = BeautifulSoup(html_doc,"html5lib",fromEncoding="GB2312")
            tables = soup.find_all("table")
            
            for table in tables:
                if table["width"] == "720" and table["border"] == "0":
                    trs = table.find_all("tr") 
                    for tr in trs:
                        if tr.get("style","") == "line-height:18px;":
                            tds = tr.find_all("td")
                            name = unicode(tds[0].text).encode('utf-8')
                            department = unicode(tds[2].text).encode('utf-8')
                            url = tds[3].a["href"] if tds[3].a["class"][0] == u"zhishi" else ""
                            f.write(name + "\t" + department + "\t" + url + "\n")        
        f.close()
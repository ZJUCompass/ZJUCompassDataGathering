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

    f = open("data/department_list.txt","w")
    for line in open("data/department.txt","r").readlines():
        terms = line.strip().split("\t")
        department = terms[0]
        url = terms[1]
        url = url + "?size=10000"
        print url
        
        html_doc = urlopen(url).read()
        soup = BeautifulSoup(html_doc,"html5lib",from_encoding="GB2312")
        tables = soup.find_all("table")
        
        count = 0   
        for table in tables:
            if table["width"] == "720" and table["border"] == "0":
                trs = table.find_all("tr") 
                for tr in trs:
                    if tr.get("style","") == "line-height:18px;":
                        tds = tr.find_all("td")
                        name = unicode(tds[0].text).encode('utf-8')
                        f.write(department + "\t" + name + "\n")
                        count += 1
        print department.encode("gbk"),count
    f.close()
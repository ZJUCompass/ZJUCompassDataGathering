# -*- coding:utf-8 -*-
from urllib import urlopen
import urllib
from bs4 import BeautifulSoup
from collections import defaultdict
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

def load_teacher_dict():
    teacher_dict = {}
    for line in open("data/teacher_list.txt","r").readlines():
        terms = line.split("\t")
        if len(terms) != 4:
            print "ERROR LINE:",line
            continue
        teacher_id = terms[0].strip()
        name = terms[1].strip()
        department = terms[2].strip()
        url = terms[3].strip()
        teacher_dict[teacher_id] = defaultdict(lambda:"")
        teacher_dict[teacher_id]["name"] = name
        teacher_dict[teacher_id]["department"] = department
        teacher_dict[teacher_id]["url"] = url


        
    return teacher_dict


def parse_url(teacher_id, url):
    global teacher_dict
    html_doc = urlopen(url).read()
    soup = BeautifulSoup(html_doc,"html5lib")

    imgs_dir = "data/teacher_imgs/"


    name = ""
    department = ""
    title = ""
    phone = ""
    email = ""
    field = ""
    img_url = ""

    uls = soup.find_all("ul")
    for ul in uls:
        if ul.get("style","") == "	list-style-type:none;margin: 0px;":
            lis = ul.find_all("li")
            for li in lis:
                text = li.text.encode("utf-8")

                if "姓名" in text:
                    name = text.split("：")[1]
                if "单位" in text:
                    department = text.split("：")[1]
                if "职称" in text:
                    title = text.split("：")[1]
    

    divs = soup.find_all("div", class_="mainItem")
    for div in divs:
        if div.a.text.encode("utf-8") == "联系方式":
            terms = div.div.text.split("\t")
            terms = [t for t in terms if t.strip()]
            for term in terms:
                if "电话" in term:
                    phone = term.split("：")[1]
                if "电子信箱" in term:
                    email = term.split("：")[1]
        if div.a.text.encode("utf-8") == "工作研究领域":
            field = div.div.text.strip()        

    imgs = soup.find_all("img")
    for img in imgs:
        ori_src = img.get("src","")
        if "teacherimage" in ori_src:
            img_url = "http://mypage.zju.edu.cn/" + ori_src
            print img_url
            data = urllib.urlretrieve(img_url,imgs_dir + teacher_id + ".jpg")
            break

    """
    f.write("name:" + name + "\n")
    f.write("department:" + department + "\n")
    f.write("title:" + title + "\n")
    f.write("phone:" + phone + "\n")
    f.write("email:" + email + "\n")
    f.write("field:" + field + "\n")
    """

    name = name.replace("\t"," ")
    name = name.replace("\n"," ")
    department = department.replace("\t"," ")
    department = department.replace("\n"," ")
    title = title.replace("\t"," ")
    title = title.replace("\n"," ")
    phone = phone.replace("\t"," ")
    phone = phone.replace("\n"," ")
    email = email.replace("\t"," ")
    email = email.replace("\n"," ")
    field = field.replace("\t"," ")
    field = field.replace("\n"," ")

    teacher_dict[teacher_id]['name'] = name
    teacher_dict[teacher_id]['department'] = department
    teacher_dict[teacher_id]['title'] = title
    teacher_dict[teacher_id]['phone'] = phone
    teacher_dict[teacher_id]['email'] = email
    teacher_dict[teacher_id]['field'] = field


def write_dict(teacher_dict):
    f = open("data/teacher_info.txt","w")
    for teacher_id in teacher_dict:
        f.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\n"%(teacher_id,teacher_dict[teacher_id]['name'],teacher_dict[teacher_id]['department'],teacher_dict[teacher_id]['title'],teacher_dict[teacher_id]['phone'],teacher_dict[teacher_id]['email'],teacher_dict[teacher_id]['field']))
    f.close()

if __name__ == "__main__":

    teacher_dict = load_teacher_dict()
    try:
        for teacher_id in teacher_dict:
            print teacher_id,teacher_dict[teacher_id]["name"]
            detail_url = teacher_dict[teacher_id]["url"]
            if detail_url:
                parse_url(teacher_id, detail_url)
    except Exception,e:
        print e
            
    write_dict(teacher_dict)
    """
    f = open("data/teacher_info.txt","w")
    url = "http://mypage.zju.edu.cn/ctz"
    parse_url("1",url)
    f.close()
    """


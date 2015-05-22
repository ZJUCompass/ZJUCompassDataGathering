# -*- coding:utf-8 -*-
import sys,os
from collections import defaultdict
import shutil
from PIL import Image
import urllib
reload(sys)
sys.setdefaultencoding("utf-8")

if __name__ == "__main__":

    teacher_info = defaultdict(lambda:defaultdict(lambda:""))
    name_id_dict = {}
    
    count = 0
    for line in open(r"data\teacher_info.txt","r").readlines():
        terms = line.split("\t")
        if len(terms) !=  7:
            print "ERROR LINE:" + line
            continue
        tmp_dict = defaultdict(lambda:"")
        teacher_id = terms[0].strip()
        tmp_dict["name"] = terms[1].strip()
        tmp_dict["department"] = terms[2].strip()
        tmp_dict["title"] = terms[3].strip()
        tmp_dict["phone"] = terms[4].strip()
        tmp_dict["email"] = terms[5].strip()
        tmp_dict["field"] = terms[6].strip()
        
        teacher_info[teacher_id] = tmp_dict
        name_id_dict[terms[1]] = teacher_id
        count += 1
    print count
    
    
    count = 0
    for line in open(r"data\address_info.csv","r").readlines():
        terms = line.split(",")
        if len(terms) != 8:
            print "ERROR LINE:" + line
        name = terms[0].strip()
        if name in name_id_dict:
            teacher_id = name_id_dict[name]
            teacher_info[teacher_id]["title"] = terms[1].strip()
            teacher_info[teacher_id]["email"] = terms[2].strip()
            teacher_info[teacher_id]["phone"] = terms[3].strip()
            teacher_info[teacher_id]["room"] = terms[4].strip()
            teacher_info[teacher_id]["building"] = terms[7].strip()
            count += 1
    print count
            
    cs_teachers = []
    count = 0
    for line in open(r"data\cs_teacher_info.csv").readlines():
        terms = line.split(",")
        if len(terms) != 10:
            print "ERROR LINE:" + line + str(len(terms))
            continue
        name = terms[1].strip()
        if name in name_id_dict:
            teacher_id = name_id_dict[name]
            teacher_info[teacher_id]["title"] = terms[3].strip()
            teacher_info[teacher_id]["email"] = terms[7].strip()
            teacher_info[teacher_id]["phone"] = terms[6].strip()
            cs_teachers.append(teacher_id)
            """
            urllib.urlretrieve("http://zudc.zju.edu.cn/tsc/dc/tsc/controller/photo.do?pid="+terms[0].strip(),"data/teacher_imgs/" + teacher_id + ".jpg")          
            
            pil_im = Image.open("data/teacher_imgs/" + teacher_id + ".jpg")
            pil_im = pil_im.convert('RGB')
            width,length = pil_im.size
            min_len = min(width,length)
            if min_len == width:
                new_length = int(length * 128.0 / width)
                new_width = 128 
            else:
                new_width = int(width * 128.0 / length)
                new_length = 128
            pil_im = pil_im.resize((new_width,new_length))
            pil_im.save("data\\cs_teachers\\teacher_imgs\\" + teacher_id + ".png")            
            """


            count += 1
    print count


    for k in teacher_info.keys():
        for term in teacher_info[k].keys():
            if not teacher_info[k][term].strip():
                del teacher_info[k][term]
        if len(teacher_info[k]) < 3:
            del teacher_info[k]
            
    f = open(r"data\finally_teacher_info.txt","w")
    sorted_list = sorted(teacher_info.keys())
    for k in sorted_list:
        f.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n"%(k, \
            teacher_info[k]["name"],teacher_info[k]["apartment"],teacher_info[k]["title"],teacher_info[k]["phone"], \
            teacher_info[k]["email"],teacher_info[k]["building"],teacher_info[k]["room"],teacher_info[k]["field"]))
    f.close()
	
    f = open(r"data\cs_teachers\teacher_info.txt","w")
    for k in cs_teachers:
        for t in teacher_info[k].keys():
            if not teacher_info[k][t].strip():
                teacher_info[k][t] = "null"
        f.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n"%(k, \
            teacher_info[k]["name"],teacher_info[k]["apartment"],teacher_info[k]["title"],teacher_info[k]["phone"], \
            teacher_info[k]["email"],teacher_info[k]["building"],teacher_info[k]["room"],teacher_info[k]["field"]))
        """
        if os.path.isfile("data\\resized_teacher_imgs\\" + k + ".jpg"):
			Image.open("data\\resized_teacher_imgs\\" + k + ".jpg").save("data\\cs_teachers\\teacher_imgs\\" + k + ".png")
            #shutil.copyfile("data\\resized_teacher_imgs\\" + k + ".jpg", "data\\cs_teachers\\teacher_imgs\\" + k + ".jpg")
        """
    f.close()
    
    
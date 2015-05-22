# -*- coding:utf-8 -*-
"""
DESP
	crawl data from bsdt.zju.edu.cn
INPUT
	trans_list.txt: manually copy from the website,where each row include a trans_id and a name
OUTPUT
	affair_info.csv: crawl detail info of each row in the trans_list.txt
	
"""
from urllib import urlopen
from bs4 import BeautifulSoup
import sys,os
reload(sys)
sys.setdefaultencoding("utf-8")


if __name__ == "__main__":

	col_names = []

	id_list = []
	for line in open("trans_list.txt").readlines():
		terms = line.strip().split("\t")
		trans_id = terms[0].strip()
		id_list.append(trans_id)

	trans_list = {}
	for trans_id in id_list:
		#for trans_id in ["131000QR001"]:
		try:
			detail_url = "http://bsdt.zju.edu.cn/zftal-web/web/lm_sxms.html?transaction_id=" + trans_id
			html_doc = urlopen(detail_url).read()
			soup = BeautifulSoup(html_doc)

			table = soup.find_all("table")[0]
			trs = table.find_all("tr")
			tmp_dict = {}
			for tr in trs:
				th = unicode(tr.th.string).encode('utf-8').strip()
				try:
					if tr.td.find("a"):
						td = unicode(tr.td.a.text).encode('utf-8').strip()
					else:
						td = unicode(tr.td.text).encode('utf-8').strip()
				except Exception,e:
					print e

				td = td.replace("\t"," ")
				td = td.replace("\n"," ")
				td = td.replace("\r","")

				if th not in col_names:
					col_names.append(th)
				if not td or td == "None":
					td = "无"
				#print td.encode("GBK")
				tmp_dict[th] = td
			tmp_dict["detail_url"] = detail_url
			trans_list[trans_id] = tmp_dict
		except Exception,e:
			print "Failed to parse url:" + detail_url
			print e

	col_names.append("detail_url")
	sorted_list=[]
	for line in open("sorted_list.txt","r").readlines():
		sorted_list.append(line.strip().split("\t")[0])

	f = open("affair_info.csv", "w")
	f.write("\t".join(col_names) + "\n")
	for id in sorted_list:
		if id not in trans_list:
			continue
		trans = trans_list[id]
		outline = []
		for name in col_names:
			outline.append(trans.get(name,"None"))
		f.write("\t".join(outline) + "\n")
	f.close()
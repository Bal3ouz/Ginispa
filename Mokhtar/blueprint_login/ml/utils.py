import pandas as pd
from flask import url_for
import os
def create_table(name):
	#data=pd.read_csv("./current_data.csv",encoding="utf-8")
	data=pd.read_csv("./"+name+".csv",encoding="utf-8")
	
	return data


def change_current_table(data):
	data.to_csv("./current_data.csv",index=True)


def create_instance():
	#data=pd.read_csv(url_for("static",filename="allData.csv"),encoding="utf-8")
	#print(os.curdir)
	data=pd.read_csv("./allData.csv",encoding="utf-8")
	data.to_csv("./current_data.csv",index=True)
	empty=pd.DataFrame(columns=data.columns)
	empty.to_csv("./save_data.csv",index=False)


def save_table(data):
	save=pd.read_csv("./save_data.csv",encoding="utf-8")
	#save.reset_index(drop=True, inplace=True)
	#data.reset_index(drop=True, inplace=True)
	save=pd.concat([save,data],axis=0,join="inner")
	save.index=range(0,save.shape[0])
	save.to_csv("./save_data.csv",index=False)


def save_instance():
	"""
	working on still not ready
	"""


	


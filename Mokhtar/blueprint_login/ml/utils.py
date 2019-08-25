import pandas as pd
from flask import url_for
import os
def create_table():
	#data=pd.read_csv(url_for("static",filename="allData.csv"),encoding="utf-8")
	#print(os.curdir)
	data=pd.read_csv("./allData.csv",encoding="utf-8")
	
	return data
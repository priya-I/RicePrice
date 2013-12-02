import csv,os,re
import sklearn
import sqlite3


data_folder="../data/"

def combine_files():
	outfile=os.path.join(data_folder,"all_prices.csv")
	print outfile
	title=['State','District','Market','Commodity','Variety','Date','MIN Price','MAX Price','MODAL Price']
	conn=sqlite3.connect('rice.db')
	c=conn.cursor()
	#c.execute('''CREATE TABLE prices (State,District,Market,Commodity,Variety,Date,MINPrice,MAXPrice,MODALPrice)''')	
	files=os.listdir(data_folder)
	i=0
	for f in files:
		f=os.path.join(data_folder,f)
		with open(f,'rb') as csvfile:
			next(csvfile)
			readr=csv.reader(csvfile)
			for row in readr:
				conn.execute('''insert into prices values '''+str(tuple(row)))
			i+=1
			print "done",i
	conn.commit()
	conn.close()
	
if __name__=='__main__':
	combine_files()
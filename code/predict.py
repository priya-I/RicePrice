import csv,os,re
import sklearn
import sqlite3
from datetime import datetime
import time
import traceback
from itertools import combinations, permutations
import nltk,random
import matplotlib.pyplot as plt
import StringIO,Image
from matplotlib.font_manager import FontProperties
import pandas as pd

data_folder="../data/"

def combine_files():
    title=['ID','State','District','Market','Commodity','Variety','Pdate','MIN Price','MAX Price','MODAL Price','Category','PDay','PMonth','PYear']
    conn=sqlite3.connect('rice.db')
    c=conn.cursor()
    
    files=os.listdir(data_folder)
    i=0
    for f in files:
        f=os.path.join(data_folder,f)
        with open(f,'rU') as csvfile:
            next(csvfile)
            readr=csv.reader(csvfile)
            for row in readr:
                if row[5]=='Date':
                    continue
                try:
                    pdate=time.strptime(row[5],"%m/%d/%Y")
                except ValueError:
                    try:
                        pdate=time.strptime(row[5],"%m/%d/%y")
                    except ValueError:
                        row[5]="0"+row[5]
                        pdate=time.strptime(row[5],"%m/%d/%y")
                month=pdate.tm_mon
                year=pdate.tm_year
                day=pdate.tm_mday
                row.extend([day,month,year])
                print row
                query='''insert into prices ('State','District','Market','Commodity','Variety','PDate','MINPrice','MAXPrice','MODALPrice','Pday','PMonth','PYear')  values ''' +str(tuple(row))
                try:
                    conn.execute(query)
                except sqlite3.OperationalError:
                    print f, row
                    print traceback.format_exc()
                    continue    

            i+=1
            print "done",i
    conn.commit()
    conn.close()
    
def groupCats():
    con=sqlite3.connect('rice.db')
    c=con.cursor()
    varieties=[]
    count=0
    rows=c.execute('select DISTINCT(Variety) from prices');
    for r in rows:
        varieties.append(str(r[0]))
    print varieties
    pairs=combinations(varieties[:5],2)
    for pair in pairs:
        print pair
    con.close()

def find_categories(varieties):
    pairs=combinations(varieties,2)
    parents=[]
    for pair in pairs:
        #r=ratio(pair[0],pair[1])
        #if(r>0.5):
        if(True):
            #print pair, r
            word1=nltk.word_tokenize(pair[0])
            word2=nltk.word_tokenize(pair[1])
            splits=list(set(word1).intersection(set(word2)))
            parent=[]
            for s in splits:
                if len(s)>1 and s!='':
                    parent.append(s)
            parents.append(" ".join(parent))
            
    return parents



def remove_dups(cats):
    parents=[]
    p1=list(set(cats))
    pairs=combinations(p1[1:],2)
    for pair in pairs:
        if pair[0].lower() in pair[1].lower():
            try:
                parents.append(pair[0])
                p1.remove(pair[1])
            except:
                continue
        elif pair[1].lower() in pair[0].lower():
            try:
                parents.append(pair[1])
                p1.remove(pair[0])
            except:
                continue
    return p1


def update_cat():
    categories={}
    #varieties=['1009 Kar', 'ADT 39', 'AP Raw Rice 5293', 'AP Raw Rice Baptla Ponni', 'AP Raw Rice PLR Soma', 'AP Raw Rice SilkyRaw', 'AP Raw Rice-1001', 'AP Raw-Rice Sona Ponni', 'Alur Sanna', 'Ambemohor Basmati', 'Amira Mogra Basmati', 'Amira Tibar Basmati', 'Amire Full Basmati', 'Amras Non Basmati', 'Annapoorna', 'Arcot Kichikdi', 'Arti Mashuri', 'B P T', 'BT Sona', 'Balesuli', 'Bangar Kaddi', 'Bangarkhovi', 'Bangarsanna', 'Bantwal', 'Basamti Dawat', 'Basmati (Rose)', 'Basmati Car', 'Basmati Charmi', 'Basmati Dawat Roz-(20KG)', 'Basmati Golden Sela New', 'Basmati Golden Sela Old', 'Basmati Haryana Sela(New)', 'Basmati Mogra (Raw/New)', 'Basmati Mogra (Raw/Old)', 'Basmati Paddy', 'Basmati Silky Kohinoor', 'Basmati Super Kohinoor', 'Basmati Trophy', 'Basmati U.P. (New)', 'Basmati U.P. (Old)', 'Basmati-370', 'Basmati-385', 'Basmati-386', 'Basmatibar (Raw/New)', 'Basmatibar (Raw/Old)', 'Basmatidubar Raw/New', 'Basmatidubar Raw/Old', 'Basumathi', 'Bellary Sanna', 'Boiled Rice', 'Broken Rice', 'CO 36', 'CO-43 (Medium) Boiled', 'CR 1009 (Coarse) Boiled', 'Chinoor', 'Chintamani Sanna', 'Coarse', 'Coarse (I.R.20)', 'Culture Ponni1', 'Culture Ponni2', 'Dappa', 'Dawal Full Basmati', 'Dawat', 'Dhoon Full Basmati', 'Doon Kinki Basmati', 'Dosa Rice', 'Duplicate Basmati', 'Durbar Basmati', 'EMR Boiled', 'Export Parmal', 'FCI Non Basmati', 'FCI Parmal', 'Farm Kaddi', 'Fine', 'Fine(Basmati)', 'Govt. Quality', 'Gowrisanna', 'H.Y.V.', 'HMT Fine Raw', 'HMT Sona Best', 'HMT Sona Medium', 'Hamsa St.', 'Hansa', 'Hassan Dappa', 'Hmt Rice-Non Basmati', 'III', 'IR 20', 'IR 20 Fine Raw', 'IR 20 Medium Boiled', 'IR 50', 'IR-8', 'IR-8 Raw (New)', 'IR-8 Raw (Old)', 'IR-8 Sela (Old)', 'IR-8 Wand', 'IR20 Parboiled', 'Intan', 'Jaya', 'Jhilli Medium', 'Kachha Basmati', 'Kaddi', 'Kalimuch', 'Kapila Sanna', 'Kattasambar', 'Kesari (Coorg)', 'Kichudi', 'Kolam-Non Basmati', 'Lashkari', 'Long Bold', 'Madhu (MR 136)', 'Mandya-vani', 'Manila', 'Masoori-Non Basmti', 'Masuri', 'Mataa Parboiled', 'Medium', 'Milled', 'Mnadyavani', 'Motta (Coarse) Boiled', 'Mull Bhatte', 'Naya', 'Nellore Sanna', 'Non Basmati Kalimunch', 'Original Basmati', 'Other', 'PR-103', 'PR-106', 'PR-108', 'PR-111', 'Padma', 'Parimal (New)', 'Parimal (Old)', 'Parmal', 'Parmal (Paddy)', 'Parmal Raw (New)', 'Parmal Sela (Old)', 'Parmal Selas (New)', 'Parmal Wand', 'Ponni', 'Ponni (Fine) Boiled', 'Ponni Fine Raw', 'Ponni parboiled', 'Popular Basmati', 'Punjab Parmal Non Basmati', 'Pusa Basmati (Paddy)', 'Pusa Basmati Raw (New)', 'Pusa Basmati Raw (Old)', 'Pusa Basmati Sela (New)', 'Pusa Basmati Sela (Old)', 'Rajahamsa', 'Rasi', 'Ratnachudi (718 5-749)', 'Rice Floor', 'Sadharan', 'Sambar', 'Sanna Bhatta', 'Sanna Honsu', 'Sarbati Raw', 'Sarbati Raw (New)', 'Sarbati Raw (Old)', 'Sarbati Sela (New)', 'Sarbati Sela (Old)', 'Shakti', 'Sharbati (Paddy)', 'Sona', 'Sona Boiled', 'Sona Coarse', 'Sona Fine', 'Sona Mansoori Non Basmati', 'Sona Medium', 'Sona Raw New', 'Sona Raw Old', 'Sujatha (B. T)', 'Super Fine', 'Suvarna Best', 'Suvarna Medium', 'Swadras Non Basmati', 'Tallahamsa (Bilihamsa)', 'Tericot Sela', 'Variety', 'Vijaya', 'White Car', 'White Parboiled', 'Zeeraga Samba Rawrice', 'andra Sanna', 'anekombu Sanna', 'anekowe']
    cats=find_categories(varieties)
    parents=remove_dups(list(set(cats)))
    parents.remove('')
    #print parents
    for v in varieties: 
            for p in parents:
                if p in v or p==v: 
                    try:
                        categories[p].append(v)
                        varieties.remove(v)
                    except ValueError:
                        continue
                    except:
                        categories[p]=[v]
    print categories


    con=sqlite3.connect('rice.db')
    c=con.cursor()
    categories={'Suvarna': ['Suvarna Medium'], 'Sela': ['Basmati Golden Sela New', 'Basmati Haryana Sela(New)', 'IR-8 Sela (Old)', 'Parmal Selas (New)', 'Pusa Basmati Sela (Old)', 'Sarbati Sela (Old)', 'Tericot Sela'], 'Basmati': ['Ambemohor Basmati', 'Amira Mogra Basmati', 'Amire Full Basmati', 'Basmati (Rose)', 'Basmati Charmi', 'Basmati Golden Sela New', 'Basmati Haryana Sela(New)', 'Basmati Mogra (Raw/Old)', 'Basmati Silky Kohinoor', 'Basmati Trophy', 'Basmati U.P. (Old)', 'Basmati-385', 'Basmatibar (Raw/New)', 'Basmatidubar Raw/New', 'Dawal Full Basmati', 'Dhoon Full Basmati', 'Durbar Basmati', 'FCI Non Basmati', 'Fine(Basmati)', 'Hmt Rice-Non Basmati', 'Kolam-Non Basmati', 'Original Basmati', 'Popular Basmati', 'Pusa Basmati (Paddy)', 'Pusa Basmati Raw (Old)', 'Pusa Basmati Sela (Old)'], 'Coarse': ['Coarse (I.R.20)', 'Motta (Coarse) Boiled'], 'New': ['Basmati Golden Sela New', 'Basmati Haryana Sela(New)', 'Basmatibar (Raw/New)', 'Basmatidubar Raw/New', 'IR-8 Raw (New)', 'Parimal (New)', 'Parmal Raw (New)', 'Parmal Selas (New)'], 'White': ['White Car', 'White Parboiled'], 'Rice': ['AP Raw Rice 5293', 'AP Raw Rice Baptla Ponni', 'AP Raw Rice SilkyRaw', 'AP Raw-Rice Sona Ponni', 'Boiled Rice', 'Dosa Rice', 'Hmt Rice-Non Basmati', 'Rice Floor'], 'Paddy': ['Pusa Basmati (Paddy)', 'Sharbati (Paddy)'], 'Sona': ['AP Raw-Rice Sona Ponni', 'BT Sona', 'HMT Sona Medium', 'Sona Boiled', 'Sona Fine', 'Sona Medium', 'Sona Raw Old'], 'Boiled': ['Boiled Rice', 'CO-43 (Medium) Boiled', 'Motta (Coarse) Boiled', 'Sona Boiled'], 'Raw': ['AP Raw Rice 5293', 'AP Raw Rice Baptla Ponni', 'AP Raw Rice SilkyRaw', 'AP Raw-Rice Sona Ponni', 'Basmati Mogra (Raw/Old)', 'Basmatibar (Raw/New)', 'Basmatidubar Raw/New', 'HMT Fine Raw', 'IR 20 Fine Raw', 'IR-8 Raw (New)', 'Parmal Raw (New)', 'Ponni Fine Raw', 'Pusa Basmati Raw (Old)', 'Sarbati Raw', 'Sarbati Raw (Old)', 'Sona Raw Old'], 'HMT': ['HMT Fine Raw', 'HMT Sona Medium'], 'Parimal': ['Parimal (New)'], 'Car': ['White Car'], 'FCI': ['FCI Non Basmati'], 'Super': ['Super Fine'], 'Ponni': ['AP Raw Rice Baptla Ponni', 'AP Raw-Rice Sona Ponni', 'Culture Ponni1', 'Ponni', 'Ponni Fine Raw'], 'IR': ['IR 20', 'IR 20 Fine Raw', 'IR 50', 'IR-8 Raw (New)', 'IR-8 Sela (Old)', 'IR20 Parboiled'], 'AP': ['AP Raw Rice 5293', 'AP Raw Rice Baptla Ponni', 'AP Raw Rice SilkyRaw', 'AP Raw-Rice Sona Ponni'], 'Medium': ['CO-43 (Medium) Boiled', 'HMT Sona Medium', 'Jhilli Medium', 'Medium', 'Sona Medium', 'Suvarna Medium'], 'Sarbati': ['Sarbati Raw', 'Sarbati Raw (Old)', 'Sarbati Sela (Old)'], 'Dawat': ['Basamti Dawat'], 'Old': ['Basmati Mogra (Raw/Old)', 'Basmati U.P. (Old)', 'IR-8 Sela (Old)', 'Pusa Basmati Raw (Old)', 'Pusa Basmati Sela (Old)', 'Sarbati Raw (Old)', 'Sarbati Sela (Old)', 'Sona Raw Old'], 'Parmal': ['Export Parmal', 'Parmal', 'Parmal Raw (New)', 'Parmal Selas (New)'], 'Sanna': ['Bellary Sanna', 'Chintamani Sanna', 'Kapila Sanna', 'Nellore Sanna', 'Sanna Bhatta', 'andra Sanna'], 'Culture': ['Culture Ponni1'], 'Kaddi': ['Bangar Kaddi', 'Farm Kaddi', 'Kaddi'], '1009': ['1009 Kar'], 'Fine': ['Fine(Basmati)', 'HMT Fine Raw', 'IR 20 Fine Raw', 'Ponni Fine Raw', 'Sona Fine', 'Super Fine']}
    min_id=1
    i=min_id
    max_id=910089
    while i<=max_id:
        id=(i,)
        res=c.execute("select Variety from prices where id=?",id)
        for row in res:
            var=str(row[0])
            print var
            for k,v in categories.items():
                if k in var:
                    print "found"
                    c.execute("update prices set category=? where id=?",(k,i))
            i+=1

    con.commit()
    con.close()

def create_colormap():
    con=sqlite3.connect('rice.db')
    c=con.cursor()
    colormap={}
    rows=c.execute("select Distinct State from prices")
    for row in rows:
        state=str(row[0])
        r=round(random.random(),2)
        b=round(random.random(),2)
        g=round(random.random(),2)
        colormap[state]=(r,g,b)
    con.close()
    return colormap

def create_plots(types=['Paddy','Basmati','Coarse'],year=2010):
    #Create visualization given a year. For creating visualization, the filters are going to be on the type of rice and the year. 
    fontp=FontProperties()
    fontp.set_size('small')
    con=sqlite3.connect('rice.db')
    c=con.cursor()
    colormap=create_colormap()
    #Filters: type and year
    #types=['Medium', 'Parmal', 'Basmati', 'Raw', 'Other', 'Coarse', 'Fine', 'Paddy']
    #types=['Paddy','Basmati','Coarse']
    if(len(types)==1):
        rows=1
        columns=1
    elif(len(types)%2==1):
        columns=2
        rows=len(types)/2+1
    else:
        columns=len(types)/2
        rows=2

    fig=plt.figure()

    for i in range(len(types)):
        fig.add_subplot(rows,columns,i)
    axes=[]
    for ax in fig.axes:
        ax.grid(True)
        axes.append(ax)
        #print ax
    
    #Getting the data from the tables
    i=0
    #months=[0,31,29,31,30,31,30,30,31,30,31,30,31]
    #monthsl=[0,31,28,31,30,31,30,30,31,30,31,30,31]
    for cat in types:
        stprice={}  
        '''months=pd.Series(months)
        prices=pd.Series(prices)'''
        #rows=c.execute("select State,Pday,PMonth,AVG(MinPrice) from prices where Pyear=? and Category=? and state=\"Karnataka\" group by Pday,PMonth,state ORDER BY PMonth,Pday",(year,cat))
        rows=c.execute("select State,PMonth,AVG(MinPrice) from prices where Pyear=? and Category=? group by PMonth,state ORDER BY PMonth",(year,cat))
        #print "select State,Pday,PMonth,AVG(MinPrice) from prices where Pyear="+year+" and Category="+cat+" group by Pday,PMonth,State" 
        check=rows.fetchone()
        #print check
        if check is not None:
            for row in rows:
                state=str(row[0])
                #day=str(row[1])
                month=int(str(row[1]))
                price=float(str(row[2]))
                '''temp=0
                if(int(year)%4==0):
                    for m in monthsl[1:month-1]:
                        temp+=m
                    day=int(day)+temp
                else:
                    for m in months[1:month-1]:
                        temp+=m
                    day=int(day)+temp
                price=float(str(row[3]))
                if day==1:
                    print row'''
                try:
                    stprice[state].append((month,price))
                    #stprice[state][1].append(price)
                except:
                    stprice[state]=[(month,price)]
                    #stprice[state].append([month])
                    #stprice[state].append([price])
                    
                '''months.append(month)
                prices.append(price)'''

            
            #stprices=pd.DataFrame({'months':months,'prices':prices})
            #stprices['months']=months
            #stprices['prices']=prices
            #print stprice
            labels=[]
            for k,v in stprice.items():
                #print k,v
                #print "\n"
                v=sorted(v)
                #print v
                months=[m[0] for m in v]
                prices=[p[1] for p in v]
                axes[i].plot(months,prices,color=colormap[k],label="state rice prices")
                labels.append(k)
            #axes[i].legend(tuple(labels),loc="lower right")
            axes[i].set_title(cat+" in the year "+year)
            if(i==0 or i==1):
                cols=3
            else:
                cols=4
            #axes[i].set_xlabel("Months")
            axes[i].legend(tuple(labels),loc="upper center",bbox_to_anchor=(0.5,-0.1),prop=fontp,fancybox=True, shadow=True, ncol=cols)
            i+=1
        else:
            print "Deleting axis",i
            #fig.delaxes(axes[i])
    con.close()
    plt.subplots_adjust(hspace=0.9,wspace=0.2,left=0.15)
    plt.xlabel('Months',fontsize=16,va="top",ha="center")
    plt.ylabel('Price',fontsize=16,ha="left")
    #plt.legend(tuple(labels),loc="center left",bbox_to_anchor=(1, 0.5),prop=fontp)

    #plt.show()
    '''imgdata=StringIO.StringIO()
    fig.save(imgdata,format='png')
    imgdata.seek(0)'''
    imgpath="./static/images/graph.png"
    #fig.set_size_inches(12,6)
    fig.savefig(imgpath)
    return imgpath

if __name__=='__main__':
    #combine_files()
    #groupCats()
    #find_categories()
    #update_cat()
    #create_colormap()
    create_plots(types,year)



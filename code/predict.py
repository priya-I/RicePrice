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


def combine_files():
    '''
    Helper method called in order to extract data from the csv files under the data folder and insert into the database 
    '''
    title=['ID','State','District','Market','Commodity','Variety','Pdate','MIN Price','MAX Price','MODAL Price','Category','PDay','PMonth','PYear']
    conn=sqlite3.connect('rice.db')
    c=conn.cursor()
    '''
    Please run this on sqlite3 before runnning the code
    CREATE TABLE "prices" (ID integer primary key autoincrement,
                                      State varchar(50),
                                      District varchar(50),
                                      Market varchar(50),
                                      Commodity varchar(50),
                                      Variety varchar(150),
                                      pdate DateTime,
                                      MINPrice INT,
                                      MAXPrice INT,
                                      MODALPrice INT,
                                      PDay varchar(2),
                                      PMonth varchar(2),
                                      PYear varchar(4),
                                      Category varchar(50));

    '''
    #Get all the files in the data folder
    files=os.listdir(data_folder)
    i=0
    #Looping through each of the csv files
    for f in files:
        f=os.path.join(data_folder,f)
        with open(f,'rU') as csvfile:
            #Skip the first line
            next(csvfile)
            readr=csv.reader(csvfile)
            for row in readr:
                #Some rows in some files have title text in them so adding this condition to avoid manual deletion
                if row[5]=='Date':
                    continue
                try:
                    #Extracting the date string in date format 
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
                #Inserting into the database
                query='''insert into prices ('State','District','Market','Commodity','Variety','PDate','MINPrice','MAXPrice','MODALPrice','Pday','PMonth','PYear')  values ''' +str(tuple(row))
                try:
                    conn.execute(query)
                except sqlite3.OperationalError:
                    print f, row
                    print traceback.format_exc()
                    continue    

            i+=1
    conn.close()
    
def groupCats():
    '''
    This method finds all the distinct varieties of rice present in the prices table.
    '''
    con=sqlite3.connect('rice.db')
    c=con.cursor()
    varieties=[]
    count=0
    rows=c.execute('select DISTINCT(Variety) from prices');
    for r in rows:
        varieties.append(str(r[0]))
    pairs=combinations(varieties[:5],2)
    for pair in pairs:
        print pair
    con.close()
    return varieties

def find_categories(varieties):
    '''
    This method clusters all the similar categories into several parent clusters based on their textual description
    '''
    #Find all combinations of distinct varieties of rice
    pairs=combinations(varieties,2)
    parents=[]
    for pair in pairs:
        if(True):
            word1=nltk.word_tokenize(pair[0])
            word2=nltk.word_tokenize(pair[1])
            #Find the intersecting words in both the varieties of rice
            splits=list(set(word1).intersection(set(word2)))
            parent=[]
            for s in splits:
                if len(s)>1 and s!='':
                    parent.append(s)
            parents.append(" ".join(parent))           
    return parents



def remove_dups(cats):
    '''
    This method removes all the redundant categories from the whole list and returns a list of parent categories
    '''
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


def update_cat(varieties):
    '''
    This method updates the prices table. There is a column named 'Category' that contains the parent category for each row. 
    This column gets updated by this method.
    '''
    categories={}
    cats=find_categories(varieties)
    parents=remove_dups(list(set(cats)))
    parents.remove('')
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
    '''
    Methods that creates a colormap based on the different states in the prices table
    '''
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
    '''
    Creates visualization given a year. For creating visualizations, the filters are going to be on the type of rice and the year. 
    '''
    fontp=FontProperties()
    fontp.set_size('xx-small')
    con=sqlite3.connect('rice.db')
    c=con.cursor()
    colormap=create_colormap()
    #Different conditions for setting the number of subplots
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
       
    #Getting the data from the tables
    i=0
    for cat in types:
        stprice={}  
        #Querying the database based on the filters passed
        rows=c.execute("select State,PMonth,AVG(MinPrice) from prices where Pyear=? and Category=? group by PMonth,state ORDER BY PMonth",(year,cat))
        check=rows.fetchone()
        #Checking to see if there are any rows returned. If none, then delete the corresponding subplot
        if check:
            #Fetching the data and creating the plots
            for row in rows:
                state=str(row[0])
                month=int(str(row[1]))
                price=float(str(row[2]))
                try:
                    stprice[state].append((month,price))
                except:
                    stprice[state]=[(month,price)]

            labels=[]
            for k,v in stprice.items():
                v=sorted(v)
                months=[m[0] for m in v]
                prices=[p[1] for p in v]
                axes[i].plot(months,prices,color=colormap[k],label=k)
                axes[i].set_xlim(1,18)
            axes[i].set_title(cat+" in the year "+year)
            x=1.05  
            y=0.5
            loc="right"
            cols=1
            axes[i].legend(loc=loc,bbox_to_anchor=(x,y),prop=fontp,fancybox=True, shadow=False, ncol=cols)
            
        else:
            print "Deleting axis",i
            fig.delaxes(axes[i])
        i+=1
    con.close()
    plt.subplots_adjust(hspace=0.9,wspace=0.2,left=0.15)
    plt.xlabel('Months',fontsize=16,va="top",ha="center")
    plt.ylabel('Price',fontsize=16,ha="left")
    imgpath="./static/images/graph.png"
    fig.savefig(imgpath)
    return imgpath

if __name__=='__main__':
    data_folder="../data/"
    '''
    Uncomment the commented lines to set up the database. Leave it commented, if database already present
    '''
    #Get all the files and upload to database
    #combine_files()
    #Get all the distinct varieties of rice from the db
    #varieties=groupCats()
    #Get the parent varieties of the different varieties of rice
    #parents=find_categories(varieties)
    #Update the database with the parent categories
    #update_cat(parents)
    types=["Other"]
    year="2010"
    create_plots(types,year)



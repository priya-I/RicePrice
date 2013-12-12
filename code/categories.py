#Find parent categories

from itertools import combinations, permutations
import nltk

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







import sqlite3
con=sqlite3.connect('rice.db')
c=con.cursor()
categories={'Suvarna': ['Suvarna Medium'], 'Sela': ['Basmati Golden Sela New', 'Basmati Haryana Sela(New)', 'IR-8 Sela (Old)', 'Parmal Selas (New)', 'Pusa Basmati Sela (Old)', 'Sarbati Sela (Old)', 'Tericot Sela'], 'Basmati': ['Ambemohor Basmati', 'Amira Mogra Basmati', 'Amire Full Basmati', 'Basmati (Rose)', 'Basmati Charmi', 'Basmati Golden Sela New', 'Basmati Haryana Sela(New)', 'Basmati Mogra (Raw/Old)', 'Basmati Silky Kohinoor', 'Basmati Trophy', 'Basmati U.P. (Old)', 'Basmati-385', 'Basmatibar (Raw/New)', 'Basmatidubar Raw/New', 'Dawal Full Basmati', 'Dhoon Full Basmati', 'Durbar Basmati', 'FCI Non Basmati', 'Fine(Basmati)', 'Hmt Rice-Non Basmati', 'Kolam-Non Basmati', 'Original Basmati', 'Popular Basmati', 'Pusa Basmati (Paddy)', 'Pusa Basmati Raw (Old)', 'Pusa Basmati Sela (Old)'], 'Coarse': ['Coarse (I.R.20)', 'Motta (Coarse) Boiled'], 'New': ['Basmati Golden Sela New', 'Basmati Haryana Sela(New)', 'Basmatibar (Raw/New)', 'Basmatidubar Raw/New', 'IR-8 Raw (New)', 'Parimal (New)', 'Parmal Raw (New)', 'Parmal Selas (New)'], 'White': ['White Car', 'White Parboiled'], 'Rice': ['AP Raw Rice 5293', 'AP Raw Rice Baptla Ponni', 'AP Raw Rice SilkyRaw', 'AP Raw-Rice Sona Ponni', 'Boiled Rice', 'Dosa Rice', 'Hmt Rice-Non Basmati', 'Rice Floor'], 'Paddy': ['Pusa Basmati (Paddy)', 'Sharbati (Paddy)'], 'Sona': ['AP Raw-Rice Sona Ponni', 'BT Sona', 'HMT Sona Medium', 'Sona Boiled', 'Sona Fine', 'Sona Medium', 'Sona Raw Old'], 'Boiled': ['Boiled Rice', 'CO-43 (Medium) Boiled', 'Motta (Coarse) Boiled', 'Sona Boiled'], 'Raw': ['AP Raw Rice 5293', 'AP Raw Rice Baptla Ponni', 'AP Raw Rice SilkyRaw', 'AP Raw-Rice Sona Ponni', 'Basmati Mogra (Raw/Old)', 'Basmatibar (Raw/New)', 'Basmatidubar Raw/New', 'HMT Fine Raw', 'IR 20 Fine Raw', 'IR-8 Raw (New)', 'Parmal Raw (New)', 'Ponni Fine Raw', 'Pusa Basmati Raw (Old)', 'Sarbati Raw', 'Sarbati Raw (Old)', 'Sona Raw Old'], 'HMT': ['HMT Fine Raw', 'HMT Sona Medium'], 'Parimal': ['Parimal (New)'], 'Car': ['White Car'], 'FCI': ['FCI Non Basmati'], 'Super': ['Super Fine'], 'Ponni': ['AP Raw Rice Baptla Ponni', 'AP Raw-Rice Sona Ponni', 'Culture Ponni1', 'Ponni', 'Ponni Fine Raw'], 'IR': ['IR 20', 'IR 20 Fine Raw', 'IR 50', 'IR-8 Raw (New)', 'IR-8 Sela (Old)', 'IR20 Parboiled'], 'AP': ['AP Raw Rice 5293', 'AP Raw Rice Baptla Ponni', 'AP Raw Rice SilkyRaw', 'AP Raw-Rice Sona Ponni'], 'Medium': ['CO-43 (Medium) Boiled', 'HMT Sona Medium', 'Jhilli Medium', 'Medium', 'Sona Medium', 'Suvarna Medium'], 'Sarbati': ['Sarbati Raw', 'Sarbati Raw (Old)', 'Sarbati Sela (Old)'], 'Dawat': ['Basamti Dawat'], 'Old': ['Basmati Mogra (Raw/Old)', 'Basmati U.P. (Old)', 'IR-8 Sela (Old)', 'Pusa Basmati Raw (Old)', 'Pusa Basmati Sela (Old)', 'Sarbati Raw (Old)', 'Sarbati Sela (Old)', 'Sona Raw Old'], 'Parmal': ['Export Parmal', 'Parmal', 'Parmal Raw (New)', 'Parmal Selas (New)'], 'Sanna': ['Bellary Sanna', 'Chintamani Sanna', 'Kapila Sanna', 'Nellore Sanna', 'Sanna Bhatta', 'andra Sanna'], 'Culture': ['Culture Ponni1'], 'Kaddi': ['Bangar Kaddi', 'Farm Kaddi', 'Kaddi'], '1009': ['1009 Kar'], 'Fine': ['Fine(Basmati)', 'HMT Fine Raw', 'IR 20 Fine Raw', 'Ponni Fine Raw', 'Sona Fine', 'Super Fine']}
min_id=910096
i=min_id
max_id=1820189
#max_id=910098
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
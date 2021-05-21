import sqlite3
import csv
import os

con = sqlite3.connect('Pokedex.db')
cur = con.cursor()


### tCharacters 
#Drop Character Table IF EXISTS
cur.execute('DROP TABLE IF EXISTS tCharacters')
con.commit()

#Create Character Table
cur.execute('CREATE TABLE IF NOT EXISTS tCharacters (CharacterID INTEGER PRIAMRY KEY, CharacterName TEXT NOT NULL)')
con.commit()

### tCharacterTypes
#Drop Character Table IF EXISTS
cur.execute('DROP TABLE IF EXISTS tCharacterTypes')
con.commit()

#Create tCharacterTypes Table
cur.execute('CREATE TABLE IF NOT EXISTS tCharacterTypes (CharacterID INTEGER PRIAMRY KEY, Type1 TEXT NOT NULL, Type2 TEXT NULL)')
con.commit()  

### tTypes
#Drop Character Table IF EXISTS
cur.execute('DROP TABLE IF EXISTS tTypes')
con.commit()

#Create tTypes Table
cur.execute('CREATE TABLE IF NOT EXISTS tTypes (TypeID INTEGER PRIAMRY KEY, Type TEXT NOT NULL)')
con.commit()  

### tTypeProperties
#Drop Character Table IF EXISTS
cur.execute('DROP TABLE IF EXISTS tTypeProperties')
con.commit()

#Create tCharacterTypes Table
cur.execute('CREATE TABLE IF NOT EXISTS tTypeProperties (TypeID INTEGER PRIAMRY KEY, AttackingTypeID INTEGER, AttackMultiplier DECIMAL(2,2))')
con.commit()  

### tCharacterRarety
#Drop Character Rarety Table IF EXISTS
cur.execute('DROP TABLE IF EXISTS tRarety')
con.commit()

#Create tCharacterTypes Table
cur.execute('CREATE TABLE IF NOT EXISTS tRarety (RaretyID INTEGER PRIAMRY KEY, PercentageChance DECIMAL(2,2))')
con.commit()

#Insert into Characters, tCharacterTypes
data = []
csvFile = os.path.join('Files','Pokemon.csv')
with open(csvFile, 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        data.append(row)

for i in data:
        cur.execute('INSERT INTO tCharacters (CharacterID, CharacterName) VALUES(?,?)',(i[1].replace('#',''),i[3],))
        if len(i) > 5:
            #print(i[0],i[1],i[2],i[3],i[4],i[5])
            cur.execute('INSERT INTO tCharacterTypes (CharacterID, Type1, Type2) VALUES(?,?,?)',(i[1].replace('#',''),i[4],i[5],))
        else:
            #print(i[0],i[1],i[2],i[3],i[4])
            cur.execute('INSERT INTO tCharacterTypes (CharacterID, Type1) VALUES(?,?)',(i[1].replace('#',''),i[4],))
        
#Insert into tTypes
cur.execute('SELECT DISTINCT * FROM (SELECT Type1 FROM tCharacterTypes UNION SELECT Type2 FROM tCharacterTypes)')
Types=cur.fetchall()
ID=1
for t in Types:
    if t[0] is not None and t[0] not in ('Type1','Type2'):
        #print(t[0])
        cur.execute('INSERT INTO tTypes (TypeID, Type) VALUES(?,?)',(ID,t[0],))
        ID=ID+1

#Insert into tTypeProperties (AttackMultiplier - 0.5=Weak, 0=No Effect, 2=Super Effective)
#https://www.polygon.com/pokemon-sword-shield-guide/2019/11/16/20968169/type-strength-weakness-super-effective-weakness-chart
#cur.execute('INSERT INTO tTypeProperties (TypeID, AttackingTypeID, AttackMultiplier) VALUES(1,6,0.5)')


## Insert Type Properties
Files=('PokemonTypePropertiesEffective.csv','PokemonTypePropertiesWeakness.csv')
for file in Files:
    csvFile = os.path.join('Files',file)
    if 'Effective' in file:
        Attribute=2
    else:
        Attribute=0.5
    data = []
    with open(csvFile, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            data.append(row)

    for row in data:
        Type=row[0]
        cur.execute('SELECT TypeID from tTypes WHERE Type=?',(Type,))
        TypeIDs=cur.fetchall()
        for ID in TypeIDs:
            TypeID=ID[0]
            #print(TypeID)
            for AtkType in enumerate(row):
                AtkType=str(AtkType[1]).replace(' ','')
                #print(AtkType)
                cur.execute('SELECT TypeID from tTypes WHERE Type=?',(AtkType,))
                AtkTypeIDs=cur.fetchall()
                for ID in AtkTypeIDs:
                    AtkTypeID=ID[0]
                    #print(AtkTypeID)
                    cur.execute('INSERT INTO tTypeProperties (TypeID, AttackingTypeID, AttackMultiplier) VALUES(?,?,?)',(TypeID,AtkTypeID,Attribute,))

  

con.commit()
#Test Characters
cur.execute('SELECT * FROM tCharacters C INNER JOIN tCharacterTypes CT ON C.CharacterID = CT.CharacterID')
#print(cur.fetchall())

#Test CharacterTypes
cur.execute('SELECT T.TypeID, T.Type FROM tTypes T')
Result=cur.fetchall()
#for row in Result:
#    print(row[0],row[1])
#con.close

#Test CharacterTypes - Properties
cur.execute('SELECT T.TypeID, T.Type, CASE TP.AttackMultiplier WHEN ".25" THEN "VERY WEAK" WHEN ".5" THEN "WEAK" WHEN "0" THEN "NO EFFECT" WHEN "2" THEN "SUPER EFFECTIVE" END EFFECT , "AGAINST", T2.Type FROM tTypes T INNER JOIN tTypeProperties TP ON T.TypeID = TP.TypeID INNER JOIN tTypes T2 ON TP.AttackingTypeID = T2.TypeID WHERE T.TypeID <> T2.TypeID')
Result=cur.fetchall()
#for row in Result:
#    print(row[1],row[2],row[3],row[4])

#Check Orphaned Types
cur.execute('SELECT * FROM tTypes T LEFT JOIN tTypeProperties TP ON TP.TypeID = TP.TypeID WHERE TP.TypeID IS NULL')
Result=cur.fetchall()
#print(Result)

con.close


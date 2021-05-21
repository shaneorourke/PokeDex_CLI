import sqlite3

con = sqlite3.connect('Pokedex.db')
cur = con.cursor()

def cls():
    print('\n'*50)

def searchByName():
    name=input('Enter Pokemon Name:')
    name=name.upper()
    cur.execute('SELECT C.CharacterID, C.CharacterName, CT.Type1, CT.Type2 FROM tCharacters C INNER JOIN tCharacterTypes CT ON C.CharacterID = CT.CharacterID WHERE UPPER(C.CharacterName) = ?',(name,))
    characterResult=cur.fetchall()
    if len(characterResult) == 0:
        print('Not a valid Pokemon name')
    else:
        try:
            from ImageOpener import ImageOpener
            ImageOpener(name.capitalize()+'.png')
        except:
            print('No Image Found')
        output=''
        for row in characterResult:
            for item in enumerate(row):
                output=output+' | '+str(item[1])
        print('####################### POKEMON #######################')
        print(' | ID | Name | Type1 | Type2 ||')
        print(output+' ||')

        print('####################### TYPES #######################')
        cur.execute('SELECT CT.Type1, CT.Type2 FROM tCharacters C INNER JOIN tCharacterTypes CT ON C.CharacterID = CT.CharacterID WHERE UPPER(C.CharacterName) = ?',(name,))
        TypeResult=cur.fetchall()
        output=''
        for row in TypeResult:
            for item in enumerate(row):
                Type=str(item[1])
                cur.execute('SELECT * FROM (SELECT T.TypeID, T.Type, CASE TP.AttackMultiplier WHEN ".25" THEN "VERY WEAK" WHEN ".5" THEN "WEAK" WHEN "0" THEN "NO EFFECT" WHEN "2" THEN "SUPER EFFECTIVE" END EFFECT , "AGAINST", T2.Type FROM tTypes T INNER JOIN tTypeProperties TP ON T.TypeID = TP.TypeID INNER JOIN tTypes T2 ON TP.AttackingTypeID = T2.TypeID WHERE T.TypeID <> T2.TypeID AND T.Type = ?) ORDER BY 1,2,3,4',(Type,))
                TypePropsResults=cur.fetchall()
                for row in TypePropsResults:
                    print('| '+row[1]+' | '+row[2],row[3]+' | '+row[4]+' |')
                    #print(row)
    con.close

def searchByType():
    name=input('Enter Pokemon Type:')
    name=name.upper()
    cur.execute('SELECT C.CharacterID, C.CharacterName, CT.Type1, CT.Type2 FROM tCharacters C INNER JOIN tCharacterTypes CT ON C.CharacterID = CT.CharacterID WHERE UPPER(CT.Type1) = ? OR UPPER(CT.Type2) = ?',(name,name))
    characterResult=cur.fetchall()
    if len(characterResult) == 0:
        print('Not a valid Pokemon Type')
    else:
        output=''
        for row in characterResult:
            for item in enumerate(row):
                output=output+' | '+str(item[1])
            output=output+' |\n'
        print('####################### POKEMON #######################')
        print(' | ID | Name | Type1 | Type2 ||')
        print(output)

        print('####################### TYPES #######################')
        cur.execute('SELECT * FROM (SELECT T.TypeID, T.Type, CASE TP.AttackMultiplier WHEN ".25" THEN "VERY WEAK" WHEN ".5" THEN "WEAK" WHEN "0" THEN "NO EFFECT" WHEN "2" THEN "SUPER EFFECTIVE" END EFFECT , "AGAINST", T2.Type FROM tTypes T INNER JOIN tTypeProperties TP ON T.TypeID = TP.TypeID INNER JOIN tTypes T2 ON TP.AttackingTypeID = T2.TypeID WHERE T.TypeID <> T2.TypeID AND UPPER(T.Type) = ?) ORDER BY 1,2,3,4',(name,))
        TypePropsResults=cur.fetchall()
        for row in TypePropsResults:
            print('| '+row[1]+' | '+row[2],row[3]+' | '+row[4]+' |')
            #print(row)
        con.close



def PokeDex():
    cls()
    Running = 'Y'
    while Running == 'Y':
        print('####################### POKEDEX #######################')
        print('1. Search by Name')
        print('2. Search by Type')
        print('3. Exit')
        Option=input('Enter Option:')
        try:
            Option=int(Option)
        except:
            print('Invalid Option')
            Running='N'

        if Option == 1:
            searchByName()
            wait=input('Press any key to continue')
        elif Option == 2:
            searchByType()
            wait=input('Press any key to continue')
        elif Option == 3:
            Running = 'N'
            break
        else:
            print('Unrecognised Option')
        cls()

    print('####################### POKEDEX CLOSED #######################')

if __name__ == "__PokeDex__":
    PokeDex()

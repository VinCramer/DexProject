from flask import Flask, g, send_file, render_template
import sqlite3

#initializes the application
app = Flask(__name__)

#location of the database file we're loading from
DATABASE = 'static/database/pokedex.sqlite'

#basic homepage
#TODO- make it look nicer
@app.route("/")
def home():
    #accesses a cursor from the database
    cursor=get_db().cursor()

    #gets lists of numbers and names of monsters for each generation to be displayed in select tags
    list1=getGen1(cursor)
    list2=getGen2(cursor)
    list3=getGen3(cursor)
    list4=getGen4(cursor)
    list5=getGen5(cursor)

    return render_template("index.html", list1=list1, list2=list2, list3=list3, list4=list4, list5=list5)

#404 error handling
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")

#Loads the database
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

#Closes our connection to database when application closes
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

#Displays the entry for the pokemon of the given number
#Right now, the entry consists solely of a picture. Will be updated to include more information.
@app.route("/<int:num>/")
def displayEntry(num):

    #if the user enters an invalid value, we'll show them an error message
    #invalid values are 0, negative, and any pokemon from after gen 5
    if num<=0 or num > 649:
        return render_template("404.html")

    #need to convert the number to a string when trying to access its image
    fileName = str(num)

    #images are named 001, 002, etc. Rather than rename all of them, we'll prepend 0s if necessary 
    if num<10:
        fileName="00"+fileName

    #images over 10 and under 100 also need a single preprended 0 
    elif num<100:
        fileName="0"+fileName

    #displays the image, and only the image, of the creature
    #return send_file("static/sprites/"+ fileName + ".gif", mimetype="image/gif")

    #accesses a cursor from the database
    cursor=get_db().cursor()

    cursor.execute("SELECT identifier FROM pokemon_species where id="+str(num))
    
    #string that will be the title of the webpage
    title = "#" + str(num) + " - "

    #fetchone() gets us the right row as a list. We call the 0th element to remove the 
    #extra characters from before and after the name. title() makes only the 1st letter capitalized
    name = cursor.fetchone()[0].title()

    title += name

    #type_id, name from type_names
    #pokemon_types is transitive table - have ids and type1/2

    #get type ids first and store in array
    cursor.execute("SELECT type_id from pokemon_types  where pokemon_id="+str(num))
    typeArr = cursor.fetchall()

    #get type1 in english
    cursor.execute("SELECT name from type_names where local_language_id=9 AND type_id="
        +str(typeArr[0][0]))
    type1 = cursor.fetchone()[0]
    
    #not all monsters have 2 types - need to check if there's 2 elements in tuple before operation 
    
    #default value
    type2=""

    if len(typeArr)==2:

        #get type2 in English
        cursor.execute("SELECT name from type_names where local_language_id=9 AND type_id="
            +str(typeArr[1][0]))
        type2 = cursor.fetchone()[0]

       

    #need to go up a level with .. since this string will be used in the templates folder
    imgLocation = "../static/sprites/gif/"+fileName+".gif"


    #abilities
    #id, identifier(name), generation_id
    #pokemon_abilities
    #pokemon_id, ability_id, is_hidden, slot (slot is 1 and 2 for normal, 3 for hidden)

    cursor.execute("SELECT ability_id FROM pokemon_abilities where slot!=3 AND pokemon_id="+str(num))
    abbArr = cursor.fetchall()

    cursor.execute("SELECT identifier FROM abilities where id="+str(abbArr[0][0]))
    ability1=cursor.fetchone()[0].title()

    cursor.execute("SELECT flavor_text FROM ability_flavor_text where language_id=9 AND ability_id="
        +str(abbArr[0][0]))
    
    #abilities can be in different languages or have different wording. 1st is 
    # sufficient for this project.
    ability1Flavor=cursor.fetchall()[0][0]


    ability2=""
    ability2Flavor=""
    if len(abbArr)==2:
        cursor.execute("SELECT identifier FROM abilities where id="+str(abbArr[1][0]))
        ability2=cursor.fetchone()[0].title()

        cursor.execute("SELECT flavor_text FROM ability_flavor_text where language_id=9 AND ability_id="
            +str(abbArr[1][0]))
        ability2Flavor=cursor.fetchall()[0][0]



    #not every monster has a hidden ability

    cursor.execute("SELECT ability_id FROM pokemon_abilities where slot=3 AND pokemon_id="+str(num))
    hidden=cursor.fetchone()
    hiddenFlavor=""
    if hidden!=None:

        hidden=hidden[0]

        #want to get the description of the hidden ability if there is a hidden ability
        cursor.execute("SELECT flavor_text FROM ability_flavor_text where language_id=9 AND "+
            "ability_id="+str(hidden))

        #if cursor got something from our query, we have a hidden ability, which has a description
        if cursor.fetchone()!=None:

            #there's multiple descriptions from multiple generations and languages, but the 1st is 
            # always in English, which is good enough for our purposes
            hiddenFlavor=cursor.fetchall()[0][0]

        cursor.execute("SELECT identifier FROM abilities where id="+str(hidden))
        hidden = cursor.fetchone()[0].title()
    
    #minor nuance with the display - displaying "Ability 1" when the monster only has 1  
    #normal ability is bad form.
    if ability2=="":
        ability1="Ability: "+ability1

    #there's a few monsters that erroneously have the same ability listed twice
    elif ability1==ability2: 
        ability2=""
        ability1="Ability: "+ability1
    else:
        ability1="Ability 1: "+ability1
        ability2="Ability 2: "+ability2

    #certain abilities are made of 2 words and have a dash in between them. This removes the dash 
    # if needed.
    ability1=ability1.replace("-", " ")
    ability2=ability2.replace("-", " ")
    if hidden!=None:
        hidden=hidden.replace("-", " ")

    # language id=9 is for English. Version_id=22 is not the same dex entry data across generations, 
    # but it's valid for all of the monsters.
    cursor.execute("SELECT flavor_text FROM pokemon_species_flavor_text where language_id=9 "+
        "AND version_id=22 AND species_id="+str(num))
    speciesFlavor = cursor.fetchone()[0]

    #want user to easily choose between the next and previous entries in the dex
    prevName=""
    nextName=""
    prevImg=""
    nextImg=""

    #if user is at the first entry, there's no entry before that
    if num-1>0:
        cursor.execute("SELECT identifier FROM pokemon_species where id="+str(num-1))
        prevName = cursor.fetchone()[0]
        prevImg="../static/sprites/pc-sprites/"+prevName+".png"
        prevName=prevName.title()

    #if user is at last entry, there's no entry behind that
    if num+1<=649:
        cursor.execute("SELECT identifier FROM pokemon_species where id="+str(num+1))
        nextName = cursor.fetchone()[0]
        nextImg="../static/sprites/pc-sprites/"+nextName+".png"
        nextName=nextName.title()
    

    #gets lists of numbers and names of monsters for each generation to be displayed in select tags
    list1=getGen1(cursor)
    list2=getGen2(cursor)
    list3=getGen3(cursor)
    list4=getGen4(cursor)
    list5=getGen5(cursor)

    #gets the stat values and classifications for each stat
    hp=getStat(cursor, num, 1)
    hpClass=getStatClass(hp)

    atk=getStat(cursor, num, 2)
    atkClass=getStatClass(atk)

    defense=getStat(cursor, num, 3)
    defenseClass=getStatClass(defense)

    spAtk=getStat(cursor, num, 4)
    spAtkClass=getStatClass(spAtk)


    spDef=getStat(cursor, num, 5)
    spDefClass=getStatClass(spDef)

    spd=getStat(cursor, num, 6)
    spdClass=getStatClass(spd)

    #gets a tuple of all of the monsters that the current one could've evolved from or could evolve into
    familyTuple = getFamilyTuple(cursor, num)

    #used for determining which family tree we're dealing with in table
    ev_id=getEvId(cursor,num)

    # used for seeing if 1 monster has 2 split evolution paths, for 3 total monsters.
    oneTwoSplit = getOneTwoSplit(num)

    #used for determining the order of certain family trees which had lower-tiered monsters 
    # added later chronologically in the series
    differentEvoOrder = getDifferentEvoOrder(num)

    
    #displays the webpage with all given variables
    return render_template("dex-entry.html", pageHeading=title, imgLocation=imgLocation, name=name, 
        type1=type1, type2=type2, ability1=ability1, ability2=ability2, hidden=hidden, 
        ability1Flavor=ability1Flavor, ability2Flavor=ability2Flavor, hiddenFlavor=hiddenFlavor, 
        speciesFlavor=speciesFlavor, prevNum=num-1, nextNum=num+1, prevName=prevName, nextName=nextName,
        prevImg=prevImg, nextImg=nextImg, list1=list1, list2=list2, list3=list3, list4=list4, 
        list5=list5, hp=hp, hpClass=hpClass, atk=atk, spAtk=spAtk, spDef=spDef, defense=defense, spd=spd,
        spdClass=spdClass, atkClass=atkClass, spAtkClass=spAtkClass, spDefClass=spDefClass, 
        defenseClass=defenseClass, familyTuple=familyTuple, ev_id=ev_id, oneTwoSplit=oneTwoSplit,
        differentEvoOrder = differentEvoOrder)



#returns true if the current index is 1 of the few species that had a precursor monster added later
def getDifferentEvoOrder(num):
    return (num==25 or num==26 or num == 172 
        or num==173 or num==35 or num==36
        or num==174 or num==39 or num==40
        or num==238 or num==124
        or num==239 or num==125 or num==466
        or num==240 or num==126 or num==467
        or num==298 or num==183 or num==184
        or num==360 or num==202
        or num==406 or num==315 or num==407
        or num==433 or num==538
        or num==438 or num==185
        or num==439 or num==122
        or num==446 or num==143
        or num==458 or num==226)

# returns true if the monster has a base form that can turn 1 of 2 forms, for a total of 3 
# in the family tree
def getOneTwoSplit(num):
    return (num==79 or num==80 or num==199 or 
        (num>=290 and num<=292) or 
        num==361 or num==362 or 
        num==479 or 
        (num>=366 and num<=368) or 
        (num>=412 and num<=414))

#gets evolution id for creature at given index
def getEvId(cursor, num):
    cursor.execute("SELECT evolution_chain_id FROM pokemon_species WHERE id="+str(num))
    return cursor.fetchone()[0]

#returns a list of the number and name(s) of all species the current monster could've evolved to or from
def getFamilyTuple(cursor, num):
    cursor.execute("SELECT id, identifier FROM pokemon_species WHERE"+
    " evolution_chain_id=(SELECT evolution_chain_id FROM pokemon_species where id="+str(num)+")")
    return cursor.fetchall()


#returns a list, where each item is the number and name of a monster from gen 1 (1-151)
def getGen1(cursor):
    cursor.execute("SELECT pokemon_species_id, name FROM pokemon_species_names WHERE "
    +"local_language_id=9 AND pokemon_species_id<152")
    genList= cursor.fetchall()
    realList=[]
    for val in genList:
        tempString=str(val[0]) + " - " + str(val[1])
        if val[0]<10:
            tempString="00"+tempString
        elif val[0]<100:
            tempString="0"+tempString
        realList.append(tempString)
    return realList
    

#returns a list, where each item is the number and name of a monster from gen 2 (152-251)
def getGen2(cursor):
    cursor.execute("SELECT pokemon_species_id, name FROM pokemon_species_names WHERE "
    +"local_language_id=9 AND pokemon_species_id>=152 AND pokemon_species_id<252")
    genList= cursor.fetchall()
    realList=[]
    for val in genList:
        tempString=str(val[0]) + " - " + str(val[1])
        realList.append(tempString)
    return realList

#returns a list, where each item is the number and name of a monster from gen 3 (252-386)
def getGen3(cursor):
    cursor.execute("SELECT pokemon_species_id, name FROM pokemon_species_names WHERE "
    +"local_language_id=9 AND pokemon_species_id>=252 AND pokemon_species_id<387")
    genList= cursor.fetchall()
    realList=[]
    for val in genList:
        tempString=str(val[0]) + " - " + str(val[1])
        realList.append(tempString)
    return realList

#returns a list, where each item is the number and name of a monster from gen 4 (387-493)
def getGen4(cursor):
    cursor.execute("SELECT pokemon_species_id, name FROM pokemon_species_names WHERE "
    +"local_language_id=9 AND pokemon_species_id>=387 AND pokemon_species_id<494")
    genList= cursor.fetchall()
    realList=[]
    for val in genList:
        tempString=str(val[0]) + " - " + str(val[1])
        realList.append(tempString)
    return realList

#returns a list, where each item is the number and name of a monster from gen 5 (494-649)
def getGen5(cursor):
    cursor.execute("SELECT pokemon_species_id, name FROM pokemon_species_names WHERE "
    +"local_language_id=9 AND pokemon_species_id>=494")
    genList= cursor.fetchall()
    realList=[]
    for val in genList:
        tempString=str(val[0]) + " - " + str(val[1])
        realList.append(tempString)
    return realList

#returns the stat value for the monster at the given index
#stat id 1->HP
#stat id 2->ATK
#stat id 3->DEF
#stat id 4->SP> ATK
#stat id 5->SP. DEF
#stat id 6->SPD
def getStat(cursor, num, statNum):
    cursor.execute("SELECT base_stat FROM pokemon_stats WHERE stat_id="+str(statNum)+
        " AND pokemon_id="+str(num))
    return cursor.fetchone()[0]

#returns name of styling class depending on what the value of the stat is
def getStatClass(stat):
    if stat<70:
        return "redStat"
    elif stat<100:
        return "yellowStat"
    else:
        return "greenStat"


#runs the program
if __name__ == "__main__":
    app.run()
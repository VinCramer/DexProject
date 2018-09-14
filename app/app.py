from flask import Flask, g, send_file, render_template
import sqlite3

#initializes the application
app = Flask(__name__)

#location of the database file we're loading from
DATABASE = 'static/database/pokedex.sqlite'

#basic homepage - will edit to display buttons to go to each dex entry
#@app.route("/")
#def hello():
#    return "homepage"

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
        return "<h1>Enter a valid pokemon number</h1>"

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
    imgLocation = "../static/sprites/"+fileName+".gif"


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

    #TODO - dex entries. They are in species flavor text table.

    return render_template("dex-entry.html", pageHeading=title, imgLocation=imgLocation, name=name, 
        type1=type1, type2=type2, ability1=ability1, ability2=ability2, hidden=hidden, 
        ability1Flavor=ability1Flavor, ability2Flavor=ability2Flavor, hiddenFlavor=hiddenFlavor)



#runs the program
if __name__ == "__main__":
    app.run()
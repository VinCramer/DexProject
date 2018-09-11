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
    title += cursor.fetchone()[0].title()




    #need to go up a level with .. since this string will be used in the templates folder
    imgLocation = "../static/sprites/"+fileName+".gif"

    return render_template("dex-entry.html", pageHeading=title, imgLocation=imgLocation)

#runs the program
if __name__ == "__main__":
    app.run()
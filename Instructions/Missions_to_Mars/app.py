from flask import Flask, render_template, redirect
import pymongo
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Setup mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_db")

@app.route("/")
def index():

    # Find one record of data from the mongo database
    mars_info = mongo.db.mars_list.find_one()
    # Return template and data
    return render_template("index.html", mars=mars_info)

@app.route("/scrape")
def scrape():
    
    mars_import = scrape_mars.scrape()
    # Update the Mongo database using update and upsert=True
    mongo.db.mars_list.update({}, mars_import, upsert=True)
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)

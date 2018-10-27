from flask import Flask, render_template,redirect
from flask_pymongo import PyMongo
import scrape_mars

#create instance of Flask app
app = Flask(__name__)

# use flask_PyMongo to setup Mongo connection
app.config["MONGO_URI"]="mongodb://localhost:27017/mars"
mongo=PyMongo(app)

#create route that renders index.html and finds documents from mongo
@app.route("/")
def home():
    #collect data from mongodb
    mars_data=mongo.db.data.find_one()

    print (mars_data)

    #return template and data
    return render_template("index.html",mars_data=mars_data)


#Route that will trigger the scrape functions and add to mongodb
@app.route("/scrape")
def scrape():
    NASA_data = scrape_mars.scrape_NASA()
    JPL_data=scrape_mars.scrape_JPL()
    mars_weather=scrape_mars.scrape_mars_weather()
    mars_facts=scrape_mars.scrape_mars_facts()
    mars_hemispheres=scrape_mars.scrape_mars_hemispheres()

    mars_data ={
        'title':NASA_data['title'],
        'paragraph':NASA_data['paragraph'],
        'featured_img_src':JPL_data,
        'weather':mars_weather,
        'facts_html':mars_facts,
        'hemispheres':mars_hemispheres
    }

    #print(mars_data)

    #Insert mars_data into database
    mongo.db.data.update({},mars_data,upsert=True)

    #Redirect back to home page
    return redirect("/", code=302)

# Run Flask App
if __name__=="__main__":
    app.run(debug=True)


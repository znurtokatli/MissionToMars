from flask import Flask, render_template,redirect
from flask_pymongo import PyMongo
from mars_scrape import scrape


#create an instance for Flask App
app = Flask(__name__) 

#connect 
app.config["MONGO_URI"]='mongodb://localhost:27017/marsdb'
mongo= PyMongo(app)


@app.route("/")
def index():
    mars=mongo.db.mars.find_one()
    return render_template ('index.html', mars=mars)

@app.route('/scrape')
def scrape_all():
    mars=mongo.db.mars
    data=scrape()
    mars.update({}, data, upsert=True)
    redirect('/',code=302)

if __name__=="__main__":
    app.run(debug=True)
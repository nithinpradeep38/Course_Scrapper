from flask import Flask, render_template
from flask_cors import CORS,cross_origin
from ScrapOps import MainScrapper
from dbops import MongoDBOps
from apscheduler.schedulers.background import BackgroundScheduler

dbretrieval= MongoDBOps(username= 'ineuronscrap', password= 'ineuron')

mainScrap=MainScrapper() #initialization of scrapping ops
scheduler=BackgroundScheduler()
scheduler.add_job(func=mainScrap.mainscrap, trigger='date')
scheduler.start()

app = Flask(__name__)
CORS(app)

@app.route('/',methods=['GET'])  # route to display the home page (index.html)
@cross_origin()
def homePage():
    return render_template("index.html") #always keep the html files inside templates folder. Don't mess spelling of folder

@app.route('/review',methods=['POST','GET']) # route to show the review comments in a web UI. Execute this when path is review
@cross_origin()  #reqd when we deploy this over a cloud platform because we don't know from which location we will deploy it.
def index():
        try:
            if dbretrieval.isCollectionPresent(dbname='ineuron', collectionName='AllCourseInfo'):
                info= dbretrieval.getdata(dbname='ineuron', collectionName='AllCourseInfo')

            return render_template('results.html', results=info)
        except Exception as e:
            print('The Exception message is: ',e)
            return 'something is wrong'
    # return render_template('results.html')

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8001, debug=True)
#app.run(debug=True)


from apscheduler.schedulers.background import BackgroundScheduler
from scrapper import Scrapper
from dbops import MongoDBOps
from logger import scrapLogger
class MainScrapper:


    def __init__(self):
        self.driver_path= './chromedriver'
        self.dbname= "ineuron"
        self.collectionName= "AllCourseInfo"
        self.dboperations= MongoDBOps(username= 'ineuronscrap', password= 'ineuron')
        self.logger = scrapLogger.ineuron_logger()

    def mainscrap(self):

        try:
            if self.dboperations.isCollectionPresent(self.dbname, self.collectionName):
                self.logger.info("MongoDB already has the records. Not proceeding to scrap")
                pass
            else:
                self.logger.info("Scrapping initiated")
                scrapper_obj = Scrapper(driver_path=self.driver_path)
                allcourselinks= scrapper_obj.get_courselink()
                print("All course links obtained")
                self.logger.info("All course links obtained")

                allcourse_info= scrapper_obj.get_courseinfo(allcourselinks)
                print("All course info received")
                self.logger.info("All course info received")
                #print(allcourse_info)
                #print(len(allcourse_info))

                self.dboperations.createDatabase(self.dbname)
                print("Database created")
                self.logger.info("Database created")

                self.dboperations.createCollection(dbname=self.dbname, collectionName=self.collectionName)
                print("Collection created")
                self.logger.info("Collection created")

                self.dboperations.insertdata(dbname= self.dbname, collectionName=self.collectionName, data= allcourse_info)
                print("Data inserted")
                self.logger.info("Data inserted")


        except Exception as e:
            self.logger.error("Error in conducting scrap operations: ", e)
            raise e













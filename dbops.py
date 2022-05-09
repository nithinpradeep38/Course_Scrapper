import pymongo

class MongoDBOps:


    def __init__(self, username, password):
        try:
            self.username= username
            self.password= password
            self.clienturl= f"mongodb+srv://{self.username}:{self.password}@webscrapper.x2dgg.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
        except Exception as e:
            raise e


    def connMongoClient(self):

        try:
            client= pymongo.MongoClient(self.clienturl)
            return client
        except Exception as e:
            raise e

    def getDatabase(self, dbname):
        try:
            client= self.connMongoClient()
            database= client[dbname]
            return database
        except Exception as e:
            raise e

    def isDatabasePresent(self,dbname):

        try:
            client= self.connMongoClient()
            if dbname in client.list_database_names():
                return True
            else:
                return False
        except Exception as e:
            raise e

    def createDatabase(self,dbname):
        try:
            client = self.connMongoClient()
            db = client[dbname]
        except Exception as e:
            raise e

    def getCollection(self, dbname, collectionName):
        try:
            db= self.getDatabase(dbname)
            collection= db[collectionName]
            return collection
        except Exception as e:
            raise e

    def isCollectionPresent(self,dbname,collectionName):
        try:
            if self.isDatabasePresent(dbname):
                database = self.getDatabase(dbname)
                if collectionName in database.list_collection_names():
                    return True
                else:
                    return False
            else:
                return False
        except Exception as e:
            raise e

    def createCollection(self, dbname, collectionName):
        try:
            database= self.getDatabase(dbname)
            collection= database[collectionName]

        except Exception as e:
            raise e

    def insertdata(self, dbname, collectionName, data):
        try:
            collection = self.getCollection(dbname, collectionName)
            collection.insert_many(data)

        except Exception as e:
            raise e

    def getdata(self,dbname, collectionName):
        try:
            if self.isCollectionPresent(dbname, collectionName):
                collection= self.getCollection(dbname,collectionName)
                data= collection.find()
                return data
        except Exception as e:
            raise e





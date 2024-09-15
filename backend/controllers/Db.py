from conf.constants import CONF,MONGO_COLL_FOR_CHATS,MONGO_COLL_FOR_FILES,MONGO_COLL_FOR_SESSIONS,MONGO_COLL_FOR_STATISTICS,MONGO_COLL_FOR_USERS
import pymongo
import json 
import logging



class DB(object):
    def __init__(self,CONF) -> None:
        if CONF.db_user=='' and CONF.db_password=='':
            self.config="mongodb://db:27017?directConnection=true"
        else:
            self.config="mongodb://"+CONF.db_user+":"+CONF.db_password+"@db:27017?directConnection=true"
        try:
            self.client=pymongo.MongoClient(self.config)
            self.db=self.client['dcaf']
        except pymongo.errors.PyMongoError as e:
            logging.error('Encountered DB Connection error: %s',e)
    def _listdbs(self):
        try:
            return self.client.list_database_names()
        except Exception as e:
            logging.error('DB Error: %s',e)
    def _listcol(self):
        try:
            return self.db.list_collection_names()
        except Exception as e:
            logging.error('DB Error: %s',e)
    def _createcol(self,name):
        try:
            self.db[name]
        except Exception as e:
            logging.error('DB Error: %s',e)
    def _insertone(self,name,record):
        try:
            return self.db.__getattr__(name).insert_one(record).inserted_id
        except Exception as e:
            logging.error('DB Error: %s',e)
    def _insertmany(self,name,myList):
        try:
            self.db.__getattr__(name).insert_many(myList)
        except Exception as e:
            logging.error('DB Error: %s',e)
    def _update(self,name,*args,**kwargs):
        try:
            self.db.__getattr__(name).update_one(*args,**kwargs)
        except Exception as e:
            logging.error('DB Error: %s',e)
    def _close(self):
        try:
            self.client.close()
        except Exception as e:
            logging.error('DB Error: %s',e)
    def _find(self,name,*args,**kwargs):
        try:
            return list(self.db.__getattr__(name).find(*args,**kwargs))
        except Exception as e:
            logging.error('DB Error: %s',e)
    def _findone(self,name,*args,**kwargs):
        try:
            return self.db.__getattr__(name).find_one(*args,**kwargs)
        except Exception as e:
            logging.error('DB Error: %s',e)
    def _findoneanddelete(self,name,*args,**kwargs):
        try:
            self.db.__getattr__(name).find_one_and_delete(*args,**kwargs)
        except Exception as e:
            logging.error('DB Error: %s',e)
    def _findoneandreplace(self,name,*args,**kwargs):
        try:
            self.db.__getattr__(name).find_one_and_replace(*args,**kwargs)
        except Exception as e:
            logging.error('DB Error: %s',e)
    def _findoneandupdate(self,name,*args,**kwargs):
        try:
            self.db.__getattr__(name).find_one_and_update(*args,**kwargs)
        except Exception as e:
            logging.error('DB Error: %s',e)
    def _count_docs(self,name,*args,**kwargs):
        try:
            return self.db.__getattr__(name).count_documents(*args,**kwargs)
        except Exception as e:
            logging.error('DB Error: %s',e)
    def _createindex(self,name,*args,**kwargs):
        try:
            self.db.__getattr__(name).create_index(*args,**kwargs)
        except Exception as e:
            logging.error('DB Error: %s',e)
    def _lookup(self,name,pipeline):
        try:
            return self.db.__getattr__(name).aggregate(pipeline)
        except Exception as e:
            logging.error('DB Error: %s',e)
    def _checkifexists(self,name,*args,**kwargs):
        try:
            return bool(list(self.db.__getattr__(name).find(*args,**kwargs)))
        except Exception as e:
            logging.error('DB Error: %s',e)
    def _deleteallrecords(self,name,*args,**kwargs):
        try:
            self.db.__getattr__(name).delete_many(*args,**kwargs)
        except Exception as e:
            logging.error('DB Error: %s',e)

class db(DB):
    def __init__(self,CONF):
        super(db,self).__init__(CONF)
        
    def __call__(self):
        self._importdbconfig()

    def _createcollections(self):
        with open('/app/conf/dcaf_config.json',"r") as file:
                schema=json.load(file)
        for x,y in schema.items():
            if x not in super(db,self)._listcol():
                logging.debug('working on ' + x)
                try:
                    super(db,self)._createcol(x)
                    if 'index' in y:
                        super(db,self)._createindex(x,y["index"],unique=True)
                    super(db,self)._insertmany(x,y["record"])
                except DuplicateKeyError:
                    pass
                except Exception as e:
                    logging.error(e)

    def _importdbconfig(self):
        try:
            if "dcaf" not in super(db,self)._listdbs():
                logging.debug("Database doesn't exist, Creating it")
                self._createcollections()
                self._close()
            else:
                logging.debug('Database Exist, Updating')
                self._createcollections()
            logging.info( "Initialized Database")
        except Exception as e:
            logging.error(e)


class MongoController(DB):
    def __init__(self):
        super(MongoController,self).__init__(CONF)

    def _add_tr_record(self,*args,**kwargs):
        return self._insertone(MONGO_COLL_FOR_STATISTICS,*args,**kwargs)

    def _find_tr_record(self,*args,**kwargs):
        return self._find(MONGO_COLL_FOR_STATISTICS,*args,**kwargs)[0]

    def _update_tr_record(self,*args,**kwargs):
        self._update(MONGO_COLL_FOR_STATISTICS,*args,**kwargs)
  
    def _create_user_session(self,*args,**kwargs):
        return self._insertone(MONGO_COLL_FOR_SESSIONS,*args,**kwargs)

    def _get_user_session(self,*args,**kwargs):
        return self._find(MONGO_COLL_FOR_SESSIONS,*args,**kwargs)
    
    def _update_user_session(self,*args,**kwards):
        self._update(MONGO_COLL_FOR_SESSIONS,*args,**kwargs)

    
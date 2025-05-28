import hashlib
import pymongo


class MongoDB:
    def __init__(self):
        conn = pymongo.MongoClient("localhost", 27017)
        db = conn['videoinfo']
        self.collection = db['mediainfo']

    def find_all(self):
        return self.collection.find()

    def find_file(self, file_path):
        file_path_md5 = hashlib.md5(file_path.encode('utf-8')).hexdigest()
        file_info = list(self.collection.find({'_id': file_path_md5}))
        if file_info:
            return file_info[0]

    def insert_file(self, file_path, ffprobe_info):
        file_path_md5 = hashlib.md5(file_path.encode('utf-8')).hexdigest()
        ffprobe_info['_id'] = file_path_md5
        ffprobe_info['file_path'] = file_path
        try:
            self.collection.insert_one(ffprobe_info)
        except Exception as e:
            print(e)

    def update_file_info(self, file_path, update_dict):
        file_path_md5 = hashlib.md5(file_path.encode('utf-8')).hexdigest()
        self.collection.update_one({'_id': file_path_md5}, {"$set": update_dict})

    def drop_file(self, file_path):
        file_path_md5 = hashlib.md5(file_path.encode('utf-8')).hexdigest()
        return self.collection.delete_one({'_id': file_path_md5})

# MongoDB().find_file(r"C:\Data\Cinema\30.Minutes.or.Less.2011.720p.BluRay.x264-DON.mkv")

import hashlib
import json
import os

import pymongo

from ffmpeg import FFmpeg

parent_directory = os.path.dirname(os.path.abspath(__file__))

class FFprobeMongo:
    def __init__(self, file_path):
        self.file_path = file_path

        conn = pymongo.MongoClient("localhost", 27017)
        db = conn['videoinfo']
        self.collection = db['mediainfo']

        self.ffmpeg_scan()

    def ffmpeg_scan(self):
        ffprobe_directory = os.path.join(parent_directory, r'ffmpeg\bin\ffprobe.exe')
        ffprobe = FFmpeg(executable=ffprobe_directory).input(
            self.file_path,
            print_format="json",
            show_streams=None,
            show_format=None,
        )
        ffprobe_info = json.loads(ffprobe.execute())
        self.insert_db(ffprobe_info)


    def insert_db(self, ffprobe_info):
        file_path_md5 = hashlib.md5(self.file_path.encode('utf-8')).hexdigest()
        ffprobe_info['_id'] = file_path_md5
        ffprobe_info['file_path'] = self.file_path
        ffprobe_info['ffmpeg_scanners'] = {}
        try:
            self.collection.insert_one(ffprobe_info)
            print(self.file_path, 'успешно добавден в базу')
        except Exception as e:
            print(e)
            print(self.file_path, 'ОШИБКА, не добавлен в Mongo')

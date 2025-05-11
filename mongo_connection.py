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

# file = MongoDB().find_file(r"C:\Data\Cinema\30.Minutes.or.Less.2011.720p.BluRay.x264-DON.mkv")
# streams = file.get('streams')
# print(streams)
# video = list(filter(lambda x: x.get('codec_type') == 'video', streams))
# audio = list(filter(lambda x: x.get('codec_type') == 'audio', streams))
# subtitle = list(filter(lambda x: x.get('codec_type') == 'subtitle', streams))
# for key, val in video[0].items():
#     print(key, val, sep='| ')
# sub_tags = subtitle[0].get('tags')
# language = sub_tags.get('language')
# title = sub_tags.get('title')
# print(language, title)
#
# cover = list(filter(lambda x: x.get('codec_type') == 'video' and x.get('level') == -99, streams))
#
# codec_type = video[0].get('codec_type')
# r_frame_rate = video[0].get('r_frame_rate')
#
# format = file.get('format')
# print(format)

# def convert_duration(seconds, fps='25/1'):
#     try:
#         seconds = float(seconds)
#         fps = eval(fps)
#         hh = int(seconds // 3600)
#         mm = int((seconds % 3600) // 60)
#         ss = int((seconds % 3600) % 60 // 1)
#         ff = int(seconds % 1 * fps)
#         conv_data = f'{hh:02}:{mm:02}:{ss:02}.{ff:02}'
#         return conv_data
#     except Exception as e:
#         print(e)
#         return ''
# print(convert_duration('4983.168000', '24000/1001'))
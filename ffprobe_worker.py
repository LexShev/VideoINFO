import hashlib
import json
import os
import pymongo
from ffmpeg import FFmpeg

from PySide6.QtCore import QRunnable, Slot, Signal, QObject

parent_directory = os.path.dirname(os.path.abspath(__file__))

class WorkerSignals(QObject):
    started = Signal(dict, str)
    progress = Signal(int)
    finished = Signal(int)
    error = Signal(str, str)

class FFprobeWorker(QRunnable):
    def __init__(self, file_path, params):
        super().__init__()
        conn = pymongo.MongoClient("localhost", 27017)
        db = conn['videoinfo']
        self.collection = db['mediainfo']

        self.signals = WorkerSignals()
        self.params = params
        self.file_path = file_path

        self._is_running = True

    @Slot()
    def run(self):
        try:
            if not self._is_running:
                return
            self.signals.started.emit(self.params, self.file_path)
            self.signals.progress.emit(self.file_path, self.params.get('num'))
            self.ffmpeg_scan()
        except Exception as e:
            self.signals.error.emit(self.file_path, str(e))

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
        ffprobe_info['ffmpeg_scanners'] = {}
        try:
            self.collection.insert_one(ffprobe_info)
        except Exception as e:
            print(e)


import hashlib
import json
import os
import pymongo
from ffmpeg import FFmpeg

from PySide6.QtCore import QRunnable, Slot, Signal, QObject

parent_directory = os.path.dirname(os.path.abspath(__file__))

class WorkerSignals(QObject):
    started = Signal(str, dict)
    progress = Signal(str, dict)
    finished = Signal(int)
    error = Signal(str, str)
    scan_result = Signal(dict)

class FFprobeWorker(QRunnable):
    def __init__(self, file_path, params={}):
        super().__init__()
        conn = pymongo.MongoClient("localhost", 27017)
        db = conn['videoinfo']
        self.collection = db['mediainfo']

        self.signals = WorkerSignals()
        self.params = params
        self.file_path = file_path
        self.scan_result = None
        self._is_running = True

    @Slot()
    def run(self):
        try:
            if not self._is_running:
                return
            self.signals.started.emit(self.file_path, self.params)
            self.signals.progress.emit(self.file_path, self.params.get('num'))
            self.ffmpeg_scan()
            self.signals.scan_result.emit(self.scan_result)
        except Exception as e:
            print(e)
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
        self.scan_result = self.update_scan_result(ffprobe_info)
        self.insert_db(self.scan_result)


    def update_scan_result(self, ffprobe_info):
        ffprobe_info['_id'] = hashlib.md5(self.file_path.encode('utf-8')).hexdigest()
        ffprobe_info['file_path'] = self.file_path
        ffprobe_info['ffmpeg_scanners'] = {}
        return ffprobe_info

    def insert_db(self, ffprobe_info):
        try:
            self.collection.insert_one(ffprobe_info)
        except Exception as e:
            print(e)

    @property
    def result(self):
        return self.scan_result
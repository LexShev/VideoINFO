import hashlib
import json
import os
import subprocess
import pymongo

from PySide6.QtCore import QRunnable, Slot, Signal, QObject

parent_directory = os.path.dirname(os.path.abspath(__file__))

class WorkerSignals(QObject):
    started = Signal(dict, int)
    progress_01 = Signal(dict, str, int)
    progress_02 = Signal(str, int)
    finished = Signal(str, str)
    error = Signal(str, str)

class FFmpegWorker(QRunnable):
    def __init__(self, file_path, params, dur, r128_i=-23, r128_lra=11, r128_tp=-2):
        super().__init__()
        conn = pymongo.MongoClient("localhost", 27017)
        db = conn['videoinfo']
        self.collection = db['mediainfo']

        self.signals = WorkerSignals()
        self.params = params
        self.dur = dur
        self.file_path = file_path
        self.r128_i = r128_i
        self.r128_lra = r128_lra
        self.r128_tp = r128_tp

        self._is_running = True

    @Slot()
    def run(self):
        try:
            if not self._is_running:
                return
            # self.signals.progress_02.emit(self.file_path, 0)
            self.extract_normalization_data()
            self.waveforms()
            self.signals.progress_02.emit(self.file_path, self.params.get('total_p'))
            self.signals.finished.emit(self.file_path, f'Scanning for file {self.file_path} was finished')

        except Exception as e:
            self.signals.error.emit(self.file_path, str(e))

    def extract_normalization_data(self):
        try:
            command = [
                "ffmpeg",
                "-hide_banner",
                "-loglevel", "info",
                '-y',
                "-i",
                self.file_path,
                "-af",
                f"loudnorm=I={self.r128_i}:LRA={self.r128_lra}:TP={self.r128_tp}:print_format=json",
                "-f",
                "null",
                "-",
            ]
            output = subprocess.Popen(command,
                                      stdout=subprocess.PIPE,
                                      stderr=subprocess.STDOUT,
                                      universal_newlines=True,
                                      encoding='utf-8',
                                      bufsize=1
                                      )
            loudnorm_stats = []
            for line in output.stdout:
                if not self._is_running:
                    output.terminate()
                    break
                if 'input_i' in line:
                    loudnorm_stats.append(line.replace(',', ''))
                if 'input_tp' in line:
                    loudnorm_stats.append(line.replace(',', ''))
                if 'input_lra' in line:
                    loudnorm_stats.append(line.replace(',', ''))
                if 'input_thresh' in line:
                    loudnorm_stats.append(line.replace(',', ''))
                # Парсим прогресс (пример для FFmpeg)
                # print('line', line)
                if "frame=" in line:
                    cur_frame = line.split('frame=')[1].strip().split('fps=')[0]
                    if cur_frame:
                        percent = int(cur_frame)*100/self.dur
                        self.signals.progress_01.emit(self.params, self.file_path, percent)

            loudnorm_dict = json.loads('{'+'\n,'.join(loudnorm_stats)+'}')
            self.update_db(loudnorm_dict)
            # output_lines = output.strip().split("\n")
            # self.parse_loudnorm_output(output_lines)
        except subprocess.CalledProcessError as e:
            raise Exception(f"Ошибка при получении данных нормализации: {e.stderr.decode('utf-8')}")
        except Exception as e:
            raise Exception(f"Ошибка при получении данных нормализации: {e}")

    # def parse_loudnorm_output(self, output_lines):
    #     loudnorm_start = False
    #     loudnorm_end = False
    #     for index, line in enumerate(output_lines):
    #         if line.startswith("[Parsed_loudnorm"):
    #             loudnorm_start = index + 1
    #             continue
    #         if loudnorm_start and line.startswith("}"):
    #             loudnorm_end = index + 1
    #             break
    #     if not (loudnorm_start and loudnorm_end):
    #         raise Exception("Невозможно получить данные")
    #     try:
    #         loudnorm_stats = json.loads("\n".join(output_lines[loudnorm_start:loudnorm_end]))
    #         export_dict = {'input_i': loudnorm_stats['input_i'],
    #                        'input_tp': loudnorm_stats['input_tp'],
    #                        'input_lra': loudnorm_stats['input_lra'],
    #                        'input_thresh': loudnorm_stats['input_thresh']
    #                        }
    #         print(export_dict)
    #         self.update_db(export_dict)
    #         return export_dict
    #     except Exception as e:
    #         raise Exception(f"Невозможно получить данные. Ощибка JSON: {e.stderr.decode('utf-8')}")

    def update_db(self, export_dict):
        file_path_md5 = hashlib.md5(self.file_path.encode('utf-8')).hexdigest()
        self.collection.update_one({'_id': file_path_md5}, {"$set": {"ffmpeg_scanners": {'r128': export_dict}}})

    def waveforms(self):
        output_directory = os.path.join(parent_directory, 'waveforms')
        ffmpeg_directory = os.path.join(parent_directory, r'ffmpeg\bin\ffmpeg.exe')
        os.makedirs(output_directory, exist_ok=True)
        file_path_md5 = hashlib.md5(self.file_path.encode('utf-8')).hexdigest()
        image_file = os.path.join(output_directory, file_path_md5 + '.png')

        command = [
            ffmpeg_directory,
            "-hide_banner",
            "-loglevel", "info",
            '-y',
            "-i", self.file_path,
            "-filter_complex", "showwavespic=s=2000x800:scale=cbrt:draw=full",
            "-frames:v", '1',
            image_file
        ]
        output = subprocess.check_output(command, stderr=subprocess.STDOUT, universal_newlines=True, encoding='utf-8')
        print(output)

    def stop(self):
        self._is_running = False
import hashlib
import json
import os
import re
import subprocess
from fractions import Fraction
import pymongo
from PySide6.QtCore import QRunnable, Slot, Signal, QObject

from modules.database.mongo_connection import MongoDB
from modules.utils.settings import FFPROBE_DIR, FFMPEG_DIR, WAVE_DIR


def find_duration(file_info):
    streams = file_info.get('streams')
    video = list(filter(lambda x: x.get('codec_type') == 'video', streams))
    format = file_info.get('format')
    v_frame_rate = video[0].get('r_frame_rate')
    f_duration = format.get('duration', 25)
    f_frame_rate = format.get('r_frame_rate')
    if v_frame_rate:
        return float(f_duration) * float(Fraction(v_frame_rate))
    elif f_frame_rate:
        return float(f_duration) * float(Fraction(f_frame_rate))
    else:
        return 1

def convert_line(line):
    data = str(line.split(':')[1].strip().replace('"', '').replace(',', ''))
    return data

def convert_tf_to_sec(time):
    hh = int(time.split(':')[0])
    mm = int(time.split(':')[1])
    ss = int(time.split(':')[2])
    sec = (hh*3600)+(mm*60)+ss
    return sec


class WorkerSignals(QObject):
    started = Signal(dict)
    progress = Signal(dict)
    finished = Signal(dict)
    error = Signal(str, str)
    scan_result = Signal(str, "PyObject")

class FFprobeScan(QRunnable):
    def __init__(self, **kwargs):
        super().__init__()
        conn = pymongo.MongoClient("localhost", 27017)
        db = conn['videoinfo']
        self.collection = db['mediainfo']

        self.signals = WorkerSignals()
        self.file_path = kwargs.get('file_path')
        print('check', self.file_path)
        self.num = kwargs.get('num')
        self.total_files = kwargs.get('total_files')
        self.scan_result = None
        self._is_running = True

    @Slot()
    def run(self):
        try:
            if not self._is_running:
                return
            self.signals.started.emit({'file_path': self.file_path, 'num': self.num, 'total_files': self.total_files})
            self.ffmpeg_scan()
            self.signals.scan_result.emit(self.file_path, self.scan_result)
            self.signals.finished.emit({'file_path': self.file_path, 'num': self.num, 'total_files': self.total_files})
            self._is_running = False
        except Exception as e:
            self.signals.error.emit(self.file_path, str(e))
            self._is_running = False

    def ffmpeg_scan(self):
        command = [
            FFPROBE_DIR,
            "-hide_banner",
            "-loglevel", "quiet",
            "-i", f"{self.file_path}",
            "-print_format", "json",
            "-show_streams",
            "-show_format"
        ]
        print(command)

        output = subprocess.check_output(
            command,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            encoding='utf-8',
            errors='replace',
            bufsize=1,
            creationflags=subprocess.CREATE_NO_WINDOW,
            shell=False
        )
        ffprobe_info = json.loads(output)
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

class R128Scan(QRunnable):
    def __init__(self, **kwargs):
        super().__init__()
        self.file_path = kwargs.get('file_path')
        self.mongo = MongoDB()
        file_info = self.mongo.find_file(self.file_path)
        self.duration = find_duration(file_info)
        self.r128_i = kwargs.get('r128_i')
        self.r128_lra = kwargs.get('r128_lra')
        self.r128_tp = kwargs.get('r128_tp')
        self.ss_r128 = kwargs.get('ss_r128', '00:00:00')
        self.to_r128 = kwargs.get('to_r128', '99:00:00')
        self.num = kwargs.get('num')
        self.total_files = kwargs.get('total_files')
        self.scan_type = kwargs.get('scan_type')

        self.signals = WorkerSignals()
        self._is_running = True

        self.scan_result = {}

    @Slot()
    def run(self):
        try:
            if not self._is_running:
                return
            self.signals.started.emit({'file_path': self.file_path, 'num': self.num, 'total_files': self.total_files})
            self.extract_loudnorm_data()
            self.signals.scan_result.emit(self.file_path, self.scan_result)
            if not self._is_running:
                return
            self.waveforms()
            self.signals.finished.emit({'file_path': self.file_path, 'num': self.num, 'total_files': self.total_files})
            print('Анализ уровня громкости файла', self.file_path, 'завершён')
            self._is_running = False

        except Exception as e:
            self.signals.error.emit(self.file_path, str(e))
            self._is_running = False

    def extract_loudnorm_data(self):

        try:
            command = [
                FFMPEG_DIR,
                "-hide_banner",
                "-loglevel", "info",
                '-y',
                "-i", f"{self.file_path}",
                "-af",
                f"loudnorm=I={self.r128_i}:LRA={self.r128_lra}:TP={self.r128_tp}:print_format=json",
                "-f",
                "null",
                "-",
            ]
            output = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                encoding='utf-8',
                errors='replace',
                bufsize=1,
                creationflags=subprocess.CREATE_NO_WINDOW,
                shell=False
            )
            loudnorm_stats = []
            for line in output.stdout:
                if not self._is_running:
                    output.terminate()
                    break
                if "frame=" in line:
                    cur_frame = line.split('frame=')[1].strip().split('fps=')[0]
                    if cur_frame:
                        percent = int(cur_frame) * 100 / self.duration
                        params = {
                            'file_path': self.file_path,
                            'num': self.num,
                            'total_files': self.total_files,
                            'scan_type': self.scan_type,
                            'percent': percent
                        }
                        self.signals.progress.emit(params)

                if 'input_i' in line:
                    loudnorm_stats.append(line.replace(',', ''))
                if 'input_tp' in line:
                    loudnorm_stats.append(line.replace(',', ''))
                if 'input_lra' in line:
                    loudnorm_stats.append(line.replace(',', ''))
                if 'input_thresh' in line:
                    loudnorm_stats.append(line.replace(',', ''))
            output.wait()
            loudnorm_dict = json.loads('{' + '\n,'.join(loudnorm_stats) + '}')
            self.scan_result = loudnorm_dict
            if not self._is_running:
                return
            self.mongo.update_file_info(self.file_path, {"ffmpeg_scanners": {'r128': loudnorm_dict}})
        except subprocess.CalledProcessError as e:
            raise Exception(f"Ошибка при получении данных нормализации: {e.stderr.decode('utf-8')}")
        except Exception as e:
            raise Exception(f"Ошибка при получении данных нормализации: {e}")



    def waveforms(self):
        file_path_md5 = hashlib.md5(self.file_path.encode('utf-8')).hexdigest()
        image_file = os.path.join(WAVE_DIR, file_path_md5 + '.png')

        command = [
            FFMPEG_DIR,
            "-hide_banner",
            "-loglevel", "info",
            '-y',
            "-i", f"{self.file_path}",
            "-filter_complex", "showwavespic=s=2000x800:scale=cbrt:draw=full",
            "-frames:v", '1',
            image_file
        ]
        output = subprocess.check_output(
            command, stderr=subprocess.STDOUT, universal_newlines=True, encoding='utf-8',
            errors='replace', creationflags=subprocess.CREATE_NO_WINDOW, shell=False
        )
        self.mongo.update_file_info(self.file_path, {'waveforms': True})

    def stop(self):
        self._is_running = False

    @property
    def result(self):
        return self.scan_result

class BlackDetect(QRunnable):
    def __init__(self, **kwargs):
        super().__init__()
        self.mongo = MongoDB()
        self.signals = WorkerSignals()
        self._is_running = True
        self.selected_db = kwargs.get('selected_db')
        self.tbl_name = kwargs.get('tbl_name')
        self.file_path = kwargs.get('file_path')
        self.num = kwargs.get('num')
        self.total_files = kwargs.get('total_files')
        self.scan_type = kwargs.get('scan_type')
        self.blck_dur = kwargs.get('blck_dur')
        self.blck_thr = kwargs.get('blck_thr')
        self.blck_tc_in = kwargs.get('blck_tc_in', '00:00:00')
        self.blck_tc_out = kwargs.get('blck_tc_out', '99:00:00')
        file_info = self.mongo.find_file(self.file_path)
        self.duration = find_duration(file_info)

        if eval(kwargs.get('black_check')):
            self.blck_tc_in = self.duration - convert_tf_to_sec(self.blck_tc_out)

        self.scan_result = []

    @Slot()
    def run(self):
        try:
            if not self._is_running:
                return
            self.signals.started.emit({'file_path': self.file_path, 'num': self.num, 'total_files': self.total_files})
            self.black()
            if not self._is_running:
                return
            self.signals.finished.emit({'file_path': self.file_path, 'num': self.num, 'total_files': self.total_files})
            self.signals.scan_result.emit(self.file_path, self.scan_result)
            print('Анализ чёрного поля файла', self.file_path, 'завершён')
            self._is_running = False
        except Exception as e:
            self.signals.error.emit(self.file_path, str(e))
            self._is_running = False


    def black(self):
        if self.blck_tc_out == '00:00:00':
            self.blck_tc_out = '99:00:00'

        try:
            command = [
                f"{FFMPEG_DIR}",
                '-y',
                "-i", f"{self.file_path}",
                '-ss', self.blck_tc_in,
                '-to', self.blck_tc_out,
                '-vf', f"blackdetect=d={self.blck_dur}:pix_th={self.blck_thr}:pic_th=0.93",
                '-an',
                '-f', 'null',
                '-'
                ]
            output = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                encoding='utf-8',
                errors='replace',
                bufsize=1,
                creationflags=subprocess.CREATE_NO_WINDOW,
                shell=False
            )


            black_detect_list = []
            pattern = r"black_start:([\d.]+)\s+black_end:([\d.]+)\s+black_duration:([\d.]+)"
            for line in output.stdout:
                if not self._is_running:
                    output.terminate()
                    break
                if 'frame=' in line:
                    cur_frame = line.split('frame=')[1].strip().split('fps=')[0]
                    if cur_frame:
                        percent = int(cur_frame) * 100 / self.duration
                        params = {
                            'file_path': self.file_path,
                            'num': self.num,
                            'total_files': self.total_files,
                            'scan_type': self.scan_type,
                            'percent': percent
                        }
                        self.signals.progress.emit(params)

                match = re.search(pattern, line)
                if match:
                    black_start = float(match.group(1))
                    black_end = float(match.group(2))
                    if self.blck_tc_in != '00:00:00':
                        black_start =+ float(self.blck_tc_in)
                        black_end = + float(self.blck_tc_in)
                    black_detect_list.append({
                        'black_start': black_start,
                        'black_end': black_end,
                        'black_duration': float(match.group(3))
                    })

            output.wait()
            if not black_detect_list:
                black_detect_list = 'N/A'
            self.scan_result = black_detect_list
            if not self._is_running:
                return
            print(black_detect_list)
            self.mongo.update_file_info(self.file_path, {'ffmpeg_scanners.black_detect': black_detect_list})

        except subprocess.CalledProcessError as e:
            raise Exception(f"Ошибка при получении данных сканирования: {e.stderr.decode('utf-8')}")

        except Exception as e:
            raise Exception(f"Ошибка при получении данных сканирования: {e}")

    def stop(self):
        self._is_running = False

    @property
    def result(self):
        return self.scan_result

class SilenceDetect(QRunnable):
    def __init__(self, **kwargs):
        super().__init__()
        self.mongo = MongoDB()
        self.signals = WorkerSignals()
        self._is_running = True
        self.selected_db = kwargs.get('selected_db')
        self.tbl_name = kwargs.get('tbl_name')
        self.file_path = kwargs.get('file_path')
        self.num = kwargs.get('num')
        self.total_files = kwargs.get('total_files')
        self.scan_type = kwargs.get('scan_type')

        self.slnc_dur = kwargs.get('slnc_dur')
        self.slnc_noize = kwargs.get('slnc_noize')
        self.slnc_tc_in = kwargs.get('slnc_tc_in', '00:00:00')
        self.slnc_tc_out = kwargs.get('slnc_tc_out', '99:00:00')
        file_info = self.mongo.find_file(self.file_path)
        self.duration = find_duration(file_info)

        self.scan_result = []

    @Slot()
    def run(self):
        try:
            if not self._is_running:
                return
            self.signals.started.emit({'file_path': self.file_path, 'num': self.num, 'total_files': self.total_files})
            self.silence()
            if not self._is_running:
                return
            self.signals.finished.emit({'file_path': self.file_path, 'num': self.num, 'total_files': self.total_files})
            self.signals.scan_result.emit(self.file_path, self.scan_result)
            print('Анализ пропусков звука файла', self.file_path, 'завершён')
            self._is_running = False

        except Exception as e:
            self.signals.error.emit(self.file_path, str(e))
            self._is_running = False

    def silence(self):
        if  self.slnc_tc_out == '00:00:00':
            self.slnc_tc_out = '99:00:00'

        try:
            command = [
                f"{FFMPEG_DIR}",
                '-y',
                "-i", f"{self.file_path}",
                '-ss', self.slnc_tc_in,
                '-to', self.slnc_tc_out,
                '-af', f"silencedetect=n={self.slnc_noize}dB:d={self.slnc_dur}:noise=-45dB",
                '-f', 'null',
                '-'
            ]
            print(command)
            output = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                encoding='utf-8',
                errors='replace',
                bufsize=1,
                creationflags=subprocess.CREATE_NO_WINDOW,
                shell=False
            )

            silence_detect_list = []
            current_triple = {}
            for line in output.stdout:
                print(line)
                if not self._is_running:
                    output.terminate()
                    break

                start_match = re.search(r'silence_start:\s*([\d.]+)', line)
                if start_match:
                    silence_start = float(start_match.group(1))
                    if self.slnc_tc_in != '00:00:00':
                        silence_start = + float(self.slnc_tc_in)
                    current_triple['silence_start'] = silence_start
                    current_triple['silence_end'] = silence_start
                    current_triple['silence_duration'] = 0.0
                end_match = re.search(r'silence_end:\s*([\d.]+)\s*\|\s*silence_duration:\s*([\d.]+)', line)
                if end_match and current_triple:
                    silence_end = float(end_match.group(1))
                    if self.slnc_tc_in != '00:00:00':
                        silence_end = + float(self.slnc_tc_in)
                    current_triple['silence_end'] = silence_end
                    current_triple['silence_duration'] = float(end_match.group(2))
                    silence_detect_list.append(current_triple)
                    current_triple = {}
                else:
                    silence_detect_list.append(current_triple)
                    current_triple = {}

                if 'frame=' in line:
                    cur_frame = line.split('frame=')[1].strip().split('fps=')[0]
                    if cur_frame:
                        percent = int(cur_frame) * 100 / self.duration
                        params = {
                            'file_path': self.file_path,
                            'num': self.num,
                            'total_files': self.total_files,
                            'scan_type': self.scan_type,
                            'percent': percent
                        }
                        self.signals.progress.emit(params)

            output.wait()
            if not silence_detect_list:
                silence_detect_list = 'N/A'
            self.scan_result = silence_detect_list
            if not self._is_running:
                return
            self.mongo.update_file_info(self.file_path, {'ffmpeg_scanners.silence_detect': silence_detect_list})

        except subprocess.CalledProcessError as e:
            raise Exception(f"Ошибка при получении данных сканирования: {e.stderr.decode('utf-8')}")

        except Exception as e:
            raise Exception(f"Ошибка при получении данных сканирования: {e}")

    def stop(self):
        self._is_running = False

    @property
    def result(self):
        return self.scan_result

class FreezeDetect(QRunnable):
    def __init__(self, **kwargs):
        super().__init__()
        self.mongo = MongoDB()
        self.signals = WorkerSignals()
        self._is_running = True
        self.selected_db = kwargs.get('selected_db')
        self.tbl_name = kwargs.get('tbl_name')
        self.file_path = kwargs.get('file_path')
        self.num = kwargs.get('num')
        self.total_files = kwargs.get('total_files')
        self.scan_type = kwargs.get('scan_type')

        self.frz_dur = kwargs.get('frz_dur')
        self.frz_noize = kwargs.get('frz_noize')
        self.frz_tc_in = kwargs.get('frz_tc_in', '00:00:00')
        self.frz_tc_out = kwargs.get('frz_tc_out', '99:00:00')
        file_info = self.mongo.find_file(self.file_path)
        self.duration = find_duration(file_info)

        self.scan_result = []

    @Slot()
    def run(self):
        try:
            if not self._is_running:
                return
            self.signals.started.emit({'file_path': self.file_path, 'num': self.num, 'total_files': self.total_files})
            self.freeze()
            if not self._is_running:
                return
            self.signals.finished.emit({'file_path': self.file_path, 'num': self.num, 'total_files': self.total_files})
            self.signals.scan_result.emit(self.file_path, self.scan_result)
            print('Анализ застывшего кадра файла', self.file_path, 'завершён')
            self._is_running = False

        except Exception as e:
            self.signals.error.emit(self.file_path, str(e))
            self._is_running = False

    def freeze(self):
        if self.frz_tc_out == '00:00:00':
            self.frz_tc_out = '99:00:00'


        try:
            command = [
                f"{FFMPEG_DIR}",
                '-y',
                "-i", f"{self.file_path}",
                '-ss', self.frz_tc_in,
                '-to', self.frz_tc_out,
                '-vf', f"freezedetect=n={self.frz_noize}dB:d={self.frz_dur}",
                '-f', 'null',
                '-'
                ]
            print(command)
            output = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                encoding='utf-8',
                errors='replace',
                bufsize=1,
                creationflags=subprocess.CREATE_NO_WINDOW,
                shell=False
            )

            freeze_detect_list = []
            current_triple = {}
            for line in output.stdout:
                if not self._is_running:
                    output.terminate()
                    break

                start_match = re.search(r'lavfi\.freezedetect\.freeze_start:\s*([\d.]+)', line)
                if start_match:
                    freeze_start = float(start_match.group(1))
                    if self.frz_tc_in != '00:00:00':
                        freeze_start = + float(self.frz_tc_in)
                    current_triple['freeze_start'] = freeze_start
                    current_triple['freeze_end'] = freeze_start
                    current_triple['freeze_duration'] = 0.0

                duration_match = re.search(r'lavfi\.freezedetect\.freeze_duration:\s*([\d.]+)', line)
                if duration_match and current_triple:
                    current_triple['freeze_duration'] = float(duration_match.group(1))

                end_match = re.search(r'lavfi\.freezedetect\.freeze_end:\s*([\d.]+)', line)
                if end_match and current_triple:
                    freeze_end = float(end_match.group(1))
                    if self.frz_tc_in != '00:00:00':
                        freeze_end = + float(self.frz_tc_in)
                    current_triple['freeze_end'] = freeze_end
                    freeze_detect_list.append(current_triple)
                    current_triple = {}


                if 'frame=' in line:
                    cur_frame = line.split('frame=')[1].strip().split('fps=')[0]
                    if cur_frame:
                        percent = int(cur_frame) * 100 / self.duration
                        params = {
                            'file_path': self.file_path,
                            'num': self.num,
                            'total_files': self.total_files,
                            'scan_type': self.scan_type,
                            'percent': percent
                        }
                        self.signals.progress.emit(params)
            output.wait()
            if not freeze_detect_list:
                freeze_detect_list = 'N/A'
            self.scan_result = freeze_detect_list
            if not self._is_running:
                return
            self.mongo.update_file_info(self.file_path, {'ffmpeg_scanners.freeze_detect': freeze_detect_list})

        except subprocess.CalledProcessError as e:
            raise Exception(f"Ошибка при получении данных сканирования: {e.stderr.decode('utf-8')}")

        except Exception as e:
            raise Exception(f"Ошибка при получении данных сканирования: {e}")

    def stop(self):
        self._is_running = False

    @property
    def result(self):
        return self.scan_result

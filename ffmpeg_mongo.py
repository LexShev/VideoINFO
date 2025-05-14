import hashlib
import json
import os
import subprocess
import pymongo

parent_directory = os.path.dirname(os.path.abspath(__file__))


class R128:
    def __init__(self):
        conn = pymongo.MongoClient("localhost", 27017)
        db = conn['videoinfo']
        self.collection = db['mediainfo']


    def extract_normalization_data(self, file_path, r128_i=-23, r128_lra=11, r128_tp=-2):
        try:
            command = [
                "ffmpeg",
                "-hide_banner",
                "-loglevel", "info",
                '-y',
                "-i",
                file_path,
                "-af",
                f"loudnorm=I={r128_i}:LRA={r128_lra}:TP={r128_tp}:print_format=json",
                "-f",
                "null",
                "-",
            ]
            output = subprocess.check_output(command, stderr=subprocess.STDOUT, universal_newlines=True, encoding='utf-8')
            output_lines = output.strip().split("\n")
            self.parse_loudnorm_output(file_path, output_lines)
        except subprocess.CalledProcessError as e:
            raise Exception(f"Ошибка при получении данных нормализации: {e.stderr.decode('utf-8')}")
        except Exception as e:
            raise Exception(f"Ошибка при получении данных нормализации: {e}")

    def parse_loudnorm_output(self, file_path, output_lines):
        loudnorm_start = False
        loudnorm_end = False
        for index, line in enumerate(output_lines):
            if line.startswith("[Parsed_loudnorm"):
                loudnorm_start = index + 1
                continue
            if loudnorm_start and line.startswith("}"):
                loudnorm_end = index + 1
                break
        if not (loudnorm_start and loudnorm_end):
            raise Exception("Невозможно получить данные")
        try:
            loudnorm_stats = json.loads("\n".join(output_lines[loudnorm_start:loudnorm_end]))
            export_dict = {'input_i': loudnorm_stats['input_i'],
                           'input_tp': loudnorm_stats['input_tp'],
                           'input_lra': loudnorm_stats['input_lra'],
                           'input_thresh': loudnorm_stats['input_thresh']
                           }
            print(export_dict)
            self.waveforms(file_path)
            self.update_db(file_path, export_dict)
            return export_dict
        except Exception as e:
            raise Exception(f"Невозможно получить данные. Ощибка JSON: {e.stderr.decode('utf-8')}")

    def waveforms(self, file_path):
        output_directory = os.path.join(parent_directory, 'waveforms')
        ffmpeg_directory = os.path.join(parent_directory, r'ffmpeg\bin\ffmpeg.exe')
        os.makedirs(output_directory, exist_ok=True)
        file_path_md5 = hashlib.md5(file_path.encode('utf-8')).hexdigest()
        image_file = os.path.join(output_directory, file_path_md5 + '.png')

        command = [
            ffmpeg_directory,
            "-hide_banner",
            "-loglevel", "info",
            '-y',
            "-i", file_path,
            "-filter_complex", "showwavespic=s=2000x800:scale=cbrt:draw=full",
            "-frames:v", '1',
            image_file
        ]
        output = subprocess.check_output(command, stderr=subprocess.STDOUT, universal_newlines=True, encoding='utf-8')
        print(output)


    def update_db(self, file_path, export_dict):
        file_path_md5 = hashlib.md5(file_path.encode('utf-8')).hexdigest()
        self.collection.update_one({'_id': file_path_md5}, {"$set": {"ffmpeg_scanners": {'r128': export_dict}}})


# R128().extract_normalization_data(r'C:/Data/Showreel/Video Editing Showreel 2023_1080pFHR.mp4')
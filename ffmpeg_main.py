from __future__ import annotations

import os
import shutil

from PySide6.QtCore import QThread

from sqlite_connection import DataLite
from posql_connection import DataPos
# pip install python-ffmpeg

from ffmpeg import FFmpeg, Progress


def convert_tf_to_sec(time):
    hh = int(time.split(':')[0])
    mm = int(time.split(':')[1])
    ss = int(time.split(':')[2])
    sec = (hh*3600)+(mm*60)+ss
    return sec


def convert_sec_to_tf(time):
    hh = int(time // 3600)
    mm = int((time % 3600) // 60)
    ss = int((time % 3600) % 60 // 1)
    tf = f'{hh:02}:{mm:02}:{ss:02}'
    return tf

def convert_fr_to_tf(frame, fps):
    sec = frame/fps
    hh = int(sec // 3600)
    mm = int((sec % 3600) // 60)
    ss = int((sec % 3600) % 60 // 1)
    ff = int(sec % 1 * fps)
    tf = f'{hh:02}:{mm:02}:{ss:02}.{ff:03}'
    return tf


def convert_r128(line):
    data = float(line.split(':')[1].strip().replace('"', '').replace(',', ''))
    print(data)
    return data


def convert_blck(line):
    data = float(line.split(':')[1].strip().replace('"', '').replace(',', ''))
    return data


def convert_slnc(line):
    data = float(line.split(':')[1].strip().replace('"', '').replace(',', ''))
    return data


def convert_frz(line):
    data = float(line.split(':')[1].strip().replace('"', '').replace(',', ''))
    return data


class WaveformSingle():

    def __init__(self, selected_db, file_path):
        self.selected_db = selected_db
        self.extract_loudnorm_data(file_path)
    # super(Waveform_single, self).__init__()

    def extract_loudnorm_data(self, file_path):
        parent_directory = os.path.dirname(os.path.abspath(__file__))
        ffmpeg_directory = os.path.join(parent_directory, r'ffmpeg\bin\ffmpeg.exe')
        temp_audio_file = 'Wave_TEMP.wav'
        ffmpeg = (
            FFmpeg(executable=ffmpeg_directory)
            .input(file_path)
            .output(
                temp_audio_file,
                af="loudnorm=I=-23:LRA=11:TP=-2:print_format=json",
                f="null",
            )
        )

        @ffmpeg.on("start")
        def on_start(arguments: list[str]):
            print("arguments:", arguments)

        @ffmpeg.on("stderr")
        def on_stderr(line):
            # print(line)
            if self.selected_db == 'SQLITE':
                if 'input_i' in line:
                    DataLite().add_data(self.selected_db, 'input_i', convert_r128(line), file_path)
                if 'input_tp' in line:
                    DataLite().add_data(self.selected_db, 'input_tp', convert_r128(line), file_path)
                if 'input_lra' in line:
                    DataLite().add_data(self.selected_db, 'input_lra', convert_r128(line), file_path)
                if 'input_thresh' in line:
                    DataLite().add_data(self.selected_db, 'input_thresh', convert_r128(line), file_path)
                if 'target_offset' in line:
                    DataLite().add_data(self.selected_db, 'target_offset', convert_r128(line), file_path)
            else:
                if 'input_i' in line:
                    DataPos().add_data(self.selected_db, 'input_i', convert_r128(line), file_path)
                if 'input_tp' in line:
                    DataPos().add_data(self.selected_db, 'input_tp', convert_r128(line), file_path)
                if 'input_lra' in line:
                    DataPos().add_data(self.selected_db, 'input_lra', convert_r128(line), file_path)
                if 'input_thresh' in line:
                    DataPos().add_data(self.selected_db, 'input_thresh', convert_r128(line), file_path)
                if 'target_offset' in line:
                    DataPos().add_data(self.selected_db, 'target_offset', convert_r128(line), file_path)


        # @ffmpeg.on("progress")
        # def on_progress(progress: Progress):
        #     print(progress)

        @ffmpeg.on("completed")
        def on_completed():
            print("completed")

        @ffmpeg.on("terminated")
        def on_terminated():
            print("terminated")

        ffmpeg.execute()

        self.waveform(file_path)

    def waveform(self, file_path):
        parent_directory = os.path.dirname(os.path.abspath(__file__))
        ffmpeg_directory = os.path.join(parent_directory, r'ffmpeg\bin\ffmpeg.exe')
        file_name = os.path.basename(file_path)
        temp_image_file = os.path.splitext(file_name)[0]+'_TEMP.png'
        input_i = DataPos().read_bd('input_i', file_path)
        input_tp = DataPos().read_bd('input_tp', file_path)
        input_lra = DataPos().read_bd('input_lra', file_path)
        input_thresh = DataPos().read_bd('input_thresh', file_path)
        text_info = f'  I = {input_i}\t\t|\t\tLRA = {input_lra}\t\t|\t\tTP = {input_tp}\t\t|\t\tTHRESHOLD = {input_thresh}  '
        ffmpeg = (
            FFmpeg(executable=ffmpeg_directory)
            .option("y")
            .input(file_path)
            .output(
                temp_image_file,
                {"frames:v": "1"},
                filter_complex="showwavespic=s=2500x1000:scale=cbrt:draw=full[t],"
                               f"[t]drawtext=fontfile=NotoSans.ttf:text={text_info}:"
                               "fontcolor=white:fontsize=50:box=1:boxcolor=white@0.4:"
                               "boxborderw=10:x=(w-text_w)/2:y=h-th-100[f]",
                map='[f]',
            )
        )

        @ffmpeg.on("start")
        def on_start(arguments: list[str]):
            print("arguments:", arguments)

        @ffmpeg.on("stderr")
        def on_stderr(line):
            print("stderr:", line)

        @ffmpeg.on("progress")
        def on_progress(progress: Progress):
            print(progress)

        @ffmpeg.on("completed")
        def on_completed():
            print("completed")

        @ffmpeg.on("terminated")
        def on_terminated():
            print("terminated")

        ffmpeg.execute()
        os.startfile(os.path.normpath(temp_image_file))


class R128:
    def __init__(self, selected_db, tbl_name, file_path, i, lra, tp, ss_r128='00:00:00', to_r128='99:00:00'):
        self.selected_db = selected_db
        self.extract_loudnorm_data(tbl_name, file_path, i, lra, tp, ss_r128, to_r128)

    def extract_loudnorm_data(self, tbl_name, file_path, i, lra, tp, ss_r128, to_r128):

        parent_directory = os.path.dirname(os.path.abspath(__file__))
        ffmpeg_directory = os.path.join(parent_directory, r'ffmpeg\bin\ffmpeg.exe')
        temp_audio_file = 'Wave_TEMP.wav'
        ffmpeg = (
            FFmpeg(executable=ffmpeg_directory)
            .input(file_path,
                   ss=ss_r128,
                   to=to_r128
                   )
            .output(
                temp_audio_file,
                af=f"loudnorm=I={i}:LRA={lra}:TP={tp}:print_format=json",
                f="null",
            )
        )

        @ffmpeg.on("start")
        def on_start(arguments: list[str]):
            print("arguments:", arguments)

        @ffmpeg.on("stderr")
        def on_stderr(line):
            # print(line)
            if self.selected_db == 'SQLITE':
                if 'input_i' in line:
                    DataLite().add_data(tbl_name, 'input_i', convert_r128(line), file_path)
                if 'input_tp' in line:
                    DataLite().add_data(tbl_name, 'input_tp', convert_r128(line), file_path)
                if 'input_lra' in line:
                    DataLite().add_data(tbl_name, 'input_lra', convert_r128(line), file_path)
                if 'input_thresh' in line:
                    DataLite().add_data(tbl_name, 'input_thresh', convert_r128(line), file_path)
                if 'target_offset' in line:
                    DataLite().add_data(tbl_name, 'target_offset', convert_r128(line), file_path)
            else:
                if 'input_i' in line:
                    DataPos().add_data(tbl_name, 'input_i', convert_r128(line), file_path)
                if 'input_tp' in line:
                    DataPos().add_data(tbl_name, 'input_tp', convert_r128(line), file_path)
                if 'input_lra' in line:
                    DataPos().add_data(tbl_name, 'input_lra', convert_r128(line), file_path)
                if 'input_thresh' in line:
                    DataPos().add_data(tbl_name, 'input_thresh', convert_r128(line), file_path)
                if 'target_offset' in line:
                    DataPos().add_data(tbl_name, 'target_offset', convert_r128(line), file_path)

        @ffmpeg.on("progress")
        def on_progress(progress: Progress):
            str_progress = str(progress)[9:-1]
            frame = str_progress.split(', ')[0].split('=')[1]
            speed = str_progress.split(', ')[-1].split('=')[1]
            # tf = convert_fr_to_tf(int(frame), fps)
            print(frame, speed)

        @ffmpeg.on("completed")
        def on_completed():
            print("completed")

        @ffmpeg.on("terminated")
        def on_terminated():
            print("terminated")

        ffmpeg.execute()
        self.waveforms(tbl_name, file_path)

    def waveforms(self, tbl_name, file_path):
        parent_directory = os.path.dirname(os.path.abspath(__file__))
        output_directory = os.path.join(parent_directory, 'waveforms')
        ffmpeg_directory = os.path.join(parent_directory, r'ffmpeg\bin\ffmpeg.exe')
        os.makedirs(output_directory, exist_ok=True)
        file_name = os.path.basename(file_path)
        image_file = os.path.abspath(os.path.join(output_directory, os.path.splitext(file_name)[0] + '_WaveForm.png'))
        image_file_path = r'\\st33\Transcode\VideoINFO\waveforms'
        backup_file_path = os.path.join(image_file_path, tbl_name)
        os.makedirs(backup_file_path, exist_ok=True)

        ffmpeg = (
            FFmpeg(executable=ffmpeg_directory)
            .option("y")
            .input(file_path)
            .output(
                image_file,
                {"frames:v": "1"},
                filter_complex="showwavespic=s=2000x800:scale=cbrt:draw=full",
            )
        )

        @ffmpeg.on("start")
        def on_start(arguments: list[str]):
            print("arguments:", arguments)

        # @ffmpeg.on("stderr")
        # def on_stderr(line):
        #     print("stderr:", line)

        # @ffmpeg.on("progress")
        # def on_progress(progress: Progress):
        #     print(progress)

        @ffmpeg.on("completed")
        def on_completed():
            print("completed")

        @ffmpeg.on("terminated")
        def on_terminated():
            print("terminated")

        ffmpeg.execute()

        if self.selected_db == 'SQLITE':
            DataLite().add_data(tbl_name, 'waveform_path', image_file, file_path)
        else:
            DataPos().add_data(tbl_name, 'waveform_path', image_file, file_path)

        try:
            shutil.copy(image_file, backup_file_path)
        except Exception:
            pass

class BlackDetect():
    def __init__(self, selected_db, tbl_name, file_path, blck_dur, blck_thr, blck_tc_in='00:00:00',
                 blck_tc_out='99:00:00'):
        self.selected_db = selected_db
        self.black(tbl_name, file_path, blck_dur, blck_thr, blck_tc_in, blck_tc_out)

    def black(self, tbl_name, file_path, blck_dur, blck_thr, blck_tc_in, blck_tc_out):
        parent_directory = os.path.dirname(os.path.abspath(__file__))
        ffmpeg_directory = os.path.join(parent_directory, r'ffmpeg\bin\ffmpeg.exe')
        if blck_tc_out == '00:00:00':
            blck_tc_out = '99:00:00'
        black_start_list = []
        black_end_list = []
        black_duration_list = []

        temp_audio_file = 'Wave_TEMP.wav'
        ffmpeg = (
            FFmpeg(executable=ffmpeg_directory)
            .input(file_path,
                   ss=blck_tc_in,
                   to=blck_tc_out
                   )
            .output(
                temp_audio_file,
                vf=f"blackdetect=d={blck_dur}:pix_th={blck_thr}",
                f="null",
            )
        )

        @ffmpeg.on("start")
        def on_start(arguments: list[str]):
            print("arguments:", arguments)

        @ffmpeg.on("stderr")
        def on_stderr(line):
            # print(line)

            if 'frame=' in line:
                print(line)

            if 'blackdetect' in line:
                black_start = line.split(' ')[3].split(':')[1]
                if blck_tc_in != '00:00:00':
                    black_start = float(black_start) + float(blck_tc_in)
                black_start_list.append(black_start)
                black_end = line.split(' ')[4].split(':')[1]
                if blck_tc_in != '00:00:00':
                    black_end = float(black_end) + float(blck_tc_in)
                black_end_list.append(black_end)
                black_duration = line.split(' ')[5].split(':')[1]
                black_duration_list.append(black_duration)

        # @ffmpeg.on("progress")
        # def on_progress(progress: Progress):
        #     print(progress)

        @ffmpeg.on("completed")
        def on_completed():
            print("completed")

        @ffmpeg.on("terminated")
        def on_terminated():
            print("terminated")

        ffmpeg.execute()

        if self.selected_db == 'SQLITE':
            if black_start_list == []:
                DataLite().add_data(tbl_name, 'black_start', 'не найдено', file_path)
            else:
                DataLite().add_data(tbl_name, 'black_start', black_start_list, file_path)

            if black_end_list == []:
                DataLite().add_data(tbl_name, 'black_end', 'не найдено', file_path)
            else:
                DataLite().add_data(tbl_name, 'black_end', black_end_list, file_path)

            if black_duration_list == []:
                DataLite().add_data(tbl_name, 'black_duration', 'не найдено', file_path)
            else:
                DataLite().add_data(tbl_name, 'black_duration', black_duration_list, file_path)
        else:
            if black_start_list == []:
                DataPos().add_data(tbl_name, 'black_start', 'не найдено', file_path)
            else:
                DataPos().add_data(tbl_name, 'black_start', black_start_list, file_path)

            if black_end_list == []:
                DataPos().add_data(tbl_name, 'black_end', 'не найдено', file_path)
            else:
                DataPos().add_data(tbl_name, 'black_end', black_end_list, file_path)

            if black_duration_list == []:
                DataPos().add_data(tbl_name, 'black_duration', 'не найдено', file_path)
            else:
                DataPos().add_data(tbl_name, 'black_duration', black_duration_list, file_path)


class SilenceDetect():
    def __init__(self, selected_db, tbl_name, file_path, slnc_dur, slnc_noize, slnc_tc_in='00:00:00', slnc_tc_out='99:00:00'):
        self.selected_db = selected_db
        self.silence(tbl_name, file_path, slnc_dur, slnc_noize, slnc_tc_in, slnc_tc_out)

    def silence(self, tbl_name, file_path, slnc_dur, slnc_noize, slnc_tc_in, slnc_tc_out):
        parent_directory = os.path.dirname(os.path.abspath(__file__))
        ffmpeg_directory = os.path.join(parent_directory, r'ffmpeg\bin\ffmpeg.exe')
        if slnc_tc_out == '00:00:00':
            slnc_tc_out = '99:00:00'
        silence_start_list = []
        silence_end_list = []
        silence_duration_list = []

        temp_audio_file = 'Wave_TEMP.wav'
        ffmpeg = (
            FFmpeg(executable=ffmpeg_directory)
            # '-to', '00:10:00',
            .input(file_path,
                   ss=slnc_tc_in,
                   to=slnc_tc_out
                   )
            .output(
                temp_audio_file,
                af=f"silencedetect=n={slnc_noize}dB:d={slnc_dur}",
                f="null",
            )
        )

        @ffmpeg.on("start")
        def on_start(arguments: list[str]):
            print("arguments:", arguments)

        @ffmpeg.on("stderr")
        def on_stderr(line):
            # print(line)
            if 'silencedetect' in line and 'silence_start' in line:
                silence_start = line.split(' ')[4]
                if slnc_tc_in != '00:00:00':
                    silence_start = float(silence_start) + float(slnc_tc_in)
                silence_start_list.append(silence_start)
            if 'silencedetect' in line and 'silence_start' not in line:
                silence_end = line.split(' ')[4]
                if slnc_tc_in != '00:00:00':
                    silence_end = float(silence_end) + float(slnc_tc_in)
                silence_end_list.append(silence_end)
                silence_duration = line.split(' ')[7]
                silence_duration_list.append(silence_duration)

        @ffmpeg.on("completed")
        def on_completed():
            print("completed")

        @ffmpeg.on("terminated")
        def on_terminated():
            print("terminated")

        ffmpeg.execute()
        if self.selected_db == 'SQLITE':
            if silence_start_list == []:
                DataLite().add_data(tbl_name, 'silence_start', 'не найдено', file_path)
            else:
                DataLite().add_data(tbl_name,  'silence_start', silence_start_list, file_path)

            if silence_end_list == []:
                DataLite().add_data(tbl_name,  'silence_end', 'не найдено', file_path)
            else:
                DataLite().add_data(tbl_name,  'silence_end', silence_end_list, file_path)

            if silence_duration_list == []:
                DataLite().add_data(tbl_name,  'silence_duration', 'не найдено', file_path)
            else:
                DataLite().add_data(tbl_name,  'silence_duration', silence_duration_list, file_path)
        else:
            if silence_start_list == []:
                DataPos().add_data(tbl_name, 'silence_start', 'не найдено', file_path)
            else:
                DataPos().add_data(tbl_name, 'silence_start', silence_start_list, file_path)

            if silence_end_list == []:
                DataPos().add_data(tbl_name, 'silence_end', 'не найдено', file_path)
            else:
                DataPos().add_data(tbl_name, 'silence_end', silence_end_list, file_path)

            if silence_duration_list == []:
                DataPos().add_data(tbl_name, 'silence_duration', 'не найдено', file_path)
            else:
                DataPos().add_data(tbl_name, 'silence_duration', silence_duration_list, file_path)


class FreezeDetect():
    def __init__(self, selected_db, tbl_name, file_path, frz_dur, frz_noize, frz_tc_in='00:00:00', frz_tc_out='99:00:00'):
        self.selected_db = selected_db
        self.freeze(tbl_name, file_path, frz_dur, frz_noize, frz_tc_in, frz_tc_out)

    def freeze(self, tbl_name, file_path, frz_dur, frz_noize, frz_tc_in, frz_tc_out):
        parent_directory = os.path.dirname(os.path.abspath(__file__))
        ffmpeg_directory = os.path.join(parent_directory, r'ffmpeg\bin\ffmpeg.exe')
        if frz_tc_out == '00:00:00':
            frz_tc_out = '99:00:00'
        freeze_start_list = []
        freeze_end_list = []
        freeze_duration_list = []

        temp_audio_file = 'Wave_TEMP.wav'
        ffmpeg = (
            FFmpeg(executable=ffmpeg_directory)
            # '-to', '00:10:00',
            .input(file_path,
                   ss=frz_tc_in,
                   to=frz_tc_out
                   )
            .output(
                temp_audio_file,
                vf=f"freezedetect=n={frz_noize}dB:d={frz_dur}",
                f="null",

            )
        )

        @ffmpeg.on("start")
        def on_start(arguments: list[str]):
            print("arguments:", arguments)

        @ffmpeg.on("stderr")
        def on_stderr(line):
            # print(line)
            #     return line
            if 'freezedetect' in line:
                print(line)
            if 'freezedetect' in line and 'freeze_start' in line:
                freeze_start = line.split(' ')[4]
                if frz_tc_in != '00:00:00':
                    freeze_start = float(freeze_start) + float(frz_tc_in)
                freeze_start_list.append(freeze_start)
            if 'freezedetect' in line and 'freeze_duration' in line:
                freeze_duration = line.split(' ')[4]
                freeze_duration_list.append(freeze_duration)
            if 'freezedetect' in line and 'freeze_end' in line:
                freeze_end = line.split(' ')[4]
                if frz_tc_in != '00:00:00':
                    freeze_end = float(freeze_end) + float(frz_tc_in)
                freeze_end_list.append(freeze_end)

        @ffmpeg.on("completed")
        def on_completed():
            print("completed")

        #
        @ffmpeg.on("terminated")
        def on_terminated():
            print("terminated")

        ffmpeg.execute()
        if self.selected_db == 'SQLITE':
            if freeze_start_list == []:
                DataLite().add_data(tbl_name,  'freeze_start', 'не найдено', file_path)
            else:
                DataLite().add_data(tbl_name, 'freeze_start', freeze_start_list, file_path)

            if freeze_end_list == []:
                DataLite().add_data(tbl_name,  'freeze_end', 'не найдено', file_path)
            else:
                DataLite().add_data(tbl_name,  'freeze_end', freeze_end_list, file_path)

            if freeze_duration_list == []:
                DataLite().add_data(tbl_name,  'freeze_duration', 'не найдено', file_path)
            else:
                DataLite().add_data(tbl_name,  'freeze_duration', freeze_duration_list, file_path)
        else:
            if freeze_start_list == []:
                DataPos().add_data(tbl_name, 'freeze_start', 'не найдено', file_path)
            else:
                DataPos().add_data(tbl_name, 'freeze_start', freeze_start_list, file_path)

            if freeze_end_list == []:
                DataPos().add_data(tbl_name, 'freeze_end', 'не найдено', file_path)
            else:
                DataPos().add_data(tbl_name, 'freeze_end', freeze_end_list, file_path)

            if freeze_duration_list == []:
                DataPos().add_data(tbl_name, 'freeze_duration', 'не найдено', file_path)
            else:
                DataPos().add_data(tbl_name, 'freeze_duration', freeze_duration_list, file_path)


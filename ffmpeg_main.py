from __future__ import annotations

import os

from db_connection import Data
# pip install python-ffmpeg
from ffmpeg import FFmpeg, Progress


class WaveformSingle():

    def __init__(self, file_path):
        self.extract_normalization_data(file_path)
    # super(Waveform_single, self).__init__()

    def extract_normalization_data(self, file_path):
        temp_audio_file = 'Wave_TEMP.wav'
        ffmpeg = (
            FFmpeg()
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
            if 'input_i' in line:
                data = float(line.split(':')[1].strip().replace('"', '').replace(',', ''))
                # print('line:', data)
                Data().add_data('input_i', data, file_path)
                # self.cursor.execute('UPDATE Video SET input_i = ? WHERE file_path = ?', (data, file_path))
            if 'input_tp' in line:
                data = float(line.split(':')[1].strip().replace('"', '').replace(',', ''))
                Data().add_data('input_tp', data, file_path)
                # print('line:', data)
                # self.cursor.execute('UPDATE Video SET input_tp = ? WHERE file_path = ?', (data, file_path))
            if 'input_lra' in line:
                data = float(line.split(':')[1].strip().replace('"', '').replace(',', ''))
                Data().add_data('input_lra', data, file_path)
                # print('line:', data)
                # self.cursor.execute('UPDATE Video SET input_lra = ? WHERE file_path = ?', (data, file_path))
            if 'input_thresh' in line:
                data = float(line.split(':')[1].strip().replace('"', '').replace(',', ''))
                Data().add_data('input_thresh', data, file_path)
            if 'target_offset' in line:
                data = float(line.split(':')[1].strip().replace('"', '').replace(',', ''))
                Data().add_data('target_offset', data, file_path)
                # print('line:', data)
                # self.cursor.execute('UPDATE Video SET input_thresh = ? WHERE file_path = ?', (data, file_path))
                # self.connection.commit()
                # self.connection.close()

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
        file_name = os.path.basename(file_path)
        temp_image_file = os.path.splitext(file_name)[0]+'_TEMP.png'
        input_i = Data().read_bd('input_i', file_path)
        input_tp = Data().read_bd('input_tp', file_path)
        input_lra = Data().read_bd('input_lra', file_path)
        input_thresh = Data().read_bd('input_thresh', file_path)
        text_info = f'  I = {input_i}\t\t|\t\tLRA = {input_lra}\t\t|\t\tTP = {input_tp}\t\t|\t\tTHRESHOLD = {input_thresh}  '
        ffmpeg = (
            FFmpeg()
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


# class WaveformMulti():
#     def waveforms(self, file_path):
#         file_name = os.path.basename(file_path)
#         image_file = f'{file_name}_WAVE.png'
#         ffmpeg = (
#             FFmpeg()
#             .option("y")
#             .input(file_path)
#             .output(
#                 image_file,
#                 {"frames:v": "1"},
#                 filter_complex="showwavespic=s=1500x800:scale=cbrt:draw=full",
#             )
#         )
#
#         @ffmpeg.on("start")
#         def on_start(arguments: list[str]):
#             print("arguments:", arguments)
#
#         @ffmpeg.on("stderr")
#         def on_stderr(line):
#             print("stderr:", line)
#
#         @ffmpeg.on("progress")
#         def on_progress(progress: Progress):
#             print(progress)
#
#         @ffmpeg.on("completed")
#         def on_completed():
#             print("completed")
#
#         @ffmpeg.on("terminated")
#         def on_terminated():
#             print("terminated")
#
#         ffmpeg.execute()
#         print('Создание', image_file, 'успешно завершено')


class R128():
    def __init__(self, file_path, i, lra, tp):
        self.extract_normalization_data(file_path, i, lra, tp)

    # self.connection = sqlite3.connect('videoinfo_my.db', check_same_thread=False)
    # self.cursor = self.connection.cursor()

    def extract_normalization_data(self, file_path, i, lra, tp):

        temp_audio_file = 'Wave_TEMP.wav'
        ffmpeg = (
            FFmpeg()
            .input(file_path)
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
            if 'input_i' in line:
                data = float(line.split(':')[1].strip().replace('"', '').replace(',', ''))
                # print('line:', data)
                Data().add_data('input_i', data, file_path)
                # self.cursor.execute('UPDATE Video SET input_i = ? WHERE file_path = ?', (data, file_path))
            if 'input_tp' in line:
                data = float(line.split(':')[1].strip().replace('"', '').replace(',', ''))
                Data().add_data('input_tp', data, file_path)
                # print('line:', data)
                # self.cursor.execute('UPDATE Video SET input_tp = ? WHERE file_path = ?', (data, file_path))
            if 'input_lra' in line:
                data = float(line.split(':')[1].strip().replace('"', '').replace(',', ''))
                Data().add_data('input_lra', data, file_path)
                # print('line:', data)
                # self.cursor.execute('UPDATE Video SET input_lra = ? WHERE file_path = ?', (data, file_path))
            if 'input_thresh' in line:
                data = float(line.split(':')[1].strip().replace('"', '').replace(',', ''))
                Data().add_data('input_thresh', data, file_path)
            if 'target_offset' in line:
                data = float(line.split(':')[1].strip().replace('"', '').replace(',', ''))
                Data().add_data('target_offset', data, file_path)
                # print('line:', data)
                # self.cursor.execute('UPDATE Video SET input_thresh = ? WHERE file_path = ?', (data, file_path))
                # self.connection.commit()
                # self.connection.close()

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

        self.waveforms(file_path)
        # data_01(data)
        # return data

    # def waveform(self, file_path):
    #     parent_directory = os.path.dirname(os.path.abspath(__file__))
    #     output_directory = os.path.join(parent_directory, 'waveforms')
    #     os.makedirs(output_directory, exist_ok=True)
    #     file_name = os.path.basename(file_path)
    #     image_file = os.path.abspath(os.path.join(output_directory, os.path.splitext(file_name)[0]+'_WaveForm.png'))
    #
    #     input_i = Data().read_bd('input_i', file_path)
    #     input_tp = Data().read_bd('input_tp', file_path)
    #     input_lra = Data().read_bd('input_lra', file_path)
    #     input_thresh = Data().read_bd('input_thresh', file_path)
    #     text_info = f'  I = {input_i}\t\t|\t\tLRA = {input_lra}\t\t|\t\tTP = {input_tp}\t\t|\t\tTHRESHOLD = {input_thresh}  '
    #     # print('image_file', image_file)
    #     ffmpeg = (
    #         FFmpeg()
    #         .option("y")
    #         .input(file_path)
    #         .output(
    #             image_file,
    #             {"frames:v": "1"},
    #             filter_complex="showwavespic=s=2500x1000:scale=cbrt:draw=full[t],"
    #                            f"[t]drawtext=fontfile=NotoSans.ttf:text={text_info}:"
    #                            "fontcolor=white:fontsize=50:box=1:boxcolor=white@0.4:"
    #                            "boxborderw=10:x=(w-text_w)/2:y=h-th-100[f]",
    #             map='[f]',
    #         )
    #     )
    #
    #     @ffmpeg.on("start")
    #     def on_start(arguments: list[str]):
    #         print("arguments:", arguments)
    #
    #     @ffmpeg.on("stderr")
    #     def on_stderr(line):
    #         print("stderr:", line)
    #
    #     # @ffmpeg.on("progress")
    #     # def on_progress(progress: Progress):
    #     #     print(progress)
    #
    #     @ffmpeg.on("completed")
    #     def on_completed():
    #         print("completed")
    #
    #     @ffmpeg.on("terminated")
    #     def on_terminated():
    #         print("terminated")
    #
    #     ffmpeg.execute()
    #     Data().add_data('waveform_path', image_file, file_path)
    #     print('Создание', os.path.basename(image_file), 'успешно завершено')
    # os.startfile(os.path.normpath(temp_image_file))

    def waveforms(self, file_path):
        parent_directory = os.path.dirname(os.path.abspath(__file__))
        output_directory = os.path.join(parent_directory, 'waveforms')
        os.makedirs(output_directory, exist_ok=True)
        file_name = os.path.basename(file_path)
        image_file = os.path.abspath(os.path.join(output_directory, os.path.splitext(file_name)[0] + '_WaveForm.png'))

        # print('image_file', image_file)
        ffmpeg = (
            FFmpeg()
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
        Data().add_data('waveform_path', image_file, file_path)

class BlackDetect():
    def __init__(self, file_path, blck_dur, blck_thr, blck_tc_in, blck_tc_out):
        self.black(file_path, blck_dur, blck_thr, blck_tc_in, blck_tc_out)

    def black(self, file_path, blck_dur, blck_thr, blck_tc_in, blck_tc_out):
        black_start_list = []
        black_end_list = []
        black_duration_list = []

        temp_audio_file = 'Wave_TEMP.wav'
        ffmpeg = (
            FFmpeg()
            # .input(file_path,
            #        to='00:10:00')
            .input(file_path,
                   ss=blck_tc_in)
            .output(
                temp_audio_file,
                vf=f"blackdetect=d={blck_dur}:pix_th={blck_thr}",
                f="null",

                # -vf "blackdetect=d=0.05:pix_th=0.10" -an -f null - 2 > & 1
            )
        )

        #     "-f",
        #     "null",
        #     "-",
        # ]
        @ffmpeg.on("start")
        def on_start(arguments: list[str]):
            print("arguments:", arguments)

        @ffmpeg.on("stderr")
        def on_stderr(line):

            # print(line)
            #     return line
            # print(line)
            if 'frame=' in line:
                print(line)

            if 'blackdetect' in line:
                black_start = line.split(' ')[3].split(':')[1]
                black_start_list.append(black_start)
                black_end = line.split(' ')[4].split(':')[1]
                black_end_list.append(black_end)
                black_duration = line.split(' ')[5].split(':')[1]
                black_duration_list.append(black_duration)



        # @ffmpeg.on("progress")
        # def on_progress(progress: Progress):
        #     print(progress)

        @ffmpeg.on("completed")
        def on_completed():
            print("completed")

        #
        @ffmpeg.on("terminated")
        def on_terminated():
            print("terminated")

        ffmpeg.execute()

        if black_start_list == []:
            Data().add_data('black_start', 'не найдено', file_path)
        else:
            Data().add_data('black_start', black_start_list, file_path)

        if black_end_list == []:
            Data().add_data('black_end', 'не найдено', file_path)
        else:
            Data().add_data('black_end', black_end_list, file_path)

        if black_duration_list == []:
            Data().add_data('black_duration', 'не найдено', file_path)
        else:
            Data().add_data('black_duration', black_duration_list, file_path)

        # media = ffmpeg.execute()
        # media = json.loads(ffmpeg.execute())
        # return media


class SilenceDetect():
    def __init__(self, file_path, slnc_dur, slnc_noize, slnc_tc_in, slnc_tc_out):
        self.silence(file_path, slnc_dur, slnc_noize, slnc_tc_in, slnc_tc_out)

    def silence(self, file_path, slnc_dur, slnc_noize, slnc_tc_in, slnc_tc_out):
        silence_start_list = []
        silence_end_list = []
        silence_duration_list = []

        temp_audio_file = 'Wave_TEMP.wav'
        ffmpeg = (
            FFmpeg()
            # '-to', '00:10:00',
            .input(file_path)
            .output(
                temp_audio_file,
                af=f"silencedetect=n={slnc_noize}dB:d={slnc_dur}",
                f="null",

                # -vf "blackdetect=d=0.05:pix_th=0.10" -an -f null - 2 > & 1
            )
        )

        #     "-f",
        #     "null",
        #     "-",
        # ]
        @ffmpeg.on("start")
        def on_start(arguments: list[str]):
            print("arguments:", arguments)

        @ffmpeg.on("stderr")
        def on_stderr(line):
            print(line)
            #     return line
            # print(line)
            if 'silencedetect' in line and 'silence_start' in line:
                silence_start = line.split(' ')[4]
                silence_start_list.append(silence_start)
            if 'silencedetect' in line and 'silence_start' not in line:
                silence_end = line.split(' ')[4]
                silence_end_list.append(silence_end)
                silence_duration = line.split(' ')[7]
                silence_duration_list.append(silence_duration)

        @ffmpeg.on("completed")
        def on_completed():
            print("completed")

        #
        @ffmpeg.on("terminated")
        def on_terminated():
            print("terminated")

        ffmpeg.execute()
        if silence_start_list != []:
            Data().add_data('silence_start', silence_start_list, file_path)
        if silence_end_list != []:
            Data().add_data('silence_end', silence_end_list, file_path)
        if silence_duration_list != []:
            Data().add_data('silence_duration', silence_duration_list, file_path)


class FreezeDetect():
    def __init__(self, file_path, frz_dur, frz_noize, frz_tc_in, frz_tc_out):
        self.freeze(file_path, frz_dur, frz_noize, frz_tc_in, frz_tc_out)

    def freeze(self, file_path, frz_dur, frz_noize, frz_tc_in, frz_tc_out):
        freeze_start_list = []
        freeze_end_list = []
        freeze_duration_list = []

        temp_audio_file = 'Wave_TEMP.wav'
        ffmpeg = (
            FFmpeg()
            # '-to', '00:10:00',
            .input(file_path)
            .output(
                temp_audio_file,
                vf=f"freezedetect=n={frz_noize}dB:d={frz_dur}",
                f="null",

            )
        )

        #     "-f",
        #     "null",
        #     "-",
        # ]
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
                freeze_start_list.append(freeze_start)
            if 'freezedetect' in line and 'freeze_duration' in line:
                freeze_duration = line.split(' ')[4]
                freeze_duration_list.append(freeze_duration)
            if 'freezedetect' in line and 'freeze_end' in line:
                freeze_end = line.split(' ')[4]
                freeze_end_list.append(freeze_end)

        @ffmpeg.on("completed")
        def on_completed():
            print("completed")

        #
        @ffmpeg.on("terminated")
        def on_terminated():
            print("terminated")

        ffmpeg.execute()

        if freeze_start_list != []:
            Data().add_data('freeze_start', freeze_start_list, file_path)
        if freeze_end_list != []:
            Data().add_data('freeze_end', freeze_end_list, file_path)
        if freeze_duration_list != []:
            Data().add_data('freeze_duration', freeze_duration_list, file_path)
# def data_01(data):
#     loudnorm_stats = json.loads("\n".join(data))
#     # print(loudnorm_stats['input_i'])
#     # add_param(self, file_path, all_headers, data):
#     return loudnorm_stats['input_i']


# file_path = r"C:\Users\a.shevchenko\Videos\Test_03.mp4"
# r128 = (R128.extract_normalization_data(file_path))
# print(r128)

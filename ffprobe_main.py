import json

import os
from sqlite_connection import DataLite
from posql_connection import DataPos
from ffmpeg import FFmpeg


def main(file_path):
    parent_directory = os.path.dirname(os.path.abspath(__file__))
    ffprobe_directory = os.path.join(parent_directory, r'ffmpeg\bin\ffprobe.exe')
    ffprobe = FFmpeg(executable=ffprobe_directory).input(
        file_path,
        print_format="json",  # ffprobe will output the results in JSON format
        show_streams=None,
        show_format=None,
    )

    media = json.loads(ffprobe.execute())
    return media


ff_dict = {}

def make_dict(header, value, file_path):
    pass
    # ff_dict[header] = value
    # print(ff_dict)
    # return ff_dict


def write_dict(make_dict, file_path):
    pass
    # print('test', make_dict)


video_probe_list = ['codec_name', 'profile', 'codec_type', 'width', 'height',
                    'sample_aspect_ratio', 'display_aspect_ratio', 'pix_fmt', 'level',
                    'color_range', 'color_space', 'field_order', 'r_frame_rate', 'tags']

audio_probe_list = ['codec_name', 'codec_type', 'sample_rate', 'channels',
                    'channel_layout', 'bit_rate', 'tags']

subtitle_probe_list = ['codec_name', 'start_time', 'tags']

cover_probe_list = ['codec_name', 'profile', 'width', 'height', 'color_space', 'tags']

format_probe_list = ['filename', 'format_name', 'duration', 'size', 'bit_rate', 'tags']

tag_probe_list = ['language', 'title', 'TITLE', 'name', 'NAME', 'handler_name', 'encoder', 'ENCODER']

class Info:
    def __init__(self, selected_db, tbl_name, file_path):
        self.file_path = file_path
        if selected_db == 'SQLITE':
            DataLite().create_table(tbl_name)
            DataLite().add_video(tbl_name, file_path)
        else:
            DataPos().create_table(tbl_name)
            DataPos().add_video(tbl_name, file_path)
        main_probe = main(file_path)
        probe = main_probe.copy()
        #super(Info, self).__init__()

        # Data().begin_additing()
        try:
            self.date_modified(selected_db, tbl_name, file_path)
        except Exception:
            pass

        try:
            self.ffprobe_video(selected_db, tbl_name, file_path, probe)
        except Exception:
            pass

        try:
            self.ffprobe_audio(selected_db, tbl_name, file_path, probe)
        except Exception:
            pass

        try:
            self.ffprobe_subtitle(selected_db, tbl_name, file_path, probe)
        except Exception:
            pass

        try:
            self.ffprobe_cover(selected_db, tbl_name, file_path, probe)
        except Exception:
            pass

        try:
            self.ffprobe_format(selected_db, tbl_name, file_path, probe)
        except Exception:
            pass

        if selected_db == 'SQLITE':
            DataLite().conf_bd()
        else:
            DataPos().conf_bd()

    def date_modified(self, selected_db, tbl_name, file_path):
        date_modified = os.path.getmtime(file_path)
        if selected_db == 'SQLITE':
            DataLite().add_ffprobe_data(tbl_name, 'date_modified', date_modified, file_path)
        else:
            DataPos().add_ffprobe_data(tbl_name, 'date_modified', date_modified, file_path)
        print('date_modified', date_modified)

    def ffprobe_video(self, selected_db, tbl_name, file_path, probe):
        max_index = probe['streams'][-1]['index']
        v_count = 0
        for i in range(0, max_index + 1):
            probe_stream = probe['streams'][i]
            if (probe['streams'][i]['codec_type'] == 'video' and probe['streams'][i]['codec_name'] != 'mjpeg'
                    and probe['streams'][i]['codec_name'] != 'png'):
                v_count += 1
                for video_probe in video_probe_list:
                    video_probe_name = f'v{v_count:02}_{video_probe}'
                    try:
                        if video_probe != 'tags':
                            video_info = probe_stream[video_probe]
                            if selected_db == 'SQLITE':
                                DataLite().add_ffprobe_data(tbl_name, video_probe_name, video_info, file_path)
                            else:
                                DataPos().add_ffprobe_data(tbl_name, video_probe_name, video_info, file_path)
                            print(video_probe_name, video_info)

                        if video_probe == 'tags':
                            for tag_probe in tag_probe_list:
                                tag_probe_name = f'v{v_count:02}_{tag_probe}'
                                try:
                                    video_info_tag = probe_stream['tags'][tag_probe]
                                    if selected_db == 'SQLITE':
                                        DataLite().add_ffprobe_data(tbl_name, tag_probe_name, video_info_tag, file_path)
                                    else:
                                        DataPos().add_ffprobe_data(tbl_name, tag_probe_name, video_info_tag, file_path)
                                    # make_dict(tag_probe_name, video_info_tag, file_path)
                                    print(tag_probe_name, video_info_tag)
                                except Exception:
                                    pass
                    except Exception:
                        video_info = 'нет данных'
                        if selected_db == 'SQLITE':
                            DataLite().add_ffprobe_data(tbl_name, video_probe_name, video_info, file_path)
                        else:
                            DataPos().add_ffprobe_data(tbl_name, video_probe_name, video_info, file_path)
                        print(video_probe_name, video_info)

    def ffprobe_audio(self, selected_db, tbl_name, file_path, probe):
        max_index = probe['streams'][-1]['index']
        a_count = 0
        for i in range(0, max_index + 1):
            probe_stream = probe['streams'][i]
            if probe['streams'][i]['codec_type'] == 'audio':
                a_count += 1
                for audio_probe in audio_probe_list:
                    audio_probe_name = f'a{a_count:02}_{audio_probe}'
                    try:
                        if audio_probe != 'tags':
                            audio_info = probe_stream[audio_probe]
                            if selected_db == 'SQLITE':
                                DataLite().add_ffprobe_data(tbl_name, audio_probe_name, audio_info, file_path)
                            else:
                                DataPos().add_ffprobe_data(tbl_name, audio_probe_name, audio_info, file_path)
                            print(audio_probe_name, audio_info)
                        if audio_probe == 'tags':
                            for tag_probe in tag_probe_list:
                                tag_probe_name = f'a{a_count:02}_{tag_probe}'
                                try:
                                    audio_info_tag = probe_stream['tags'][tag_probe]
                                    if selected_db == 'SQLITE':
                                        DataLite().add_ffprobe_data(tbl_name, tag_probe_name, audio_info_tag, file_path)
                                    else:
                                        DataPos().add_ffprobe_data(tbl_name, tag_probe_name, audio_info_tag, file_path)
                                    print(tag_probe_name, audio_info_tag)
                                except Exception:
                                    pass

                    except Exception:
                        audio_info = 'нет данных'
                        if selected_db == 'SQLITE':
                            DataLite().add_ffprobe_data(tbl_name, audio_probe_name, audio_info, file_path)
                        else:
                            DataPos().add_ffprobe_data(tbl_name, audio_probe_name, audio_info, file_path)
                        print(audio_probe_name, audio_info)
        if selected_db == 'SQLITE':
            DataLite().add_ffprobe_data(tbl_name, 'audio_streams', a_count, file_path)
        else:
            DataPos().add_ffprobe_data(tbl_name, 'audio_streams', a_count, file_path)

    def ffprobe_subtitle(self, selected_db, tbl_name, file_path, probe):
        max_index = probe['streams'][-1]['index']
        s_count = 0
        for i in range(0, max_index + 1):
            probe_stream = probe['streams'][i]
            if probe['streams'][i]['codec_type'] == 'subtitle':
                s_count += 1
                for subtitle_probe in subtitle_probe_list:
                    subtitle_probe_name = f's{s_count:02}_{subtitle_probe}'
                    try:
                        if subtitle_probe != 'tags':
                            subtitle_info = probe_stream[subtitle_probe]
                            if selected_db == 'SQLITE':
                                DataLite().add_ffprobe_data(tbl_name, subtitle_probe_name, subtitle_info, file_path)
                            else:
                                DataPos().add_ffprobe_data(tbl_name, subtitle_probe_name, subtitle_info, file_path)
                            print(subtitle_probe_name, subtitle_info)
                        if subtitle_probe == 'tags':
                            for tag_probe in tag_probe_list:
                                tag_probe_name = f's{s_count:02}_{tag_probe}'
                                try:
                                    subtitle_info_tag = probe_stream['tags'][tag_probe]
                                    if selected_db == 'SQLITE':
                                        DataLite().add_ffprobe_data(tbl_name, tag_probe_name, subtitle_info_tag, file_path)
                                    else:
                                        DataPos().add_ffprobe_data(tbl_name, tag_probe_name, subtitle_info_tag, file_path)
                                    print(tag_probe_name, subtitle_info_tag)
                                except Exception:
                                    pass
                    except Exception:
                        subtitle_info = 'нет данных'
                        if selected_db == 'SQLITE':
                            DataLite().add_ffprobe_data(tbl_name, subtitle_probe_name, subtitle_info, file_path)
                        else:
                            DataPos().add_ffprobe_data(tbl_name, subtitle_probe_name, subtitle_info, file_path)
                        print(subtitle_probe_name, subtitle_info)

    def ffprobe_cover(self, selected_db, tbl_name, file_path, probe):
        max_index = probe['streams'][-1]['index']
        c_count = 0
        for i in range(0, max_index + 1):
            probe_stream = probe['streams'][i]
            if (probe['streams'][i]['codec_type'] == 'video' and probe['streams'][i]['codec_name'] == 'png'
                    or probe['streams'][i]['codec_type'] == 'video' and probe['streams'][i]['codec_name'] == 'mjpeg'):
                c_count += 1
                for cover_probe in cover_probe_list:
                    cover_probe_name = f'c{c_count:02}_{cover_probe}'
                    try:
                        if cover_probe != 'tags':
                            cover_info = probe_stream[cover_probe]
                            if selected_db == 'SQLITE':
                                DataLite().add_ffprobe_data(tbl_name, cover_probe_name, cover_info, file_path)
                            else:
                                DataPos().add_ffprobe_data(tbl_name, cover_probe_name, cover_info, file_path)
                            print(cover_probe_name, cover_info)
                    except Exception:
                        cover_info = 'нет данных'
                        if selected_db == 'SQLITE':
                            DataLite().add_ffprobe_data(tbl_name, cover_probe_name, cover_info, file_path)
                        else:
                            DataPos().add_ffprobe_data(tbl_name, cover_probe_name, cover_info, file_path)
                        print(cover_probe_name, cover_info)

    def ffprobe_format(self, selected_db, tbl_name, file_path, probe):
        probe_format = probe['format']
        # print('probe_format', probe_format)
        for format_probe in format_probe_list:
            format_probe_name = f'f_{format_probe}'
            try:
                if format_probe != 'tags':
                    format_info = probe_format[format_probe]
                    if selected_db == 'SQLITE':
                        DataLite().add_ffprobe_data(tbl_name, format_probe_name, format_info, file_path)
                    else:
                        DataPos().add_ffprobe_data(tbl_name, format_probe_name, format_info, file_path)
                    print(format_probe_name, format_info)
                if format_probe == 'tags':
                    for tag_probe in tag_probe_list:
                        tag_probe_name = f'f_{tag_probe}'
                        try:
                            format_info_tag = probe_format['tags'][tag_probe]
                            if selected_db == 'SQLITE':
                                DataLite().add_ffprobe_data(tbl_name, tag_probe_name, format_info_tag, file_path)
                            else:
                                DataPos().add_ffprobe_data(tbl_name, tag_probe_name, format_info_tag, file_path)
                            print(tag_probe_name, format_info_tag)
                        except Exception:
                            pass
            except Exception:
                format_info = 'нет данных'
                if selected_db == 'SQLITE':
                    DataLite().add_ffprobe_data(tbl_name, format_probe_name, format_info, file_path)
                else:
                    DataPos().add_ffprobe_data(tbl_name, format_probe_name, format_info, file_path)
                print(format_probe_name, format_info)

        print('_' * 50)


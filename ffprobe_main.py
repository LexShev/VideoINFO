import json

from db_connection import Data
from ffmpeg import FFmpeg


def main(file_path):
    ffprobe = FFmpeg(executable="ffprobe").input(
        file_path,
        print_format="json",  # ffprobe will output the results in JSON format
        show_streams=None,
        show_format=None,
    )

    media = json.loads(ffprobe.execute())
    print(media)
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
    def __init__(self, file_path):
        self.file_path = file_path
        Data().add_video(file_path)
        main_probe = main(file_path)
        probe = main_probe.copy()
        #super(Info, self).__init__()

        # Data().begin_additing()
        try:
            self.ffprobe_video(file_path, probe)
        except Exception:
            pass

        try:
            self.ffprobe_audio(file_path, probe)
        except Exception:
            pass

        try:
            self.ffprobe_subtitle(file_path, probe)
        except Exception:
            pass

        try:
            self.ffprobe_cover(file_path, probe)
        except Exception:
            pass

        try:
            self.ffprobe_format(file_path, probe)
        except Exception:
            pass

        Data().conf_bd()
        # write_dict(make_dict, file_path)


    # def res_ffprobe(self, file_path):
    #     all_dict = []
    #     # all_res = {}
    #
    #     file_name = os.path.basename(file_path)
    #     main_probe = main(file_path)
    #     probe = main_probe.copy()
    #
    #     # Data().add_video(file_path)
    #     try:
    #         res_vid = self.ffprobe_video(file_path, file_name, probe)
    #         res_aud = self.ffprobe_audio(file_path, file_name, probe)
    #         res_sub = self.ffprobe_subtitle(file_path, file_name, probe)
    #         res_cov = self.ffprobe_cover(file_path, file_name, probe)
    #         res_form = self.ffprobe_format(file_path, file_name, probe)
    #
    #         all_res.update(res_vid)
    #         all_res.update(res_aud)
    #         all_res.update(res_sub)
    #         all_res.update(res_cov)
    #         all_res.update(res_form)
    #
    #     except Exception:
    #         all_res = {file_path: 'Файл повреждён'}
    #         print('Файл повреждён')

        # all_dict.append(all_res)
        # print('all_res:', all_res)
        # print('all_dict:', all_dict)

        # return all_res
        # media_dict, media_headers, media_data = self.ffprobe_format()
        # print(media_dict)
        # print(media_headers)
        # print(media_data)

    def ffprobe_video(self, file_path, probe):
        max_index = probe['streams'][-1]['index']
        v_count = 0
        for i in range(0, max_index + 1):
            probe_stream = probe['streams'][i]
            if (probe['streams'][i]['codec_type'] == 'video' and probe['streams'][i]['codec_name'] != 'mjpeg'
                    and probe['streams'][i]['codec_name'] != 'png'):
                v_count += 1
                for video_probe in video_probe_list:
                    video_probe_name = f'V{v_count:02}_{video_probe}'
                    try:
                        if video_probe != 'tags':
                            video_info = probe_stream[video_probe]
                            Data().add_ffprobe_data(video_probe_name, video_info, file_path)
                            print(video_probe_name, video_info)

                        if video_probe == 'tags':
                            for tag_probe in tag_probe_list:
                                tag_probe_name = f'V{v_count:02}_{tag_probe}'
                                try:
                                    video_info_tag = probe_stream['tags'][tag_probe]
                                    Data().add_ffprobe_data(tag_probe_name, video_info_tag, file_path)
                                    # make_dict(tag_probe_name, video_info_tag, file_path)
                                    print(tag_probe_name, video_info_tag)
                                except Exception:
                                    pass
                    except Exception:
                        video_info = 'нет данных'
                        Data().add_ffprobe_data(video_probe_name, video_info, file_path)
                        print(video_probe_name, video_info)

    def ffprobe_audio(self,file_path, probe):
        max_index = probe['streams'][-1]['index']
        a_count = 0
        for i in range(0, max_index + 1):
            probe_stream = probe['streams'][i]
            if probe['streams'][i]['codec_type'] == 'audio':
                a_count += 1
                for audio_probe in audio_probe_list:
                    audio_probe_name = f'A{a_count:02}_{audio_probe}'
                    try:
                        if audio_probe != 'tags':
                            audio_info = probe_stream[audio_probe]
                            Data().add_ffprobe_data(audio_probe_name, audio_info, file_path)
                            print(audio_probe_name, audio_info)
                        if audio_probe == 'tags':
                            for tag_probe in tag_probe_list:
                                tag_probe_name = f'A{a_count:02}_{tag_probe}'
                                try:
                                    audio_info_tag = probe_stream['tags'][tag_probe]
                                    Data().add_ffprobe_data(tag_probe_name, audio_info_tag, file_path)
                                    print(tag_probe_name, audio_info_tag)
                                except Exception:
                                    pass

                    except Exception:
                        audio_info = 'нет данных'
                        Data().add_ffprobe_data(audio_probe_name, audio_info, file_path)
                        print(audio_probe_name, audio_info)
        Data().add_ffprobe_data('audio_streams', a_count, file_path)

    def ffprobe_subtitle(self, file_path, probe):
        max_index = probe['streams'][-1]['index']
        s_count = 0
        for i in range(0, max_index + 1):
            probe_stream = probe['streams'][i]
            if probe['streams'][i]['codec_type'] == 'subtitle':
                s_count += 1
                for subtitle_probe in subtitle_probe_list:
                    subtitle_probe_name = f'S{s_count:02}_{subtitle_probe}'
                    try:
                        if subtitle_probe != 'tags':
                            subtitle_info = probe_stream[subtitle_probe]
                            Data().add_ffprobe_data(subtitle_probe_name, subtitle_info, file_path)
                            print(subtitle_probe_name, subtitle_info)
                        if subtitle_probe == 'tags':
                            for tag_probe in tag_probe_list:
                                tag_probe_name = f'S{s_count:02}_{tag_probe}'
                                try:
                                    subtitle_info_tag = probe_stream['tags'][tag_probe]
                                    Data().add_ffprobe_data(tag_probe_name, subtitle_info_tag, file_path)
                                    print(tag_probe_name, subtitle_info_tag)
                                except Exception:
                                    pass
                    except Exception:
                        subtitle_info = 'нет данных'
                        Data().add_ffprobe_data(subtitle_probe_name, subtitle_info, file_path)
                        print(subtitle_probe_name, subtitle_info)

    def ffprobe_cover(self, file_path, probe):
        max_index = probe['streams'][-1]['index']
        c_count = 0
        for i in range(0, max_index + 1):
            probe_stream = probe['streams'][i]
            if (probe['streams'][i]['codec_type'] == 'video' and probe['streams'][i]['codec_name'] == 'png'
                    or probe['streams'][i]['codec_type'] == 'video' and probe['streams'][i]['codec_name'] == 'mjpeg'):
                c_count += 1
                for cover_probe in cover_probe_list:
                    cover_probe_name = f'C{c_count:02}_{cover_probe}'
                    try:
                        if cover_probe != 'tags':
                            cover_info = probe_stream[cover_probe]
                            Data().add_ffprobe_data(cover_probe_name, cover_info, file_path)
                            print(cover_probe_name, cover_info)
                    except Exception:
                        cover_info = 'нет данных'
                        Data().add_ffprobe_data(cover_probe_name, cover_info, file_path)
                        print(cover_probe_name, cover_info)


    def ffprobe_format(self, file_path, probe):
        probe_format = probe['format']
        # print('probe_format', probe_format)
        for format_probe in format_probe_list:
            format_probe_name = f'F_{format_probe}'
            try:
                if format_probe != 'tags':
                    format_info = probe_format[format_probe]
                    Data().add_ffprobe_data(format_probe_name, format_info, file_path)
                    print(format_probe_name, format_info)
                if format_probe == 'tags':
                    for tag_probe in tag_probe_list:
                        tag_probe_name = f'F_{tag_probe}'
                        try:
                            format_info_tag = probe_format['tags'][tag_probe]
                            Data().add_ffprobe_data(tag_probe_name, format_info_tag, file_path)
                            print(tag_probe_name, format_info_tag)
                        except Exception:
                            pass
            except Exception:
                format_info = 'нет данных'
                Data().add_ffprobe_data(format_probe_name, format_info, file_path)
                print(format_probe_name, format_info)

        print('_' * 50)


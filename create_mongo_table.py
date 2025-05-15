import os

import pymongo
from PySide6.QtCore import QAbstractTableModel, QModelIndex, Qt

def convert_fps(data):
    try:
        fps = eval(data)
        unit = 'fps'
        if fps % 1 == 0:
            data = f'{int(fps)} {unit}'
        else:
            data = f'{round(fps, 3)} {unit}'
    except ZeroDivisionError:
        data = '0'
    return data


def convert_khz(data):
    try:
        val = f'{float(data) / 1000} kHz'
        return val
    except Exception:
        pass


def convert_bytes(size, unit):
    try:
        # 2**10 = 1024
        size = int(size)
        power = (2 ** 10)
        n = 0
        labels = ['', 'K', 'M', 'G', 'T']
        while size > power:
            size /= power
            n += 1
        val = f'{round(size, 2)} {labels[n]}{unit}'
        return val
    except Exception as e:
        print(e)
        return size

def convert_duration(seconds, fps='25/1'):
    try:
        seconds = float(seconds)
        fps = eval(fps)
        hh = int(seconds // 3600)
        mm = int((seconds % 3600) // 60)
        ss = int((seconds % 3600) % 60 // 1)
        ff = int(seconds % 1 * fps)
        conv_data = f'{hh:02}:{mm:02}:{ss:02}.{ff:02}'
        return conv_data
    except Exception as e:
        print(e)
        return ''


def prepare_data(file_info):

    streams = file_info.get('streams')
    video = list(filter(lambda x: x.get('codec_type') == 'video', streams))
    audio = list(filter(lambda x: x.get('codec_type') == 'audio', streams))
    subtitle = list(filter(lambda x: x.get('codec_type') == 'subtitle', streams))
    cover = list(filter(lambda x: x.get('codec_type') == 'video' and x.get('level') == -99, streams))
    format = file_info.get('format')
    ffmpeg_scanners = file_info.get('ffmpeg_scanners')

    file_path = file_info.get('file_path')
    file_name = os.path.basename(file_path)
    a_audio_map = len(audio)
    v_codec_type = video[0].get('codec_type')
    v_codec_name = video[0].get('codec_name')
    v_width = video[0].get('width')
    v_height = video[0].get('height')
    v_sample_aspect_ratio = video[0].get('sample_aspect_ratio')
    v_display_aspect_ratio = video[0].get('display_aspect_ratio')
    v_frame_rate = video[0].get('r_frame_rate')

    a_codec_name = audio[0].get('codec_name')
    a_sample_rate = audio[0].get('sample_rate')
    a_channels = audio[0].get('channels')
    a_bit_rate = audio[0].get('bit_rate')

    f_bit_rate = format.get('bit_rate')
    f_duration = format.get('duration')
    f_size = format.get('size')
    f_frame_rate = format.get('r_frame_rate')

    r128 = ffmpeg_scanners.get('r128')
    if r128:
        input_i = r128.get('input_i')
        input_tp = r128.get('input_tp')
        input_lra = r128.get('input_lra')
        input_thresh = r128.get('input_thresh')
    else:
        input_i = ''
        input_tp = ''
        input_lra = ''
        input_thresh = ''

    black_screen = ffmpeg_scanners.get('black_screen')
    silence = ffmpeg_scanners.get('silence')
    freeze = ffmpeg_scanners.get('freeze')

    return (file_path, file_name, convert_bytes(f_bit_rate, "bit/s"), v_codec_name, v_width, v_height,
            v_sample_aspect_ratio, v_display_aspect_ratio, convert_fps(v_frame_rate),
            convert_duration(f_duration, v_frame_rate), a_audio_map, a_codec_name, convert_khz(a_sample_rate),
            a_channels, convert_bytes(a_bit_rate, "bit/s"), input_i, input_tp, input_lra, input_thresh,
            black_screen, silence, freeze)


class MongoTableModel(QAbstractTableModel):
    def __init__(self, data=None, parent=None):
        super().__init__(parent)
        self._data = data or []
        self._headers = [
            'file_path', 'Name', 'Bit rate', 'Codec', 'Width', 'Height', 'SAR', 'DAR', 'Frame rate',
            'Duration', 'Audio map', 'Audio codec', 'Sample rate', 'Channels', 'Audio bit rate',
            'Integrated', 'True Peak', 'LRA', 'Threshold', 'Black Screen', 'Silence', 'Freeze'
        ]

    def load_from_mongo(self, query={}, collection='mediainfo'):
        conn = pymongo.MongoClient("localhost", 27017)
        db = conn['videoinfo']
        collection = db[collection]
        self.beginResetModel()  # Уведомляем Qt о сбросе модели
        self._data = [prepare_data(file_info) for file_info in list(collection.find(query))]  # Получаем данные
        self.endResetModel()  # Говорим Qt, что модель обновлена

    def rowCount(self, parent=QModelIndex()):
        return len(self._data)

    def columnCount(self, parent=QModelIndex()):
        return len(self._headers)

    def data(self, index, role=Qt.DisplayRole):
        """Возвращает данные для отображения в ячейке"""
        if not index.isValid():
            return None

        if role == Qt.DisplayRole:
            row = index.row()
            col = index.column()
            return self._data[row][col]

        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        """Заголовки столбцов и строк"""
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return self._headers[section]
        return None
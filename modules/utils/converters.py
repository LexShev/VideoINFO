from datetime import datetime
from fractions import Fraction



def now():
    return datetime.now().strftime("%d-%m-%Y %H:%M:%S")

def convert_frame_duration(file_info):
    try:
        streams = file_info.get('streams')
        video = list(filter(lambda x: x.get('codec_type') == 'video', streams))
        format = file_info.get('format')
        f_duration = format.get('duration')

        v_frame_rate = video[0].get('r_frame_rate')
        f_frame_rate = format.get('r_frame_rate')

        # print(v_frame_rate, type(eval(v_frame_rate)), f_frame_rate, type(eval(f_frame_rate)), f_duration, type(float(f_duration)))
        if v_frame_rate:
            return float(f_duration) * float(Fraction(v_frame_rate))
        else:
            return float(f_duration) * float(Fraction(f_frame_rate))
    except Exception as e:
        print(e)
        return 1

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

def convert_duration_sec(data, fps=25):
    print('data', type(data), data)
    hh = int(data // 3600)
    mm = int((data % 3600) // 60)
    ss = int((data % 3600) % 60 // 1)
    ff = int(data % 1 * fps)
    return f'{hh:02}:{mm:02}:{ss:02}.{ff:02}'


def convert_tf_to_sec(time):
    hh = int(time.split(':')[0])
    mm = int(time.split(':')[1])
    ss = int(time.split(':')[2])
    sec = (hh*3600)+(mm*60)+ss
    return sec
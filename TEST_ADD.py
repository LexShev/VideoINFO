import sqlite3


class Data:
    def __init__(self):
        self.db_name = 'videoinfo.db'
        self.tbl_name = 'Video'
        self.connection = sqlite3.connect(self.db_name, isolation_level=None)
        self.cursor = self.connection.cursor()
        self.cursor.execute('PRAGMA temp_store = MEMORY')
        self.cursor.execute('PRAGMA synchronous = OFF')


        self.add_ffprobe_data('input_i', 'test_h264 ', r'//slave/storage/ContentX/FILMS/F_Янтарный замок_1959_1080p25_H264_6Mbps.mp4')

    def add_ffprobe_data(self, header, data, file_path):
        # self.cursor.execute('UPDATE Video SET freeze_start=? WHERE file_path=?', ('freeze_start', 'file_path'))
        # self.cursor.execute('UPDATE Video SET freeze_end=? WHERE file_path=?', ('freeze_end', 'file_path'))
        # self.cursor.execute('UPDATE Video SET freeze_duration=? WHERE file_path=?', ('freeze_duration', 'file_path'))
        # self.cursor.execute(f'ALTER TABLE Video ADD COLUMN "{header}" TEXT DEFAULT "нет данных";')
        # print('Колонка добавлена')
        # self.cursor.execute(f'UPDATE Video SET {header} = ? WHERE file_path = ?', (header, 'file_path'))
        # print('Ключи добавлены')
        self.cursor.execute(f'UPDATE Video SET {header} = ? WHERE file_path = ?', (data, file_path))
        print('ready')
        self.connection.commit()
        self.connection.close()


Data()
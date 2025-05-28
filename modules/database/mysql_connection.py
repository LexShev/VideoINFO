import os
# pip install mysql-connector-python
import mysql.connector as mysql

# pip install XlsxWriter
from xlsxwriter.workbook import Workbook


class Data:
    def __init__(self):
        self.tbl_name = 'films'
        self.connection = mysql.connect(host='localhost', database='TEST', user='root', password='@RG3nt!NA5_0')
        self.cursor = self.connection.cursor()
        self.cursor.execute('SET SESSION TRANSACTION ISOLATION LEVEL READ UNCOMMITTED')


    def choose_db(self):
        pass

    def choose_tbl(self):
        pass

    def show_all_tbl(self):
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        res = self.cursor.fetchall()
        all_tbls = [col[0] for col in res]
        return all_tbls


    def show_all_headers(self):
        self.cursor.execute(f'''
        SHOW columns FROM {self.tbl_name}
        ''')
        all_headers = [column[0] for column in self.cursor.fetchall()]
        return all_headers

    def create_database(self):
        self.cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {self.tbl_name} (
        file_path TEXT NOT NULL DEFAULT ('нет данных'),
        file_name  TEXT NOT NULL DEFAULT ('нет данных'),
        input_i TEXT NOT NULL DEFAULT ('нет данных'),
        input_tp TEXT NOT NULL DEFAULT ('нет данных'),
        input_lra TEXT NOT NULL DEFAULT ('нет данных'),
        input_thresh TEXT NOT NULL DEFAULT ('нет данных'),
        target_offset TEXT NOT NULL DEFAULT ('нет данных'),
        waveform_path TEXT NOT NULL DEFAULT ('нет данных'),
        audio_streams TEXT NOT NULL DEFAULT ('нет данных'),
        black_start TEXT NOT NULL DEFAULT ('нет данных'),
        black_end TEXT NOT NULL DEFAULT ('нет данных'),
        black_duration TEXT NOT NULL DEFAULT ('нет данных'),
        silence_start TEXT NOT NULL DEFAULT ('нет данных'),
        silence_end TEXT NOT NULL DEFAULT ('нет данных'),
        silence_duration TEXT NOT NULL DEFAULT ('нет данных'),
        freeze_start TEXT NOT NULL DEFAULT ('нет данных'),
        freeze_end TEXT NOT NULL DEFAULT ('нет данных'),
        freeze_duration TEXT NOT NULL DEFAULT ('нет данных'),
        marks TEXT NOT NULL DEFAULT ('нет данных')
        )
        ''')

        self.connection.commit()
        # self.connection.close()

    def add_video(self, file_path):
        file_name = os.path.basename(file_path)
        headers = '''
        (file_path, file_name)
        '''
        values = (file_path, file_name)
        try:
            self.cursor.execute(f"INSERT IGNORE INTO {self.tbl_name} {headers} VALUES {values}")
        except Exception:
            print(f'Файл {file_path} уже присутствует в списке')

        self.connection.commit()
        # self.connection.close()

    def conf_bd(self):
        # pass
        self.connection.commit()
        # self.connection.close()



    def add_ffprobe_data(self, header, data, file_path):
        try:
            self.cursor.execute(f"ALTER TABLE {self.tbl_name} ADD {header} TEXT NOT NULL DEFAULT ('нет данных')")
        except Exception:
            pass

        try:
            self.cursor.execute(f'UPDATE {self.tbl_name} SET {header} = %s WHERE file_path = %s', (data, file_path))
        except Exception:
            print('Ошибка добавления файла в базу')
            pass
        self.connection.commit()
        # self.connection.close()

    def add_data(self, header, data, file_path):
        try:
            self.cursor.execute(f'UPDATE {self.tbl_name} SET {header} = %s WHERE file_path = %s', (str(data), file_path))
        except Exception:
            print('Ошибка добавления данных')
            pass
        self.connection.commit()
    def reset_data(self, file_path):
        try:
            self.cursor.execute(
                f'UPDATE {self.tbl_name} SET input_i = ?, input_tp = ?, input_lra = ?, input_thresh = ?,'
                'target_offset = ?, waveform_path = ?, black_start = ?, black_end = ?, black_duration = ?,'
                'silence_start = ?, silence_end = ?, silence_duration = ?, freeze_start = ?, freeze_end = ?,'
                'freeze_duration = ? WHERE file_path = ?',
                ('нет данных', 'нет данных', 'нет данных', 'нет данных', 'нет данных', 'нет данных',
                 'нет данных', 'нет данных', 'нет данных', 'нет данных', 'нет данных', 'нет данных', 'нет данных',
                 'нет данных', 'нет данных', file_path))
        except Exception:
            print('Ошибка сброса данных')
            pass

    def delete_data(self, file_path):
        try:
            self.cursor.execute(f'DELETE FROM {self.tbl_name} WHERE file_path = ?', (file_path,))
        except Exception:
            print('Ошибка удаления строки')
            pass

        # def add_columns(self, header):
        #     try:
        #         self.connection.execute(f'''
        #         ALTER TABLE Video ADD COLUMN "{header}";
        #         ''')
        #     except Exception:
        #         pass
        #     self.connection.commit()

        # def add_headers(self, header):
        # try:
        #     self.cursor.execute('INSERT INTO Video (file_path) VALUES (?)', ('file_path',))
        # except Exception:
        #     pass
        # self.connection.commit()

        # try:
        #     self.cursor.execute(f'UPDATE Video SET {header} = ? WHERE file_path = ?', (header, 'file_path'))
        # except Exception:
        #     print('Ошибка добавления ключей')
        #     pass
        # self.connection.commit()

        # def add_param(self, file_path, all_headers, data):
        #     for header in all_headers:
        #         try:
        #             self.cursor.execute(f'UPDATE Video SET {header} = ? WHERE file_path = ?', (data[header], file_path))
        #         except Exception:
        #             print('Ошибка добавления файла в базу')
        #             pass
        self.connection.commit()
        self.connection.close()

    def read_bd(self, header, file_path):
        try:
            self.cursor.execute(f'SELECT {header} FROM {self.tbl_name} WHERE file_path = %s', (file_path,))
            data = self.cursor.fetchone()[0]
            # print('data:', data)
            # if data is None:
            #     data = 'empty'
        except Exception:
            data = 'нет данных'
            pass
        # print('data0:', data[0][0])
        # print('header:', header)
        # print('data:', data)
        return data

    def read_bd_multi(self, header):
        try:
            self.cursor.execute(f'SELECT {header} FROM {self.tbl_name}')
            column = self.cursor.fetchall()
            # all_data = []
            # for col in column:
            #     all_data.append(col[0])
            all_data = [col[0] for col in column]
            # if data is None:
            #     data = 'empty'
        except Exception:
            all_data = 'нет данных'
            pass
        # print('data0:', data[0][0])
        # print('all_data', tuple(all_data))
        return tuple(all_data)

    # def read_bd_all_data(self, file_path):
    #     try:
    #         self.cursor.execute(f'SELECT {file_path} FROM Video')
    #         column = self.cursor.fetchall()
    #         # all_data = []
    #         # for col in column:
    #         #     all_data.append(col[0])
    #         all_data = [col[0] for col in column]
    #         # if data is None:
    #         #     data = 'empty'
    #     except Exception:
    #         all_data = 'нет данных'
    #         pass
    #     # print('data0:', data[0][0])
    #     # print('all_data', tuple(all_data))
    #     return tuple(all_data)

    def read_all_data(self, file_path):
        self.cursor.execute(f'SELECT * FROM {self.tbl_name} WHERE file_path = %s', (file_path,))
        all_data = self.cursor.fetchone()
        # print('all_data', all_data)
        return all_data  # [::-1]

    def export_xlsx(self):
        workbook = Workbook('db_dump.xlsx')
        worksheet = workbook.add_worksheet()
        # Pass in the database path, db.s3db or test.sqlite
        mysel = self.cursor.execute(f"SELECT * FROM {self.tbl_name}")
        for i, row in enumerate(mysel):
            for j, value in enumerate(row):
                worksheet.write(i, j, value)
        workbook.close()
        print('Экспорт базы данных успешно завершён')

    def del_bd(self):
        self.cursor.execute(f'DROP TABLE IF EXISTS {self.tbl_name}')
        self.connection.commit()
        self.connection.close()

    def close_db(self):
        self.connection.commit()
        self.connection.close()

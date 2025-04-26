import os
import sqlite3
import configparser
# pip install XlsxWriter
from xlsxwriter.workbook import Workbook


class DataLite:
    def __init__(self):
        parent_directory = os.path.dirname(os.path.abspath(__file__))
        settings_directory = os.path.join(parent_directory, 'config')
        settings_name = os.path.join(settings_directory, 'settings.ini')
        config = configparser.ConfigParser()
        config.read(settings_name)

        db_directory = os.path.join(parent_directory, 'db')
        os.makedirs(db_directory, exist_ok=True)
        self.db_name = os.path.join(db_directory, config['Sqlite']['database'])

        self.connection = sqlite3.connect(self.db_name, isolation_level=None)
        self.cursor = self.connection.cursor()
        # self.dest = sqlite3.connect(':memory:')
        # self.connection.backup(self.dest)
        # self.cursor.execute.isolation_level = None
        # isolation_level = None
        self.cursor.execute('PRAGMA temp_store = MEMORY')
        self.cursor.execute('PRAGMA synchronous = OFF')

    def choose_db(self):
        pass

    def choose_tbl(self):
        pass

    def show_all_tbl(self):
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        res = self.cursor.fetchall()
        all_tbls = [col[0] for col in res]
        return all_tbls

    def create_table(self, tbl_name):
        # db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        # db.setDatabaseName('videoinfo_my.db')

        self.cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {tbl_name} (
        file_path TEXT PRIMARY KEY DEFAULT 'нет данных',
        file_name TEXT DEFAULT 'нет данных',
        input_i TEXT DEFAULT 'нет данных',
        input_tp TEXT DEFAULT 'нет данных',
        input_lra TEXT DEFAULT 'нет данных',
        input_thresh TEXT DEFAULT 'нет данных',
        target_offset TEXT DEFAULT 'нет данных',
        waveform_path TEXT DEFAULT 'нет данных',
        audio_streams TEXT DEFAULT 'нет данных',
        black_start TEXT DEFAULT 'нет данных',
        black_end TEXT DEFAULT 'нет данных',
        black_duration TEXT DEFAULT 'нет данных',
        silence_start TEXT DEFAULT 'нет данных',
        silence_end TEXT DEFAULT 'нет данных',
        silence_duration TEXT DEFAULT 'нет данных',
        freeze_start TEXT DEFAULT 'нет данных',
        freeze_end TEXT DEFAULT 'нет данных',
        freeze_duration TEXT DEFAULT 'нет данных',
        marks TEXT DEFAULT 'нет данных',
        date_modified TEXT DEFAULT 'нет данных'
        )
        ''')
        self.connection.commit()
        # self.connection.close()

    def check_connect(self):
        if self.cursor:
            status = 'Connect'
        else:
            status = 'Not connect'
        return status
    def add_video(self, tbl_name,  file_path):
        file_name = os.path.basename(file_path)
        try:
            self.cursor.execute(f'INSERT INTO {tbl_name} (file_path, file_name) VALUES (?,?)',
                                (file_path, file_name,))
        except Exception:
            print(f'Файл {file_path} уже присутствует в списке')

        self.connection.commit()
        # self.connection.close()

    def conf_bd(self):
        # pass
        self.connection.commit()
        # self.connection.close()

    def add_ffprobe_data(self, tbl_name, header, data, file_path):
        try:
            self.cursor.execute(f'''
            ALTER TABLE {tbl_name} ADD COLUMN "{header}" TEXT DEFAULT 'нет данных';
            ''')
        except Exception:
            pass

        try:
            self.cursor.execute(f'UPDATE {tbl_name} SET {header} = ? WHERE file_path = ?', (header, 'file_path'))
        except Exception:
            print('Ошибка добавления ключей')
            pass

        try:
            self.cursor.execute(f'UPDATE {tbl_name} SET {header} = ? WHERE file_path = ?', (data, file_path))
        except Exception:
            print('Ошибка добавления файла в базу')
            pass
        # self.connection.commit()
        # self.connection.close()

    def add_data(self, tbl_name, header, data, file_path):
        try:
            self.cursor.execute(f'UPDATE {tbl_name} SET {header} = ? WHERE file_path = ?', (str(data), file_path))
        except Exception:
            print('Ошибка добавления данных')
            pass

    def reset_data(self, tbl_name, file_path):
        try:
            self.cursor.execute(
                f'UPDATE {tbl_name} SET input_i = ?, input_tp = ?, input_lra = ?, input_thresh = ?,'
                'target_offset = ?, waveform_path = ?, black_start = ?, black_end = ?, black_duration = ?,'
                'silence_start = ?, silence_end = ?, silence_duration = ?, freeze_start = ?, freeze_end = ?,'
                'freeze_duration = ? WHERE file_path = ?',
                ('нет данных', 'нет данных', 'нет данных', 'нет данных', 'нет данных', 'нет данных',
                 'нет данных', 'нет данных', 'нет данных', 'нет данных', 'нет данных', 'нет данных', 'нет данных',
                 'нет данных', 'нет данных', file_path))
        except Exception:
            print('Ошибка сброса данных')
            pass

    def update_data(self, tbl_name, old_file_path, new_file_path):
        try:
            self.cursor.execute(f'PRAGMA table_info ({tbl_name})')
            all_headers = tuple([column[1] for column in self.cursor.fetchall()])
            self.cursor.execute(f'SELECT * FROM {tbl_name} WHERE file_path = ?', (old_file_path,))
            old_data = self.cursor.fetchone()
            self.cursor.execute(f'DELETE FROM {tbl_name} WHERE file_path = ?', (old_file_path,))
            new_data = list(old_data[:])
            new_data[0] = new_file_path
            new_data[1] = os.path.basename(new_file_path)
            new_data = tuple(new_data)
            self.cursor.execute(f'INSERT INTO {tbl_name} {all_headers} VALUES {new_data}',)
        except Exception:
            print(f'Ошибка обновления данных для файла {old_file_path}')
        self.connection.commit()

    def delete_data(self, tbl_name, file_path):
        try:
            self.cursor.execute(f'DELETE FROM {tbl_name} WHERE file_path = ?', (file_path,))
        except Exception:
            print('Ошибка удаления строки')
            pass

        self.connection.commit()
        self.connection.close()

    def read_bd(self, tbl_name, header, file_path):
        try:
            self.cursor.execute(f'SELECT {header} FROM {tbl_name} WHERE file_path = ?', (file_path,))
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

    def read_bd_multi(self, tbl_name, header):
        try:
            self.cursor.execute(f'SELECT {header} FROM {tbl_name}')
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

    def read_all_headers(self, tbl_name):
        self.cursor.execute(f'PRAGMA table_info ({tbl_name})')
        all_headers = [column[1] for column in self.cursor.fetchall()]
        return all_headers
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

    def read_all_data_for_file(self, tbl_name, file_path):
        self.cursor.execute(f'SELECT * FROM {tbl_name} WHERE file_path = ?', (file_path,))
        all_data = self.cursor.fetchone()
        # print('all_data', all_data)
        return all_data  # [::-1]

    def read_all_files(self, tbl_name):
        self.cursor.execute(f'SELECT * FROM {tbl_name}')
        all_files = [column[0] for column in self.cursor.fetchall()]
        return all_files

    def export_tbl_to_xlsx(self, tbl_name):
        workbook = Workbook(f'sqlite_{tbl_name}_dump.xlsx')
        worksheet = workbook.add_worksheet(tbl_name)
        data = self.cursor.execute(f"SELECT * FROM {tbl_name}")
        for i, row in enumerate(data):
            for j, value in enumerate(row):
                worksheet.write(i, j, value)
        workbook.close()
        print('Экспорт базы данных успешно завершён')

    def export_db_to_xlsx(self):
        workbook = Workbook('sqlite_all_db_dump.xlsx')
        all_tables = self.show_all_tbl()
        for table in all_tables:
            worksheet = workbook.add_worksheet(table)
            data = self.cursor.execute(f"SELECT * FROM {table}")
            for i, row in enumerate(data):
                for j, value in enumerate(row):
                    worksheet.write(i, j, value)
        workbook.close()
        print('Экспорт базы данных успешно завершён')

    def rename_table(self, old_name, new_name):
        self.cursor.execute(f'ALTER TABLE {old_name} RENAME TO {new_name}')

    def del_tbl(self, tbl_name):
        self.cursor.execute(f'DROP TABLE IF EXISTS {tbl_name}')
        self.connection.commit()
        self.connection.close()

    def del_db(self):
        self.connection.commit()
        self.connection.close()

    def close_db(self):
        self.connection.commit()
        self.connection.close()


import os
# pip install psycopg2
import psycopg2
from psycopg2 import Error
import configparser

# pip install XlsxWriter
from xlsxwriter.workbook import Workbook


class DataPos:
    def __init__(self):
        parent_directory = os.path.dirname(os.path.abspath(__file__))
        settings_directory = os.path.join(parent_directory, 'config')
        settings_name = os.path.join(settings_directory, 'settings.ini')
        config = configparser.ConfigParser()
        config.read(settings_name)

        self.connection = psycopg2.connect(
            host=config['Posql']['host'],
            database=config['Posql']['database'],
            user=config['Posql']['user'],
            port=config['Posql']['port'],
            password=config['Posql']['password']
        )
        self.cursor = self.connection.cursor()
        # self.cursor.execute('SET SESSION TRANSACTION ISOLATION LEVEL READ UNCOMMITTED')

    def choose_db(self):
        pass

    def choose_tbl(self):
        pass

    def show_all_tbl(self):
        self.cursor.execute("SELECT * FROM pg_catalog.pg_tables where schemaname='public';")
        res = self.cursor.fetchall()
        all_tbls = [col[1] for col in res]
        return all_tbls

    def read_all_headers(self, tbl_name):
        self.cursor.execute(f'SELECT * FROM {tbl_name}')
        all_headers = [column[0] for column in self.cursor.description]
        return all_headers


    def create_table(self, tbl_name):
        self.cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {tbl_name} (
        file_path TEXT  PRIMARY KEY NOT NULL DEFAULT ('нет данных'),
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
        marks TEXT NOT NULL DEFAULT ('нет данных'),
        date_modified TEXT NOT NULL DEFAULT ('нет данных')
        )
        ''')
        self.connection.commit()
        # self.connection.close()

    def check_connect(self):
        try:
            self.cursor.execute("SELECT state FROM pg_stat_activity WHERE state = 'active';")
            status = 'Connect'
        except Exception:
            status = 'Not2 connect'
        return status

    # def check_connect(self):
    #     self.cursor.execute("SELECT state FROM pg_stat_activity WHERE state = 'active';")
    #     if self.cursor.fetchone()[0] == 'active':
    #         status = 'Connect'
    #     else:
    #         status = 'Not connect'
    #     return status

    def add_video(self, tbl_name, file_path):
        file_name = os.path.basename(file_path)
        headers = '(file_path, file_name)'
        values = (file_path, file_name)
        try:
            self.cursor.execute(f"INSERT INTO {tbl_name} {headers} VALUES {values}"
                                f"ON CONFLICT (file_path) DO NOTHING")
        except Exception:
            print(f'Файл {file_path} уже присутствует в списке')

        self.connection.commit()
        # self.connection.close()

    def add_full_video(self, tbl_name, file_path, headers, values):
        headers = ', '.join(headers)
        for header in headers:
            try:
                self.cursor.execute(f"ALTER TABLE {tbl_name} ADD {header} TEXT NOT NULL DEFAULT ('нет данных')")
                self.connection.commit()
            except (Exception, Error) as error:
                print('Ошибка добавления ключей в базу', error)
                self.connection.rollback()
        try:
            self.cursor.execute(f"INSERT INTO {tbl_name} ({headers}) VALUES {values}"
                                f"ON CONFLICT (file_path) DO NOTHING")
        except Exception:
            print(f'Файл {file_path} уже присутствует в списке')
        self.connection.commit()

    def move_video(self, tbl_name, file_path, headers, data):
        headers = ', '.join(headers)
        try:
            self.cursor.execute(f"INSERT INTO {tbl_name} ({headers}) VALUES {data}"
                                f"ON CONFLICT (file_path) DO NOTHING")

        except (Exception, Error) as error:
            print(f'Файл {file_path} уже присутствует в списке', error)

        self.connection.commit()

    def conf_bd(self):
        self.connection.commit()
        # self.connection.close()


    def add_ffprobe_data(self, tbl_name, header, data, file_path):
        try:
            self.cursor.execute(f"ALTER TABLE {tbl_name} ADD {header} TEXT NOT NULL DEFAULT ('нет данных')")
            self.connection.commit()
        except (Exception, Error) as error:
            print('Ошибка добавления ключей в базу', error)
            self.connection.rollback()

        try:
            self.cursor.execute(f'UPDATE {tbl_name} SET {header} = %s WHERE file_path = %s', (data, file_path))
        except (Exception, Error) as error:
            print('Ошибка добавления файла в базу', error)

        self.connection.commit()
        self.cursor.close()
        self.connection.close()

    def add_columns(self, tbl_name, headers):
        for header in headers:
            try:
                self.cursor.execute(f"ALTER TABLE {tbl_name} ADD {header} TEXT NOT NULL DEFAULT ('нет данных')")
                self.connection.commit()
            except (Exception, Error) as error:
                print('Ошибка добавления ключей в базу', error)
                self.connection.rollback()
                pass
    def add_data(self, tbl_name, header, data, file_path):
        try:
            self.cursor.execute(f'UPDATE {tbl_name} SET {header} = %s WHERE file_path = %s', (str(data), file_path))
        except (Exception, Error) as error:
            print('Ошибка добавления данных', error)
        self.connection.commit()

    def reset_data(self, tbl_name, file_path):
        try:
            self.cursor.execute(
                f'UPDATE {tbl_name} SET input_i = %s, input_tp = %s, input_lra = %s, input_thresh = %s,'
                'target_offset = %s, waveform_path = %s, black_start = %s, black_end = %s, black_duration = %s,'
                'silence_start = %s, silence_end = %s, silence_duration = %s, freeze_start = %s, freeze_end = %s,'
                'freeze_duration = %s WHERE file_path = %s',
                ('нет данных', 'нет данных', 'нет данных', 'нет данных', 'нет данных', 'нет данных',
                 'нет данных', 'нет данных', 'нет данных', 'нет данных', 'нет данных', 'нет данных', 'нет данных',
                 'нет данных', 'нет данных', file_path))
        except Exception:
            print('Ошибка сброса данных')
        self.connection.commit()

    def update_data(self, tbl_name, old_file_path, new_file_path):
        try:
            self.cursor.execute(f'SELECT * FROM {tbl_name}')
            all_headers = [column[0] for column in self.cursor.description]
            all_headers = ', '.join(all_headers)
            self.cursor.execute(f'SELECT * FROM {tbl_name} WHERE file_path = %s', (old_file_path,))
            old_data = self.cursor.fetchone()
            self.cursor.execute(f'DELETE FROM {tbl_name} WHERE file_path = %s', (old_file_path,))
            new_data = list(old_data[:])
            new_data[0] = new_file_path
            new_data[1] = os.path.basename(new_file_path)
            new_data = tuple(new_data)
            self.cursor.execute(f"INSERT INTO {tbl_name} ({all_headers}) VALUES {new_data} ON CONFLICT (file_path) DO NOTHING")
        except Exception:
            print(f'Ошибка обновления данных для файла {old_file_path}')
        self.connection.commit()

    def delete_data(self, tbl_name, file_path):
        try:
            self.cursor.execute(f'DELETE FROM {tbl_name} WHERE file_path = %s', (file_path,))
        except Exception:
            print('Ошибка удаления строки')

        self.connection.commit()
        self.connection.close()

    def read_bd(self, tbl_name, header, file_path):
        try:
            self.cursor.execute(f'SELECT {header} FROM {tbl_name} WHERE file_path = %s', (file_path,))
            data = self.cursor.fetchone()[0]
            # print('data:', data)
            # if data is None:
            #     data = 'empty'
        except Exception:
            data = 'нет данных'
        # print('data0:', data[0][0])
        # print('header:', header)
        print('data:', data)
        return data

    def read_bd_multi(self, tbl_name, header):
        try:
            self.cursor.execute(f'SELECT {header} FROM {tbl_name}')
            column = self.cursor.fetchall()
            all_data = [col[0] for col in column]
            # if data is None:
            #     data = 'empty'
        except Exception:
            all_data = 'нет данных'
        return tuple(all_data)

    def read_all_data_for_file(self, tbl_name, file_path):
        self.cursor.execute(f'SELECT * FROM {tbl_name} WHERE file_path = %s', (file_path,))
        all_data = self.cursor.fetchone()
        return all_data  # [::-1]

    def read_all_data(self, tbl_name):
        self.cursor.execute(f'SELECT * FROM {tbl_name}')
        all_data = [column for column in self.cursor.fetchall()]
        return all_data

    def read_all_files(self, tbl_name):
        self.cursor.execute(f'SELECT * FROM {tbl_name}')
        all_files = [column[0] for column in self.cursor.fetchall()]
        return all_files

    def export_tbl_to_xlsx(self, tbl_name):
        workbook = Workbook(f'posql_{tbl_name}_dump.xlsx')
        worksheet = workbook.add_worksheet(tbl_name)
        data = self.cursor.execute(f"SELECT * FROM {tbl_name}")
        for i, row in enumerate(self.cursor.fetchall()):
            for j, value in enumerate(row):
                worksheet.write(i, j, value)
        workbook.close()
        print('Экспорт базы данных успешно завершён')

    def export_xlsx(self):
        print('Экспорт базы данных...')
        workbook = Workbook('posql_db_dump.xlsx')
        all_tables = self.show_all_tbl()
        for table in all_tables:
            worksheet = workbook.add_worksheet(table)
            self.cursor.execute(f"SELECT * FROM {table}")
            for i, row in enumerate(self.cursor.fetchall()):
                for j, value in enumerate(row):
                    worksheet.write(i, j, value)
        workbook.close()
        print('Экспорт базы данных успешно завершён')

    def del_table(self, tbl_name):
        self.cursor.execute(f'DROP TABLE IF EXISTS {tbl_name}')
        self.connection.commit()
        # self.connection.close()

    def close_db(self):
        self.connection.commit()
        self.connection.close()

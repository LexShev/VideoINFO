import sqlite3

connection = sqlite3.connect('videoinfo.db')
cursor = connection.cursor()

def add_columns():
    cursor.execute('ALTER TABLE Video ADD COLUMN freeze_start TEXT DEFAULT "нет данных"')
    cursor.execute('ALTER TABLE Video ADD COLUMN freeze_end TEXT DEFAULT "нет данных"')
    cursor.execute('ALTER TABLE Video ADD COLUMN freeze_duration TEXT DEFAULT "нет данных"')
    # cursor.execute('ALTER TABLE Video ADD COLUMN silence_start TEXT DEFAULT "нет данных"')
    # cursor.execute('ALTER TABLE Video ADD COLUMN silence_end TEXT DEFAULT "нет данных"')
    # cursor.execute('ALTER TABLE Video ADD COLUMN silence_duration TEXT DEFAULT "нет данных"')
    print('готово')
    connection.commit()
    # connection.close()
    # print('Ошибка добавления')
def update_data():
    cursor.execute('UPDATE Video SET freeze_start=? WHERE file_path=?', ('freeze_start', 'file_path'))
    cursor.execute('UPDATE Video SET freeze_end=? WHERE file_path=?', ('freeze_end', 'file_path'))
    cursor.execute('UPDATE Video SET freeze_duration=? WHERE file_path=?', ('freeze_duration', 'file_path'))
    # cursor.execute('UPDATE Video SET silence_start=? WHERE file_path=?', ('silence_start', 'file_path'))
    # cursor.execute('UPDATE Video SET silence_end=? WHERE file_path=?', ('silence_end', 'file_path'))
    # cursor.execute('UPDATE Video SET silence_duration=? WHERE file_path=?', ('silence_duration', 'file_path'))
    print('готово')
    connection.commit()
    connection.close()

# add_columns()
update_data()


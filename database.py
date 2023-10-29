import sqlite3

# устанавливаем соединение с БД
conn = sqlite3.connect('configurator_v1.db')
cursor = conn.cursor()

# создаем таблицу с правильными типами данных
cursor.execute('''
ALTER TABLE motherboards_new RENAME TO motherboards;

''')

# сохраняем изменения в БД
conn.commit()

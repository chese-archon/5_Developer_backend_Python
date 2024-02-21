import sqlite3
import datetime
import statistics

conn = sqlite3.connect('device_data.db')
cursor = conn.cursor()

# Таблица "data" для хранения данных с устройств, полям "device_id", "x", "y", "z" и "timestamp"
cursor.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='data' ''')
if cursor.fetchone()[0] == 0:
    # Таблица не существует, создаем её
    cursor.execute('''CREATE TABLE data
                    (id INTEGER PRIMARY KEY, device_id TEXT, x REAL, y REAL, z REAL, timestamp TEXT)''')
#cursor.execute('''CREATE TABLE data ...''')
#cursor.execute('''CREATE TABLE data
#                (id INTEGER PRIMARY KEY, device_id TEXT, x REAL, y REAL, z REAL, timestamp TEXT)''')
conn.commit()
conn.close()
# Сохранение данных устройства в базе данных
def save_device_data(device_id, x, y, z):
    conn = sqlite3.connect('device_data.db')
    cursor = conn.cursor()
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute('INSERT INTO data (device_id, x, y, z, timestamp) VALUES (?, ?, ?, ?, ?)', (device_id, x, y, z, timestamp))
    conn.commit()  # Важно добавить эту строку для сохранения изменений в базе данных
    conn.close()

# Анализ данных устройства за определенный период
def analyze_device_data(device_id, start_date='1970-01-01 00:00:00', end_date=None):
    conn = sqlite3.connect('device_data.db')
    cursor = conn.cursor()
    if end_date is None:
        end_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    results = {}
    for column_name in ['x', 'y', 'z']:
        if device_id == 'all':
            cursor.execute('SELECT {} FROM data WHERE timestamp BETWEEN ? AND ?'.format(column_name),
                           (start_date, end_date))
        else:
            cursor.execute('SELECT {} FROM data WHERE device_id=? AND timestamp BETWEEN ? AND ?'.format(column_name),
                           (device_id, start_date, end_date))
        values = [row[0] for row in cursor.fetchall()]

        minimum_value = min(values)
        maximum_value = max(values)
        count = len(values)
        total = sum(values)
        median = statistics.median(values)

        results[column_name] = {
            'minimum_value': minimum_value,
            'maximum_value': maximum_value,
            'count': count,
            'total': total,
            'median': median}
    conn.close()
    return results

#Все полученные данные
def get_all_data():
    conn = sqlite3.connect('device_data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM data')
    rows = cursor.fetchall()
    conn.close()
    return rows

#conn.close()
# database.py
import mysql.connector
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME

# 连接数据库
def get_db_connection():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

# 初始化数据库，创建统计表
def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS channel_stats (
        id INT AUTO_INCREMENT PRIMARY KEY,
        channel_name VARCHAR(255),
        date DATE,
        members_count INT,
        daily_new_subscribers INT
    )
    ''')
    conn.commit()
    cursor.close()
    conn.close()

# 插入统计数据
def insert_stats(channel_name, date, members_count, daily_new_subscribers):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO channel_stats (channel_name, date, members_count, daily_new_subscribers)
    VALUES (%s, %s, %s, %s)
    ''', (channel_name, date, members_count, daily_new_subscribers))
    conn.commit()
    cursor.close()
    conn.close()

# 获取某个频道的最新统计数据
def get_last_stats(channel_name):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('''
    SELECT * FROM channel_stats WHERE channel_name = %s ORDER BY date DESC LIMIT 1
    ''', (channel_name,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result

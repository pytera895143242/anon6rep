import pymysql

async def reg_user_mysql(chat_id):
    try:
        connection = pymysql.connect(host='92.53.96.20',
                                     port=3306,
                                     user='cu14708_1',
                                     database='cu14708_1',
                                     password='EspEwD2A')
        print('success')
        try:
            cursor = connection.cursor()
            cursor.execute("""CREATE TABLE IF NOT EXISTS user (
                        id int,
                        chat_id int
                        )""")
            cursor.execute(f"SELECT chat_id FROM user WHERE chat_id = '{int(chat_id)}'")
            if cursor.fetchone() is None:
                cursor.execute(f"INSERT INTO `user` (chat_id) VALUES ({chat_id});")
                connection.commit()
        finally:
            connection.close()

    except Exception as ex:
        print('Mistakes for connection')
        print(ex)

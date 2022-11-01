import sqlite3

db = sqlite3.connect('server.db')
sql = db.cursor()


def reg_bd():
    sql.execute(""" CREATE TABLE IF NOT EXISTS queue (
            chat_id,
            gender_find,
            my_gender
            ) """)
    db.commit()

    sql.execute(""" CREATE TABLE IF NOT EXISTS sessions (
                id,
                chat_one,
                chat_two
                ) """)
    db.commit()

    sql.execute(""" CREATE TABLE IF NOT EXISTS users (
                    chat_id,
                    gender,
                    first_name,
                    ref,
                    status_man,
                    count_next
                    ) """)
    db.commit()

    sql.execute(""" CREATE TABLE IF NOT EXISTS trafik (
                chanel,
                parametr,
                chat_channel,
                person
                ) """)
    db.commit()
    sql.execute(f"SELECT chanel FROM trafik WHERE chanel = 'channel1'")
    if sql.fetchone() is None:
        sql.execute(f"INSERT INTO trafik VALUES (?,?,?,?)", ('channel1', 'chennel', -111, 100))
        sql.execute(f"INSERT INTO trafik VALUES (?,?,?,?)", ('channel2', 'chennel', -111, 100))
        sql.execute(f"INSERT INTO trafik VALUES (?,?,?,?)", ('channel3', 'chennel', -111, 100))
        sql.execute(f"INSERT INTO trafik VALUES (?,?,?,?)", ('channel4', 'chennel4', -111, 100))
        sql.execute(f"INSERT INTO trafik VALUES (?,?,?,?)", ('channel5', 'https://t.me/chennel4/', 0, 100))
        db.commit()

def info_members(): #Информация о трафике
    db = sqlite3.connect('server.db')
    sql = db.cursor()

    all = sql.execute(f'SELECT COUNT(*) FROM users').fetchone()[0]
    man = sql.execute(f"SELECT COUNT(*) FROM users WHERE gender = 'man'").fetchone()[0]
    woman = sql.execute(f"SELECT COUNT(*) FROM users WHERE gender = 'woman'").fetchone()[0]
    biman = sql.execute(f"SELECT COUNT(*) FROM users WHERE gender = 'wait'").fetchone()[0]
    next = sql.execute(f"SELECT count_next FROM users").fetchall()
    count_next = 0
    for n in next:
        count_next += int(n[0])

    return all,woman,man,biman,count_next


def info_members_ref(ref): #Информация о трафике по рефералке
    db = sqlite3.connect('server.db')
    sql = db.cursor()

    all = sql.execute(f"SELECT COUNT(*) FROM users WHERE ref = '{ref}'").fetchone()[0]
    man = sql.execute(f"SELECT COUNT(*) FROM users WHERE gender = 'man' and ref = '{ref}'").fetchone()[0]
    woman = sql.execute(f"SELECT COUNT(*) FROM users WHERE gender = 'woman' and ref = '{ref}'").fetchone()[0]
    biman = sql.execute(f"SELECT COUNT(*) FROM users WHERE gender = 'wait' and ref = '{ref}'").fetchone()[0]
    next = sql.execute(f"SELECT count_next FROM users").fetchall()
    count_next = 0
    for n in next:
        count_next += int(n[0])

    return all,woman,man,biman,count_next



def reg_in_users(chat_id, first_name, ref):
    sql.execute(f"SELECT chat_id FROM users WHERE chat_id ='{chat_id}'")
    if sql.fetchone() is None:
        sql.execute(f"INSERT INTO users VALUES (?,?,?,?,?,?)", (
            str(chat_id),
            'wait',
            first_name,
            str(ref),
            'wait',
            '0',))
        db.commit()


def get_my_gender(chat_id):
    my_gender = sql.execute(f"SELECT gender FROM users WHERE chat_id = '{chat_id}'").fetchone()
    return my_gender[0]


def reg_gender(chat_id, gender, first_name):
    sql.execute(f"SELECT chat_id FROM users WHERE chat_id ='{chat_id}' and gender = 'wait'")
    if sql.fetchone() is not None:
        if gender == 'man':  # Меняем статус прогрева у мужиков на "0"
            sql.execute(f"UPDATE users SET status_man = '0' WHERE chat_id ='{chat_id}' and gender = 'wait'")
        else:  # Меняем статус прогрева у девушек на "ignore"
            sql.execute(f"UPDATE users SET status_man = 'ignore' WHERE chat_id ='{chat_id}' and gender = 'wait'")
        sql.execute(
            f"UPDATE users SET gender = '{gender}' WHERE chat_id ='{chat_id}' and gender = 'wait'")  # Устанавливаем пол юзеру
        db.commit()

        return '1'

    else:
        sql.execute(f"SELECT chat_id FROM users WHERE chat_id ='{chat_id}' and (gender = 'man' or gender = 'woman')")
        if sql.fetchone() is None:
            """Не нашел кому менять пол (создаю запись)"""
            if gender == 'man':  # Меняем статус прогрева у мужиков на "0"
                status_man = '0'
            else:  # Меняем статус прогрева у девушек на "ignore"
                status_man = 'ignore'
            sql.execute(f"INSERT INTO users VALUES (?,?,?,?,?,?)",
                        (str(chat_id), gender, first_name, '1', status_man, '0'))
            db.commit()

            return '1'
        else:
            return '0'


def find_any(chat_id):  # Рандомный поиск
    my_gender = get_my_gender(chat_id=chat_id)

    a = sql.execute(f"SELECT * FROM queue WHERE gender_find = '{my_gender}' or gender_find = 'any'").fetchone()
    if a is None:
        q = 'Поставлен в очередь'
        sql.execute(f"SELECT chat_id FROM queue WHERE chat_id ='{chat_id}'")
        if sql.fetchone() is None:
            sql.execute(f"INSERT INTO queue VALUES (?,?,?)", (str(chat_id), 'any', my_gender))
            db.commit()
    else:
        if (a[0]) != str(chat_id):  # ПРОВЕРКА ЧТОБЫ ЧЕЛОВЕК НЕ ПОДКЛЮЧИЛСЯ САМ К СЕБЕ
            reg_session(chat_one=chat_id, chat_two=a[0])
            q = f'Соединен с {a[0]}'
            return [a[0], 'True']
    return '1'


def del_in_queue(chat_id):  # Удаляем с очереди
    sql.execute("DELETE FROM queue WHERE chat_id = ?", (str(chat_id),))
    db.commit()


def reg_session(chat_one, chat_two):  # Регистрация сессии
    # Теперь чистим очередь
    print(f'Чистка {chat_two} {chat_one}')

    sql.execute("DELETE FROM queue WHERE chat_id = ? ", (str(chat_one),))

    sql.execute("DELETE FROM queue WHERE chat_id = ? ", (str(chat_two),))

    sql.execute(f"SELECT chat_one FROM sessions WHERE chat_one = '{chat_one}' or chat_one = '{chat_two}'")
    if sql.fetchone() is None:  # Если никто не учавствует в другом диалоге, то созадем сессию
        sql.execute(f"INSERT INTO sessions VALUES (?,?,?)", (0, str(chat_one), str(chat_two)))
        db.commit()


def del_session(chat_id):  # Удаление сессии
    another_id = cheack_another_chat_id(chat_id=chat_id)
    try:
        sql.execute("DELETE FROM sessions WHERE chat_one = ? ", (str(chat_id),))
    except:
        pass
    try:
        sql.execute("DELETE FROM sessions WHERE chat_two = ? ", (str(chat_id),))
    except:
        pass

    db.commit()
    return another_id


def next_plues_one(chat, n = 1):
    s = int(sql.execute(f"SELECT count_next FROM users WHERE chat_id ='{chat}'").fetchone()[0])
    sql.execute(f"UPDATE users SET count_next = {s+n} WHERE chat_id ='{chat}'")
    db.commit()
    return s



def cheack_another_chat_id(chat_id):
    try:
        chats_all = \
        (sql.execute(f"SELECT * FROM sessions WHERE chat_one = '{chat_id}' or chat_two = '{chat_id}'").fetchall())[0]
        if chats_all[1] == str(chat_id):
            return chats_all[2]
        else:
            return chats_all[1]
    except:
        return '1'


def cheack_session(chat_id):
    try:
        chats_all = \
        (sql.execute(f"SELECT * FROM sessions WHERE chat_one = '{chat_id}' or chat_two = '{chat_id}'").fetchall())[0]
        return 0
    except:
        return '1'


def man_progrev(chat_id):
    gender = get_my_gender(chat_id)
    if gender == 'man':  # Проверяем на статус монетизации
        status = (sql.execute(f"SELECT status_man FROM users WHERE chat_id ='{chat_id}'").fetchone())[0]
        if status == '0':  # СТАВИМ СТАТУС "1". Возвращаем 1 (чтобы сделать рассылку на дейтинг)
            sql.execute(f"UPDATE users SET status_man= '1' WHERE chat_id ='{chat_id}'")
            db.commit()
            return 1

        else:  # Возвращаем 0 - чтобы не делать рассылку
            return 0

    else:
        return 'woman'

def cheak_traf():
    c1 = sql.execute(f"SELECT parametr FROM trafik WHERE chanel = 'channel1'").fetchone()[0]
    c2 = sql.execute(f"SELECT parametr FROM trafik WHERE chanel = 'channel2'").fetchone()[0]
    c3 = sql.execute(f"SELECT parametr FROM trafik WHERE chanel = 'channel3'").fetchone()[0]
    c4 = sql.execute(f"SELECT parametr FROM trafik WHERE chanel = 'channel4'").fetchone()[0]
    c5 = sql.execute(f"SELECT parametr FROM trafik WHERE chanel = 'channel5'").fetchone()[0]
    list = [c1,c2,c3,c4,c5]
    return list


def obnovatrafika1(link_one,id_channel1):
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    sql.execute(f"UPDATE trafik SET parametr= '{link_one}' WHERE chanel = 'channel1'")
    sql.execute(f"UPDATE trafik SET chat_channel= '{id_channel1}' WHERE chanel = 'channel1'")
    db.commit()

def obnovatrafika2(link_one,id_channel1):
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    sql.execute(f"UPDATE trafik SET parametr= '{link_one}' WHERE chanel = 'channel2'")
    sql.execute(f"UPDATE trafik SET chat_channel= '{id_channel1}' WHERE chanel = 'channel2'")
    db.commit()


def obnovatrafika3(link_one,id_channel1):
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    sql.execute(f"UPDATE trafik SET parametr= '{link_one}' WHERE chanel = 'channel3'")
    sql.execute(f"UPDATE trafik SET chat_channel= '{id_channel1}' WHERE chanel = 'channel3'")
    db.commit()

def obnovatrafika4(link_one,id_channel1):
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    sql.execute(f"UPDATE trafik SET parametr= '{link_one}' WHERE chanel = 'channel4'")
    sql.execute(f"UPDATE trafik SET chat_channel= '{id_channel1}' WHERE chanel = 'channel4'")
    db.commit()

def cheak_chat_id():
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    i1 = sql.execute(f"SELECT chat_channel FROM trafik WHERE chanel = 'channel1'").fetchone()[0]
    i2 = sql.execute(f"SELECT chat_channel FROM trafik WHERE chanel = 'channel2'").fetchone()[0]
    i3 = sql.execute(f"SELECT chat_channel FROM trafik WHERE chanel = 'channel3'").fetchone()[0]
    i4 = sql.execute(f"SELECT chat_channel FROM trafik WHERE chanel = 'channel4'").fetchone()[0]

    return i1,i2,i3


###### Количество подписок на каналы партнеров
def delite_user(id):
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    sql.execute(f'DELETE FROM users WHERE chat_id = "{id}"')
    db.commit()
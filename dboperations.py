# -*- coding: utf-8 -*-
"""
Работа с базой данных
"""
import sqlite3
# import contextlib


# @contextlib.contextmanager
# def DataConn():
#     db_name = "db/database.db"
#     conn = sqlite3.connect(db_name)
#     yield # код из блока with выполнится тут
#     conn.close()


class DataConn:
    """
    Класс Context Manager
    Создает связь с базой данных SQLite и закрывает её по окончанию работы
    """
    # def __init__(self, db_name):
    def __init__(self):
        """Конструктор"""
        # self.db_name = db_name
        self.db_name = "db/database.db"
        self.conn = None

    def __enter__(self):
        """
        Открываем подключение с базой данных.
        """
        self.conn = sqlite3.connect(self.db_name)
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Закрываем подключение.
        """
        self.conn.close()
        if exc_val:
            raise


def create_table():
    """Создание базы данных"""
    with DataConn() as conn:
        with conn:
            cursor = conn.cursor()

            # Создание таблицы
            cursor.execute("""CREATE TABLE transformer
                              (manufacturer text, model text, nominal_voltage_HV text, nominal_voltage_LV text,
                              connection_windings text, full_rated_capacity text)
                           """)


def set_data_to_table():
    """Внесение данных в таблицу"""
    with DataConn() as conn:
        with conn:
            cursor = conn.cursor()

            # Внесение данных в таблицу
            cursor.execute("""INSERT INTO transformer
                              VALUES ('ГОСТ', 'ТМ', '10', '400', 'Y/Yн-0', '160', '2.7', '5.5')
                              """)


def find_manufacturers():
    with DataConn() as conn:
        cursor = conn.cursor()
        sql = "SELECT manufacturer FROM transformer"
        cursor.execute(sql)
        manufacturers = [i[0] for i in cursor.fetchall()]
    return set(manufacturers)


def find_models(text):
    with DataConn() as conn:
        cursor = conn.cursor()
        sql = "SELECT model FROM transformer WHERE manufacturer=?"
        cursor.execute(sql, [text])
        models = [i[0] for i in cursor.fetchall()]
    return set(models)


def find_nominal_voltage_HV(manufacturer, model):
    with DataConn() as conn:
        cursor = conn.cursor()
        sql = "SELECT nominal_voltage_HV FROM transformer WHERE manufacturer=? AND model=?"
        cursor.execute(sql, [manufacturer, model])
        nominal_voltage_HV = [i[0] for i in cursor.fetchall()]
    return set(nominal_voltage_HV)


def find_nominal_voltage_LV(manufacturer, model, nominal_voltage_HV):
    with DataConn() as conn:
        cursor = conn.cursor()
        sql = "SELECT nominal_voltage_LV FROM transformer WHERE manufacturer=? AND model=? AND nominal_voltage_HV=?"
        cursor.execute(sql, [manufacturer, model, nominal_voltage_HV])
        nominal_voltage_LV = [i[0] for i in cursor.fetchall()]
    return set(nominal_voltage_LV)


def find_connection_windings(manufacturer, model, nominal_voltage_HV, nominal_voltage_LV):
    with DataConn() as conn:
        cursor = conn.cursor()
        sql = """SELECT connection_windings FROM transformer
                  WHERE manufacturer=? AND model=? AND nominal_voltage_HV=? AND nominal_voltage_LV=?"""
        cursor.execute(sql, [manufacturer, model, nominal_voltage_HV, nominal_voltage_LV])
        connection_windings = [i[0] for i in cursor.fetchall()]
    return set(connection_windings)


def find_full_rated_capacity(manufacturer, model, nominal_voltage_HV, nominal_voltage_LV, connection_windings):
    with DataConn() as conn:
        cursor = conn.cursor()
        sql = """SELECT full_rated_capacity FROM transformer
                  WHERE manufacturer=? AND model=? AND nominal_voltage_HV=? AND 
                        nominal_voltage_LV=? AND connection_windings=?"""
        cursor.execute(sql, [manufacturer, model, nominal_voltage_HV, nominal_voltage_LV, connection_windings])
        full_rated_capacity = [i[0] for i in cursor.fetchall()]
        full_rated_capacity.sort()
        full_rated_capacity.sort(key=len)
        # full_rated_capacity.sort(key=lambda item: (-len(item), item))
    return full_rated_capacity


def find_short_circuit_loss(manufacturer, model, nominal_voltage_HV, nominal_voltage_LV, connection_windings,
                            full_rated_capacity):
    with DataConn() as conn:
        cursor = conn.cursor()
        sql = """SELECT short_circuit_loss FROM transformer
                  WHERE manufacturer=? AND model=? AND nominal_voltage_HV=? AND 
                        nominal_voltage_LV=? AND connection_windings=? AND full_rated_capacity=?"""
        cursor.execute(sql, [manufacturer, model, nominal_voltage_HV, nominal_voltage_LV, connection_windings,
                             full_rated_capacity])
        rows = cursor.fetchall()
        short_circuit_loss = [i[0] for i in rows]

        if len(short_circuit_loss) > 1:
            short_circuit_loss.sort()
            short_circuit_loss.sort(key=len)
    return short_circuit_loss


# def find_impedance_voltage(manufacturer, model, nominal_voltage_HV, nominal_voltage_LV, connection_windings,
#                             full_rated_capacity, short_circuit_loss):
#     with DataConn() as conn:
#         cursor = conn.cursor()
#         sql = """SELECT impedance_voltage FROM transformer
#                   WHERE manufacturer=? AND model=? AND nominal_voltage_HV=? AND 
#                         nominal_voltage_LV=? AND connection_windings=? AND 
#                         full_rated_capacity=? AND short_circuit_loss=?"""
#         cursor.execute(sql, [manufacturer, model, nominal_voltage_HV, nominal_voltage_LV, connection_windings,
#                              full_rated_capacity, short_circuit_loss])
#         rows = cursor.fetchall()
#         impedance_voltage = [i[0] for i in rows]

#         if len(impedance_voltage) > 1:
#             impedance_voltage.sort()
#             impedance_voltage.sort(key=len)
#     return impedance_voltage

def find_impedance_voltage(*args):
    with DataConn() as conn:
        cursor = conn.cursor()
        sql = """SELECT impedance_voltage FROM transformer
                  WHERE manufacturer=? AND model=? AND nominal_voltage_HV=? AND 
                        nominal_voltage_LV=? AND connection_windings=? AND 
                        full_rated_capacity=? AND short_circuit_loss=?"""
        cursor.execute(sql, args)
        rows = cursor.fetchall()
        impedance_voltage = [i[0] for i in rows]

        if len(impedance_voltage) > 1:
            impedance_voltage.sort()
            impedance_voltage.sort(key=len)
    return impedance_voltage


if __name__ == "__main__":
    # set_data_to_table()
    pass

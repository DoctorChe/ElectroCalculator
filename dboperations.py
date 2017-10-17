# -*- coding: utf-8 -*-
"""
Работа с базой данных
"""
import csv
import sqlite3
# import contextlib
from PyQt5 import QtSql, QtCore

from sortedcontainers import SortedSet

DB_PATH = "db/database.db"


# @contextlib.contextmanager
# def DataConn(db_name):
#     conn = sqlite3.connect(db_name)
#     yield # код из блока with выполнится тут
#     conn.close()


class DataConn:
    """
    Класс Context Manager
    Создает связь с базой данных SQLite и закрывает её по окончанию работы
    """

    def __init__(self, db_name):
        """Конструктор"""
        self.db_name = db_name
        self.conn = None

    def __enter__(self):
        """Открываем подключение к базе данных"""
        self.conn = sqlite3.connect(self.db_name)
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Закрываем подключение.
        """
        self.conn.close()
        if exc_val:
            raise


def create_table(table_name):
    """Создание базы данных"""
    with DataConn(DB_PATH) as conn:
        with conn:
            cursor = conn.cursor()
            if table_name == 'transformer':
                # Создание таблицы "трансформатор"
                cursor.execute("""CREATE TABLE IF NOT EXISTS transformer
                                  (manufacturer TEXT, model TEXT, nominal_voltage_HV TEXT, nominal_voltage_LV TEXT,
                                  connection_windings TEXT, full_rated_capacity TEXT)
                               """)
            elif table_name == 'cable':
                # Создание таблицы "кабель"
                cursor.execute("""CREATE TABLE IF NOT EXISTS cable
                                  (linetype TEXT, 
                                  material_of_cable_core TEXT, 
                                  size_of_cable_phase REAL, size_of_cable_neutral REAL, 
                                  R1 TEXT, X1 TEXT, R0 TEXT, X0 TEXT)
                               """)
            elif table_name == 'busway':
                # Создание таблицы "шинопровод"
                cursor.execute("""CREATE TABLE IF NOT EXISTS busway
                                  (manufacturer TEXT, 
                                  model TEXT,
                                  rated_current TEXT, 
                                  material TEXT, 
                                  R1 TEXT, X1 TEXT, Rnc TEXT, Xnc TEXT)
                               """)


def set_data_to_table():
    """Внесение данных в таблицу"""
    with DataConn(DB_PATH) as conn:
        with conn:
            cursor = conn.cursor()

            # # Внесение данных в таблицу "трансформатор"
            # cursor.execute("""INSERT INTO transformer
            #                   VALUES ('ГОСТ', 'ТМ', '10', '400', 'Y/Yн-0', '160', '2.7', '5.5')
            #                   """)

            # Внесение данных в таблицу "кабель"
            cursor.execute("""INSERT INTO cable
                              VALUES ('Кабель с алюминиевыми жилами в алюминиевой оболочке',
                                      'Алюминий', 
                                      '4', '-1', 
                                      '9.61', '0.092', '10.95', '0.579')
                              """)


def copy_from_csv_to_db(filename, tablename):
    """Копирование данных их файлов CSV в базу данных"""
    sql = {'busway':
               ("""SELECT * FROM busway 
                      WHERE manufacturer=? AND model=? AND rated_current=? AND material=? AND 
                      R1=? AND X1=? AND Rnc=? AND Xnc=?""",
                'INSERT OR IGNORE INTO busway VALUES (?,?,?,?,?,?,?,?)'),
           'cable':
               ("""SELECT * FROM cable
                    WHERE linetype=? AND material_of_cable_core=? AND size_of_cable_phase=? 
                    AND size_of_cable_neutral=? AND R1=? AND X1=? AND R0=? AND X0=?""",
                'INSERT OR IGNORE INTO cable VALUES (?,?,?,?,?,?,?,?)'
                )
           }
    with DataConn(DB_PATH) as conn:
        with conn:
            cursor = conn.cursor()
            create_table(tablename)  # Создать таблицу, если не существует
            with open(filename, newline='') as f:
                reader = csv.reader(f)
                for row in reader:
                    cursor.execute(sql[tablename][0], row)
                    if not cursor.fetchall():  # проверка на существование идентичной записи
                        cursor.execute(sql[tablename][1], row)  # Внесение данных в таблицу


def find_tables():
    con = QtSql.QSqlDatabase.addDatabase('QSQLITE')
    con.setDatabaseName(DB_PATH)
    con.open()
    if con.isOpen():
        tables = con.tables()
    else:
        tables = []
        # s = "Возникла ошибка: " + con.lastError().text()
    con.close()
    # self.txtOutput.setText(s)

    # with DataConn(DB_PATH) as conn:
    #     cursor = conn.cursor()
    #     sql = "SELECT name FROM sqlite_temp_master WHERE type='table'"
    #     cursor.execute(sql)
    #     tables = [i[0] for i in cursor.fetchall()]
    return tables


def show_table(equipment):
    con = QtSql.QSqlDatabase.addDatabase('QSQLITE')
    con.setDatabaseName(DB_PATH)
    con.open()

    model = QtSql.QSqlQueryModel(parent=None)
    model.setQuery('select * from good order by goodname')
    # model.setSort(1, QtCore.Qt.AscendingOrder)
    # model.select()
    model.setHeaderData(1, QtCore.Qt.Horizontal, 'Завод изготовитель')
    model.setHeaderData(2, QtCore.Qt.Horizontal, 'Модель')
    model.setHeaderData(3, QtCore.Qt.Horizontal, 'Номинальное напряжение ВН')
    model.setHeaderData(4, QtCore.Qt.Horizontal, 'Номинальное напряжение НН')
    model.setHeaderData(5, QtCore.Qt.Horizontal, 'Схема соединения обмоток')
    model.setHeaderData(6, QtCore.Qt.Horizontal, 'Полная номинальная мощность')
    model.setHeaderData(7, QtCore.Qt.Horizontal, 'Потери короткого замыкания')
    model.setHeaderData(8, QtCore.Qt.Horizontal, 'Напряжение короткого замыкания')

    # equipment_table = con.record("transformer")
    # field_count = equipment_table.count()
    # for field in range(0, field_count):
    #     field_name = equipment_table.field(field).name()
    #     # if field_name != "id":
    #     #     self.cboSort.addItem(field_name)

    model.setQuery("select * from transformer")

    # stm = QtSql.QSqlRelationalTableModel()
    # stm.setEditStrategy(QtSql.QSqlTableModel.OnManualSubmit)
    # stm.setTable(equipment)
    # # tables = con.tables()
    # # table_count = len(tables)
    # # if table_count > 0:
    # #     stm.
    # table = con.record(equipment)
    # field_count = table.count()
    # field_list = []
    # for field_index in range(0, field_count):
    #     field = table.field(field_index)
    #     field_list.append(field)
    #
    # stm.setSort(1, QtCore.Qt.AscendingOrder)
    # # stm.setRelation(3, QtSql.QSqlRelation('category', 'id', 'catname'))
    # stm.setRelation(3, QtSql.QSqlRelation(field_list))
    # stm.select()
    # stm.setHeaderData(1, QtCore.Qt.Horizontal, 'Название')
    # stm.setHeaderData(2, QtCore.Qt.Horizontal, 'Кол-во')
    # stm.setHeaderData(3, QtCore.Qt.Horizontal, 'Категория')

    con.close()


def find_busway_manufactures():
    with DataConn(DB_PATH) as conn:
        cursor = conn.cursor()
        sql = "SELECT manufacturer FROM busway"
        cursor.execute(sql)
        res = [i[0] for i in cursor.fetchall()]
    return SortedSet(res)


def find_busway_model(*args):
    with DataConn(DB_PATH) as conn:
        cursor = conn.cursor()
        sql = "SELECT model FROM busway WHERE manufacturer=?"
        cursor.execute(sql, args)
        res = [i[0] for i in cursor.fetchall()]
    return SortedSet(res)


def find_busway_rated_current(*args):
    with DataConn(DB_PATH) as conn:
        cursor = conn.cursor()
        sql = "SELECT rated_current FROM busway WHERE manufacturer=? AND model=?"
        cursor.execute(sql, args)
        res = [i[0] for i in cursor.fetchall()]
    return SortedSet(res)


def find_busway_material(*args):
    with DataConn(DB_PATH) as conn:
        cursor = conn.cursor()
        sql = "SELECT material FROM busway WHERE manufacturer=? AND model=? AND rated_current=?"
        cursor.execute(sql, args)
        res = [i[0] for i in cursor.fetchall()]
    return SortedSet(res)


def find_busway_resistance(*args):
    with DataConn(DB_PATH) as conn:
        cursor = conn.cursor()
        sql = "SELECT R1, X1, Rnc, Xnc FROM busway " \
              "WHERE manufacturer=? AND model=? AND rated_current=? AND material=?"
        cursor.execute(sql, args)
        res = cursor.fetchone()
    return res


def find_linetypes():
    with DataConn(DB_PATH) as conn:
        cursor = conn.cursor()
        sql = "SELECT linetype FROM cable"
        cursor.execute(sql)
        res = [i[0] for i in cursor.fetchall()]
    return SortedSet(res)


def find_material_of_cable_core(*args):
    with DataConn(DB_PATH) as conn:
        cursor = conn.cursor()
        sql = "SELECT material_of_cable_core FROM cable WHERE linetype=?"
        cursor.execute(sql, args)
        res = [i[0] for i in cursor.fetchall()]
    return SortedSet(res)


def find_size_of_cable_phase(*args):
    with DataConn(DB_PATH) as conn:
        cursor = conn.cursor()
        sql = "SELECT size_of_cable_phase FROM cable WHERE linetype=? AND material_of_cable_core=?"
        cursor.execute(sql, args)
        res = [i[0] for i in cursor.fetchall()]
        # res = list(set(res))
        # if len(res) > 1:
        #     res.sort()
            # res.sort(key=len)
    return SortedSet(res)


def find_size_of_cable_neutral(*args):
    with DataConn(DB_PATH) as conn:
        cursor = conn.cursor()
        sql = "SELECT size_of_cable_neutral FROM cable " \
              "WHERE linetype=? AND material_of_cable_core=? AND size_of_cable_phase=?"
        cursor.execute(sql, args)
        res = [i[0] for i in cursor.fetchall()]
        res = list(set(res))
        # if len(res) > 1:
        #     res.sort()
            # res.sort(key=len)
    return SortedSet(res)


def find_resistance(*args):
    with DataConn(DB_PATH) as conn:
        cursor = conn.cursor()
        sql = "SELECT R1, X1, R0, X0 FROM cable " \
              "WHERE linetype=? AND material_of_cable_core=? AND size_of_cable_phase=? AND size_of_cable_neutral=?"
        cursor.execute(sql, args)
        res = cursor.fetchone()
    return res


def find_manufacturers():
    with DataConn(DB_PATH) as conn:
        cursor = conn.cursor()
        sql = "SELECT manufacturer FROM transformer"
        cursor.execute(sql)
        manufacturers = [i[0] for i in cursor.fetchall()]
    return SortedSet(manufacturers)


def find_models(*args):
    with DataConn(DB_PATH) as conn:
        cursor = conn.cursor()
        sql = "SELECT model FROM transformer WHERE manufacturer=?"
        cursor.execute(sql, args)
        models = [i[0] for i in cursor.fetchall()]
    return SortedSet(models)


def find_nominal_voltage_HV(*args):
    with DataConn(DB_PATH) as conn:
        cursor = conn.cursor()
        sql = "SELECT nominal_voltage_HV FROM transformer WHERE manufacturer=? AND model=?"
        cursor.execute(sql, args)
        res = [i[0] for i in cursor.fetchall()]
        res = list(set(res))
        if len(res) > 1:
            res.sort()
            res.sort(key=len)
    return res


def find_nominal_voltage_LV(*args):
    with DataConn(DB_PATH) as conn:
        cursor = conn.cursor()
        sql = "SELECT nominal_voltage_LV FROM transformer WHERE manufacturer=? AND model=? AND nominal_voltage_HV=?"
        cursor.execute(sql, args)
        res = [i[0] for i in cursor.fetchall()]
        res = list(set(res))
        if len(res) > 1:
            res.sort()
            res.sort(key=len)
    return res


def find_connection_windings(*args):
    with DataConn(DB_PATH) as conn:
        cursor = conn.cursor()
        sql = """SELECT connection_windings FROM transformer
                  WHERE manufacturer=? AND model=? AND nominal_voltage_HV=? AND nominal_voltage_LV=?"""
        cursor.execute(sql, args)
        connection_windings = [i[0] for i in cursor.fetchall()]
    return SortedSet(connection_windings)


def find_full_rated_capacity(*args):
    with DataConn(DB_PATH) as conn:
        cursor = conn.cursor()
        sql = """SELECT full_rated_capacity FROM transformer
                  WHERE manufacturer=? AND model=? AND nominal_voltage_HV=? AND 
                        nominal_voltage_LV=? AND connection_windings=?"""
        cursor.execute(sql, args)
        res = [i[0] for i in cursor.fetchall()]
        res = list(set(res))
        if len(res) > 1:
            res.sort()
            res.sort(key=len)
    return res


def find_short_circuit_loss(*args):
    with DataConn(DB_PATH) as conn:
        cursor = conn.cursor()
        sql = """SELECT short_circuit_loss FROM transformer
                  WHERE manufacturer=? AND model=? AND nominal_voltage_HV=? AND 
                        nominal_voltage_LV=? AND connection_windings=? AND full_rated_capacity=?"""
        cursor.execute(sql, args)
        rows = cursor.fetchall()
        res = [i[0] for i in rows]
        if len(res) > 1:
            res.sort()
            res.sort(key=len)
    return res


def find_impedance_voltage(*args):
    with DataConn(DB_PATH) as conn:
        cursor = conn.cursor()
        sql = """SELECT impedance_voltage FROM transformer
                  WHERE manufacturer=? AND model=? AND nominal_voltage_HV=? AND 
                        nominal_voltage_LV=? AND connection_windings=? AND 
                        full_rated_capacity=? AND short_circuit_loss=?"""
        cursor.execute(sql, args)
        rows = cursor.fetchall()
        res = [i[0] for i in rows]
        if len(res) > 1:
            res.sort()
            res.sort(key=len)
    return res


if __name__ == "__main__":
    # set_data_to_table()
    # create_table()
    copy_from_csv_to_db('db/Шинопровод.csv', 'busway')
    # for i in range(6,15):
    #     copy_from_csv_to_db('db/Таблица' + str(i) + '.csv', 'cable')
    pass

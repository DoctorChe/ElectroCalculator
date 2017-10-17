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
                                  size_of_cable_phase TEXT, size_of_cable_neutral TEXT, 
                                  R1 TEXT, X1 TEXT, R0 TEXT, X0 TEXT)
                               """)
            elif table_name == 'busway':
                # Создание таблицы "шинопровод"
                cursor.execute("""CREATE TABLE IF NOT EXISTS busway
                                  (manufacturer TEXT, 
                                  model TEXT,
                                  rated_current TEXT, 
                                  material TEXT, 
                                  R1 TEXT, X1 TEXT, Rnс TEXT, Xnс TEXT)
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
                      R1=? AND X1=? AND Rnс=? AND Xnс=?""",
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


def find_linetypes():
    with DataConn(DB_PATH) as conn:
        cursor = conn.cursor()
        sql = "SELECT linetype FROM cable"
        cursor.execute(sql)
        linetypes = [i[0] for i in cursor.fetchall()]
    return SortedSet(linetypes)


def find_material_of_cable_core(text):
    with DataConn(DB_PATH) as conn:
        cursor = conn.cursor()
        sql = "SELECT material_of_cable_core FROM cable WHERE linetype=?"
        cursor.execute(sql, [text])
        res = [i[0] for i in cursor.fetchall()]
    return SortedSet(res)


def find_size_of_cable_phase(*args):
    with DataConn(DB_PATH) as conn:
        cursor = conn.cursor()
        sql = "SELECT size_of_cable_phase FROM cable WHERE linetype=? AND material_of_cable_core=?"
        cursor.execute(sql, args)
        res = [i[0] for i in cursor.fetchall()]
        if len(res) > 1:
            res.sort()
            res.sort(key=len)
    return SortedSet(res)


def find_size_of_cable_neutral(*args):
    with DataConn(DB_PATH) as conn:
        cursor = conn.cursor()
        sql = "SELECT size_of_cable_neutral FROM cable " \
              "WHERE linetype=? AND material_of_cable_core=? AND size_of_cable_phase=?"
        cursor.execute(sql, args)
        res = [i[0] for i in cursor.fetchall()]
        if len(res) > 1:
            res.sort()
            res.sort(key=len)
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


def find_models(text):
    with DataConn(DB_PATH) as conn:
        cursor = conn.cursor()
        sql = "SELECT model FROM transformer WHERE manufacturer=?"
        cursor.execute(sql, [text])
        models = [i[0] for i in cursor.fetchall()]
    return SortedSet(models)


def find_nominal_voltage_HV(manufacturer, model):
    with DataConn(DB_PATH) as conn:
        cursor = conn.cursor()
        sql = "SELECT nominal_voltage_HV FROM transformer WHERE manufacturer=? AND model=?"
        cursor.execute(sql, [manufacturer, model])
        nominal_voltage_HV = [i[0] for i in cursor.fetchall()]
    return SortedSet(nominal_voltage_HV)


def find_nominal_voltage_LV(manufacturer, model, nominal_voltage_HV):
    with DataConn(DB_PATH) as conn:
        cursor = conn.cursor()
        sql = "SELECT nominal_voltage_LV FROM transformer WHERE manufacturer=? AND model=? AND nominal_voltage_HV=?"
        cursor.execute(sql, [manufacturer, model, nominal_voltage_HV])
        nominal_voltage_LV = [i[0] for i in cursor.fetchall()]
    return SortedSet(nominal_voltage_LV)


def find_connection_windings(manufacturer, model, nominal_voltage_HV, nominal_voltage_LV):
    with DataConn(DB_PATH) as conn:
        cursor = conn.cursor()
        sql = """SELECT connection_windings FROM transformer
                  WHERE manufacturer=? AND model=? AND nominal_voltage_HV=? AND nominal_voltage_LV=?"""
        cursor.execute(sql, [manufacturer, model, nominal_voltage_HV, nominal_voltage_LV])
        connection_windings = [i[0] for i in cursor.fetchall()]
    return SortedSet(connection_windings)


def find_full_rated_capacity(manufacturer, model, nominal_voltage_HV, nominal_voltage_LV, connection_windings):
    with DataConn(DB_PATH) as conn:
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
    with DataConn(DB_PATH) as conn:
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


def find_impedance_voltage(*args):
    with DataConn(DB_PATH) as conn:
        cursor = conn.cursor()
        sql = """SELECT impedance_voltage FROM transformer
                  WHERE manufacturer=? AND model=? AND nominal_voltage_HV=? AND 
                        nominal_voltage_LV=? AND connection_windings=? AND 
                        full_rated_capacity=? AND short_circuit_loss=?"""
        cursor.execute(sql, args)
        rows = cursor.fetchall()
        impedance_voltage = [i[0] for i in rows]

        res = SortedSet(impedance_voltage)

    # if len(impedance_voltage) > 1:
    #         impedance_voltage.sort()
    #         impedance_voltage.sort(key=len)
    # return impedance_voltage
    return res


if __name__ == "__main__":
    # set_data_to_table()
    # create_table()
    # for i in range(6,15):
    #     copy_from_csv_to_db('db/Таблица' + str(i) + '.csv', 'cable')
    pass

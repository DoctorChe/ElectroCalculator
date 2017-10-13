# -*- coding: utf-8 -*-
"""
Работа с базой данных
"""
import sqlite3
# import contextlib
from PyQt5 import QtSql, QtCore


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

            # # Создание таблицы "трансформатор"
            # cursor.execute("""CREATE TABLE transformer
            #                   (manufacturer text, model text, nominal_voltage_HV text, nominal_voltage_LV text,
            #                   connection_windings text, full_rated_capacity text)
            #                """)

            # Создание таблицы "кабель"
            cursor.execute("""CREATE TABLE cable
                              (linetype TEXT, 
                              material_of_cable_core TEXT, 
                              size_of_cable_phase TEXT, size_of_cable_neutral TEXT, 
                              R1 TEXT, x1 TEXT, R0 TEXT, x0 TEXT)
                           """)


def set_data_to_table():
    """Внесение данных в таблицу"""
    with DataConn() as conn:
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


def find_tables():
    con = QtSql.QSqlDatabase.addDatabase('QSQLITE')
    con.setDatabaseName("db/database.db")
    con.open()
    if con.isOpen():
        tables = con.tables()
    else:
        tables = []
        # s = "Возникла ошибка: " + con.lastError().text()
    con.close()
    # self.txtOutput.setText(s)

    # with DataConn() as conn:
    #     cursor = conn.cursor()
    #     sql = "SELECT name FROM sqlite_temp_master WHERE type='table'"
    #     cursor.execute(sql)
    #     tables = [i[0] for i in cursor.fetchall()]
    return tables


def show_table(equipment):
    con = QtSql.QSqlDatabase.addDatabase('QSQLITE')
    con.setDatabaseName("db/database.db")
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
    with DataConn() as conn:
        cursor = conn.cursor()
        sql = "SELECT linetype FROM cable"
        cursor.execute(sql)
        linetypes = [i[0] for i in cursor.fetchall()]
    return set(linetypes)


def find_material_of_cable_core(text):
    with DataConn() as conn:
        cursor = conn.cursor()
        sql = "SELECT material_of_cable_core FROM cable WHERE linetype=?"
        cursor.execute(sql, [text])
        res = [i[0] for i in cursor.fetchall()]
    return set(res)


def find_size_of_cable_phase(*args):
    with DataConn() as conn:
        cursor = conn.cursor()
        sql = "SELECT size_of_cable_phase FROM cable WHERE linetype=? AND material_of_cable_core=?"
        cursor.execute(sql, args)
        res = [i[0] for i in cursor.fetchall()]
        if len(res) > 1:
            res.sort()
            res.sort(key=len)
            # TODO Исправить сортировку (иногда не сортируются значения)
    return set(res)


def find_size_of_cable_neutral(*args):
    with DataConn() as conn:
        cursor = conn.cursor()
        sql = "SELECT size_of_cable_neutral FROM cable " \
              "WHERE linetype=? AND material_of_cable_core=? AND size_of_cable_phase=?"
        cursor.execute(sql, args)
        res = [i[0] for i in cursor.fetchall()]
        if len(res) > 1:
            res.sort()
            res.sort(key=len)
    return set(res)


def find_resistance(*args):
    with DataConn() as conn:
        cursor = conn.cursor()
        sql = "SELECT R1, X1, R0, X0 FROM cable " \
              "WHERE linetype=? AND material_of_cable_core=? AND size_of_cable_phase=? AND size_of_cable_neutral=?"
        cursor.execute(sql, args)
        res = cursor.fetchone()
    return res


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
    # create_table()
    pass

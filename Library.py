import sqlite3
import sys


class Series:

    def __init__(self, name0, type0, season0):
        self.name0 = name0
        self.type0 = type0
        self.season0 = season0

    def __str__(self):
        return "Name of the series: {}\nType: {}\nNumber of season: {}\n".format(self.name0, self.type0, self.season0)


class Library:

    def __init__(self):

        self.connection()

    def connection(self):

        self.con = sqlite3.connect("kütüphane.db")

        self.cursor = self.con.cursor()

        query = "Create Table If not exists diziler (name TEXT,type TEXT, season INTEGER)"

        self.cursor.execute(query)

        self.con.commit()

    def disconnect(self):

        self.con.close()

    def show_the_series(self):

        query = "Select * From diziler"

        self.cursor.execute(query)

        lib = self.cursor.fetchall()

        return lib

    def add_series0(self, dizi):

        self.cursor.execute("SELECT rowid FROM diziler WHERE name = ?", (dizi.name0,))
        data = self.cursor.fetchone()

        if data is None:

            query = "INSERT into diziler Values(?,?,?)"
            self.cursor.execute(query, (dizi.name0, dizi.type0, dizi.season0))
            self.con.commit()
            sys.stdout.write("Dizi eklendi\n")
            return True

        else:
            print("Bu dizi listenizde mevcut.\n")
            return False

    def remove_series0(self, name):

        self.cursor.execute("SELECT rowid FROM diziler WHERE name = ?", (name,))
        data = self.cursor.fetchone()

        if data is None:

            print("Böyle bir dizi bulunmuyor.")
            return True

        else:

            query = "Delete From diziler where name = ?"
            self.cursor.execute(query, (name,))
            self.con.commit()
            return False

    def order_by_alphabetic(self):
        query = "SELECT * FROM diziler ORDER BY name"
        data = self.cursor.execute(query).fetchall()
        return data

    def order_by_seasons(self):
        query = "SELECT * FROM diziler ORDER BY season"
        data = self.cursor.execute(query).fetchall()
        return data

    def order_by_type(self):
        query = "SELECT * FROM diziler ORDER BY type"
        data = self.cursor.execute(query).fetchall()
        print(data)
        return data

import sqlite3

DB = "libenix.db"

def conectar():
    return sqlite3.connect(DB)
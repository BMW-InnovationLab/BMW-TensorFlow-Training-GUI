import sqlite3

conn = sqlite3.connect('aliases.db')

def add_alias(name: str, alias: str):
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS aliasTable (name, alias)")
    
    data = (name, alias)
    c.execute("INSERT INTO aliasTable VALUES (?,?)", data)

    conn.commit()


def get_name_from_alias(alias: str):
    try:
        c = conn.cursor()

        data = (alias,) 

        c.execute("SELECT name FROM aliasTable WHERE alias=?", data)
        return c.fetchone()[0]

    except:
        return None


def get_alias_from_name(name: str):
    try:
        c = conn.cursor()

        data = (name,) 

        c.execute("SELECT alias FROM aliasTable WHERE name=?", data)
        return c.fetchone()[0]
    except:
        return None

def delete_alias(alias: str):
    c = conn.cursor()

    data = (alias,)

    c.execute("DELETE FROM aliasTable WHERE alias=?", data)
    conn.commit()


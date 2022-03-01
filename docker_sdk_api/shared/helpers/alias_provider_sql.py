import sqlite3

from domain.models.container_info import ContainerInfo

conn = sqlite3.connect('/docker_sdk_api/assets/aliases.db')


def add_alias(name: str, alias: str, model: str, dataset: str, author: str):
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS aliasTable (name, alias, model, dataset, author)")

    data = (name, alias, model, dataset, author)
    c.execute("INSERT INTO aliasTable VALUES (?,?,?,?,?)", data)

    conn.commit()


def get_all_from_name(name: str):
    try:
        c = conn.cursor()

        data = (name,)

        c.execute("SELECT alias, model, dataset, author FROM aliasTable WHERE name=?", data)
        record = c.fetchone()
        container_info: ContainerInfo = ContainerInfo(name=record[0], model=record[1], dataset=record[2],
                                                      author=record[3])
        return container_info

    except:
        return None


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


def register_tensorboard_mapping(name: str, port: int):
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS tensorboardTable (name, port)")

    data = (name, port)
    c.execute("INSERT INTO tensorboardTable VALUES (?,?)", data)
    conn.commit()


def get_tensorboard_port_from_name(name: str):
    try:
        c = conn.cursor()

        data = (name,)
        c.execute("SELECT port FROM tensorboardTable WHERE name=?", data)

        return c.fetchone()[0]

    except:
        return None


def get_all_ports() -> list:
    try:
        c = conn.cursor()

        c.execute("SELECT port FROM tensorboardTable")
        result = [str(item[0]) for item in c.fetchall()]
        return result

    except:
        return list()


def delete_tensorboard_mapping(name: str):
    try:
        c = conn.cursor()

        data = (name,)
        c.execute("DELETE FROM tensorboardTable WHERE name=?", data)
        conn.commit()

    except:
        return None

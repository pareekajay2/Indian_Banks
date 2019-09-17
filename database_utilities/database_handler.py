import psycopg2
import pandas as pd


def make_connection_prod():
    try:
        conn = psycopg2.connect(
            database="postgres",
            user="postgres",
            password="yagami",
            host="127.0.0.1",
            port="5432",
        )
        return conn
    except:
        print("Unable to connect to the DB")
        return False


def insert_row_banks(bank_id, bank_name):
    conn = make_connection_prod()
    cur = conn.cursor()
    cur.execute("""
        insert into banks values ('%s', %s)
    """ % (bank_name, bank_id))
    conn.commit()


def insert_row_branches(ifsc, bank_id, branch, address, city, district, state):
    conn = make_connection_prod()
    cur = conn.cursor()
    cur.execute("""
            insert into branches values ('%s', '%s', '%s', '%s', '%s', '%s', '%s')
        """ % (ifsc, bank_id, branch, address, city, district, state))
    conn.commit()


def is_bank_exists(bank_id):
    conn = make_connection_prod()
    cur = conn.cursor()
    cur.execute("""
                    select * from banks where id = '%s'
                """ % (bank_id))
    dataframe = pd.DataFrame(cur.fetchall())
    if len(dataframe) != 0:
        return True
    else:
        return False


def is_ifsc_exists(ifsc):
    conn = make_connection_prod()
    cur = conn.cursor()
    cur.execute("""
                        select * from branches where ifsc = '%s'
                    """ % (ifsc))
    dataframe = pd.DataFrame(cur.fetchall())
    if len(dataframe) != 0:
        return True
    else:
        return False
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


csv_data = pd.read_csv("bank_branches.csv")

for row in range(10000):
    bank_id = int(csv_data['bank_id'].iloc[row])
    bank_name = str(csv_data['bank_name'].iloc[row]).replace("'", "''")
    ifsc = csv_data['ifsc'].iloc[row]
    branch = str(csv_data['branch'].iloc[row]).replace("'", "''")
    address = csv_data['address'].iloc[row].replace("'", "''")
    city = csv_data['city'].iloc[row]
    district = csv_data['district'].iloc[row]
    state = csv_data['state'].iloc[row]
    check = is_bank_exists(bank_id)
    check_2 = is_ifsc_exists(ifsc)
    if check == False:
        insert_row_banks(bank_id, bank_name)
    if check_2 == False:
        insert_row_branches(ifsc, bank_id, branch, address, city, district, state)
        
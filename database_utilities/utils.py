from database_utilities.database_handler import make_connection_prod
import pandas as pd


def get_data_banks(ifsc):
    conn = make_connection_prod()
    cur = conn.cursor()
    cur.execute("""
        select b.name, br.*
        from banks b
        inner join branches br
        on b.id = br.bank_id
        where ifsc = '%s'
        """ % (ifsc))
    dataframe = pd.DataFrame(cur.fetchall())

    if len(dataframe) == 0:
        return pd.DataFrame()
    else:
        dataframe.columns = ['bank_name', 'ifsc', 'bank_id', 'branch', 'address', 'city', 'district', 'state']
        return {
            "bank_name": dataframe['bank_name'].iloc[0],
            "ifsc": dataframe['ifsc'].iloc[0],
            "bank_id": int(dataframe['bank_id'].iloc[0]),
            "branch": dataframe['branch'].iloc[0],
            "address": dataframe['address'].iloc[0],
            "city": dataframe['city'].iloc[0],
            "district": dataframe['district'].iloc[0],
            "state": dataframe['state'].iloc[0]
        }


def get_data_branchs(city, bank_name, offset, limit):
    conn = make_connection_prod()
    cur = conn.cursor()
    if limit == None:
        cur.execute("""
            select b.name, br.*
            from banks b
            inner join branches br
            on b.id = br.bank_id
            where city = '%s'
            and name = '%s'
            order by ifsc asc
            offset %s

            """ % (city, bank_name, int(offset)))
    else:
        cur.execute("""
                    select b.name, br.*
                    from banks b
                    inner join branches br
                    on b.id = br.bank_id
                    where city = '%s'
                    and name = '%s'
                    order by ifsc asc
                    offset %s limit %s

                    """ % (city, bank_name, int(offset), int(limit)))
    dataframe = pd.DataFrame(cur.fetchall())

    if len(dataframe) == 0:
        return pd.DataFrame()
    else:
        dataframe.columns = ['bank_name', 'ifsc', 'bank_id', 'branch', 'address', 'city', 'district', 'state']
        return dataframe


def get_branch_details(city, bank_name, offset, limit):
    dataframe = get_data_branchs(city, bank_name, offset, limit)
    data_frame = []
    for row in range(len(dataframe)):
        data_frame.append({
            "bank_name": dataframe['bank_name'].iloc[row],
            "ifsc": dataframe['ifsc'].iloc[row],
            "bank_id": int(dataframe['bank_id'].iloc[row]),
            "branch": dataframe['branch'].iloc[row],
            "address": dataframe['address'].iloc[row],
            "city": dataframe['city'].iloc[row],
            "district": dataframe['district'].iloc[row],
            "state": dataframe['state'].iloc[row]
        })
    return data_frame
from sqlalchemy import create_engine
import pandas as pandas


def read_csv(csv):
    data = pandas.read_csv(csv)
    df = pandas.DataFrame(data)
    print(df.head(10))
    return None


# set tables

def auto_seed_csv(csv, table_name, connection_url):
    database_engine = create_engine(
        connection_url
    )
    data = pandas.read_csv(csv)
    df = pandas.DataFrame(data)
    df.to_sql(table_name, database_engine, if_exists='replace')
    return None

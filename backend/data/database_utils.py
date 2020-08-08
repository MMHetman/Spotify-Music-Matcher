from sqlalchemy import create_engine


def upload_dataframe_as_table(dataframe, table_name):
    sql_engine = create_engine('mysql+pymysql://root:password@localhost/spotify_music_matcher', pool_recycle=3600)
    db_connection = sql_engine.connect()

    try:
        dataframe.to_sql(table_name, db_connection, if_exists='fail')
    except ValueError as vx:
        print(vx)
    except Exception as ex:
        print(ex)
    else:
        print("Table %s created successfully." % table_name)
    finally:
        db_connection.close()

import pandas as pd
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


def get_tracks_sample_by_genres(sample_size, genres):
    sql_engine = create_engine('mysql+pymysql://root:password@localhost/spotify_music_matcher', pool_recycle=3600)
    genres_query = 'SELECT DISTINCT genre_name FROM genres'
    db_genres = pd.read_sql(genres_query, sql_engine)
    db_genres = db_genres['genre_name'].tolist()
    genres_str = ''
    for genre in genres:
        if genre not in db_genres:
            raise Exception('No such a genre: ' + genre)
        genres_str += "'" + genre + "', "
    genres_str = genres_str[:-2]
    print(genres_str)
    tracks_query = 'select distinct track_name, artist_name, tracks.track_id, genre_name ' \
                   'from tracks join track_n_artist tna on tracks.track_id = tna.track_id ' \
                   'join artists a on tna.artist_id = a.artist_id join artist_n_genre ang on a.artist_id = ang.artist_id ' \
                   'join genres g on ang.genre_id = g.genre_id ' \
                   'where genre_name in (' + genres_str + ') and sample is not null;'

    tracks_df = pd.read_sql(tracks_query, sql_engine)
    return tracks_df.groupby('genre_name').apply(lambda s: s.sample(min(len(s), sample_size)))





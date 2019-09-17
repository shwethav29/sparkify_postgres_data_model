import os
import glob
import psycopg2
import time
import csv
import pandas as pd
from sql_queries import *
from io import StringIO
import io


def process_song_file(cur, filepath):
    # open song file
    df = pd.read_json(filepath, lines=True)

    # insert song record
    song_data = df[['song_id', 'title', 'artist_id', 'year', 'duration']].values[0].tolist()

    cur.execute(song_table_insert, song_data)

    # insert artist record
    artist_data = df[['artist_id', 'artist_name', 'artist_location', 'artist_latitude', 'artist_longitude']].values[
        0].tolist()

    cur.execute(artist_table_insert, artist_data)


def create_stage_table(cur, table_name):
    query = create_stage_table_queries[table_name]
    cur.execute(query)


def load_data_from_stage_table(cur, table_name):
    query = load_from_stage_table_queries[table_name]
    cur.execute(query)


def drop_stage_table(cur, table_name):
    query = drop_stage_table_queries[table_name]
    cur.execute(query)

def load_data_to_database(cur,data_df,stage_table_name,table_name,seperator):
    data_io = io.StringIO()
    data_df.to_csv(data_io, header=False, index=False,sep=seperator)
    data_io.seek(0)
    cur.copy_from(data_io,stage_table_name,sep=seperator)
    load_data_from_stage_table(cur,table_name)

def process_log_file(cur, filepath):
    # open log file
    df = pd.read_json(filepath, lines=True)

    # filter by NextSong action
    df = df[df.page == 'NextSong']

    # convert timestamp column to datetime
    t = pd.to_datetime(df['ts'], unit='ms')

    # insert time data records
    time_data = (df['ts'], t.dt.hour, t.dt.day, t.dt.weekofyear, t.dt.month, t.dt.year, t.dt.weekday)
    column_labels = ('start_time', 'hour', 'day', 'week', 'month', 'year', 'weekday')
    time_df = pd.DataFrame(dict(zip(column_labels, time_data)))
    load_data_to_database(cur,time_df,"temp_time","time",',')

    # for i, row in time_df.iterrows():
    #    cur.execute(time_table_insert, list(row))

    # load user table then copy to csv use copy from to load data to POSTGRES
    user_df = df[['userId', 'firstName', 'lastName', 'gender', 'level']]
    user_df = user_df.drop_duplicates(subset=['userId'], keep=False)
    load_data_to_database(cur, user_df, "temp_users", "users", ',')

    # insert user records
    # for i, row in user_df.iterrows():
    #    cur.execute(user_table_insert, row)

    #load songplays data
    song_play_df = df[['ts', 'userId', 'level', 'song', 'artist', 'sessionId', 'location', 'length', 'userAgent']]
    load_data_to_database(cur, song_play_df, "temp_songplays", "songplays", '\t')

def process_data(cur, conn, filepath, func):
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root, '*.json'))
        for f in files:
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()
    # create stage tables
    start = time.time()
    create_stage_table(cur, "time")
    create_stage_table(cur, "users")
    create_stage_table(cur, "songplays")

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    # drop stage tables
    drop_stage_table(cur, "users")
    drop_stage_table(cur, "time")
    drop_stage_table(cur, "songplays")

    end = time.time()
    print("the etl takes", end - start, "seconds")
    conn.close()


if __name__ == "__main__":
    main()
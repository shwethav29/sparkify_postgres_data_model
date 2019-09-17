# DROP TABLES

songplay_table_drop = "DROP TABLE IF EXISTS songplays"
user_table_drop = "DROP TABLE IF EXISTS users"
song_table_drop = "DROP TABLE IF EXISTS songs"
artist_table_drop = "DROP TABLE IF EXISTS artists"
time_table_drop = "DROP TABLE IF EXISTS time"

# CREATE TABLES

songplay_table_create = ("""CREATE TABLE IF NOT EXISTS songplays(songplay_id SERIAL PRIMARY KEY,start_time bigint,user_id bigint,
level varchar,song_id varchar,artist_id varchar,session_id varchar,location varchar,user_agent varchar,
CONSTRAINT u_constraint UNIQUE(start_time,user_id,level,song_id,artist_id,session_id,location,user_agent));
""")

user_table_create = ("""CREATE TABLE IF NOT EXISTS users(user_id varchar PRIMARY KEY,first_name varchar,last_name varchar,
gender varchar,level varchar)
""")

song_table_create = ("""CREATE TABLE IF NOT EXISTS songs(song_id varchar PRIMARY KEY,title varchar,artist_id varchar,year int,
duration numeric(10,6))
""")

artist_table_create = ("""CREATE TABLE IF NOT EXISTS artists(artist_id varchar PRIMARY KEY,name varchar,location varchar,latitude varchar,
longitude varchar) 
""")

time_table_create = ("""CREATE TABLE IF NOT EXISTS time(start_time bigint PRIMARY KEY,hour int,day int,week int,month int, year int,weekday int)
""")

# INSERT RECORDS

songplay_table_insert = ("""INSERT INTO songplays(start_time,user_id,level,song_id,artist_id,session_id,location,user_agent)
VALUES(%s,%s,%s,%s,%s,%s,%s,%s)
""")

user_table_insert = ("""INSERT INTO users(user_id,first_name,last_name,gender,level) VALUES(%s,%s,%s,%s,%s)
ON CONFLICT (user_id) DO NOTHING;
""")

song_table_insert = ("""INSERT INTO songs(song_id,title,artist_id,year,duration) VALUES(%s,%s,%s,%s,%s)
ON CONFLICT (song_id) DO NOTHING;
""")

artist_table_insert = ("""INSERT INTO artists(artist_id,name,location,latitude,longitude) VALUES(%s,%s,%s,%s,%s)
ON CONFLICT (artist_id) DO NOTHING;
""")


time_table_insert = ("""INSERT INTO time(start_time,hour,day,week,month,year,weekday) VALUES(%s,%s,%s,%s,%s,%s,%s)
ON CONFLICT (start_time) DO NOTHING;
""")

# FIND SONGS

song_select = ("""select songs.song_id,songs.artist_id from songs join artists on songs.artist_id=artists.artist_id where songs.title = %s and artists.name=%s and songs.duration=%s
""")

# QUERY LISTS

create_table_queries = [songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]

#CREATE STAGE TABLE
create_users_stage=("""CREATE UNLOGGED TABLE IF NOT EXISTS temp_users(user_id varchar,first_name varchar,last_name varchar,
gender varchar,level varchar)
""")

create_time_stage =("""CREATE UNLOGGED TABLE IF NOT EXISTS temp_time(start_time bigint,hour int,day int,week int,month int, year int,weekday int)
""")

create_songplays_stage=("""CREATE TABLE IF NOT EXISTS temp_songplays(start_time bigint,user_id bigint,
level varchar,song varchar,artist varchar,session_id varchar,location varchar,length numeric(10,6),user_agent varchar)""")

create_stage_table_queries = {"users":create_users_stage,"time":create_time_stage,"songplays":create_songplays_stage}

#LOAD from stage table
load_from_stage_temp_users_users =("""INSERT INTO users(user_id,first_name,last_name,gender,level)
SELECT tu.user_id,tu.first_name,tu.last_name,tu.gender,tu.level from temp_users tu inner join (select DISTINCT(user_id) from temp_users) u on tu.user_id = u.user_id
ON CONFLICT (user_id) DO NOTHING;
""")

load_from_stage_temp_time_time=("""INSERT INTO time(start_time,hour,day,week,month,year,weekday) 
SELECT tt.start_time,tt.hour,day,tt.week,tt.month,tt.year,tt.weekday from temp_time tt inner join (select DISTINCT(start_time) from temp_time) t on tt.start_time = t.start_time
ON CONFLICT (start_time) DO NOTHING;
""")


load_from_stage_temp_songplays_songplays=("""INSERT INTO songplays (start_time,user_id,level,song_id,artist_id,session_id,location,user_agent)

SELECT DISTINCT start_time,user_id,level,song_id,artist_id,session_id,location,user_agent

FROM(

SELECT se.start_time, se.user_id, se.level, sa.song_id, sa.artist_id, se.session_id, se.location, se.user_agent

FROM temp_songplays se

JOIN

(SELECT songs.song_id, artists.artist_id, songs.title, artists.name,songs.duration

FROM songs

JOIN artists

ON songs.artist_id = artists.artist_id) AS sa

ON (sa.title = se.song

AND sa.name = se.artist

AND sa.duration = se.length)) as details
ON CONFLICT (start_time,user_id,level,song_id,artist_id,session_id,location,user_agent) DO NOTHING;
""")

load_from_stage_table_queries ={"users":load_from_stage_temp_users_users,"time":load_from_stage_temp_time_time,"songplays":load_from_stage_temp_songplays_songplays}

#DROP stage tables
drop_users_stage="DROP TABLE IF EXISTS temp_users"

drop_time_stage="DROP TABLE IF EXISTS temp_time"

drop_songplays_stage="DROP TABLE IF EXISTS temp_songplays"

drop_stage_table_queries={"users":drop_users_stage,"time":drop_time_stage,"songplays":drop_songplays_stage}


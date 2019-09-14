# SPARKIFY

Sparkify is a music streaming startup. They have been collecting songs metadata and user activity of their app.

Going forward their analytics team wants to use this data, and understand what songs are the users listening to. Currently data resides in directory of JSON logs and song data in JSON metadata files.

## Purpose

The purpose of this project is to make the data easily available to the Sparkify analytics team. To achieve this we need to design a Postgres database optimized for queries on songs play data analysis.

####> Steps to follow.
>>1 Identify the facts and dimension tables for creating star schema. 

>>2 Build a ETL pipeline using python, to transfer data from files, in the two directories under data directory to PostGres.

## Schema
We will be creating a star schema with following facts and dimension tables

###>**Fact table**
 >>**1. SONGPLAYS -** log data associated with song play, which is with page='NextPage'.
 >>>>songplay_id a auto_increment id column, start_time bigint,user_id bigint,level varchar,song_id varchar,artist_id varchar,session_id varchar,location varchar,user_agent varchar
 
### >**Dimension tables**
 >>**1. USERS -** user data from the log_data
 >>>>user_id varchar,first_name varchar,last_name varchar,gender varchar,level varchar

>>**2. ARTISTS -** artists data from song_data directory
 >>>>artist_id varchar,name varchar,location varchar,latitude varchar,longitude varchar

>>**3. SONGS -** song data from the song_data directory
 >>>>song_id varchar,title varchar,artist_id varchar,year int,duration numeric

>>**4. TIME -** time data extracted from the timestamp field of lod_data
 >>>>start_time bigint,hour int,day int,week int,month int, year int,weekday int 

 
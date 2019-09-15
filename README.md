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
In case of Sparkify app, the songs played by the users is the business process that needs to be modelled. The song played is the fact grain.  The ETL pipeline will extract this data from the 
files in the log_data and will populate this table. The primary key for this table is the songplay_id
which is auto generated. 
 >>**1. SONGPLAYS -** log data associated with song play, which is with page='NextPage'.
 >>>>songplay_id a auto_increment id column, start_time bigint,user_id bigint,level varchar,song_id varchar,artist_id varchar,session_id varchar,location varchar,user_agent varchar
 
### >**Dimension tables**
We have recognised 4 dimension tables to capture user data, song data, artist data and to provide a 
time data. The time table helps to slice and dice data based on different time variables.
 >>**1. USERS -** user data from the log_data
 >>>>user_id varchar,first_name varchar,last_name varchar,gender varchar,level varchar

>>**2. ARTISTS -** artists data from song_data directory
 >>>>artist_id varchar,name varchar,location varchar,latitude varchar,longitude varchar

>>**3. SONGS -** song data from the song_data directory
 >>>>song_id varchar,title varchar,artist_id varchar,year int,duration numeric

>>**4. TIME -** time data extracted from the timestamp field of lod_data
 >>>>start_time bigint,hour int,day int,week int,month int, year int,weekday int 

### >**ETL Pipeline**
We will be using python pandas to read the json files from the log_data and song_data. Firstly we will be populating the dimension tables.
Followed by reading the artist_id and song_id keys from these dimension table to populate the songplays table.
We are interested only in log_data with page='NextPage'. The timestamp column mapped to the time table by extracting datetime properties for the give timestamp. 
##Project Structure
1.All the sql queries are defined in sql_queries.py
2.create_tables.sql creates sparkify schema.
3.etl.py is the ETL pipeline to process the log_data and song_data under data directory and populate the tables.

##Steps
1. execute create_tables.py
2. execute etl.py
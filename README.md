#Purpose
Sparkify is a music streaming startup. They have been collecting songs metadata and user activity of their app.

Going forward their analytics team wants to use this data, and understand what songs are the users listening to. Currently data resides in directory of JSON logs and song data in JSON metadata files.

The purpose of this project is to make the data easily available to the Sparkify analytics team. To achieve this we need to design a Postgres database optimized for queries on songs data.

####>Steps to follow.
>>1 Identify the facts and dimension tables for creating star schema. 

>>2 Build a ETL pipeline using python, to transfer data from files, in the two directories under data directory to PostGres.


 
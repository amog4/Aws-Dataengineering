from logging import exception
import boto3
import json,time

# A session stores configuration state and allows you to create service clients and resources 


session = boto3.Session(profile_name='working-dev')

athene_client = session.client('athena')

s3 = session.client('s3')

bucket_name ='userdata'

# Binary files and network io (stores data in ram)
with open('social_media_data/social_media.csv', 'rb') as r:
    s3.upload_fileobj(r, bucket_name, 'social_media_files.csv')

#Similar behavior as S3Transfer's upload_file() method, except that parameters are capitalized. Detailed examples can be #found at S3Transfer's Usage.
s3.upload_file(
        Filename='social_media_data/social media visitors.csv' ,
        Bucket=bucket_name,
        Key='social_media_files/social media visitors.csv')


# first need to create a workgroup only once

try:
    response = athene_client.create_work_group(
        Name='data-analysis-wg',
        Configuration={
            'ResultConfiguration': {
                'OutputLocation': f's3://{bucket_name}/athena_workgroup',
                'EncryptionConfiguration': {
                'EncryptionOption': 'SSE_S3'
                
            }
                
            },
            'EnforceWorkGroupConfiguration': True,
            'PublishCloudWatchMetricsEnabled': True,
            'RequesterPaysEnabled': True
        },
        Description='Athena work group'
        
    )
except Exception as e:
    pass

# create metadata database in athena 

create_database = """ create database if not exists social_media_db"""

db = athene_client.start_query_execution(
    QueryString=create_database,
    WorkGroup='data-analysis-wg'
)

#schema 
data_catalog_query = f""" CREATE EXTERNAL TABLE if not exists social_media_db.socialmedia (
                        `ID` string,
                        `Datef` date,
                        `DailyEngaged_Users`  string,
                        `MonthlyEngagedUsers` string,
                        `WeeklyPageEngagedUsers` string,
                        `LifetimeTotalLikes` string,
                        `DailyotalReach` string,
                        `WeeklytotalReach` string,
                        `TotalMonthlyReach` string
                        )
                        ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.lazy.LazySimpleSerDe'
                        WITH SERDEPROPERTIES (
                        'serialization.format' = ',',
                        'field.delim' = ','
                        ) LOCATION 's3://{bucket_name}/social_media_files.csv'
                        TBLPROPERTIES ('has_encrypted_data'='false') """


# get the responce 

responce = athene_client.start_query_execution(
    QueryString=data_catalog_query,
    WorkGroup='data-analysis-wg'
)

# run select query


query = "select * from social_media_db.socialmedia"

responce = athene_client.start_query_execution(
    QueryString=query,
    WorkGroup='data-analysis-wg'
)


execution_info = athene_client.get_query_execution(QueryExecutionId = responce['QueryExecutionId'])

# get file location

path= execution_info['QueryExecution']['ResultConfiguration']['OutputLocation']

print(path)

# how we can use the path and read the file using boto3
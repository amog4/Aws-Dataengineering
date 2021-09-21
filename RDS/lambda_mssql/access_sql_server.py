import pyodbc
import os,json



server = os.getenv('MSSQL_SERVER')
username  = os.getenv('MSSQL_USERNAME')
password = os.getenv('MSSQL_PASSWORD')

def sql_server_connect(server ,database,username ,password):
    conn = pyodbc.connect(r"DRIVER={ODBC Driver 17 for SQL Server};SERVER="+server+';PORT=1433'+';DATABASE='+database+';UID='+username+';PWD='+password)
    return conn

def lambda_handler(event, context):
    conn = sql_server_connect(server = server,
                        database = 'master',
                        username =username ,
                        password =password)


    cur =  conn.cursor()

    sql_01 = """
                SELECT * FROM INFORMATION_SCHEMA.TABLES

            """
    x = cur.execute(sql_01) 

    print(x.fetchall())
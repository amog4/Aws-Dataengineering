# Connect mssql rds from Lambda 

* As Lambda is a linux environment package pyodbc requires addition packages like MS odbc driver and unixodbc 

* I followed [this](https://medium.com/@narayan.anurag/breaking-the-ice-between-aws-lambda-pyodbc-6f53d5e2bd26) blog to get the additional requirements package.zip (very useful)

* Create a layer and push the zip by CLI

* Lambda should be in same VPC



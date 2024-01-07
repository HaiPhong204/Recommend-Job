import pyodbc
import pandas as pd

connection_string = "Driver={ODBC Driver 18 for SQL Server};Server=tcp:windydb.database.windows.net,1433;Database=CliverDB;Uid=windy-server;Pwd=Phongpro279;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"

connection = pyodbc.connect(connection_string)

# Query để lấy dữ liệu từ bảng Jobs
jobs_query = "SELECT * FROM Post"
jobs_data = pd.read_sql(jobs_query, connection)

# Đóng kết nối
connection.close()


# Xuất DataFrame vào một tệp Excel
jobs_data.to_excel('job_data.xlsx', index=False)

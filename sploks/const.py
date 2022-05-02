import mysql.connector

# TODO: Replace "..." with your own SQL config
con = mysql.connector.connect(
    host="localhost",
    user="splAdmin",
    password="Pa$$w0rd",
    database="sploks",
    auth_plugin='mysql_native_password'
)
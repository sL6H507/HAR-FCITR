import mysql.connector
import os

mydb = mysql.connector.connect(
  host="",
  user="",
  password='',
  database="fcitrprojectkh"
)
cursor = mydb.cursor()

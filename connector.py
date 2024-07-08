import mysql.connector
import os

mydb = mysql.connector.connect(
  host="database-1.cz48cuo4sfq2.us-east-1.rds.amazonaws.com",
  user="admin",
  password='bKKWss1YA2xaEsEpj73l',
  database="fcitrprojectkh"
)
cursor = mydb.cursor()
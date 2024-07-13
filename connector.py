import mysql.connector
import os

mydb = mysql.connector.connect(
  host="database-1.cz48cuo4sfq2.us-east-1.rds.amazonaws.com",
  user="fcitrproject3",
  password='dEqAze6u',
  database="fcitrprojectkh"
)
cursor = mydb.cursor()
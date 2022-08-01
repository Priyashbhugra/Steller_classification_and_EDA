from app import db
print("Creating database table")
# create database for storing the entries and predictions
db.create_all()
print("Table created")
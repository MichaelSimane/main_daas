import csv
import os
import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine("postgresql+psycopg2://postgres:postgres@localhost/DAAS")
# engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

def main():
    data = pd.read_csv (r'Yejubie.csv')   
    df = pd.DataFrame(data)
    
    for row in df.itertuples():
        # we use these if we don't know the value yet 
        db.execute("INSERT INTO dbapi_Weather (year, month, day, tmin, tmax, rain, district_id) VALUES(:year, :month, :day, :tmin, :tmax, :rain, 3)", {"year": row.year, "month": row.month, "day": row.day, "tmin": row.tmin, "tmax": row.tmax, "rain": row.rain})
        print(f"Added weather from {row.year} , {row.month}, day {row.day}")
        # saves the change 
        db.commit()
if __name__ =="__main__":
	main()		


# import pandas as pd
# import pyodbc

# # Import CSV
# data = pd.read_csv (r'Debre_elias.csv')   
# df = pd.DataFrame(data)

# # Connect to SQL Server
# # conn_str = (
# #     "DRIVER={PostgreSQL};"
# #     "DATABASE=postgres;"
# #     "UID=postgres;"
# #     "PWD=postgres;"
# #     "SERVER=localhost;"
# #     "PORT=5432;"
# #     )
# conn = pyodbc.connect("Driver={SQL Server};Server=localhost;Port=5432;Database=DAAS;Uid=postgres;Pwd=postgres;")
# cursor = conn.cursor()

# # Create Table

# # Insert DataFrame to Table
# for row in df.itertuples():
#     cursor.execute('INSERT INTO Weather (year, month, day, tmin, tmax, rain) VALUES (?,?,?,?,?,?)', row.year, row.month, row.day, row.tmin, row.tmax, row.rain)
#     print(f"Added weather from {row.year} , {row.month}, day {row.day}")
# conn.commit()
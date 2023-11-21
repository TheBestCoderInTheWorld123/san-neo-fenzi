from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote_plus
from model import *

db_host = '51.20.144.184'
db_username = 'iot_dev'
db_password = 'iod@developer'
db_name = 'iot_penguin'
encoded_password = quote_plus(db_password)
# Adjust the connection URL
db_url = f'postgresql://{db_username}:{encoded_password}@{db_host}/{db_name}'

engine = create_engine(db_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
# Create the database tables
Base.metadata.create_all(engine)

# Function to insert test data
def insert_test_data():
    db = SessionLocal()

    # Sample test data to insert into the table
    test_items = [
        {"address_id": 1, "address_line1": "pakistain, islamabad", "address_line2": "house 45, 13th street, sector 12", "city": "islamabad", "postal_code": "44000", "country": "pakistain", "latitude": "23.00", "longitude": "23.00", "created_by": "shayan", "created_at": "11-20-2023", "updated_by": "shayan", "updated_at": "11-20-2023"}
        # Add more test data as needed
    ]

    try:
        for item_data in test_items:
            db_item = Address(**item_data)
            db.add(db_item)

        db.commit()
        print("Test data inserted successfully")
    except Exception as e:
        db.rollback()
        print(f"Failed to insert test data: {str(e)}")
    finally:
        db.close()

if __name__ == "__main__":
    insert_test_data()  # Call the function when the script is executed

from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from model import Base, History, Device, DeviceTag, Tag, db_url # Import your model classes
from datetime import datetime

# Assuming your database URI is stored in 'DATABASE_URI'
# DATABASE_URI = 'your_database_uri'
engine = create_engine(db_url)
Session = sessionmaker(bind=engine)

# Your data
data = {
    0: [{'IMEI': '862174069140333'}, {'AQ': '10.0'}, {'status': '>'}, {'date_time': datetime(2023, 11, 21, 13, 2)}],
    1: [{'IMEI': '862174069140333'}, {'HUM': '51'}, {'status': ''}, {'date_time': datetime(2023, 11, 21, 13, 2)}],
    2: [{'IMEI': '862174069140333'}, {'TMP': '32'}, {'status': ''}, {'date_time': datetime(2023, 11, 21, 13, 2)}]
}

def get_device_id(session, imei):
    return session.query(Device.device_id).filter(Device.device_serial_number == imei).scalar()

def get_tag_id(session, description):
    return session.query(Tag.tag_id).filter(Tag.description == description).scalar()

def get_device_tag_id(session, device_id, tag_id):
    return session.query(DeviceTag.ID).filter(DeviceTag.device_id == device_id, DeviceTag.tag_id == tag_id).scalar()

def insert_history_data(session, data):
    for _, entries in data.items():
        imei = entries[0]['IMEI']
        device_id = get_device_id(session, imei)

        for entry in entries[1:]:
            for tag_description, value in entry.items():
                if tag_description in ['status', 'date_time']:
                    continue

                tag_id = get_tag_id(session, tag_description)
                device_tag_id = get_device_tag_id(session, device_id, tag_id)
                history_entry = History(
                    device_tag_id=device_tag_id,
                    value=float(value),
                    status=entries[2]['status'],
                    recorded_date_time=entries[3]['date_time'],
                    created_by = 'mqtt',
                    created_at = datetime.now(),
                    updated_by = 'mqtt' ,
                    updated_at = datetime.now()

                )
                session.add(history_entry)
    session.commit()

# Main execution
session = Session()
# insert_history_data(session, data)

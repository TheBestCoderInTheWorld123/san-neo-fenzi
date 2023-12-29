from contextlib import contextmanager
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from model import * # Import your model classes
from app import sqlalchemy_to_dict
from datetime import datetime, timedelta
import requests
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

def get_device_type(session, imei):
    return session.query(Device.device_type_id).filter(Device.device_serial_number == imei).scalar()

def get_device_id(session, imei):
    return session.query(Device.device_id).filter(Device.device_serial_number == imei).scalar()

def get_tag_id(session, description):
    return session.query(Tag.tag_id).filter(Tag.description == description).scalar()

def get_device_tag_id(session, device_id, tag_id):
    return session.query(DeviceTag.ID).filter(DeviceTag.device_id == device_id, DeviceTag.tag_id == tag_id).scalar()

def insert_alert(session, data):
    bln_insert = True
    if bln_insert:
        for i, entries in data.items():
            imei = entries[0]['IMEI']
            imei = imei.replace('"', '')
            time_stamp = entries[3]['date_time']
            tag_name, tag_value = next(iter(entries[1].items()))

            tag_id = get_tag_id(session, tag_name)
            device_id = get_device_id(session, imei)
            device_tag_id = get_device_tag_id(session, device_id, tag_id)

            # Check if tag_id exists in AlertConfig and meets your condition
            alert_configs = session.query(AlertConfig).filter(
                AlertConfig.tag_id == tag_id,
                AlertConfig.device_id == device_id
            ).all()

            # Iterate over each alert_config record
            for alert_config in alert_configs:
                alert_type = alert_config.alert_type
                # Assuming alert_type is a field in AlertConfig
                # current_tag_value = your_current_tag_value  # Replace with the current tag value you have
                # Example timestamp
                # Convert the string to a datetime object
                # print('alert', datetime)
                # timestamp = datetime.strptime(time_stamp, '%Y/%m/%d %H:%M')
                # print('alert', time_stamp)
                time_threshold = time_stamp - timedelta(minutes=30)  # Adjust the timedelta as needed

                # Query to get records from the last 30 minutes for a specific tag_id
                recent_records = session.query(History).filter(
                    History.device_tag_id == device_tag_id,
                    History.recorded_date_time >= time_threshold
                ).all()

                # Check if any of the recent records have the same tag_value
                alert_needed = any(record.value == float(tag_value) for record in recent_records)
                print('is alert needed for the tag value:', tag_value, ' ',alert_needed)

                alert_flag = False
                # Generate an alert if needed
                if alert_needed:
                    if tag_name == 'AQ':
                        if alert_config.tag_value_min < float(tag_value) < alert_config.tag_value_max:
                            alert_flag = True
                    else:
                        if float(tag_value) < alert_config.tag_value_min or float(tag_value) > alert_config.tag_value_max:
                            alert_flag = True

                if alert_flag:
                    # Create an alert
                    alert = alert_values_out_of_range(
                        tag_id=tag_id,
                        tag_value=float(tag_value),
                        tag_name=tag_name,
                        alert_type=alert_type,
                        time=time_stamp,
                        device_serial_num=imei
                    )
                    session.add(alert)

            # Commit all new alert records to the database
            session.commit()


def insert_history_data(session, data):
    for _, entries in data.items():
        imei = entries[0]['IMEI']
        imei = imei.replace('"', '')
        # print('imei', imei)
        device_id = get_device_id(session, imei)
        # device_type_id = get_device_type(session, imei)
        # print('device_id',device_id)
        bln_insert = True
        # for entry in entries[1:]:
            # for tag_description, value in entry.items():

                # if tag_description == 'AQ':
                #     # logic for AQ tag as per discussion with client
                #     value = (-1) * ((float(value) * 2) - 20)
                #     value = round(value, 2)
                #     if value == 15.06 or value == 11.76:
                #         bln_insert = False
        if bln_insert:

            for entry in entries[1:]:
                for tag_description, value in entry.items():
                    if tag_description in ['status', 'date_time']:
                        continue

                    tag_id = get_tag_id(session, tag_description)
                    device_tag_id = get_device_tag_id(session, device_id, tag_id)
                    # if tag_description == 'AQ' or tag_id == 1:
                    #     # logic for AQ tag as per discussion with client
                    #     value = (-1) * ((float(value)*2) - 20)
                    #     value = round(value, 2)
                        # if(value == 15.06 or value == 11.76):

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


@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()

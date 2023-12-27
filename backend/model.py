# coding: utf-8
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, DECIMAL, BIGINT, Numeric, Table, Sequence
from sqlalchemy.sql import text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from urllib.parse import quote_plus
from sqlalchemy.orm import mapper
from sqlalchemy.orm import registry
from sqlalchemy import MetaData
from sqlalchemy import select
# Create an instance of MetaData
metadata = MetaData()

# Update the database connection information
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

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class ActionType(Base):
    __tablename__ = 'action_types'

    action_type_id = Column(Integer, primary_key=True, server_default=text("nextval('action_types_action_type_id_seq'::regclass)"))
    description = Column(String(255))
    created_by = Column(String(255))
    created_at = Column(DateTime)
    updated_by = Column(String(255))
    updated_at = Column(DateTime)


class Address(Base):
    __tablename__ = 'addresses'

    address_id = Column(Integer, primary_key=True, server_default=text("nextval('addresses_address_id_seq'::regclass)"))
    address_line1 = Column(String(255))
    address_line2 = Column(String(255))
    city = Column(String(255))
    state = Column(String(255))
    postal_code = Column(String(255))
    country = Column(String(255))
    latitude = Column(Numeric(10, 7))
    longitude = Column(Numeric(10, 7))
    created_by = Column(String(255))
    created_at = Column(DateTime)
    updated_by = Column(String(255))
    updated_at = Column(DateTime)

    # users = relationship('User', secondary='user_addresses')


class AssetType(Base):
    __tablename__ = 'asset_types'

    asset_type_id = Column(Integer, primary_key=True, server_default=text("nextval('asset_types_asset_type_id_seq'::regclass)"))
    description = Column(String(255))
    created_by = Column(String(255))
    created_at = Column(DateTime)
    updated_by = Column(String(255))
    updated_at = Column(DateTime)


class ConnectionType(Base):
    __tablename__ = 'connection_types'

    connection_type_id = Column(Integer, primary_key=True, server_default=text("nextval('connection_types_connection_type_id_seq'::regclass)"))
    description = Column(String(255))
    created_by = Column(String(255))
    created_at = Column(DateTime)
    updated_by = Column(String(255))
    updated_at = Column(DateTime)


class ContactType(Base):
    __tablename__ = 'contact_types'

    contact_type_id = Column(Integer, primary_key=True, server_default=text("nextval('contact_types_contact_type_id_seq'::regclass)"))
    description = Column(String(255))
    created_by = Column(String(255))
    created_at = Column(DateTime)
    updated_by = Column(String(255))
    updated_at = Column(DateTime)


class DeviceType(Base):
    __tablename__ = 'device_type'

    device_type_id = Column(Integer, primary_key=True, server_default=text("nextval('device_type_device_type_id_seq'::regclass)"))
    description = Column(String(255))
    created_by = Column(String(255))
    created_at = Column(DateTime)
    updated_by = Column(String(255))
    updated_at = Column(DateTime)


class Tag(Base):
    __tablename__ = 'tags'

    tag_id = Column(Integer, primary_key=True, server_default=text("nextval('tags_tag_id_seq'::regclass)"))
    description = Column(String(255))
    unit_of_measure = Column(String(255))
    created_by = Column(String(255))
    created_at = Column(DateTime)
    updated_by = Column(String(255))
    updated_at = Column(DateTime)


class UserGroup(Base):
    __tablename__ = 'user_group'

    user_group_id = Column(Integer, primary_key=True, server_default=text("nextval('user_group_user_group_id_seq'::regclass)"))
    group_name = Column(String(255))
    created_by = Column(String(255))
    created_at = Column(DateTime)
    updated_by = Column(String(255))
    updated_at = Column(DateTime)

    # users = relationship('User', secondary='user_group_membership')


class UserRole(Base):
    __tablename__ = 'user_role'

    role_id = Column(Integer, primary_key=True, server_default=text("nextval('user_role_role_id_seq'::regclass)"))
    role_name = Column(String(255))
    created_by = Column(String(255))
    created_at = Column(DateTime)
    updated_by = Column(String(255))
    updated_at = Column(DateTime)

    # users = relationship('User', secondary='user_role_assignment')


class Action(Base):
    __tablename__ = 'actions'

    action_id = Column(Integer, primary_key=True, server_default=text("nextval('actions_action_id_seq'::regclass)"))
    description = Column(String(255))
    action_type_id = Column(ForeignKey('action_types.action_type_id'))
    action_taken_datetime = Column(DateTime)
    created_by = Column(String(255))
    created_at = Column(DateTime)
    updated_by = Column(String(255))
    updated_at = Column(DateTime)

    # action_type = relationship('ActionType')
    # alerts = relationship('Alert', secondary='actions_alert')
    # historys = relationship('History', secondary='actions_history')


class Asset(Base):
    __tablename__ = 'assets'

    asset_id = Column(Integer, primary_key=True, server_default=text("nextval('assets_asset_id_seq'::regclass)"))
    asset_type_id = Column(ForeignKey('asset_types.asset_type_id'))
    created_by = Column(String(255))
    created_at = Column(DateTime)
    updated_by = Column(String(255))
    updated_at = Column(DateTime)

    # asset_type = relationship('AssetType')


class Contact(Base):
    __tablename__ = 'contacts'

    contact_id = Column(Integer, primary_key=True, server_default=text("nextval('contacts_contact_id_seq'::regclass)"))
    contact_description = Column(String(255))
    contact_type_id = Column(ForeignKey('contact_types.contact_type_id'))
    created_by = Column(String(255))
    created_at = Column(DateTime)
    updated_by = Column(String(255))
    updated_at = Column(DateTime)

    # contact_type = relationship('ContactType')
    # locations = relationship('Location', secondary='location_contacts')
    # users = relationship('User', secondary='user_contacts')


class Location(Base):
    __tablename__ = 'locations'

    location_id = Column(Integer, primary_key=True, server_default=text("nextval('locations_location_id_seq'::regclass)"))
    location_name = Column(String(255))
    location_desc = Column(String(255))
    location_type_id = Column(Integer)
    location_root = Column(ForeignKey('locations.location_id'))
    latitude = Column(Numeric(10, 7))
    longitude = Column(Numeric(10, 7))
    address_id = Column(ForeignKey('addresses.address_id'))
    contact_id = Column(ForeignKey('contacts.contact_id'))
    created_by = Column(String(255))
    created_at = Column(DateTime)
    updated_by = Column(String(255))
    updated_at = Column(DateTime)

    # address = relationship('Address')
    # contact = relationship('Contact')
    # parent = relationship('Location', remote_side=[location_id])


class Right(Base):
    __tablename__ = 'rights'

    right_id = Column(Integer, primary_key=True, server_default=text("nextval('rights_right_id_seq'::regclass)"))
    asset_id = Column(ForeignKey('assets.asset_id'))
    create_right = Column(Boolean)
    edit_right = Column(Boolean)
    delete_right = Column(Boolean)
    read_data = Column(Boolean)
    view_right = Column(Boolean)
    created_by = Column(String(255))
    created_at = Column(DateTime)
    updated_by = Column(String(255))
    updated_at = Column(DateTime)

    # asset = relationship('Asset')
    # users = relationship('User', secondary='user_rights')
    # roles = relationship('UserRole', secondary='role_rights')


class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True, server_default=text("nextval('users_user_id_seq'::regclass)"))
    user_name = Column(String(255))
    email = Column(String(255))
    hex_password = Column(String(255))
    is_active = Column(Boolean)
    is_verified = Column(Boolean)
    created_by = Column(String(255))
    created_at = Column(DateTime)
    updated_by = Column(String(255))
    updated_at = Column(DateTime)
    
    # users = relationship('Address', secondary='user_addresses')

class DeviceTagHistory(Base):
    __tablename__ = 'device_tag_history'

    unique_row_id = Column(Integer, primary_key=True)
    did = Column(Integer)
    sr_no = Column(String)
    tag_desc = Column(String)
    tag_value = Column(String)
    tag_status = Column(String)
    recorded_date_time = Column(DateTime)
    uom = Column(String)


class Device(Base):
    __tablename__ = 'devices'

    device_id = Column(Integer, primary_key=True, server_default=text("nextval('devices_device_id_seq'::regclass)"))
    device_root_id = Column(ForeignKey('devices.device_id'))
    device_type_id = Column(ForeignKey('device_type.device_type_id'))
    location_id = Column(ForeignKey('locations.location_id'))
    device_serial_number = Column(String(255))
    description = Column(String(255))
    model_number = Column(String(255))
    brand_name = Column(String(255))
    is_active = Column(Boolean)
    created_by = Column(String(255))
    created_at = Column(DateTime)
    updated_by = Column(String(255))
    updated_at = Column(DateTime)

    # device_root = relationship('Device', remote_side=[device_id])
    # device_type = relationship('DeviceType')
    # location = relationship('Location')


t_location_contacts = Table(
    'location_contacts', metadata,
    Column('location_id', ForeignKey('locations.location_id'), primary_key=True, nullable=False),
    Column('contact_id', ForeignKey('contacts.contact_id'), primary_key=True, nullable=False)
)


class DeviceDefaultTags(Base):
    __tablename__ = 'device_default_tags'

    tag_id = Column(Integer, primary_key=True)
    device_type_id = Column(Integer)


t_role_rights = Table(
    'role_rights', metadata,
    Column('role_id', ForeignKey('user_role.role_id'), primary_key=True, nullable=False),
    Column('right_id', ForeignKey('rights.right_id'), primary_key=True, nullable=False)
)


user_addresses = Table(
    'user_addresses', metadata,
    Column('user_id', ForeignKey('users.user_id'), primary_key=True, nullable=False),
    Column('address_id', ForeignKey('addresses.address_id'), primary_key=True, nullable=False)
)


t_user_contacts = Table(
    'user_contacts', metadata,
    Column('user_id', ForeignKey('users.user_id'), primary_key=True, nullable=False),
    Column('contact_id', ForeignKey('contacts.contact_id'), primary_key=True, nullable=False)
)


t_user_group_membership = Table(
    'user_group_membership', metadata,
    Column('user_id', ForeignKey('users.user_id'), primary_key=True, nullable=False),
    Column('user_group_id', ForeignKey('user_group.user_group_id'), primary_key=True, nullable=False)
)


class UserLogHistory(Base):
    __tablename__ = 'user_log_history'

    log_id = Column(Integer, primary_key=True, server_default=text("nextval('user_log_history_log_id_seq'::regclass)"))
    remote_host = Column(String(255))
    identity = Column(String(255))
    user_name = Column(String(255))
    time_received = Column(DateTime)
    request_line = Column(String(255))
    status_code = Column(Integer)
    response_size = Column(Integer)
    referer = Column(String(255))
    user_agent = Column(String(255))
    user_id = Column(ForeignKey('users.user_id'))
    created_by = Column(String(255))
    created_at = Column(DateTime)
    updated_by = Column(String(255))
    updated_at = Column(DateTime)

    # user = relationship('User')


t_user_rights = Table(
    'user_rights', metadata,
    Column('user_id', ForeignKey('users.user_id'), primary_key=True, nullable=False),
    Column('right_id', ForeignKey('rights.right_id'), primary_key=True, nullable=False)
)


t_user_role_assignment = Table(
    'user_role_assignment', metadata,
    Column('user_id', ForeignKey('users.user_id'), primary_key=True, nullable=False),
    Column('role_id', ForeignKey('user_role.role_id'), primary_key=True, nullable=False)
)


class Alert(Base):
    __tablename__ = 'alerts'

    alert_id = Column(Integer, primary_key=True, server_default=text("nextval('alerts_alert_id_seq'::regclass)"))
    device_id = Column(ForeignKey('devices.device_id'))
    alert_description = Column(String(255))
    created_by = Column(String(255))
    created_at = Column(DateTime)
    updated_by = Column(String(255))
    updated_at = Column(DateTime)

    # device = relationship('Device')


class Connection(Base):
    __tablename__ = 'connections'

    connection_id = Column(Integer, primary_key=True, server_default=text("nextval('connections_connection_id_seq'::regclass)"))
    connection_type_id = Column(ForeignKey('connection_types.connection_type_id'))
    device_id = Column(ForeignKey('devices.device_id'))
    created_by = Column(String(255))
    created_at = Column(DateTime)
    updated_by = Column(String(255))
    updated_at = Column(DateTime)

    # connection_type = relationship('ConnectionType')
    # device = relationship('Device')


class DeviceTag(Base):
    __tablename__ = 'device_tags'

    device_id = Column(ForeignKey('devices.device_id'), nullable=False)
    tag_id = Column(ForeignKey('tags.tag_id'), nullable=False)
    ID = Column(BIGINT, Sequence('device_tag_id_seq'), primary_key=True)

    # device = relationship('Device')
    # tag = relationship('Tag')


t_actions_alert = Table(
    'actions_alert', metadata,
    Column('action_id', ForeignKey('actions.action_id'), primary_key=True, nullable=False),
    Column('alert_id', ForeignKey('alerts.alert_id'), primary_key=True, nullable=False)
)

class AlertConfig(Base):
    __tablename__ = 'alert_config'

    config_id = Column(Integer, Sequence('alert_config_config_id_seq'), primary_key=True)
    tag_id = Column(Integer, nullable=False)
    tag_value_min = Column(DECIMAL, nullable=False)
    tag_value_max = Column(DECIMAL, nullable=False)
    alert_type = Column(String(255), nullable=False)
    device_id = Column(Integer, nullable=False)


class alert_values_out_of_range(Base):
    __tablename__ = 'alert_history'

    id = Column(Integer, Sequence('alert_values_out_of_range_id_seq'), primary_key=True)
    tag_id = Column(Integer)
    tag_value = Column(DECIMAL)
    tag_name = Column(String(255))
    alert_type = Column(String(255))
    time = Column(DateTime)
    device_serial_num = Column(String(255))


class AlertExpression(Base):
    __tablename__ = 'alert_expressions'

    expression_id = Column(Integer, primary_key=True, server_default=text("nextval('alert_expressions_expression_id_seq'::regclass)"))
    alert_id = Column(ForeignKey('alerts.alert_id'))
    expression = Column(String(255))
    input_field_name = Column(String(255))
    arithmetic_operator = Column(String(255))
    constant_value = Column(Integer)
    brace_value = Column(String(255))
    logical_operator = Column(String(255))
    description = Column(String(255))
    created_by = Column(String(255))
    created_at = Column(DateTime)
    updated_by = Column(String(255))
    updated_at = Column(DateTime)

    # alert = relationship('Alert')


class ConnectionDetail(Base):
    __tablename__ = 'connection_details'

    connection_detail_id = Column(Integer, primary_key=True, server_default=text("nextval('connection_details_connection_detail_id_seq'::regclass)"))
    connection_id = Column(ForeignKey('connections.connection_id'))
    field_type = Column(String(255))
    field_value = Column(String(255))
    created_by = Column(String(255))
    created_at = Column(DateTime)
    updated_by = Column(String(255))
    updated_at = Column(DateTime)

    # connection = relationship('Connection')


class History(Base):
    __tablename__ = 'history'

    history_id = Column(Integer, primary_key=True, server_default=text("nextval('history_history_id_seq'::regclass)"))
    device_tag_id = Column(ForeignKey('device_tags.ID'))
    value = Column(DECIMAL)
    status = Column(String(255))
    recorded_date_time = Column(DateTime)
    alert_id = Column(ForeignKey('alerts.alert_id'))
    created_by = Column(String(255))
    created_at = Column(DateTime)
    updated_by = Column(String(255))
    updated_at = Column(DateTime)

    # alert = relationship('Alert')
    # device_tag = relationship('DeviceTag')

t_actions_history = Table(
    'actions_history', metadata,
    Column('action_id', ForeignKey('actions.action_id'), primary_key=True, nullable=False),
    Column('history_id', ForeignKey('history.history_id'), primary_key=True, nullable=False)
)
class DeviceLatestRecord(Base):
    __tablename__ = 'device_latest_records'
    _table_args_ = {'autoload_with': engine}
    # Assuming devices_device_id is unique and can act as a pseudo-primary key
    id = Column(BIGINT, primary_key=True)
    devices_device_id = Column(Integer)
    devices_device_serial_number = Column(String)
    tag_description = Column(String)
    tag_value = Column(String)
    anon_1_latest_recorded_date = Column(DateTime)
    
#################################################
from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal

class AddressPydantic(BaseModel):
    address_id: Optional[int] = None
    address_line1: str
    address_line2: str
    city: str
    state: str
    postal_code: str
    country: str
    latitude: Decimal
    longitude: Decimal
    created_by: str
    created_at: datetime
    updated_by: str
    updated_at: datetime
    class Config:
        orm_mode = True     

class ActionTypePydantic(BaseModel):
    action_type_id: Optional[int] = None
    description: str
    created_by: str
    created_at: datetime
    updated_by: str
    updated_at: datetime
    class Config:
        orm_mode = True


class ConnectionTypePydantic(BaseModel):
    connection_type_id: Optional[int] = None
    description: str
    created_by: str
    created_at: datetime
    updated_by: str
    updated_at: datetime
    class Config:
        orm_mode = True

class ContactTypePydantic(BaseModel):
    contact_type_id: Optional[int] = None
    description: str
    created_by: str
    created_at: datetime
    updated_by: str
    updated_at: datetime
    
    class Config:
        orm_mode = True

class DeviceTypePydantic(BaseModel):
    device_type_id: Optional[int] = None
    description: str
    created_by: str
    created_at: datetime
    updated_by: str
    updated_at: datetime
    class Config:
        orm_mode = True


class TagPydantic(BaseModel):
    tag_id: Optional[int] = None
    description: str
    unit_of_measure: str
    created_by: str
    created_at: datetime
    updated_by: str
    updated_at: datetime
    class Config:
        orm_mode = True


class UserGroupPydantic(BaseModel):
    user_group_id: Optional[int] = None
    group_name: str
    created_by: str
    created_at: datetime
    updated_by: str
    updated_at: datetime
    class Config:
        orm_mode = True



class UserRolePydantic(BaseModel):
    role_id: Optional[int] = None
    role_name: str
    created_by: str
    created_at: datetime
    updated_by: str
    updated_at: datetime
    class Config:
        orm_mode = True


class ActionPydantic(BaseModel):
    action_id: Optional[int] = None
    description: str
    action_type_id: int  # ForeignKey relationship, represented as int
    action_taken_datetime: datetime
    created_by: str
    created_at: datetime
    updated_by: str
    updated_at: datetime
    class Config:
        orm_mode = True


class AssetPydantic(BaseModel):
    asset_id: Optional[int] = None
    asset_type_id: int  # ForeignKey relationship, represented as int
    created_by: str
    created_at: datetime
    updated_by: str
    updated_at: datetime
    class Config:
        orm_mode = True


class ContactPydantic(BaseModel):
    contact_id: Optional[int] = None
    contact_description: str
    contact_type_id: int  # ForeignKey relationship, represented as int
    created_by: str
    created_at: datetime
    updated_by: str
    updated_at: datetime

    class Config:
        orm_mode = True


class LocationPydantic(BaseModel):
    location_id: Optional[int] = None
    location_name: str
    location_desc: str
    location_type_id: int
    location_root: int  # ForeignKey relationship, represented as int
    latitude:  Optional[Decimal]  = Field(None, title="Latitude with up to 7 decimal places")
    longitude:  Optional[Decimal]  = Field(None, title="Longitude with up to 7 decimal places")
    address_id: int  # ForeignKey relationship, represented as int
    contact_id: int  # ForeignKey relationship, represented as int
    created_by: str
    created_at: datetime
    updated_by: str
    updated_at: datetime

    class Config:
        orm_mode = True
        from_orm = True
        from_attributes = True

class RightPydantic(BaseModel):
    right_id: Optional[int] = None
    asset_id: int  # ForeignKey relationship, represented as int
    create_right: bool
    edit_right: bool
    delete_right: bool
    read_data: bool
    view_right: bool
    created_by: str
    created_at: datetime
    updated_by: str
    updated_at: datetime
    class Config:
        orm_mode = True

# user_id = Column(Integer, primary_key=True, server_default=text("nextval('users_user_id_seq'::regclass)"))
#     user_name = Column(String(255))
#     email = Column(String(255))
#     hex_password = Column(String(255))
#     is_active = Column(Boolean)
#     is_verified = Column(Boolean)
#     created_by = Column(String(255))
#     created_at = Column(DateTime)
#     updated_by = Column(String(255))
#     updated_at = Column(DateTime)

class UserPydantic(BaseModel):
    user_id: Optional[int] = None
    user_name: str
    email: str
    hex_password: str
    is_active: Optional[bool] = None
    is_verified: Optional[bool] = None
    created_by: str
    updated_by: str
    class Config:
        orm_mode = True

class UserReponsePydantic(BaseModel):
    user_id: Optional[int] = None
    email: EmailStr

    class Config:
        from_attributes = True
        orm_mode = True

class UserCreatePydantic(BaseModel):
    email: Optional[EmailStr]=None
    user_name: Optional[str]=None
    password: str  # Accept plaintext password
    # other fields as necessary
    class Config:
        orm_mode = True


class DevicePydantic(BaseModel):
    device_id: Optional[int] = None
    device_root_id: int  # ForeignKey relationship, represented as int
    device_type_id: int  # ForeignKey relationship, represented as int
    location_id: int  # ForeignKey relationship, represented as int
    device_serial_number: str
    description: str
    model_number: str
    brand_name: str
    is_active: bool
    created_by: str
    created_at: datetime
    updated_by: str
    updated_at: datetime
    class Config:
        orm_mode = True


class UserLogHistoryPydantic(BaseModel):
    log_id: Optional[int] = None
    remote_host: str
    identity: str
    user_name: str
    time_received: datetime
    request_line: str
    status_code: int
    response_size: int
    referer: str
    user_agent: str
    user_id: int  # ForeignKey relationship, represented as int
    created_by: str
    created_at: datetime
    updated_by: str
    updated_at: datetime
    class Config:
        orm_mode = True


class AlertPydantic(BaseModel):
    alert_id: Optional[int] = None
    device_id: int  # ForeignKey relationship, represented as int
    alert_description: str
    created_by: str
    created_at: datetime
    updated_by: str
    updated_at: datetime
    class Config:
        orm_mode = True


class ConnectionPydantic(BaseModel):
    connection_id: Optional[int] = None
    connection_type_id: int  # ForeignKey relationship, represented as int
    device_id: int  # ForeignKey relationship, represented as int
    created_by: str
    created_at: datetime
    updated_by: str
    updated_at: datetime
    class Config:
        orm_mode = True


class DeviceTagPydantic(BaseModel):
    device_id: int  # ForeignKey relationship, represented as int
    tag_id: int  # ForeignKey relationship, represented as int
    ID: Optional[int] = None
    class Config:
        orm_mode = True


class AlertExpressionPydantic(BaseModel):
    expression_id: Optional[int] = None
    alert_id: int  # ForeignKey relationship, represented as int
    expression: str
    input_field_name: str
    arithmetic_operator: str
    constant_value: int
    brace_value: str
    logical_operator: str
    description: str
    created_by: str
    created_at: datetime
    updated_by: str
    updated_at: datetime
    class Config:
        orm_mode = True

class ConnectionDetailPydantic(BaseModel):
    connection_detail_id: Optional[int] = None
    connection_id: int  # ForeignKey relationship, represented as int
    field_type: str
    field_value: str
    created_by: str
    created_at: datetime
    updated_by: str
    updated_at: datetime
    class Config:
        orm_mode = True


class HistoryPydantic(BaseModel):
    history_id: Optional[int] = None
    device_tag_id: int  # ForeignKey relationship, represented as int
    value: float
    status:  Optional[str] = None
    recorded_date_time: datetime
    alert_id: Optional[int] = None  # ForeignKey relationship, represented as int
    class Config:
        orm_mode = True

class UserLoginPydantic(BaseModel):
    username: str
    password: str
    class Config:
        orm_mode = True

class LocationContactPydantic(BaseModel):
    location_id: int
    contact_id: int
    class Config:
        orm_mode = True



class UserContactPydantic(BaseModel):
    user_id: int
    contact_id: int
    class Config:
        orm_mode = True



class UserAddressPydantic(BaseModel):
    user_id: int
    adress_id: int
    class Config:
        orm_mode = True



class UserGroupMembershipPydantic(BaseModel):
    user_id: int
    user_group_id: int
    class Config:
        orm_mode = True



class UserRoleAssignmentPydantic(BaseModel):
    user_id: int
    role_id: int
    class Config:
        orm_mode = True



class AssetTypePydantic(BaseModel):
    asset_type_id: Optional[int] = None
    description: Optional[str]
    created_by: Optional[str]
    created_at: Optional[datetime]
    updated_by: Optional[str]
    updated_at: Optional[datetime]
    class Config:
        orm_mode = True



class UserRightPydantic(BaseModel):
    user_id: int
    right_id: int
    class Config:
        orm_mode = True


class RoleRightPydantic(BaseModel):
    role_id: int
    right_id: int
    class Config:
        orm_mode = True


class ActionHistoryPydantic(BaseModel):
    action_id: int
    history_id: int
    class Config:
        orm_mode = True


class ActionAlertPydantic(BaseModel):
    action_id: int
    alert_id: int
    class Config:
        orm_mode = True

class DeviceTagHistoryPydantic(BaseModel):
    did: Optional[int] = None
    sr_no: Optional[str] = None
    tag_desc: Optional[str] = None
    tag_value: Optional[int] = None
    tag_status: Optional[str] = None
    recorded_date_time: Optional[datetime] = None
    uom: Optional[str] = None
Base.metadata.create_all(engine)

class AlertConfigPydantic(BaseModel):
    config_id: Optional[int] = None
    tag_id: int
    tag_value_min: int
    tag_value_max: int
    alert_type: str
    device_id: int

    class Config:
        orm_mode = True

class alert_values_out_of_rangePydantic(BaseModel):
    id: Optional[int] = None
    tag_id: int
    tag_value: int
    tag_name: str
    alert_type: str
    time: datetime
    device_serial_num: str

    class Config:
        orm_mode = True


class DeviceDefaultTagsPydantic(BaseModel):
    tag_id: int
    device_type_id: int

class NewDevicePydantic(BaseModel):
    location_type_id: int
    device_id_root: int
    device_serial_number: str
    description: str
    model_number: str
    brand_name: str
    is_active: bool
    device_type_description: str
    location_name: str
    location_description: str
    location_root: int
    latitude: float
    longitude: float
    address_line_1: str
    address_line_2: str
    city: str
    state: str
    postal_code: str
    country: str
    contact_description: str
    contact_type_description: str

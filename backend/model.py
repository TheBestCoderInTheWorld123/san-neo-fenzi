from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, DECIMAL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel
from typing import Optional
from urllib.parse import quote_plus
 
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


class Address(Base):
    __tablename__ = 'addresses'

    address_id = Column(Integer, primary_key=True)
    address_line1 = Column(String(255))
    address_line2 = Column(String(255))
    city = Column(String(255))
    state = Column(String(255))
    postal_code = Column(String(255))
    country = Column(String(255))
    latitude = Column(DECIMAL(10, 7))
    longitude = Column(DECIMAL(10, 7))
    created_by = Column(String(255))
    created_at = Column(DateTime)
    updated_by = Column(String(255))
    updated_at = Column(DateTime)

class AddressPydandic(BaseModel):
    address_id: int
    address_line1: Optional[str]
    address_line2: Optional[str]
    city: Optional[str]
    state: Optional[str]
    postal_code: Optional[str]
    country: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]
    created_by: Optional[str]
    created_at: Optional[str]
    updated_by: Optional[str]
    updated_at: Optional[str]

class ContactType(Base):
    __tablename__ = 'contact_types'

    contact_type_id = Column(Integer, primary_key=True)
    description = Column(String(255))
    created_by = Column(String(255))
    created_at = Column(DateTime)
    updated_by = Column(String(255))
    updated_at = Column(DateTime)

class ContactTypePydandic(BaseModel):
   contact_type_id: int
   description: Optional[str]
   created_by: Optional[str]
   created_at: Optional[str]
   updated_by: Optional[str]
   updated_at: Optional[str]

class Contact(Base):
    __tablename__ = 'contacts'

    contact_id = Column(Integer, primary_key=True)
    contact_description = Column(String(255))
    contact_type_id = Column(Integer, ForeignKey('contact_types.contact_type_id'))
    created_by = Column(String(255))
    created_at = Column(DateTime)
    updated_by = Column(String(255))
    updated_at = Column(DateTime)
    contact_type = relationship("ContactType", backref="contacts")

class ContactPydandic(BaseModel):
    contact_id: int
    contact_description: Optional[str]
    contact_type_id: int
    created_by: Optional[str]
    created_at: Optional[str]
    updated_by: Optional[str]
    updated_at: Optional[str]
    contact_type: Optional[str]

class Location(Base):
    __tablename__ = 'locations'

    location_id = Column(Integer, primary_key=True)
    location_name = Column(String(255))
    location_desc = Column(String(255))
    location_type_id = Column(Integer)
    location_root = Column(Integer, ForeignKey('locations.location_id'))
    latitude = Column(DECIMAL(10, 7))
    longitude = Column(DECIMAL(10, 7))
    address_id = Column(Integer, ForeignKey('addresses.address_id'))
    contact_id = Column(Integer, ForeignKey('contacts.contact_id'))
    created_by = Column(String(255))
    created_at = Column(DateTime)
    updated_by = Column(String(255))
    updated_at = Column(DateTime)

    # Relationships
    location_root_relation = relationship("Location", remote_side=[location_id])
    address = relationship("Address")
    contact = relationship("Contact")

class LocationPydandic(BaseModel):
    location_id: int
    location_name: Optional[str]
    location_desc: Optional[str]
    location_type_id: Optional[int]
    location_root: Optional[int]
    latitude: Optional[float]
    longitude: Optional[float]
    address_id: Optional[int]
    contact_id: Optional[int]
    created_by: Optional[str]
    created_at: Optional[str]
    updated_by: Optional[str]
    updated_at: Optional[str]


class LocationContact(Base):
    __tablename__ = 'location_contacts'

    location_id = Column(Integer, ForeignKey('locations.location_id'), primary_key=True)
    contact_id = Column(Integer, ForeignKey('contacts.contact_id'), primary_key=True)
    location = relationship("Location")
    contact = relationship("Contact")

class LocationContactPydandic(BaseModel):
    location_id: int
    contact_id: int

class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True)
    email = Column(String(255))
    hex_password = Column(String(255))
    contact_id = Column(Integer, ForeignKey('contacts.contact_id'))
    address_id = Column(Integer, ForeignKey('addresses.address_id'))
    is_active = Column(Boolean)
    is_verified = Column(Boolean)
    created_by = Column(String(255))
    created_at = Column(DateTime)
    updated_by = Column(String(255))
    updated_at = Column(DateTime)
    contact = relationship("Contact")
    address = relationship("Address")

class UserPydandic(BaseModel):
    user_id: int
    email: Optional[str]
    hex_password: Optional[str]
    contact_id: int
    address_id: int
    is_active: Optional[bool]
    is_verified: Optional[bool]
    created_by: Optional[str]
    created_at: Optional[str]
    updated_by: Optional[str]
    updated_at: Optional[str]
    contact: Optional[str]
    address: Optional[str]

class UserContact(Base):
    __tablename__ = 'user_contacts'

    user_id = Column(Integer, ForeignKey('users.user_id'), primary_key=True)
    contact_id = Column(Integer, ForeignKey('contacts.contact_id'), primary_key=True)
    user = relationship("User")
    contact = relationship("Contact")

class UserContactPydandic(BaseModel):
    user_id: int
    contact_id: int

class UserAddress(Base):
    __tablename__ = 'user_addresses'

    user_id = Column(Integer, ForeignKey('users.user_id'), primary_key=True)
    address_id = Column(Integer, ForeignKey('addresses.address_id'), primary_key=True)
    user = relationship("User")
    address = relationship("Address")

class UserAddressPydandic(BaseModel):
    user_id: int
    adress_id: int
    user: Optional[str]
    address: Optional[str]

class UserGroup(Base):
    __tablename__ = 'user_group'

    user_group_id = Column(Integer, primary_key=True)
    group_name = Column(String(255))
    created_by = Column(String(255))
    created_at = Column(DateTime)
    updated_by = Column(String(255))
    updated_at = Column(DateTime)

class UserGroupPydandic(BaseModel):
    user_group_id: int
    group_name: Optional[str]
    created_by: Optional[str]
    created_at: Optional[str]
    updated_by: Optional[str]
    updated_at: Optional[str]

class UserRole(Base):
    __tablename__ = 'user_role'

    role_id = Column(Integer, primary_key=True)
    role_name = Column(String(255))
    created_by = Column(String(255))
    created_at = Column(DateTime)
    updated_by = Column(String(255))
    updated_at = Column(DateTime)

class UserRolePydandic(BaseModel):
    role_id: int
    role_name: Optional[str]
    created_by: Optional[str]
    created_at: Optional[str]
    updated_by: Optional[str]
    updated_at: Optional[str]

class UserGroupMembership(Base):
    __tablename__ = 'user_group_membership'

    user_id = Column(Integer, ForeignKey('users.user_id'), primary_key=True)
    user_group_id = Column(Integer, ForeignKey('user_group.user_group_id'), primary_key=True)
    user = relationship("User")
    user_group = relationship("UserGroup")

class UserGroupMembershipPydandic(BaseModel):
    user_id: int
    user_group_id: int


class UserRoleAssignment(Base):
    __tablename__ = 'user_role_assignment'

    user_id = Column(Integer, ForeignKey('users.user_id'), primary_key=True)
    role_id = Column(Integer, ForeignKey('user_role.role_id'), primary_key=True)
    user = relationship("User")
    user_role = relationship("UserRole")

class UserRoleAssignmentPydandic(BaseModel):
    user_id: int
    role_id: int

class AssetType(Base):
    __tablename__ = 'asset_types'

    asset_type_id = Column(Integer, primary_key=True)
    description = Column(String(255))
    created_by = Column(String(255))
    created_at = Column(DateTime)
    updated_by = Column(String(255))
    updated_at = Column(DateTime)

class AssetTypePydandic(BaseModel):
    asset_type_id: int
    description: Optional[str]
    created_by: Optional[str]
    created_at: Optional[str]
    updated_by: Optional[str]
    updated_at: Optional[str]

class Asset(Base):
    __tablename__ = 'assets'

    asset_id = Column(Integer, primary_key=True)
    asset_type_id = Column(Integer, ForeignKey('asset_types.asset_type_id'))
    created_by = Column(String(255))
    created_at = Column(DateTime)
    updated_by = Column(String(255))
    updated_at = Column(DateTime)
    asset_type = relationship("AssetType")

class AssetPydandic(BaseModel):
    asset_id: int
    asset_type_id: int
    created_by: Optional[str]
    created_at: Optional[str]
    updated_by: Optional[str]
    updated_at: Optional[str]

class Right(Base):
    __tablename__ = 'rights'

    right_id = Column(Integer, primary_key=True)
    asset_id = Column(Integer, ForeignKey('assets.asset_id'))
    create_right = Column(Boolean)
    edit_right = Column(Boolean)
    delete_right = Column(Boolean)
    read_data = Column(Boolean)
    view_right = Column(Boolean)
    created_by = Column(String(255))
    created_at = Column(DateTime)
    updated_by = Column(String(255))
    updated_at = Column(DateTime)
    asset = relationship("Asset")

class RightPydandic(BaseModel):
    right_id: int
    asset_id: int
    create_right: Optional[bool]
    edit_right: Optional[bool]
    delete_right: Optional[bool]
    read_data: Optional[bool]
    view_right: Optional[bool]
    created_by: Optional[str]
    created_at: Optional[str]
    updated_by: Optional[str]
    updated_at: Optional[str]

class UserRight(Base):
    __tablename__ = 'user_rights'

    user_id = Column(Integer, ForeignKey('users.user_id'), primary_key=True)
    right_id = Column(Integer, ForeignKey('rights.right_id'), primary_key=True)
    user = relationship("User")
    right = relationship("Right")

class UserRightPydandic(BaseModel):
    user_id: int
    right_id: int

class RoleRight(Base):
    __tablename__ = 'role_rights'

    role_id = Column(Integer, ForeignKey('user_role.role_id'), primary_key=True)
    right_id = Column(Integer, ForeignKey('rights.right_id'), primary_key=True)
    role = relationship("UserRole")
    right = relationship("Right")

class RoleRightPydandic(BaseModel):
    role_id: int
    right_id: int

class Tag(Base):
    __tablename__ = 'tags'

    tag_id = Column(Integer, primary_key=True)
    description = Column(String(255))
    unit_of_measure = Column(String(255))
    created_by = Column(String(255))
    created_at = Column(DateTime)
    updated_by = Column(String(255))
    updated_at = Column(DateTime)

class TagPydandic(BaseModel):
    tag_id: int
    description: Optional[str]
    unit_of_measure: Optional[str]
    created_by: Optional[str]
    created_at: Optional[str]
    updated_by: Optional[str]
    updated_at: Optional[str]

class DeviceType(Base):
    __tablename__ = 'device_type'

    device_type_id = Column(Integer, primary_key=True)
    description = Column(String(255))
    created_by = Column(String(255))
    created_at = Column(DateTime)
    updated_by = Column(String(255))
    updated_at = Column(DateTime)

class DeviceTypePydandic(BaseModel):
    device_type_id: int
    description: Optional[str]
    created_by: Optional[str]
    created_at: Optional[str]
    updated_by: Optional[str]
    updated_at: Optional[str]

class Device(Base):
    __tablename__ = 'devices'

    device_id = Column(Integer, primary_key=True)
    device_root_id = Column(Integer, ForeignKey('devices.device_id'))
    device_type_id = Column(Integer, ForeignKey('device_type.device_type_id'))
    location_id = Column(Integer, ForeignKey('locations.location_id'))
    device_serial_number = Column(String(255))
    description = Column(String(255))
    model_number = Column(String(255))
    brand_name = Column(String(255))
    is_active = Column(Boolean)
    latitude = Column(DECIMAL(10, 7))
    longitude = Column(DECIMAL(10, 7))
    created_by = Column(String(255))
    created_at = Column(DateTime)
    updated_by = Column(String(255))
    updated_at = Column(DateTime)

    # Relationships
    device_root = relationship("Device", remote_side=[device_id])
    device_type = relationship("DeviceType")
    location = relationship("Location")

class DevicePydandic(BaseModel):
    device_id: int
    device_root_id: int
    device_type_id: int
    location_id: int
    device_serial_number: Optional[str]
    description: Optional[str]
    model_number: Optional[str]
    brand_name: Optional[str]
    is_active: Optional[bool]
    latitude: int
    longitude: int
    created_by: Optional[str]
    created_at: Optional[str]
    updated_by: Optional[str]
    updated_at: Optional[str]

class DeviceTag(Base):
    __tablename__ = 'device_tags'

    device_id = Column(Integer, ForeignKey('devices.device_id'), primary_key=True)
    tag_id = Column(Integer, ForeignKey('tags.tag_id'), primary_key=True)
    device = relationship("Device")
    tag = relationship("Tag")

class DeviceTagPydandic(BaseModel):
    device_id: int
    tag_id: int

class ConnectionType(Base):
    __tablename__ = 'connection_types'

    connection_type_id = Column(Integer, primary_key=True)
    description = Column(String(255))
    created_by = Column(String(255))
    created_at = Column(DateTime)
    updated_by = Column(String(255))
    updated_at = Column(DateTime)

class ConnectionTypePydandic(BaseModel):
    connection_type_id: int
    description: Optional[str]
    created_by: Optional[str]
    created_at: Optional[str]
    updated_by: Optional[str]
    updated_at: Optional[str]

class Connection(Base):
    __tablename__ = 'connections'

    connection_id = Column(Integer, primary_key=True)
    connection_type_id = Column(Integer, ForeignKey('connection_types.connection_type_id'))
    device_id = Column(Integer, ForeignKey('devices.device_id'))
    created_by = Column(String(255))
    created_at = Column(DateTime)
    updated_by = Column(String(255))
    updated_at = Column(DateTime)

    # Relationships
    connection_type = relationship("ConnectionType")
    device = relationship("Device")

class ConnectionPydandic(BaseModel):
    connection_id: int
    connection_type_id: int
    device_id: int
    created_by: Optional[str]
    created_at: Optional[str]
    updated_by: Optional[str]
    updated_at: Optional[str]

class ConnectionDetail(Base):
    __tablename__ = 'connection_details'

    connection_detail_id = Column(Integer, primary_key=True)
    connection_id = Column(Integer, ForeignKey('connections.connection_id'))
    field_type = Column(String(255))
    field_value = Column(String(255))
    created_by = Column(String(255))
    created_at = Column(DateTime)
    updated_by = Column(String(255))
    updated_at = Column(DateTime)

    # Relationship
    connection = relationship("Connection")

class ConnectionDetailPydandic(BaseModel):
    connection_detail_id: int
    connection_id: int
    field_type: Optional[str]
    field_value: Optional[str]
    created_by: Optional[str]
    created_at: Optional[str]
    updated_by: Optional[str]
    updated_at: Optional[str]

class UserLogHistory(Base):
    __tablename__ = 'user_log_history'

    log_id = Column(Integer, primary_key=True)
    remote_host = Column(String(255))
    identity = Column(String(255))
    user_name = Column(String(255))
    time_received = Column(DateTime)
    request_line = Column(String(255))
    status_code = Column(Integer)
    response_size = Column(Integer)
    referer = Column(String(255))
    user_agent = Column(String(255))
    user_id = Column(Integer, ForeignKey('users.user_id'))
    created_by = Column(String(255))
    created_at = Column(DateTime)
    updated_by = Column(String(255))
    updated_at = Column(DateTime)

    # Relationship
    user = relationship("User")

class UserLogHistoryPydandic(BaseModel):
    log_id: int
    remote_host: Optional[str]
    identity: Optional[str]
    user_name: Optional[str]
    time_received: Optional[str]
    request_line: Optional[str]
    status_code: Optional[int]
    response_size: Optional[int]
    referer: Optional[str]
    user_agent: Optional[str]
    user_id: Optional[int]
    created_by: Optional[str]
    created_at: Optional[str]
    updated_by: Optional[str]
    updated_at: Optional[str]

class Alert(Base):
    __tablename__ = 'alerts'

    alert_id = Column(Integer, primary_key=True)
    device_id = Column(Integer, ForeignKey('devices.device_id'))
    alert_description = Column(String(255))
    created_by = Column(String(255))
    created_at = Column(DateTime)
    updated_by = Column(String(255))
    updated_at = Column(DateTime)

    # Relationship
    device = relationship("Device")

class AlertPydandic(BaseModel):
    alert_id: int
    device_id: int
    alert_description: Optional[str]
    created_by: Optional[str]
    created_at: Optional[str]
    updated_by: Optional[str]
    updated_at: Optional[str]

class AlertExpression(Base):
    __tablename__ = 'alert_expressions'

    expression_id = Column(Integer, primary_key=True)
    alert_id = Column(Integer, ForeignKey('alerts.alert_id'))
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

    # Relationship
    alert = relationship("Alert")

class AlertExpressionPydandic(BaseModel):
    expression_id: int
    alert_id: int
    expression: Optional[str]
    input_field_name: Optional[str]
    arithmetic_operator: Optional[str]
    constant_value: Optional[int]
    brace_value: Optional[str]
    logical_operator: Optional[str]
    description: Optional[str]
    created_by: Optional[str]
    created_at: Optional[str]
    updated_by: Optional[str]
    updated_at: Optional[str]

class History(Base):
    __tablename__ = 'history'

    history_id = Column(Integer, primary_key=True)
    device_id = Column(Integer, ForeignKey('devices.device_id'))
    value = Column(Integer)
    status = Column(String(255))
    datetime = Column(DateTime)
    alert_id = Column(Integer, ForeignKey('alerts.alert_id'))
    created_by = Column(String(255))
    created_at = Column(DateTime)
    updated_by = Column(String(255))
    updated_at = Column(DateTime)

    # Relationships
    device = relationship("Device")
    alert = relationship("Alert")

class HistoryPydandic(BaseModel):
    history_id: int
    device_id: int
    value: Optional[int]
    status: Optional[str]
    datetime: Optional[str]
    alert_id: Optional[int]
    created_by: Optional[str]
    created_at: Optional[str]
    updated_by: Optional[str]
    updated_at: Optional[str]

class ActionType(Base):
    __tablename__ = 'action_types'

    action_type_id = Column(Integer, primary_key=True)
    description = Column(String(255))
    created_by = Column(String(255))
    created_at = Column(DateTime)
    updated_by = Column(String(255))
    updated_at = Column(DateTime)

class ActionTypePydandic(BaseModel):
    action_type_id: int
    description: Optional[str]
    created_by: Optional[str]
    created_at: Optional[str]
    updated_by: Optional[str]
    updated_at: Optional[str]

class Action(Base):
    __tablename__ = 'actions'

    action_id = Column(Integer, primary_key=True)
    description = Column(String(255))
    action_type_id = Column(Integer, ForeignKey('action_types.action_type_id'))
    action_taken_datetime = Column(DateTime)
    created_by = Column(String(255))
    created_at = Column(DateTime)
    updated_by = Column(String(255))
    updated_at = Column(DateTime)

    # Relationship
    action_type = relationship("ActionType")

class ActionPydandic(BaseModel):
    action_id: int
    description: Optional[str]
    action_type_id: Optional[int]
    action_taken_datetime: Optional[str]
    created_by: Optional[str]
    created_at: Optional[str]
    updated_by: Optional[str]
    updated_at: Optional[str]

class ActionHistory(Base):
    __tablename__ = 'actions_history'

    action_id = Column(Integer, ForeignKey('actions.action_id'), primary_key=True)
    history_id = Column(Integer, ForeignKey('history.history_id'), primary_key=True)

    action = relationship("Action")
    history = relationship("History")

class ActionHistoryPydandic(BaseModel):
    action_id: int
    history_id: int

class ActionAlert(Base):
    __tablename__ = 'actions_alert'

    action_id = Column(Integer, ForeignKey('actions.action_id'), primary_key=True)
    alert_id = Column(Integer, ForeignKey('alerts.alert_id'), primary_key=True)

    action = relationship("Action")
    alert = relationship("Alert")

class ActionAlertPydandic(BaseModel):
    action_id: int
    alert_id: int


Base.metadata.create_all(engine)
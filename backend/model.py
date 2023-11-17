from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, DECIMAL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

db_username = 'postgres'
db_password = 'admin_1'
db_host = '162.216.113.6'
db_name = 'iot_db'
db_port = '5423'

db_url = f'postgresql://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}'

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

class ContactType(Base):
    __tablename__ = 'contact_types'

    contact_type_id = Column(Integer, primary_key=True)
    description = Column(String(255))
    created_by = Column(String(255))
    created_at = Column(DateTime)
    updated_by = Column(String(255))
    updated_at = Column(DateTime)

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

class LocationContact(Base):
    __tablename__ = 'location_contacts'

    location_id = Column(Integer, ForeignKey('locations.location_id'), primary_key=True)
    contact_id = Column(Integer, ForeignKey('contacts.contact_id'), primary_key=True)
    location = relationship("Location")
    contact = relationship("Contact")

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


class UserContact(Base):
    __tablename__ = 'user_contacts'

    user_id = Column(Integer, ForeignKey('users.user_id'), primary_key=True)
    contact_id = Column(Integer, ForeignKey('contacts.contact_id'), primary_key=True)
    user = relationship("User")
    contact = relationship("Contact")

class UserAddress(Base):
    __tablename__ = 'user_addresses'

    user_id = Column(Integer, ForeignKey('users.user_id'), primary_key=True)
    address_id = Column(Integer, ForeignKey('addresses.address_id'), primary_key=True)
    user = relationship("User")
    address = relationship("Address")


class UserGroup(Base):
    __tablename__ = 'user_group'

    user_group_id = Column(Integer, primary_key=True)
    group_name = Column(String(255))
    created_by = Column(String(255))
    created_at = Column(DateTime)
    updated_by = Column(String(255))
    updated_at = Column(DateTime)



class UserRole(Base):
    __tablename__ = 'user_role'

    role_id = Column(Integer, primary_key=True)
    role_name = Column(String(255))
    created_by = Column(String(255))
    created_at = Column(DateTime)
    updated_by = Column(String(255))
    updated_at = Column(DateTime)


class UserGroupMembership(Base):
    __tablename__ = 'user_group_membership'

    user_id = Column(Integer, ForeignKey('users.user_id'), primary_key=True)
    user_group_id = Column(Integer, ForeignKey('user_group.user_group_id'), primary_key=True)
    user = relationship("User")
    user_group = relationship("UserGroup")

class UserRoleAssignment(Base):
    __tablename__ = 'user_role_assignment'

    user_id = Column(Integer, ForeignKey('users.user_id'), primary_key=True)
    role_id = Column(Integer, ForeignKey('user_role.role_id'), primary_key=True)
    user = relationship("User")
    user_role = relationship("UserRole")

class AssetType(Base):
    __tablename__ = 'asset_types'

    asset_type_id = Column(Integer, primary_key=True)
    description = Column(String(255))
    created_by = Column(String(255))
    created_at = Column(DateTime)
    updated_by = Column(String(255))
    updated_at = Column(DateTime)

class Asset(Base):
    __tablename__ = 'assets'

    asset_id = Column(Integer, primary_key=True)
    asset_type_id = Column(Integer, ForeignKey('asset_types.asset_type_id'))
    created_by = Column(String(255))
    created_at = Column(DateTime)
    updated_by = Column(String(255))
    updated_at = Column(DateTime)
    asset_type = relationship("AssetType")



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

class UserRight(Base):
    __tablename__ = 'user_rights'

    user_id = Column(Integer, ForeignKey('users.user_id'), primary_key=True)
    right_id = Column(Integer, ForeignKey('rights.right_id'), primary_key=True)
    user = relationship("User")
    right = relationship("Right")

class RoleRight(Base):
    __tablename__ = 'role_rights'

    role_id = Column(Integer, ForeignKey('user_role.role_id'), primary_key=True)
    right_id = Column(Integer, ForeignKey('rights.right_id'), primary_key=True)
    role = relationship("UserRole")
    right = relationship("Right")

class Tag(Base):
    __tablename__ = 'tags'

    tag_id = Column(Integer, primary_key=True)
    description = Column(String(255))
    unit_of_measure = Column(String(255))
    created_by = Column(String(255))
    created_at = Column(DateTime)
    updated_by = Column(String(255))
    updated_at = Column(DateTime)

class DeviceType(Base):
    __tablename__ = 'device_type'

    device_type_id = Column(Integer, primary_key=True)
    description = Column(String(255))
    created_by = Column(String(255))
    created_at = Column(DateTime)
    updated_by = Column(String(255))
    updated_at = Column(DateTime)

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
    created_by = Column(String(255))
    created_at = Column(DateTime)
    updated_by = Column(String(255))
    updated_at = Column(DateTime)

    # Relationships
    device_root = relationship("Device", remote_side=[device_id])
    device_type = relationship("DeviceType")
    location = relationship("Location")

class DeviceTag(Base):
    __tablename__ = 'device_tags'

    device_id = Column(Integer, ForeignKey('devices.device_id'), primary_key=True)
    tag_id = Column(Integer, ForeignKey('tags.tag_id'), primary_key=True)
    device = relationship("Device")
    tag = relationship("Tag")

class ConnectionType(Base):
    __tablename__ = 'connection_types'

    connection_type_id = Column(Integer, primary_key=True)
    description = Column(String(255))
    created_by = Column(String(255))
    created_at = Column(DateTime)
    updated_by = Column(String(255))
    updated_at = Column(DateTime)

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
class ActionType(Base):
    __tablename__ = 'action_types'

    action_type_id = Column(Integer, primary_key=True)
    description = Column(String(255))
    created_by = Column(String(255))
    created_at = Column(DateTime)
    updated_by = Column(String(255))
    updated_at = Column(DateTime)
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
class ActionHistory(Base):
    __tablename__ = 'actions_history'

    action_id = Column(Integer, ForeignKey('actions.action_id'), primary_key=True)
    history_id = Column(Integer, ForeignKey('history.history_id'), primary_key=True)

    action = relationship("Action")
    history = relationship("History")
class ActionAlert(Base):
    __tablename__ = 'actions_alert'

    action_id = Column(Integer, ForeignKey('actions.action_id'), primary_key=True)
    alert_id = Column(Integer, ForeignKey('alerts.alert_id'), primary_key=True)

    action = relationship("Action")
    alert = relationship("Alert")

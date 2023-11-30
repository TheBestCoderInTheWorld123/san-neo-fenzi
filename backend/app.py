from datetime import datetime, timedelta
from model import *
from typing import List, Dict
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Integer, String, DateTime, ForeignKey, Boolean, distinct
from sqlalchemy.orm import sessionmaker, relationship, Session
from urllib.parse import quote_plus
import bcrypt
from fastapi import FastAPI, Response
from starlette.status import HTTP_101_SWITCHING_PROTOCOLS, HTTP_401_UNAUTHORIZED
from sqlalchemy import func, select
from sqlalchemy.orm import aliased
from sqlalchemy.sql import text
from sqlalchemy import desc, and_  # Add this import
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import IntegrityError
from sqlalchemy import delete

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
session = SessionLocal()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],  # You can specify specific HTTP methods here
    allow_headers=["*"],  # You can specify specific headers here
)


def sqlalchemy_to_dict(obj):
    """
    Convert SQLAlchemy model instance to dictionary.
    """
    return {column.name: getattr(obj, column.name) for column in obj.__table__.columns}


@app.post("/addresses/", response_model=AddressPydantic)
def create_address(address: AddressPydantic, db: Session = Depends(get_db)):
    db_address = Address(
        address_line1 = address.address_line1,
        address_line2 = address.address_line2,
        city = address.city,
        state = address.state,
        postal_code = address.postal_code,
        country = address.country,
        latitude = address.latitude,
        longitude = address.longitude,
        created_by = address.created_by,
        created_at = address.created_at,
        updated_by = address.updated_by,
        updated_at = address.updated_at
    )
    db.add(db_address)
    db.commit()
    db.refresh(db_address)
    db_address_dict = sqlalchemy_to_dict(db_address)
    return AddressPydantic(**db_address_dict)


@app.get("/addresses/{address_id}", response_model=AddressPydantic)
def read_address(address_id: int, db: Session = Depends(get_db)):
    db_address = db.query(Address).filter(Address.address_id == address_id).first()
    if db_address is None:
        raise HTTPException(status_code=404, detail="Address not found")
    db_address_dict = sqlalchemy_to_dict(db_address)
    return AddressPydantic(**db_address_dict)


@app.put("/addresses/{address_id}", response_model=AddressPydantic)
def update_address(address_id: int, address: AddressPydantic, db: Session = Depends(get_db)):
    db_address = db.query(Address).filter(Address.address_id == address_id).first()
    if db_address is None:
        raise HTTPException(status_code=404, detail="Address not found")
    for field, value in address.dict().items():
        setattr(db_address, field, value)
    db.commit()
    db.refresh(db_address)
    db_address_dict = sqlalchemy_to_dict(db_address)
    return AddressPydantic(**db_address_dict)


@app.delete("/addresses/{address_id}", response_model=AddressPydantic)
def delete_address(address_id: int, db: Session = Depends(get_db)):
    db_address = db.query(Address).filter(Address.address_id == address_id).first()
    if db_address is None:
        raise HTTPException(status_code=404, detail="Address not found")
    db.delete(db_address)
    db.commit()
    db_address_dict = sqlalchemy_to_dict(db_address)
    return AddressPydantic(**db_address_dict)


@app.post("/contact_types/", response_model=ContactTypePydantic)
def create_contact_type(contact_type: ContactTypePydantic, db: Session = Depends(get_db)):
    contact_type_db = ContactType(
        description=contact_type.description,
        created_by=contact_type.created_by,
        created_at=contact_type.created_at,
        updated_by=contact_type.updated_by,
        updated_at=contact_type.updated_at
    )

    db.add(contact_type_db)
    db.commit()
    db.refresh(contact_type_db)
    
    return ContactTypePydantic.from_orm(contact_type_db)


@app.get("/contact_types/", response_model=List[ContactTypePydantic])
def read_contact_types(db: Session = Depends(get_db)):
    contact_types = db.query(ContactType).all()
    return [ContactTypePydantic.from_orm(contact_type) for contact_type in contact_types]


@app.get("/contact_types/{contact_type_id}", response_model=ContactTypePydantic)
def read_contact_type(contact_type_id: int, db: Session = Depends(get_db)):
    db_contact_type = db.query(ContactType).filter(ContactType.contact_type_id == contact_type_id).first()
    if db_contact_type is None:
        raise HTTPException(status_code=404, detail="Contact type not found")
    db_contact_type = sqlalchemy_to_dict(db_contact_type)
    return ContactTypePydantic(**db_contact_type)


@app.put("/contact_types/{contact_type_id}", response_model=ContactTypePydantic)
def update_contact_type(contact_type_id: int, description: str, db: Session = Depends(get_db)):
    db_contact_type = db.query(ContactType).filter(ContactType.contact_type_id == contact_type_id).first()
    if db_contact_type is None:
        raise HTTPException(status_code=404, detail="Contact type not found")
    db_contact_type.description = description
    db.commit()
    db.refresh(db_contact_type)
    db_contact_type = sqlalchemy_to_dict(db_contact_type)
    return ContactTypePydantic(**db_contact_type)


@app.delete("/contact_types/{contact_type_id}", response_model=ContactTypePydantic)
def delete_contact_type(contact_type_id: int, db: Session = Depends(get_db)):
    db_contact_type = db.query(ContactType).filter(ContactType.contact_type_id == contact_type_id).first()
    if db_contact_type is None:
        raise HTTPException(status_code=404, detail="Contact type not found")
    db.delete(db_contact_type)
    db.commit()
    db_contact_type = sqlalchemy_to_dict(db_contact_type)
    return ContactTypePydantic(**db_contact_type)


@app.post("/contacts/", response_model=ContactPydantic)
def create_contact(contact: ContactPydantic, db: Session = Depends(get_db)):
    new_contact = Contact(
        contact_description=contact.contact_description,
        contact_type_id=contact.contact_type_id,
        created_by=contact.created_by,
        created_at=contact.created_at,
        updated_by=contact.updated_by,
        updated_at=contact.updated_at
    )

    db.add(new_contact)
    db.commit()
    db.refresh(new_contact)

    return ContactPydantic.from_orm(new_contact)


@app.get("/contacts/", response_model=List[ContactPydantic])
def read_contacts(db: Session = Depends(get_db)):
    contacts = db.query(Contact).all()
    return [ContactPydantic.from_orm(contact) for contact in contacts]


@app.get("/contacts/{contact_id}", response_model=ContactPydantic)
def read_contact(contact_id: int, db: Session = Depends(get_db)):
    db_contact = db.query(Contact).filter(Contact.contact_id == contact_id).first()
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    contact = sqlalchemy_to_dict(db_contact)
    return ContactPydantic(**contact)


@app.put("/contacts/{contact_id}", response_model=ContactPydantic)
def update_contact(contact_id: int, contact: ContactPydantic, db: Session = Depends(get_db)):
    db_contact = db.query(Contact).filter(Contact.contact_id == contact_id).first()
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    for field, value in contact.dict().items():
        setattr(db_contact, field, value)
    db.commit()
    db.refresh(db_contact)
    contact = sqlalchemy_to_dict(db_contact)
    return ContactPydantic(**contact)


@app.delete("/contacts/{contact_id}", response_model=ContactPydantic)
def delete_contact(contact_id: int, db: Session = Depends(get_db)):
    db_contact = db.query(Contact).filter(Contact.contact_id == contact_id).first()
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    db.delete(db_contact)
    db.commit()
    contact = sqlalchemy_to_dict(db_contact)
    return ContactPydantic(**contact)



@app.post("/locations/", response_model=LocationPydantic)
def create_location(location: LocationPydantic, db: Session = Depends(get_db)):
    location = Location(
        location_name=location.location_name,
        location_desc=location.location_desc,
        location_type_id=location.location_type_id,
        location_root=location.location_root,
        latitude=location.latitude,
        longitude=location.longitude,
        address_id=location.address_id,
        contact_id=location.contact_id,
        created_by=location.created_by,
        created_at=location.created_at,
        updated_by=location.updated_by,
        updated_at=location.updated_at
    )
    db.add(location)
    db.commit()
    db.refresh(location)
    return LocationPydantic.from_orm(location)


def create_tree(locations: List[LocationPydantic]) -> List[Dict]:
    location_dict = {location.location_id: location.dict() for location in locations}
    tree = []
    for location in locations:
        if location.location_id == location.location_root:
            tree.append(location.dict())
        else:
            parent = location_dict.get(location.location_root)
            if parent is not None:
                if 'children' not in parent:
                    parent['children'] = []
                parent['children'].append(location.dict())
    return tree


@app.get("/locations/", response_model=List[LocationPydantic])
def read_locations(db: Session = Depends(get_db)):
    locations = db.query(Location).all()
    locations_data = [LocationPydantic.from_orm(location) for location in locations]
    return locations_data


@app.get("/locations/{location_id}", response_model=LocationPydantic)
def read_location(location_id: int, db: Session = Depends(get_db)):
    db_location = db.query(Location).filter(Location.location_id == location_id).first()
    if db_location is None:
        raise HTTPException(status_code=404, detail="Location not found")
    location = sqlalchemy_to_dict(db_location)
    return LocationPydantic(**location)


@app.put("/locations/{location_id}", response_model=LocationPydantic)
def update_location(location_id: int, location: LocationPydantic, db: Session = Depends(get_db)):
    db_location = db.query(Location).filter(Location.location_id == location_id).first()
    if db_location is None:
        raise HTTPException(status_code=404, detail="Location not found")
    for field, value in location.dict().items():
        setattr(db_location, field, value)
    db.commit()
    db.refresh(db_location)
    location = sqlalchemy_to_dict(db_location)
    return LocationPydantic(**location)




@app.delete("/locations/{location_id}", response_model=LocationPydantic)
def delete_location(location_id: int, db: Session = Depends(get_db)):
    db_location = db.query(Location).filter(Location.location_id == location_id).first()
    if db_location is None:
        raise HTTPException(status_code=404, detail="Location not found")
    db.delete(db_location)
    db.commit()
    location = sqlalchemy_to_dict(db_location)
    return LocationPydantic(**location)


@app.post("/location_contacts/", response_model=LocationContactPydantic)
def create_location_contact(
    location_id: int, contact_id: int, db: Session = Depends(get_db)
):
    insert_stmt = t_location_contacts.insert().values(location_id=location_id, contact_id=contact_id)
    db.execute(insert_stmt)
    db.commit()
    location_contact = LocationContactPydantic(location_id=location_id, contact_id=contact_id)
    return location_contact

@app.delete("/location_contacts/")
def delete_location_contact(
    location_id: int, contact_id: int, db: Session = Depends(get_db)
):
    delete_stmt = t_location_contacts.delete().where(
        (t_location_contacts.c.location_id == location_id) &
        (t_location_contacts.c.contact_id == contact_id)
    )
    affected_rows = db.execute(delete_stmt)
    db.commit()
    if affected_rows.rowcount == 0:
        raise HTTPException(status_code=404, detail="Record not found")
    deleted_contact = LocationContactPydantic(location_id=location_id, contact_id=contact_id)
    return deleted_contact



def get_location_hierarchy(location_id):
    result = []

    def get_location_data(loc_id):
        location = session.query(Location).filter(Location.location_id == loc_id).first()
        if location:
            result.append(location)

            children = session.query(Location).filter(Location.location_root == loc_id).all()
            for child in children:
                get_location_data(child.location_id)

    get_location_data(location_id)
    return result

@app.get("/location_hierarchy/{location_id}", response_model=list[LocationPydantic])
def read_location_hierarchy(location_id: int):
    location_hierarchy = get_location_hierarchy(location_id)
    if not location_hierarchy:
        raise HTTPException(status_code=404, detail="Location not found")
    return location_hierarchy

@app.get("/device_get_all", response_model = list[DevicePydantic])
def get_all_device(db: Session = Depends(get_db)):
    devices = db.query(Device).all()
    return [DevicePydantic.from_orm(device) for device in devices]

@app.get("/history_by_device_serial_no")
def history_by_device_serial_no(sno: str, tdate: datetime, fdate: datetime, db: Session = Depends(get_db)):
    dth = db.query(DeviceTagHistory).filter(DeviceTagHistory.sr_no == sno and DeviceTagHistory.recorded_date_time >= fdate and DeviceTagHistory.recorded_date_time <= tdate).all()
    result = []
    current_time = datetime.now()
    for record in dth:
        device_id = record.did
        sr_no = record.sr_no
        tag_description = record.tag_desc
        tag_value = record.tag_value
        tag_status = record.tag_status
        
        latest_recorded_date = record.recorded_date_time.strftime("%Y-%m-%d %H:%M:%S")
        result.append({'device_serial_number': sr_no, 'tags': tag_description, "tag_value": tag_value, 'latest_recorded_date': latest_recorded_date, 'satus': tag_status})

    return {"records": result}
# Login API 

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())

@app.post("/login")
async def login(user_login: UserLoginPydantic, db: Session = Depends(get_db)):
    
    user = db.query(User).filter(User.user_name == user_login.username).first()
    if not user or not verify_password(user_login.password, user.hex_password):
        raise HTTPException(
            status_code = HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    else :
        status_code = HTTP_101_SWITCHING_PROTOCOLS
    return {"message": "Login successful", "status_code":status_code }

# Registration API 
@app.post("/user_reg/", response_model=UserPydantic)
def Registration(user_data: UserCreatePydantic, db: Session = Depends(get_db)):
    # Check if user already exists
    db_user = db.query(User).filter(User.email == user_data.email or User.user_name == user_data.user_name).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Hash the password
    hashed_password = bcrypt.hashpw(user_data.password.encode(), bcrypt.gensalt())

    # Create new User instance with hashed password
    user = User(
        email=user_data.email,
        hex_password=hashed_password.decode(),  # Store hashed password as string
        is_active=True,  # Set other fields as necessary
        is_verified=False,
        created_at = datetime.now(),
        updated_at =datetime.now()
        # ...
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


@app.post("/users/", response_model=UserPydantic)
def create_user(user: UserPydantic, db: Session = Depends(get_db)):
    db_user = User(
        user_name=user.user_name,
        email=user.email,
        hex_password=user.hex_password,
        is_active=user.is_active,
        is_verified=user.is_verified,
        created_by=user.created_by,
        updated_by=user.updated_by,
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


@app.get("/users/", response_model=list[UserPydantic])
def read_users(db: Session = Depends(get_db)):
    return db.query(User).all()


@app.get("/users/{user_id}", response_model=UserPydantic)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.user_id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.put("/users/{user_id}", response_model=UserPydantic)
def update_user(user_id: int, user: UserPydantic, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.user_id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    for field, value in user.dict().items():
        setattr(db_user, field, value)
    db.commit()
    db.refresh(db_user)
    return db_user


@app.delete("/users/{user_id}", response_model=UserPydantic)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.user_id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return db_user

@app.post("/user_contacts/", response_model=UserContactPydantic)
def create_user_contact(
    user_id: int, contact_id: int, db: Session = Depends(get_db)
):
    db_user = db.query(User).filter(User.user_id == user_id).first()
    db_contact = db.query(Contact).filter(Contact.contact_id == contact_id).first()

    if not db_user or not db_contact:
        raise HTTPException(status_code=404, detail="User or Contact not found")
    db.execute(
    t_user_contacts.insert().values(user_id=user_id, contact_id=contact_id)
    )
    db.commit()
    return UserContactPydantic(user_id=user_id, contact_id=contact_id)


@app.delete("/user_contacts/")
def delete_user_contact(
    user_id: int, contact_id: int, db: Session = Depends(get_db)
):
    db_user = db.query(User).filter(User.user_id == user_id).first()
    db_contact = db.query(Contact).filter(Contact.contact_id == contact_id).first()

    if not db_user or not db_contact:
        raise HTTPException(status_code=404, detail="User or Contact not found")

    db.execute(
            t_user_contacts.delete().where(
                (t_user_contacts.c.user_id == user_id) & (t_user_contacts.c.contact_id == contact_id)
            )
        )
    db.commit()
    return UserContactPydantic(user_id=user_id, contact_id=contact_id)

@app.post("/user_addresses/", response_model=UserAddressPydantic)
def create_user_address(
    user_id: int, address_id: int, db: Session = Depends(get_db)
):
    db_user = db.query(User).filter(User.user_id == user_id).first()
    db_address = db.query(Address).filter(Address.address_id == address_id).first()

    if not db_user or not db_address:
        raise HTTPException(status_code=404, detail="User or Address not found")

    # Insert a new row into the user_addresses table
    db.execute(user_addresses.insert().values(user_id=user_id, address_id=address_id))
    db.commit()

    return {"detail": "User-Address relationship created"}

@app.delete("/user_addresses/")
def delete_user_address(
    user_id: int, address_id: int, db: Session = Depends(get_db)
):
    db_user = db.query(User).filter(User.user_id == user_id).first()
    db_address = db.query(Address).filter(Address.address_id == address_id).first()

    if not db_user or not db_address:
        raise HTTPException(status_code=404, detail="User or Address not found")

    # Insert a new row into the user_addresses table
    db.execute(user_addresses.delete().where(
                (user_addresses.c.user_id == user_id) & (user_addresses.c.address_id == address_id)))
    db.commit()

    return {"detail": "User-Address relationship deleted"}


@app.post("/user_groups/", response_model=UserGroupPydantic)
def create_user_group(user_group: UserGroupPydantic, db: Session = Depends(get_db)):
    db_user_group = UserGroup(**user_group.dict())
    db.add(db_user_group)
    db.commit()
    db.refresh(db_user_group)
    return UserGroupPydantic.from_orm(db_user_group)


@app.get("/user_groups/", response_model=list[UserGroupPydantic])
def read_user_groups(db: Session = Depends(get_db)):
    return db.query(UserGroup).all()


@app.get("/user_groups/{user_group_id}", response_model=UserGroupPydantic)
def read_user_group(user_group_id: int, db: Session = Depends(get_db)):
    db_user_group = db.query(UserGroup).filter(UserGroup.user_group_id == user_group_id).first()
    if db_user_group is None:
        raise HTTPException(status_code=404, detail="User Group not found")
    return db_user_group


@app.put("/user_groups/{user_group_id}", response_model=UserGroupPydantic)
def update_user_group(user_group_id: int, user_group: UserGroupPydantic, db: Session = Depends(get_db)):
    db_user_group = db.query(UserGroup).filter(UserGroup.user_group_id == user_group_id).first()
    if db_user_group is None:
        raise HTTPException(status_code=404, detail="User Group not found")
    for field, value in user_group.dict().items():
        setattr(db_user_group, field, value)
    db.commit()
    db.refresh(db_user_group)
    return db_user_group


@app.delete("/user_groups/{user_group_id}", response_model=UserGroupPydantic)
def delete_user_group(user_group_id: int, db: Session = Depends(get_db)):
    db_user_group = db.query(UserGroup).filter(UserGroup.user_group_id == user_group_id).first()
    if db_user_group is None:
        raise HTTPException(status_code=404, detail="User Group not found")
    db.delete(db_user_group)
    db.commit()
    return db_user_group



@app.post("/user_roles/", response_model=UserRolePydantic)
def create_user_role(user_role: UserRolePydantic, db: Session = Depends(get_db)):
    user_role = UserRole(**user_role.dict())
    db.add(user_role)
    db.commit()
    db.refresh(user_role)
    return user_role


@app.get("/user_roles/", response_model=list[UserRolePydantic])
def read_user_roles(db: Session = Depends(get_db)):
    return db.query(UserRole).all()


@app.get("/user_roles/{role_id}", response_model=UserRolePydantic)
def read_user_role(role_id: int, db: Session = Depends(get_db)):
    db_user_role = db.query(UserRole).filter(UserRole.role_id == role_id).first()
    if db_user_role is None:
        raise HTTPException(status_code=404, detail="User Role not found")
    return db_user_role


@app.put("/user_roles/{role_id}", response_model=UserRolePydantic)
def update_user_role(role_id: int, user_role: UserRolePydantic, db: Session = Depends(get_db)):
    db_user_role = db.query(UserRole).filter(UserRole.role_id == role_id).first()
    if db_user_role is None:
        raise HTTPException(status_code=404, detail="User Role not found")
    for field, value in user_role.dict().items():
        setattr(db_user_role, field, value)
    db.commit()
    db.refresh(db_user_role)
    return db_user_role


@app.delete("/user_roles/{role_id}", response_model=UserRolePydantic)
def delete_user_role(role_id: int, db: Session = Depends(get_db)):
    db_user_role = db.query(UserRole).filter(UserRole.role_id == role_id).first()
    if db_user_role is None:
        raise HTTPException(status_code=404, detail="User Role not found")
    db.delete(db_user_role)
    db.commit()
    return db_user_role


@app.post("/user_group_memberships/", response_model=UserGroupMembershipPydantic)
def create_user_group_membership(
    user_id: int, user_group_id: int, db: Session = Depends(get_db)
):
    db_user = db.query(User).filter(User.user_id == user_id).first()
    db_user_group = db.query(UserGroup).filter(UserGroup.user_group_id == user_group_id).first()

    if not db_user or not db_user_group:
        raise HTTPException(status_code=404, detail="User or User Group not found")

    db.execute(
        t_user_group_membership.insert().values(user_id=user_id, user_group_id=user_group_id)
    )
    db.commit()
    return UserGroupMembershipPydantic(user_id=user_id, user_group_id=user_group_id)


@app.delete("/user_group_memberships/")
def create_user_group_membership(
    user_id: int, user_group_id: int, db: Session = Depends(get_db)
):
    db_user = db.query(User).filter(User.user_id == user_id).first()
    db_user_group = db.query(UserGroup).filter(UserGroup.user_group_id == user_group_id).first()

    if not db_user or not db_user_group:
        raise HTTPException(status_code=404, detail="User or User Group not found")

    db.execute(
        t_user_group_membership.delete().where(t_user_group_membership.c.user_id==user_id, t_user_group_membership.c.user_group_id==user_group_id)
    )
    db.commit()
    return {"message": "User added to User Group successfully"}


@app.post("/user_role_assignments/", response_model=UserRoleAssignmentPydantic)
def create_user_role_assignment(
    user_id: int, role_id: int, db: Session = Depends(get_db)
):
    db_user = db.query(User).filter(User.user_id == user_id).first()
    db_role = db.query(UserRole).filter(UserRole.role_id == role_id).first()

    if not db_user or not db_role:
        raise HTTPException(status_code=404, detail="User or UserRole not found")

    # Assuming t_user_role_assignment is your SQLAlchemy Core Table object
    db.execute(
        t_user_role_assignment.insert().values(user_id=user_id, role_id=role_id)
    )
    db.commit()

    # Return the created user_id and role_id
    return UserRoleAssignmentPydantic(user_id=user_id, role_id=role_id)


@app.delete("/user_role_assignments/")
def delete_user_role_assignment(
    user_id: int, role_id: int, db: Session = Depends(get_db)
):
    db_user = db.query(User).filter(User.user_id == user_id).first()
    db_user_group = db.query(UserRole).filter(UserRole.role_id == role_id).first()

    if not db_user or not db_user_group:
        raise HTTPException(status_code=404, detail="User or User Group not found")

    db.execute(
        t_user_role_assignment.delete().where(t_user_role_assignment.c.user_id==user_id, t_user_role_assignment.c.role_id==role_id)
    )
    db.commit()
    return {"message": "User removed from User role assignment successfully"}


@app.post("/asset_types/", response_model=AssetTypePydantic)
def create_asset_type(asset_type: AssetTypePydantic, db: Session = Depends(get_db)):
    asset_type_db = AssetType(**asset_type.dict())
    db.add(asset_type_db)
    db.commit()
    db.refresh(asset_type_db)
    return {"response": "data inserted successfully"}

@app.get("/asset_types/", response_model=list[AssetTypePydantic])
def read_asset_types(db: Session = Depends(get_db)):
    return db.query(AssetType).all()


@app.get("/asset_types/{asset_type_id}", response_model=AssetTypePydantic)
def read_asset_type(asset_type_id: int, db: Session = Depends(get_db)):
    db_asset_type = db.query(AssetType).filter(AssetType.asset_type_id == asset_type_id).first()
    if db_asset_type is None:
        raise HTTPException(status_code=404, detail="Asset Type not found")
    return db_asset_type


@app.put("/asset_types/{asset_type_id}", response_model=AssetTypePydantic)
def update_asset_type(asset_type_id: int, asset_type: AssetTypePydantic, db: Session = Depends(get_db)):
    db_asset_type = db.query(AssetType).filter(AssetType.asset_type_id == asset_type_id).first()
    if db_asset_type is None:
        raise HTTPException(status_code=404, detail="Asset Type not found")
    for field, value in asset_type.dict().items():
        setattr(db_asset_type, field, value)
    db.commit()
    db.refresh(db_asset_type)
    return db_asset_type


@app.delete("/asset_types/{asset_type_id}", response_model=AssetTypePydantic)
def delete_asset_type(asset_type_id: int, db: Session = Depends(get_db)):
    db_asset_type = db.query(AssetType).filter(AssetType.asset_type_id == asset_type_id).first()
    if db_asset_type is None:
        raise HTTPException(status_code=404, detail="Asset Type not found")
    db.delete(db_asset_type)
    db.commit()
    return db_asset_type





@app.post("/assets/", response_model=AssetPydantic)
def create_asset(asset: AssetPydantic, db: Session = Depends(get_db)):
    asset = Asset(**asset.dict())
    db.add(asset)
    db.commit()
    db.refresh(asset)
    return asset


@app.get("/assets/", response_model=list[AssetPydantic])
def read_assets(db: Session = Depends(get_db)):
    return db.query(Asset).all()


@app.get("/assets/{asset_id}", response_model=AssetPydantic)
def read_asset(asset_id: int, db: Session = Depends(get_db)):
    db_asset = db.query(Asset).filter(Asset.asset_id == asset_id).first()
    if db_asset is None:
        raise HTTPException(status_code=404, detail="Asset not found")
    return db_asset


@app.put("/assets/{asset_id}", response_model=AssetPydantic)
def update_asset(asset_id: int, asset: AssetPydantic, db: Session = Depends(get_db)):
    db_asset = db.query(Asset).filter(Asset.asset_id == asset_id).first()
    if db_asset is None:
        raise HTTPException(status_code=404, detail="Asset not found")
    for field, value in asset.dict().items():
        setattr(db_asset, field, value)
    db.commit()
    db.refresh(db_asset)
    return db_asset


@app.delete("/assets/{asset_id}", response_model=AssetPydantic)
def delete_asset(asset_id: int, db: Session = Depends(get_db)):
    db_asset = db.query(Asset).filter(Asset.asset_id == asset_id).first()
    if db_asset is None:
        raise HTTPException(status_code=404, detail="Asset not found")
    db.delete(db_asset)
    db.commit()
    return db_asset


@app.post("/rights/", response_model=RightPydantic)
def create_right(right: RightPydantic, db: Session = Depends(get_db)):
    right = Right(**right.dict())
    db.add(right)
    db.commit()
    db.refresh(right)
    return right


@app.get("/rights/", response_model=list[RightPydantic])
def read_rights(db: Session = Depends(get_db)):
    return db.query(Right).all()


@app.get("/rights/{right_id}", response_model=RightPydantic)
def read_right(right_id: int, db: Session = Depends(get_db)):
    db_right = db.query(Right).filter(Right.right_id == right_id).first()
    if db_right is None:
        raise HTTPException(status_code=404, detail="Right not found")
    return db_right


@app.put("/rights/{right_id}", response_model=RightPydantic)
def update_right(right_id: int, right: RightPydantic, db: Session = Depends(get_db)):
    db_right = db.query(Right).filter(Right.right_id == right_id).first()
    if db_right is None:
        raise HTTPException(status_code=404, detail="Right not found")
    for field, value in right.dict().items():
        setattr(db_right, field, value)
    db.commit()
    db.refresh(db_right)
    return db_right


@app.delete("/rights/{right_id}", response_model=RightPydantic)
def delete_right(right_id: int, db: Session = Depends(get_db)):
    db_right = db.query(Right).filter(Right.right_id == right_id).first()
    if db_right is None:
        raise HTTPException(status_code=404, detail="Right not found")
    db.delete(db_right)
    db.commit()
    return db_right



@app.post("/user_rights/", response_model=UserRightPydantic)
def create_user_right(
    user_id: int, right_id: int, db: Session = Depends(get_db)
):
    db_user = db.query(User).filter(User.user_id == user_id).first()
    db_right = db.query(Right).filter(Right.right_id == right_id).first()

    if not db_user or not db_right:
        raise HTTPException(status_code=404, detail="User or Right not found")

    db.execute(t_user_rights.insert().values(user_id=user_id, right_id=right_id))
    db.commit()
    return UserRightPydantic(user_id=user_id, right_id=right_id )


@app.delete("/user_rights/")
def delete_user_right(
    user_id: int, right_id: int, db: Session = Depends(get_db)
):
    db_user = db.query(User).filter(User.user_id == user_id).first()
    db_user_group = db.query(Right).filter(Right.right_id == right_id).first()

    if not db_user or not db_user_group:
        raise HTTPException(status_code=404, detail="User or User Group not found")

    db.execute(
        t_user_rights.delete().where(t_user_rights.c.user_id==user_id, t_user_rights.c.right_id==right_id)
    )
    db.commit()
    return {"message": "removed successfully"}




@app.post("/role_rights/", response_model=RoleRightPydantic)
def create_role_right(
    role_id: int, right_id: int, db: Session = Depends(get_db)
):
    db_role = db.query(UserRole).filter(UserRole.role_id == role_id).first()
    db_right = db.query(Right).filter(Right.right_id == right_id).first()

    if not db_role or not db_right:
        raise HTTPException(status_code=404, detail="Role or Right not found")

    db.execute(t_role_rights.insert().values(role_id=role_id, right_id=right_id))
    db.commit()
    return RoleRightPydantic(role_id=role_id, right_id=right_id )


@app.delete("/role_rights/")
def delete_role_right(
    role_id: int, right_id: int, db: Session = Depends(get_db)
):
    db_user = db.query(UserRole).filter(UserRole.role_id == role_id).first()
    db_user_group = db.query(Right).filter(Right.right_id == right_id).first()

    if not db_user or not db_user_group:
        raise HTTPException(status_code=404, detail="User or User Group not found")

    db.execute(
        t_role_rights.delete().where(t_role_rights.c.role_id==role_id, t_role_rights.c.right_id==right_id)
    )
    db.commit()
    return {"message": "removed successfully"}



@app.post("/tags/", response_model=TagPydantic)
def create_tag(tag: TagPydantic, db: Session = Depends(get_db)):
    tag = Tag(**tag.dict())
    db.add(tag)
    db.commit()
    db.refresh(tag)
    return tag


@app.get("/tags/", response_model=list[TagPydantic])
def read_tags(db: Session = Depends(get_db)):
    return db.query(Tag).all()


@app.get("/tags/{tag_id}", response_model=TagPydantic)
def read_tag(tag_id: int, db: Session = Depends(get_db)):
    db_tag = db.query(Tag).filter(Tag.tag_id == tag_id).first()
    if db_tag is None:
        raise HTTPException(status_code=404, detail="Tag not found")
    return db_tag


@app.put("/tags/{tag_id}", response_model=TagPydantic)
def update_tag(tag_id: int, tag: TagPydantic, db: Session = Depends(get_db)):
    db_tag = db.query(Tag).filter(Tag.tag_id == tag_id).first()
    if db_tag is None:
        raise HTTPException(status_code=404, detail="Tag not found")
    for field, value in tag.dict().items():
        setattr(db_tag, field, value)
    db.commit()
    db.refresh(db_tag)
    return db_tag


@app.delete("/tags/{tag_id}", response_model=TagPydantic)
def delete_tag(tag_id: int, db: Session = Depends(get_db)):
    db_tag = db.query(Tag).filter(Tag.tag_id == tag_id).first()
    if db_tag is None:
        raise HTTPException(status_code=404, detail="Tag not found")
    db.delete(db_tag)
    db.commit()
    return db_tag


@app.post("/device_types/", response_model=DeviceTypePydantic)
def create_device_type(device_type: DeviceTypePydantic, db: Session = Depends(get_db)):
    device_type = DeviceType(**device_type.dict())
    db.add(device_type)
    db.commit()
    db.refresh(device_type)
    return device_type


@app.get("/device_types/", response_model=list[DeviceTypePydantic])
def read_device_types(db: Session = Depends(get_db)):
    return db.query(DeviceType).all()


@app.get("/device_types/{device_type_id}", response_model=DeviceTypePydantic)
def read_device_type(device_type_id: int, db: Session = Depends(get_db)):
    db_device_type = db.query(DeviceType).filter(DeviceType.device_type_id == device_type_id).first()
    if db_device_type is None:
        raise HTTPException(status_code=404, detail="Device Type not found")
    return db_device_type


@app.put("/device_types/{device_type_id}", response_model=DeviceTypePydantic)
def update_device_type(device_type_id: int, device_type: DeviceTypePydantic, db: Session = Depends(get_db)):
    db_device_type = db.query(DeviceType).filter(DeviceType.device_type_id == device_type_id).first()
    if db_device_type is None:
        raise HTTPException(status_code=404, detail="Device Type not found")
    for field, value in device_type.dict().items():
        setattr(db_device_type, field, value)
    db.commit()
    db.refresh(db_device_type)
    return db_device_type


@app.delete("/device_types/{device_type_id}", response_model=DeviceTypePydantic)
def delete_device_type(device_type_id: int, db: Session = Depends(get_db)):
    db_device_type = db.query(DeviceType).filter(DeviceType.device_type_id == device_type_id).first()
    if db_device_type is None:
        raise HTTPException(status_code=404, detail="Device Type not found")
    db.delete(db_device_type)
    db.commit()
    return db_device_type


@app.post("/devices/", response_model=DevicePydantic)
def create_device(device: DevicePydantic, db: Session = Depends(get_db)):
    device = Device(**device.dict())
    db.add(device)
    db.commit()
    db.refresh(device)
    return device


@app.get("/devices/", response_model=list[DevicePydantic])
def read_devices(db: Session = Depends(get_db)):
    return db.query(Device).all()


@app.get("/devices/{device_id}", response_model=DevicePydantic)
def read_device(device_id: int, db: Session = Depends(get_db)):
    db_device = db.query(Device).filter(Device.device_id == device_id).first()
    if db_device is None:
        raise HTTPException(status_code=404, detail="Device not found")
    return db_device


@app.put("/devices/{device_id}", response_model=DevicePydantic)
def update_device(device_id: int, device: DevicePydantic, db: Session = Depends(get_db)):
    db_device = db.query(Device).filter(Device.device_id == device_id).first()
    if db_device is None:
        raise HTTPException(status_code=404, detail="Device not found")
    for field, value in device.dict().items():
        setattr(db_device, field, value)
    db.commit()
    db.refresh(db_device)
    return db_device


@app.delete("/devices/{device_id}", response_model=DevicePydantic)
def delete_device(device_id: int, db: Session = Depends(get_db)):
    db_device = db.query(Device).filter(Device.device_id == device_id).first()
    if db_device is None:
        raise HTTPException(status_code=404, detail="Device not found")
    db.delete(db_device)
    db.commit()
    return db_device



@app.post("/device_tags/", response_model=DeviceTagPydantic)
def create_device_tag(device: DeviceTagPydantic, db: Session = Depends(get_db)):
    device = DeviceTag(**device.dict())
    db.add(device)
    db.commit()
    db.refresh(device)
    return device



@app.delete("/device_tags/")
def delete_device_tag(
    ID: int, db: Session = Depends(get_db)
):
    db_device_type = db.query(DeviceTag).filter(DeviceTag.ID == ID).first()
    if db_device_type is None:
        raise HTTPException(status_code=404, detail="Device Type not found")
    db.delete(db_device_type)
    db.commit()
    return db_device_type



@app.post("/connection_types/", response_model=ConnectionTypePydantic)
def create_connection_type(connection_type: ConnectionTypePydantic, db: Session = Depends(get_db)):
    connection_type = ConnectionType(**connection_type.dict())
    db.add(connection_type)
    db.commit()
    db.refresh(connection_type)
    return connection_type


@app.get("/connection_types/", response_model=list[ConnectionTypePydantic])
def read_connection_types(db: Session = Depends(get_db)):
    return db.query(ConnectionType).all()


@app.get("/connection_types/{connection_type_id}", response_model=ConnectionTypePydantic)
def read_connection_type(connection_type_id: int, db: Session = Depends(get_db)):
    db_connection_type = db.query(ConnectionType).filter(ConnectionType.connection_type_id == connection_type_id).first()
    if db_connection_type is None:
        raise HTTPException(status_code=404, detail="Connection Type not found")
    return db_connection_type


@app.put("/connection_types/{connection_type_id}", response_model=ConnectionTypePydantic)
def update_connection_type(connection_type_id: int, connection_type: ConnectionTypePydantic, db: Session = Depends(get_db)):
    db_connection_type = db.query(ConnectionType).filter(ConnectionType.connection_type_id == connection_type_id).first()
    if db_connection_type is None:
        raise HTTPException(status_code=404, detail="Connection Type not found")
    for field, value in connection_type.dict().items():
        setattr(db_connection_type, field, value)
    db.commit()
    db.refresh(db_connection_type)
    return db_connection_type


@app.delete("/connection_types/{connection_type_id}", response_model=ConnectionTypePydantic)
def delete_connection_type(connection_type_id: int, db: Session = Depends(get_db)):
    db_connection_type = db.query(ConnectionType).filter(ConnectionType.connection_type_id == connection_type_id).first()
    if db_connection_type is None:
        raise HTTPException(status_code=404, detail="Connection Type not found")
    db.delete(db_connection_type)
    db.commit()
    return db_connection_type



@app.post("/connections/", response_model=ConnectionPydantic)
def create_connection(connection: ConnectionPydantic, db: Session = Depends(get_db)):
    connection = Connection(**connection.dict())
    db.add(connection)
    db.commit()
    db.refresh(connection)
    return connection


@app.get("/connections/", response_model=list[ConnectionPydantic])
def read_connections(db: Session = Depends(get_db)):
    return db.query(Connection).all()


@app.get("/connections/{connection_id}", response_model=ConnectionPydantic)
def read_connection(connection_id: int, db: Session = Depends(get_db)):
    db_connection = db.query(Connection).filter(Connection.connection_id == connection_id).first()
    if db_connection is None:
        raise HTTPException(status_code=404, detail="Connection not found")
    return db_connection


@app.put("/connections/{connection_id}", response_model=ConnectionPydantic)
def update_connection(connection_id: int, connection: ConnectionPydantic, db: Session = Depends(get_db)):
    db_connection = db.query(Connection).filter(Connection.connection_id == connection_id).first()
    if db_connection is None:
        raise HTTPException(status_code=404, detail="Connection not found")
    for field, value in connection.dict().items():
        setattr(db_connection, field, value)
    db.commit()
    db.refresh(db_connection)
    return db_connection


@app.delete("/connections/{connection_id}", response_model=ConnectionPydantic)
def delete_connection(connection_id: int, db: Session = Depends(get_db)):
    db_connection = db.query(Connection).filter(Connection.connection_id == connection_id).first()
    if db_connection is None:
        raise HTTPException(status_code=404, detail="Connection not found")
    db.delete(db_connection)
    db.commit()
    return db_connection





@app.post("/connection_details/", response_model=ConnectionDetailPydantic)
def create_connection_detail(connection_detail: ConnectionDetailPydantic, db: Session = Depends(get_db)):
    connection_detail = ConnectionDetail(**connection_detail.dict())
    db.add(connection_detail)
    db.commit()
    db.refresh(connection_detail)
    return connection_detail


@app.get("/connection_details/", response_model=list[ConnectionDetailPydantic])
def read_connection_details(db: Session = Depends(get_db)):
    return db.query(ConnectionDetail).all()


@app.get("/connection_details/{connection_detail_id}", response_model=ConnectionDetailPydantic)
def read_connection_detail(connection_detail_id: int, db: Session = Depends(get_db)):
    db_connection_detail = db.query(ConnectionDetail).filter(ConnectionDetail.connection_detail_id == connection_detail_id).first()
    if db_connection_detail is None:
        raise HTTPException(status_code=404, detail="Connection Detail not found")
    return db_connection_detail


@app.put("/connection_details/{connection_detail_id}", response_model=ConnectionDetailPydantic)
def update_connection_detail(connection_detail_id: int, connection_detail: ConnectionDetailPydantic, db: Session = Depends(get_db)):
    db_connection_detail = db.query(ConnectionDetail).filter(ConnectionDetail.connection_detail_id == connection_detail_id).first()
    if db_connection_detail is None:
        raise HTTPException(status_code=404, detail="Connection Detail not found")
    for field, value in connection_detail.dict().items():
        setattr(db_connection_detail, field, value)
    db.commit()
    db.refresh(db_connection_detail)
    return db_connection_detail


@app.delete("/connection_details/{connection_detail_id}", response_model=ConnectionDetailPydantic)
def delete_connection_detail(connection_detail_id: int, db: Session = Depends(get_db)):
    db_connection_detail = db.query(ConnectionDetail).filter(ConnectionDetail.connection_detail_id == connection_detail_id).first()
    if db_connection_detail is None:
        raise HTTPException(status_code=404, detail="Connection Detail not found")
    db.delete(db_connection_detail)
    db.commit()
    return db_connection_detail


@app.post("/user_log_history/", response_model=UserLogHistoryPydantic)
def create_user_log_history(user_log_history: UserLogHistoryPydantic, db: Session = Depends(get_db)):
    user_log_history = UserLogHistory(**user_log_history.dict())
    db.add(user_log_history)
    db.commit()
    db.refresh(user_log_history)
    return user_log_history

@app.get("/user_log_history/", response_model=list[UserLogHistoryPydantic])
def read_user_log_history(db: Session = Depends(get_db)):
    return db.query(UserLogHistory).all()


@app.get("/user_log_history/{log_id}", response_model=UserLogHistoryPydantic)
def read_user_log_by_id(log_id: int, db: Session = Depends(get_db)):
    db_user_log = db.query(UserLogHistory).filter(UserLogHistory.log_id == log_id).first()
    if db_user_log is None:
        raise HTTPException(status_code=404, detail="User Log not found")
    return db_user_log


@app.put("/user_log_history/{log_id}", response_model=UserLogHistoryPydantic)
def update_user_log_history(log_id: int, user_log_history: UserLogHistoryPydantic, db: Session = Depends(get_db)):
    db_user_log = db.query(UserLogHistory).filter(UserLogHistory.log_id == log_id).first()
    if db_user_log is None:
        raise HTTPException(status_code=404, detail="User Log not found")
    for field, value in user_log_history.dict().items():
        setattr(db_user_log, field, value)
    db.commit()
    db.refresh(db_user_log)
    return db_user_log


@app.delete("/user_log_history/{log_id}", response_model=UserLogHistoryPydantic)
def delete_user_log_history(log_id: int, db: Session = Depends(get_db)):
    db_user_log = db.query(UserLogHistory).filter(UserLogHistory.log_id == log_id).first()
    if db_user_log is None:
        raise HTTPException(status_code=404, detail="User Log not found")
    db.delete(db_user_log)
    db.commit()
    return db_user_log


    

@app.post("/alerts/", response_model=AlertPydantic)
def create_alert(alert: AlertPydantic, db: Session = Depends(get_db)):
    alert = Alert(**alert.dict())
    db.add(alert)
    db.commit()
    db.refresh(alert)
    return alert


@app.get("/alerts/", response_model=list[AlertPydantic])
def read_alerts(db: Session = Depends(get_db)):
    return db.query(Alert).all()


@app.get("/alerts/{alert_id}", response_model=AlertPydantic)
def read_alert(alert_id: int, db: Session = Depends(get_db)):
    db_alert = db.query(Alert).filter(Alert.alert_id == alert_id).first()
    if db_alert is None:
        raise HTTPException(status_code=404, detail="Alert not found")
    return db_alert


@app.put("/alerts/{alert_id}", response_model=AlertPydantic)
def update_alert(alert_id: int, alert: AlertPydantic, db: Session = Depends(get_db)):
    db_alert = db.query(Alert).filter(Alert.alert_id == alert_id).first()
    if db_alert is None:
        raise HTTPException(status_code=404, detail="Alert not found")
    for field, value in alert.dict().items():
        setattr(db_alert, field, value)
    db.commit()
    db.refresh(db_alert)
    return db_alert


@app.delete("/alerts/{alert_id}", response_model=AlertPydantic)
def delete_alert(alert_id: int, db: Session = Depends(get_db)):
    db_alert = db.query(Alert).filter(Alert.alert_id == alert_id).first()
    if db_alert is None:
        raise HTTPException(status_code=404, detail="Alert not found")
    db.delete(db_alert)
    db.commit()
    return db_alert



@app.post("/alert_expressions/", response_model=AlertExpressionPydantic)
def create_alert_expression(alert_expression: AlertExpressionPydantic, db: Session = Depends(get_db)):
    alert_expression = AlertExpression(**alert_expression.dict())
    db.add(alert_expression)
    db.commit()
    db.refresh(alert_expression)
    return alert_expression


@app.get("/alert_expressions/", response_model=list[AlertExpressionPydantic])
def read_alert_expressions(db: Session = Depends(get_db)):
    return db.query(AlertExpressionPydantic).all()


@app.get("/alert_expressions/{expression_id}", response_model=AlertExpressionPydantic)
def read_alert_expression(expression_id: int, db: Session = Depends(get_db)):
    db_alert_expression = db.query(AlertExpression).filter(AlertExpression.expression_id == expression_id).first()
    if db_alert_expression is None:
        raise HTTPException(status_code=404, detail="Alert Expression not found")
    return db_alert_expression


@app.put("/alert_expressions/{expression_id}", response_model=AlertExpressionPydantic)
def update_alert_expression(expression_id: int, alert_expression: AlertExpressionPydantic, db: Session = Depends(get_db)):
    db_alert_expression = db.query(AlertExpression).filter(AlertExpression.expression_id == expression_id).first()
    if db_alert_expression is None:
        raise HTTPException(status_code=404, detail="Alert Expression not found")
    for field, value in alert_expression.dict().items():
        setattr(db_alert_expression, field, value)
    db.commit()
    db.refresh(db_alert_expression)
    return db_alert_expression


@app.delete("/alert_expressions/{expression_id}", response_model=AlertExpressionPydantic)
def delete_alert_expression(expression_id: int, db: Session = Depends(get_db)):
    db_alert_expression = db.query(AlertExpression).filter(AlertExpression.expression_id == expression_id).first()
    if db_alert_expression is None:
        raise HTTPException(status_code=404, detail="Alert Expression not found")
    db.delete(db_alert_expression)
    db.commit()
    return db_alert_expression




@app.post("/history/", response_model=HistoryPydantic)
def create_history(history: HistoryPydantic, db: Session = Depends(get_db)):
    history = History(**history.dict())
    db.add(history)
    db.commit()
    db.refresh(history)
    return history


@app.get("/history/", response_model=list[HistoryPydantic])
def read_history(db: Session = Depends(get_db)):
    return db.query(History).all()


@app.get("/history/{history_id}", response_model=HistoryPydantic)
def read_history_by_id(history_id: int, db: Session = Depends(get_db)):
    db_history = db.query(History).filter(History.history_id == history_id).first()
    if db_history is None:
        raise HTTPException(status_code=404, detail="History not found")
    return db_history


@app.put("/history/{history_id}", response_model=HistoryPydantic)
def update_history(history_id: int, history: HistoryPydantic, db: Session = Depends(get_db)):
    db_history = db.query(History).filter(History.history_id == history_id).first()
    if db_history is None:
        raise HTTPException(status_code=404, detail="History not found")
    for field, value in history.dict().items():
        setattr(db_history, field, value)
    db.commit()
    db.refresh(db_history)
    return db_history


@app.delete("/history/{history_id}", response_model=HistoryPydantic)
def delete_history(history_id: int, db: Session = Depends(get_db)):
    db_history = db.query(History).filter(History.history_id == history_id).first()
    if db_history is None:
        raise HTTPException(status_code=404, detail="History not found")
    db.delete(db_history)
    db.commit()
    return db_history


@app.post("/action_types/", response_model=ActionTypePydantic)
def create_action_type(action_type: ActionTypePydantic, db: Session = Depends(get_db)):
    action_type = ActionType(**action_type.dict())
    db.add(action_type)
    db.commit()
    db.refresh(action_type)
    return action_type


@app.get("/action_types/", response_model=list[ActionTypePydantic])
def read_action_types(db: Session = Depends(get_db)):
    return db.query(ActionType).all()


@app.get("/action_types/{action_type_id}", response_model=ActionTypePydantic)
def read_action_type(action_type_id: int, db: Session = Depends(get_db)):
    db_action_type = db.query(ActionType).filter(ActionType.action_type_id == action_type_id).first()
    if db_action_type is None:
        raise HTTPException(status_code=404, detail="Action Type not found")
    return db_action_type


@app.put("/action_types/{action_type_id}", response_model=ActionTypePydantic)
def update_action_type(action_type_id: int, action_type: ActionTypePydantic, db: Session = Depends(get_db)):
    db_action_type = db.query(ActionType).filter(ActionType.action_type_id == action_type_id).first()
    if db_action_type is None:
        raise HTTPException(status_code=404, detail="Action Type not found")
    for field, value in action_type.dict().items():
        setattr(db_action_type, field, value)
    db.commit()
    db.refresh(db_action_type)
    return db_action_type


@app.delete("/action_types/{action_type_id}", response_model=ActionTypePydantic)
def delete_action_type(action_type_id: int, db: Session = Depends(get_db)):
    db_action_type = db.query(ActionType).filter(ActionType.action_type_id == action_type_id).first()
    if db_action_type is None:
        raise HTTPException(status_code=404, detail="Action Type not found")
    db.delete(db_action_type)
    db.commit()
    return db_action_type




@app.post("/actions/", response_model=ActionPydantic)
def create_action(action: ActionPydantic, db: Session = Depends(get_db)):
    action = Action(**action.dict())
    db.add(action)
    db.commit()
    db.refresh(action)
    return action


@app.get("/actions/", response_model=list[ActionPydantic])
def read_actions(db: Session = Depends(get_db)):
    return db.query(Action).all()


@app.get("/actions/{action_id}", response_model=ActionPydantic)
def read_action(action_id: int, db: Session = Depends(get_db)):
    db_action = db.query(Action).filter(Action.action_id == action_id).first()
    if db_action is None:
        raise HTTPException(status_code=404, detail="Action not found")
    return db_action


@app.put("/actions/{action_id}", response_model=ActionPydantic)
def update_action(action_id: int, action: ActionPydantic, db: Session = Depends(get_db)):
    db_action = db.query(Action).filter(Action.action_id == action_id).first()
    if db_action is None:
        raise HTTPException(status_code=404, detail="Action not found")
    for field, value in action.dict().items():
        setattr(db_action, field, value)
    db.commit()
    db.refresh(db_action)
    return db_action


@app.delete("/actions/{action_id}", response_model=ActionPydantic)
def delete_action(action_id: int, db: Session = Depends(get_db)):
    db_action = db.query(Action).filter(Action.action_id == action_id).first()
    if db_action is None:
        raise HTTPException(status_code=404, detail="Action not found")
    db.delete(db_action)
    db.commit()
    return db_action


@app.post("/action_history/")
def create_action_history(action_id: int, history_id: int, db: Session = Depends(get_db)):
    action = db.query(Action).filter(Action.action_id == action_id).first()
    history = db.query(History).filter(History.history_id == history_id).first()
    if action is None or history is None:
        raise HTTPException(status_code=404, detail="Action or History not found")
    db.execute(t_actions_history.insert().values(action_id=action_id, history_id=history_id))
    db.commit()
    return ActionHistoryPydantic(action_id=action_id, history_id=history_id)


@app.delete("/action_history/")
def delete_action_history(action_id: int, history_id: int, db: Session = Depends(get_db)):
    action = db.query(Action).filter(Action.action_id == action_id).first()
    history = db.query(History).filter(History.history_id == history_id).first()
    if action is None or history is None:
        raise HTTPException(status_code=404, detail="Action or History not found")
    db.execute(t_actions_history.delete().where(t_actions_history.c.action_id==action_id, t_actions_history.c.history_id==history_id))
    db.commit()
    return {"message": "Association deleted successfully"}



@app.post("/action_alert/")
def create_action_alert(action_id: int, alert_id: int, db: Session = Depends(get_db)):
    action = db.query(Action).filter(Action.action_id == action_id).first()
    alert = db.query(Alert).filter(Alert.alert_id == alert_id).first()
    if action is None or alert is None:
        raise HTTPException(status_code=404, detail="Action or Alert not found")
    db.execute(t_actions_alert.insert().values(action_id=action_id, alert_id=alert_id))
    db.commit()
    return ActionAlertPydantic(action_id=action_id, alert_id=alert_id)


@app.delete("/action_alert/")
def delete_action_alert(action_id: int, alert_id: int, db: Session = Depends(get_db)):
    action = db.query(Action).filter(Action.action_id == action_id).first()
    alert = db.query(Alert).filter(Alert.alert_id == alert_id).first()
    if action is None or alert is None:
        raise HTTPException(status_code=404, detail="Action or Alert not found")
    db.execute(t_actions_alert.delete().where(t_actions_alert.c.action_id==action_id, t_actions_alert.c.alert_id==alert_id))
    db.commit()
    return ActionAlertPydantic(action_id=action_id, alert_id=alert_id)
    
# Define the GET method to retrieve all active device data
@app.get("/active_devices/")
def get_active_devices(db: Session = Depends(get_db)):
    # Join necessary tables to fetch required data
    query = (
        db.query(
            History.recorded_date_time,
            func.max(Device.device_id).label("device_id"),
            func.max(Device.device_serial_number).label("device_serial_number"),
            Tag.description.label("tag_description"),
            func.max(History.value).label("tag_value")
        )
        .join(DeviceTag, DeviceTag.tag_id == History.device_tag_id)
        .join(Tag, DeviceTag.tag_id == Tag.tag_id)
        .join(Device, DeviceTag.device_id == Device.device_id)
        .filter(Device.is_active == True)
        .group_by(History.recorded_date_time, Tag.description)
        .order_by(History.recorded_date_time.desc())
        .all()
    )

    result = {}
    for recorded_date_time, device_id, device_serial_number, tag_description, tag_value in query:
        if recorded_date_time not in result:
            result[recorded_date_time] = {'device_id': device_id, 'device_serial_number': device_serial_number, 'tags': []}
        
        tag_info = {'description': tag_description, 'value': tag_value}
        result[recorded_date_time]['tags'].append(tag_info)

    return result

@app.get("/get_devices_history/")
def get_devices_history(db: Session = Depends(get_db)):
    subq = (
        db.query(
            History.device_tag_id,
            History.recorded_date_time,
            func.row_number().over(
                partition_by=History.device_tag_id,
                order_by=History.recorded_date_time.desc()
            ).label("row_number"),
        )
        .subquery("subq_alias")  # Using a unique alias for the subquery
    )

    query = (
        db.query(
            subq.c.recorded_date_time,
            Device.device_id,
            Device.device_serial_number,
            Tag.description.label("tag_description"),
            History.value.label("tag_value")
        )
        .join(DeviceTag, DeviceTag.tag_id == subq.c.device_tag_id)
        .join(Tag, DeviceTag.tag_id == Tag.tag_id)
        .join(Device, DeviceTag.device_id == Device.device_id)
        .filter(Device.is_active == True)
        .filter(subq.c.row_number == 1)
        .order_by(subq.c.recorded_date_time.desc())
        .all()
    )

    result = {}
    for recorded_date_time, device_id, device_serial_number, tag_description, tag_value in query:
        if recorded_date_time not in result:
            result[recorded_date_time] = {'device_id': device_id, 'device_serial_number': device_serial_number, 'tags': []}

        tag_info = {'description': tag_description, 'value': tag_value}
        result[recorded_date_time]['tags'].append(tag_info)

    return result


@app.get("/get_latest_devices_data/")
def get_latest_devices_data(db: Session = Depends(get_db)):
#     subq = (
#         db.query(
#             History.device_tag_id,
#             func.max(History.recorded_date_time).label("latest_recorded_date")
#         )
#         .group_by(History.device_tag_id)
#         .subquery()
#     )
# 
#     latest_data = (
#         db.query(
#             Device.device_id,
#             Device.device_serial_number,
#             Tag.description.label("tag_description"),
#             History.value.label("tag_value"),
#             subq.c.latest_recorded_date
#         )
#         .join(DeviceTag, DeviceTag.device_id == Device.device_id)
#         .join(Tag, Tag.tag_id == DeviceTag.tag_id)
#         .join(subq, subq.c.device_tag_id == DeviceTag.tag_id)
#         .join(History, and_(
#             History.device_tag_id == subq.c.device_tag_id,
#             History.recorded_date_time == subq.c.latest_recorded_date
#         ))
#         .filter(Device.is_active == True)
# #        .filter(Tag.description.in_(["AQ", "TMP", "HUM"]))
#         .order_by(desc(subq.c.latest_recorded_date))
#         .all()
#     )
    subq = (
        db.query(
            History.device_tag_id.label('device_tag_id'),
            func.max(History.recorded_date_time).label("latest_recorded_date")
        )
        .group_by(History.device_tag_id)
        .subquery()
    )
    
    latest_data = (
        db.query(
            Device.device_id,
            Device.device_serial_number,
            Tag.description.label("tag_description"),
            History.value.label("tag_value"),
            subq.c.latest_recorded_date
        )
        .join(DeviceTag, DeviceTag.device_id == Device.device_id)
        .join(Tag, Tag.tag_id == DeviceTag.tag_id)
        .join(subq, subq.c.device_tag_id == DeviceTag.ID)
        .join(History, and_(
            History.device_tag_id == subq.c.device_tag_id,
            History.recorded_date_time == subq.c.latest_recorded_date,
            Device.is_active == True
        ))
        .order_by(desc(subq.c.latest_recorded_date))
        .all()
    )
    result = {}
    for device_id, device_serial_number, tag_description, tag_value, latest_recorded_date in latest_data:
        if device_id not in result:
            result[device_id] = {'device_serial_number': device_serial_number, 'tags': {}, 'latest_recorded_date': latest_recorded_date}

        if tag_description not in result[device_id]['tags']:
            result[device_id]['tags'][tag_description] = tag_value

    return result


@app.get("/get_device_latest_records")
async def get_device_latest_records(db: Session = Depends(get_db)):
    deviceslatestrecords = db.query(DeviceLatestRecord).all()

    result = {}
    current_time = datetime.now()
    for record in deviceslatestrecords:
        device_id = record.devices_device_id
        device_serial_number = record.devices_device_serial_number
        tag_description = record.tag_description
        tag_value = record.tag_value
        latest_recorded_date = record.anon_1_latest_recorded_date.strftime("%Y-%m-%d %H:%M:%S")
        # Assuming latest_recorded_date is in the format "YYYY-MM-DD HH:MM:SS"
        latest_recorded_date_ = record.anon_1_latest_recorded_date  # Assuming this is a string

        # Calculate the time difference between current_time and latest_recorded_date
        time_difference = current_time - latest_recorded_date_
        minutes_difference = time_difference.total_seconds() / 60  # Convert to minutes

        # Assign comm_status based on time difference
        if minutes_difference <= 31:
            comm_status = 'green'
        elif 31 < minutes_difference <= 61:
            comm_status = 'orange'
        else:
            comm_status = 'red'
        if device_id not in result:
            result[device_id] = {'device_serial_number': device_serial_number, 'tags': {},
                                 'latest_recorded_date': latest_recorded_date, 'comm_satus': comm_status}

        if tag_description not in result[device_id]['tags']:
            result[device_id]['tags'][tag_description] = tag_value

    return {"records": list(result.values())}

@app.get("/get_device_piehart_data")
async def get_device_pichart_data(db: Session = Depends(get_db)):
    # deviceslatestrecords = db.query(DeviceLatestRecord).all()

    dlr_alias = aliased(DeviceLatestRecord)

    # Subquery to assign row numbers partitioned by devices_device_id
    subq = (
        select(
            DeviceLatestRecord,
            func.row_number()
            .over(partition_by=DeviceLatestRecord.devices_device_id)
            .label('rn')
        )
        .select_from(DeviceLatestRecord)
        .cte('numbered')
    )

    # Query to fetch one row per unique devices_device_id
    unique_records_query = (
        select(subq.c)
        .where(subq.c.rn == 1)
        .order_by(subq.c.devices_device_id)
    )

    # Execute the query to get the unique rows
    deviceslatestrecords = db.execute(unique_records_query).fetchall()
    result = {}
    current_time = datetime.now()
    live_count = 0
    offline_count = 0
    for record in deviceslatestrecords:
        device_id = record.devices_device_id
        device_serial_number = record.devices_device_serial_number
        tag_description = record.tag_description
        tag_value = record.tag_value
        latest_recorded_date = record.anon_1_latest_recorded_date.strftime("%Y-%m-%d %H:%M:%S")
        # Assuming latest_recorded_date is in the format "YYYY-MM-DD HH:MM:SS"
        latest_recorded_date_ = record.anon_1_latest_recorded_date  # Assuming this is a string

        # Calculate the time difference between current_time and latest_recorded_date
        time_difference = current_time - latest_recorded_date_
        minutes_difference = time_difference.total_seconds() / 60  # Convert to minutes

        # Assign comm_status based on time difference
        if minutes_difference <= 31:
            comm_status = 'green'
            live_count += 1
        elif 31 < minutes_difference <= 61:
            comm_status = 'orange'
            offline_count += 1
        else:
            comm_status = 'red'
            offline_count += 1

        if device_id not in result:
            result[device_id] = {'device_serial_number': device_serial_number, 'tags': {},
                                 'latest_recorded_date': latest_recorded_date, 'comm_satus': comm_status}

        if tag_description not in result[device_id]['tags']:
            result[device_id]['tags'][tag_description] = tag_value

    total_devices = len(result)
    live_percentage = (live_count / total_devices) * 100 if total_devices > 0 else 0
    offline_percentage = (offline_count / total_devices) * 100 if total_devices > 0 else 0

    return {
        "total_devices": total_devices,
        "live": live_count,
        "offline": offline_count,
        "live_perc": round(live_percentage, 2),
        "offline_perc": round(offline_percentage, 2)
    }
    # return {"records": list(result.values())}
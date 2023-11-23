from model import *
from typing import List
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import sessionmaker, relationship, Session
from urllib.parse import quote_plus
import bcrypt
from fastapi import FastAPI, Response
from starlette.status import HTTP_101_SWITCHING_PROTOCOLS, HTTP_401_UNAUTHORIZED
from sqlalchemy import func, select
from sqlalchemy.orm import aliased
from sqlalchemy.sql import text


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


app = FastAPI()

@app.post("/addresses/", response_model=AddressPydantic)
def create_address(address: AddressPydantic, db: Session = Depends(get_db)):
    db.add(address)
    db.commit()
    db.refresh(address)
    return address


@app.get("/addresses/{address_id}", response_model=AddressPydantic)
def read_address(address_id: int, db: Session = Depends(get_db)):
    db_address = db.query(AddressPydantic).filter(AddressPydantic.address_id == address_id).first()
    if db_address is None:
        raise HTTPException(status_code=404, detail="Address not found")
    return db_address


@app.put("/addresses/{address_id}", response_model=AddressPydantic)
def update_address(address_id: int, address: AddressPydantic, db: Session = Depends(get_db)):
    db_address = db.query(AddressPydantic).filter(AddressPydantic.address_id == address_id).first()
    if db_address is None:
        raise HTTPException(status_code=404, detail="Address not found")
    for field, value in address.dict().items():
        setattr(db_address, field, value)
    db.commit()
    db.refresh(db_address)
    return db_address


@app.delete("/addresses/{address_id}", response_model=AddressPydantic)
def delete_address(address_id: int, db: Session = Depends(get_db)):
    db_address = db.query(AddressPydantic).filter(AddressPydantic.address_id == address_id).first()
    if db_address is None:
        raise HTTPException(status_code=404, detail="Address not found")
    db.delete(db_address)
    db.commit()
    return db_address


@app.post("/contact_types/", response_model=ContactTypePydantic)
def create_contact_type(contact_type: ContactTypePydantic, db: Session = Depends(get_db)):
    db.add(contact_type)
    db.commit()
    db.refresh(contact_type)
    return contact_type


@app.get("/contact_types/", response_model=List[ContactTypePydantic])
def read_contact_types(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(ContactTypePydantic).offset(skip).limit(limit).all()


@app.get("/contact_types/{contact_type_id}", response_model=ContactTypePydantic)
def read_contact_type(contact_type_id: int, db: Session = Depends(get_db)):
    db_contact_type = db.query(ContactTypePydantic).filter(ContactTypePydantic.contact_type_id == contact_type_id).first()
    if db_contact_type is None:
        raise HTTPException(status_code=404, detail="Contact type not found")
    return db_contact_type


@app.put("/contact_types/{contact_type_id}", response_model=ContactTypePydantic)
def update_contact_type(contact_type_id: int, description: str, db: Session = Depends(get_db)):
    db_contact_type = db.query(ContactTypePydantic).filter(ContactTypePydantic.contact_type_id == contact_type_id).first()
    if db_contact_type is None:
        raise HTTPException(status_code=404, detail="Contact type not found")
    db_contact_type.description = description
    db.commit()
    db.refresh(db_contact_type)
    return db_contact_type


@app.delete("/contact_types/{contact_type_id}", response_model=ContactTypePydantic)
def delete_contact_type(contact_type_id: int, db: Session = Depends(get_db)):
    db_contact_type = db.query(ContactTypePydantic).filter(ContactTypePydantic.contact_type_id == contact_type_id).first()
    if db_contact_type is None:
        raise HTTPException(status_code=404, detail="Contact type not found")
    db.delete(db_contact_type)
    db.commit()
    return db_contact_type


@app.post("/contacts/", response_model=ContactPydantic)
def create_contact(contact: ContactPydantic, db: Session = Depends(get_db)):
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


@app.get("/contacts/", response_model=List[ContactPydantic])
def read_contacts(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(ContactPydantic).offset(skip).limit(limit).all()


@app.get("/contacts/{contact_id}", response_model=ContactPydantic)
def read_contact(contact_id: int, db: Session = Depends(get_db)):
    db_contact = db.query(ContactPydantic).filter(ContactPydantic.contact_id == contact_id).first()
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact


@app.put("/contacts/{contact_id}", response_model=ContactPydantic)
def update_contact(contact_id: int, contact: ContactPydantic, db: Session = Depends(get_db)):
    db_contact = db.query(ContactPydantic).filter(ContactPydantic.contact_id == contact_id).first()
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    for field, value in contact.dict().items():
        setattr(db_contact, field, value)
    db.commit()
    db.refresh(db_contact)
    return db_contact


@app.delete("/contacts/{contact_id}", response_model=ContactPydantic)
def delete_contact(contact_id: int, db: Session = Depends(get_db)):
    db_contact = db.query(ContactPydantic).filter(ContactPydantic.contact_id == contact_id).first()
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    db.delete(db_contact)
    db.commit()
    return db_contact



@app.post("/locations/", response_model=LocationPydantic)
def create_location(location: LocationPydantic, db: Session = Depends(get_db)):
    db.add(location)
    db.commit()
    db.refresh(location)
    return location


@app.get("/locations/", response_model=List[LocationPydantic])
def read_locations(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(LocationPydantic).offset(skip).limit(limit).all()


@app.get("/locations/{location_id}", response_model=LocationPydantic)
def read_location(location_id: int, db: Session = Depends(get_db)):
    db_location = db.query(LocationPydantic).filter(LocationPydantic.location_id == location_id).first()
    if db_location is None:
        raise HTTPException(status_code=404, detail="Location not found")
    return db_location


@app.put("/locations/{location_id}", response_model=LocationPydantic)
def update_location(location_id: int, location: LocationPydantic, db: Session = Depends(get_db)):
    db_location = db.query(LocationPydantic).filter(LocationPydantic.location_id == location_id).first()
    if db_location is None:
        raise HTTPException(status_code=404, detail="Location not found")
    for field, value in location.dict().items():
        setattr(db_location, field, value)
    db.commit()
    db.refresh(db_location)
    return db_location


@app.delete("/locations/{location_id}", response_model=LocationPydantic)
def delete_location(location_id: int, db: Session = Depends(get_db)):
    db_location = db.query(LocationPydantic).filter(LocationPydantic.location_id == location_id).first()
    if db_location is None:
        raise HTTPException(status_code=404, detail="Location not found")
    db.delete(db_location)
    db.commit()
    return db_location


@app.post("/location_contacts/", response_model=LocationContactPydantic)
def create_location_contact(
    location_id: int, contact_id: int, db: Session = Depends(get_db)
):
    db_location = db.query(LocationPydantic).filter(LocationPydantic.location_id == location_id).first()
    db_contact = db.query(ContactPydantic).filter(ContactPydantic.contact_id == contact_id).first()

    if not db_location or not db_contact:
        raise HTTPException(status_code=404, detail="Location or Contact not found")

    location_contact = LocationContactPydantic(location_id=location_id, contact_id=contact_id)
    db.add(location_contact)
    db.commit()
    db.refresh(location_contact)
    return location_contact


@app.delete("/location_contacts/")
def delete_location_contact(
    location_id: int, contact_id: int, db: Session = Depends(get_db)
):
    
    location_contact = (
        db.query(LocationContactPydantic)
        .filter(
            LocationContactPydantic.location_id == location_id,
            LocationContactPydantic.contact_id == contact_id,
        )
        .first()
    )

    if location_contact is None:
        raise HTTPException(
            status_code=404, detail="Location-Contact relationship not found"
        )

    db.delete(location_contact)
    db.commit()
    return {"detail": "Location-Contact relationship deleted"}


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
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@app.get("/users/", response_model=list[UserPydantic])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(UserPydantic).offset(skip).limit(limit).all()


@app.get("/users/{user_id}", response_model=UserPydantic)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(UserPydantic).filter(UserPydantic.user_id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.put("/users/{user_id}", response_model=UserPydantic)
def update_user(user_id: int, user: UserPydantic, db: Session = Depends(get_db)):
    db_user = db.query(UserPydantic).filter(UserPydantic.user_id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    for field, value in user.dict().items():
        setattr(db_user, field, value)
    db.commit()
    db.refresh(db_user)
    return db_user


@app.delete("/users/{user_id}", response_model=UserPydantic)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(UserPydantic).filter(UserPydantic.user_id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return db_user

@app.post("/user_contacts/", response_model=UserContactPydantic)
def create_user_contact(
    user_id: int, contact_id: int, db: Session = Depends(get_db)
):
    db_user = db.query(UserPydantic).filter(UserPydantic.user_id == user_id).first()
    db_contact = db.query(ContactPydantic).filter(ContactPydantic.contact_id == contact_id).first()

    if not db_user or not db_contact:
        raise HTTPException(status_code=404, detail="User or Contact not found")

    user_contact = UserContactPydantic(user_id=user_id, contact_id=contact_id)
    db.add(user_contact)
    db.commit()
    db.refresh(user_contact)
    return user_contact


@app.delete("/user_contacts/")
def delete_user_contact(
    user_id: int, contact_id: int, db: Session = Depends(get_db)
):
    user_contact = (
        db.query(UserContactPydantic)
        .filter(
            UserContactPydantic.user_id == user_id,
            UserContactPydantic.contact_id == contact_id,
        )
        .first()
    )

    if user_contact is None:
        raise HTTPException(
            status_code=404, detail="User-Contact relationship not found"
        )

    db.delete(user_contact)
    db.commit()
    return {"detail": "User-Contact relationship deleted"}


@app.post("/user_addresses/", response_model=UserAddressPydantic)
def create_user_address(
    user_id: int, address_id: int, db: Session = Depends(get_db)
):
    db_user = db.query(UserPydantic).filter(UserPydantic.user_id == user_id).first()
    db_address = db.query(AddressPydantic).filter(AddressPydantic.address_id == address_id).first()

    if not db_user or not db_address:
        raise HTTPException(status_code=404, detail="User or Address not found")

    user_address = UserAddressPydantic(user_id=user_id, address_id=address_id)
    db.add(user_address)
    db.commit()
    db.refresh(user_address)
    return user_address


@app.delete("/user_addresses/")
def delete_user_address(
    user_id: int, address_id: int, db: Session = Depends(get_db)
):
    user_address = (
        db.query(UserAddressPydantic)
        .filter(
            UserAddressPydantic.user_id == user_id,
            UserAddressPydantic.address_id == address_id,
        )
        .first()
    )

    if user_address is None:
        raise HTTPException(
            status_code=404, detail="User-Address relationship not found"
        )

    db.delete(user_address)
    db.commit()
    return {"detail": "User-Address relationship deleted"}


@app.post("/user_groups/", response_model=UserGroupPydantic)
def create_user_group(user_group: UserGroupPydantic, db: Session = Depends(get_db)):
    db.add(user_group)
    db.commit()
    db.refresh(user_group)
    return user_group


@app.get("/user_groups/", response_model=list[UserGroupPydantic])
def read_user_groups(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(UserGroupPydantic).offset(skip).limit(limit).all()


@app.get("/user_groups/{user_group_id}", response_model=UserGroupPydantic)
def read_user_group(user_group_id: int, db: Session = Depends(get_db)):
    db_user_group = db.query(UserGroupPydantic).filter(UserGroupPydantic.user_group_id == user_group_id).first()
    if db_user_group is None:
        raise HTTPException(status_code=404, detail="User Group not found")
    return db_user_group


@app.put("/user_groups/{user_group_id}", response_model=UserGroupPydantic)
def update_user_group(user_group_id: int, user_group: UserGroupPydantic, db: Session = Depends(get_db)):
    db_user_group = db.query(UserGroupPydantic).filter(UserGroupPydantic.user_group_id == user_group_id).first()
    if db_user_group is None:
        raise HTTPException(status_code=404, detail="User Group not found")
    for field, value in user_group.dict().items():
        setattr(db_user_group, field, value)
    db.commit()
    db.refresh(db_user_group)
    return db_user_group


@app.delete("/user_groups/{user_group_id}", response_model=UserGroupPydantic)
def delete_user_group(user_group_id: int, db: Session = Depends(get_db)):
    db_user_group = db.query(UserGroupPydantic).filter(UserGroupPydantic.user_group_id == user_group_id).first()
    if db_user_group is None:
        raise HTTPException(status_code=404, detail="User Group not found")
    db.delete(db_user_group)
    db.commit()
    return db_user_group



@app.post("/user_roles/", response_model=UserRolePydantic)
def create_user_role(user_role: UserRolePydantic, db: Session = Depends(get_db)):
    db.add(user_role)
    db.commit()
    db.refresh(user_role)
    return user_role


@app.get("/user_roles/", response_model=list[UserRolePydantic])
def read_user_roles(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(UserRolePydantic).offset(skip).limit(limit).all()


@app.get("/user_roles/{role_id}", response_model=UserRolePydantic)
def read_user_role(role_id: int, db: Session = Depends(get_db)):
    db_user_role = db.query(UserRolePydantic).filter(UserRolePydantic.role_id == role_id).first()
    if db_user_role is None:
        raise HTTPException(status_code=404, detail="User Role not found")
    return db_user_role


@app.put("/user_roles/{role_id}", response_model=UserRolePydantic)
def update_user_role(role_id: int, user_role: UserRolePydantic, db: Session = Depends(get_db)):
    db_user_role = db.query(UserRolePydantic).filter(UserRolePydantic.role_id == role_id).first()
    if db_user_role is None:
        raise HTTPException(status_code=404, detail="User Role not found")
    for field, value in user_role.dict().items():
        setattr(db_user_role, field, value)
    db.commit()
    db.refresh(db_user_role)
    return db_user_role


@app.delete("/user_roles/{role_id}", response_model=UserRolePydantic)
def delete_user_role(role_id: int, db: Session = Depends(get_db)):
    db_user_role = db.query(UserRolePydantic).filter(UserRolePydantic.role_id == role_id).first()
    if db_user_role is None:
        raise HTTPException(status_code=404, detail="User Role not found")
    db.delete(db_user_role)
    db.commit()
    return db_user_role


@app.post("/user_group_memberships/", response_model=UserGroupMembershipPydantic)
def create_user_group_membership(
    user_id: int, user_group_id: int, db: Session = Depends(get_db)
):
    db_user = db.query(UserPydantic).filter(UserPydantic.user_id == user_id).first()
    db_user_group = db.query(UserGroupPydantic).filter(UserGroupPydantic.user_group_id == user_group_id).first()

    if not db_user or not db_user_group:
        raise HTTPException(status_code=404, detail="User or User Group not found")

    user_group_membership = UserGroupMembershipPydantic(user_id=user_id, user_group_id=user_group_id)
    db.add(user_group_membership)
    db.commit()
    db.refresh(user_group_membership)
    return user_group_membership


@app.delete("/user_group_memberships/")
def delete_user_group_membership(
    user_id: int, user_group_id: int, db: Session = Depends(get_db)
):
    user_group_membership = (
        db.query(UserGroupMembershipPydantic)
        .filter(
            UserGroupMembershipPydantic.user_id == user_id,
            UserGroupMembershipPydantic.user_group_id == user_group_id,
        )
        .first()
    )

    if user_group_membership is None:
        raise HTTPException(
            status_code=404, detail="User-UserGroup Membership not found"
        )

    db.delete(user_group_membership)
    db.commit()
    return {"detail": "User-UserGroup Membership deleted"}


@app.post("/user_role_assignments/", response_model=UserRoleAssignmentPydantic)
def create_user_role_assignment(
    user_id: int, role_id: int, db: Session = Depends(get_db)
):
    db_user = db.query(UserPydantic).filter(UserPydantic.user_id == user_id).first()
    db_role = db.query(UserRolePydantic).filter(UserRolePydantic.role_id == role_id).first()

    if not db_user or not db_role:
        raise HTTPException(status_code=404, detail="User or UserRole not found")

    user_role_assignment = UserRoleAssignmentPydantic(user_id=user_id, role_id=role_id)
    db.add(user_role_assignment)
    db.commit()
    db.refresh(user_role_assignment)
    return user_role_assignment


@app.delete("/user_role_assignments/")
def delete_user_role_assignment(
    user_id: int, role_id: int, db: Session = Depends(get_db)
):
    user_role_assignment = (
        db.query(UserRoleAssignmentPydantic)
        .filter(
            UserRoleAssignmentPydantic.user_id == user_id,
            UserRoleAssignmentPydantic.role_id == role_id,
        )
        .first()
    )

    if user_role_assignment is None:
        raise HTTPException(
            status_code=404, detail="User-UserRole Assignment not found"
        )

    db.delete(user_role_assignment)
    db.commit()
    return {"detail": "User-UserRole Assignment deleted"}


@app.post("/asset_types/", response_model=AssetTypePydantic)
def create_asset_type(asset_type: AssetTypePydantic, db: Session = Depends(get_db)):
    db.add(asset_type)
    db.commit()
    db.refresh(asset_type)
    return asset_type


@app.get("/asset_types/", response_model=list[AssetTypePydantic])
def read_asset_types(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(AssetTypePydantic).offset(skip).limit(limit).all()


@app.get("/asset_types/{asset_type_id}", response_model=AssetTypePydantic)
def read_asset_type(asset_type_id: int, db: Session = Depends(get_db)):
    db_asset_type = db.query(AssetTypePydantic).filter(AssetTypePydantic.asset_type_id == asset_type_id).first()
    if db_asset_type is None:
        raise HTTPException(status_code=404, detail="Asset Type not found")
    return db_asset_type


@app.put("/asset_types/{asset_type_id}", response_model=AssetTypePydantic)
def update_asset_type(asset_type_id: int, asset_type: AssetTypePydantic, db: Session = Depends(get_db)):
    db_asset_type = db.query(AssetTypePydantic).filter(AssetTypePydantic.asset_type_id == asset_type_id).first()
    if db_asset_type is None:
        raise HTTPException(status_code=404, detail="Asset Type not found")
    for field, value in asset_type.dict().items():
        setattr(db_asset_type, field, value)
    db.commit()
    db.refresh(db_asset_type)
    return db_asset_type


@app.delete("/asset_types/{asset_type_id}", response_model=AssetTypePydantic)
def delete_asset_type(asset_type_id: int, db: Session = Depends(get_db)):
    db_asset_type = db.query(AssetTypePydantic).filter(AssetTypePydantic.asset_type_id == asset_type_id).first()
    if db_asset_type is None:
        raise HTTPException(status_code=404, detail="Asset Type not found")
    db.delete(db_asset_type)
    db.commit()
    return db_asset_type





@app.post("/assets/", response_model=AssetPydantic)
def create_asset(asset: AssetPydantic, db: Session = Depends(get_db)):
    db.add(asset)
    db.commit()
    db.refresh(asset)
    return asset


@app.get("/assets/", response_model=list[AssetPydantic])
def read_assets(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(AssetPydantic).offset(skip).limit(limit).all()


@app.get("/assets/{asset_id}", response_model=AssetPydantic)
def read_asset(asset_id: int, db: Session = Depends(get_db)):
    db_asset = db.query(AssetPydantic).filter(AssetPydantic.asset_id == asset_id).first()
    if db_asset is None:
        raise HTTPException(status_code=404, detail="Asset not found")
    return db_asset


@app.put("/assets/{asset_id}", response_model=AssetPydantic)
def update_asset(asset_id: int, asset: AssetPydantic, db: Session = Depends(get_db)):
    db_asset = db.query(AssetPydantic).filter(AssetPydantic.asset_id == asset_id).first()
    if db_asset is None:
        raise HTTPException(status_code=404, detail="Asset not found")
    for field, value in asset.dict().items():
        setattr(db_asset, field, value)
    db.commit()
    db.refresh(db_asset)
    return db_asset


@app.delete("/assets/{asset_id}", response_model=AssetPydantic)
def delete_asset(asset_id: int, db: Session = Depends(get_db)):
    db_asset = db.query(AssetPydantic).filter(AssetPydantic.asset_id == asset_id).first()
    if db_asset is None:
        raise HTTPException(status_code=404, detail="Asset not found")
    db.delete(db_asset)
    db.commit()
    return db_asset


@app.post("/rights/", response_model=RightPydantic)
def create_right(right: RightPydantic, db: Session = Depends(get_db)):
    db.add(right)
    db.commit()
    db.refresh(right)
    return right


@app.get("/rights/", response_model=list[RightPydantic])
def read_rights(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(RightPydantic).offset(skip).limit(limit).all()


@app.get("/rights/{right_id}", response_model=RightPydantic)
def read_right(right_id: int, db: Session = Depends(get_db)):
    db_right = db.query(RightPydantic).filter(RightPydantic.right_id == right_id).first()
    if db_right is None:
        raise HTTPException(status_code=404, detail="Right not found")
    return db_right


@app.put("/rights/{right_id}", response_model=RightPydantic)
def update_right(right_id: int, right: RightPydantic, db: Session = Depends(get_db)):
    db_right = db.query(RightPydantic).filter(RightPydantic.right_id == right_id).first()
    if db_right is None:
        raise HTTPException(status_code=404, detail="Right not found")
    for field, value in right.dict().items():
        setattr(db_right, field, value)
    db.commit()
    db.refresh(db_right)
    return db_right


@app.delete("/rights/{right_id}", response_model=RightPydantic)
def delete_right(right_id: int, db: Session = Depends(get_db)):
    db_right = db.query(RightPydantic).filter(RightPydantic.right_id == right_id).first()
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

    user_right = UserRightPydantic(user_id=user_id, right_id=right_id)
    db.add(user_right)
    db.commit()
    db.refresh(user_right)
    return user_right


@app.delete("/user_rights/")
def delete_user_right(
    user_id: int, right_id: int, db: Session = Depends(get_db)
):
    user_right = (
        db.query(UserRightPydantic)
        .filter(
            UserRightPydantic.user_id == user_id,
            UserRightPydantic.right_id == right_id,
        )
        .first()
    )

    if user_right is None:
        raise HTTPException(
            status_code=404, detail="User-Right Relationship not found"
        )

    db.delete(user_right)
    db.commit()
    return {"detail": "User-Right Relationship deleted"}




@app.post("/role_rights/", response_model=RoleRightPydantic)
def create_role_right(
    role_id: int, right_id: int, db: Session = Depends(get_db)
):
    db_role = db.query(UserRolePydantic).filter(UserRolePydantic.role_id == role_id).first()
    db_right = db.query(RightPydantic).filter(RightPydantic.right_id == right_id).first()

    if not db_role or not db_right:
        raise HTTPException(status_code=404, detail="Role or Right not found")

    role_right = RoleRightPydantic(role_id=role_id, right_id=right_id)
    db.add(role_right)
    db.commit()
    db.refresh(role_right)
    return role_right


@app.delete("/role_rights/")
def delete_role_right(
    role_id: int, right_id: int, db: Session = Depends(get_db)
):
    role_right = (
        db.query(RoleRightPydantic)
        .filter(
            RoleRightPydantic.role_id == role_id,
            RoleRightPydantic.right_id == right_id,
        )
        .first()
    )

    if role_right is None:
        raise HTTPException(
            status_code=404, detail="Role-Right Relationship not found"
        )

    db.delete(role_right)
    db.commit()
    return {"detail": "Role-Right Relationship deleted"}



@app.post("/tags/", response_model=TagPydantic)
def create_tag(tag: TagPydantic, db: Session = Depends(get_db)):
    db.add(tag)
    db.commit()
    db.refresh(tag)
    return tag


@app.get("/tags/", response_model=list[TagPydantic])
def read_tags(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(TagPydantic).offset(skip).limit(limit).all()


@app.get("/tags/{tag_id}", response_model=TagPydantic)
def read_tag(tag_id: int, db: Session = Depends(get_db)):
    db_tag = db.query(TagPydantic).filter(TagPydantic.tag_id == tag_id).first()
    if db_tag is None:
        raise HTTPException(status_code=404, detail="Tag not found")
    return db_tag


@app.put("/tags/{tag_id}", response_model=TagPydantic)
def update_tag(tag_id: int, tag: TagPydantic, db: Session = Depends(get_db)):
    db_tag = db.query(TagPydantic).filter(TagPydantic.tag_id == tag_id).first()
    if db_tag is None:
        raise HTTPException(status_code=404, detail="Tag not found")
    for field, value in tag.dict().items():
        setattr(db_tag, field, value)
    db.commit()
    db.refresh(db_tag)
    return db_tag


@app.delete("/tags/{tag_id}", response_model=TagPydantic)
def delete_tag(tag_id: int, db: Session = Depends(get_db)):
    db_tag = db.query(TagPydantic).filter(TagPydantic.tag_id == tag_id).first()
    if db_tag is None:
        raise HTTPException(status_code=404, detail="Tag not found")
    db.delete(db_tag)
    db.commit()
    return db_tag


@app.post("/device_types/", response_model=DeviceTypePydantic)
def create_device_type(device_type: DeviceTypePydantic, db: Session = Depends(get_db)):
    db.add(device_type)
    db.commit()
    db.refresh(device_type)
    return device_type


@app.get("/device_types/", response_model=list[DeviceTypePydantic])
def read_device_types(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(DeviceTypePydantic).offset(skip).limit(limit).all()


@app.get("/device_types/{device_type_id}", response_model=DeviceTypePydantic)
def read_device_type(device_type_id: int, db: Session = Depends(get_db)):
    db_device_type = db.query(DeviceTypePydantic).filter(DeviceTypePydantic.device_type_id == device_type_id).first()
    if db_device_type is None:
        raise HTTPException(status_code=404, detail="Device Type not found")
    return db_device_type


@app.put("/device_types/{device_type_id}", response_model=DeviceTypePydantic)
def update_device_type(device_type_id: int, device_type: DeviceTypePydantic, db: Session = Depends(get_db)):
    db_device_type = db.query(DeviceTypePydantic).filter(DeviceTypePydantic.device_type_id == device_type_id).first()
    if db_device_type is None:
        raise HTTPException(status_code=404, detail="Device Type not found")
    for field, value in device_type.dict().items():
        setattr(db_device_type, field, value)
    db.commit()
    db.refresh(db_device_type)
    return db_device_type


@app.delete("/device_types/{device_type_id}", response_model=DeviceTypePydantic)
def delete_device_type(device_type_id: int, db: Session = Depends(get_db)):
    db_device_type = db.query(DeviceTypePydantic).filter(DeviceTypePydantic.device_type_id == device_type_id).first()
    if db_device_type is None:
        raise HTTPException(status_code=404, detail="Device Type not found")
    db.delete(db_device_type)
    db.commit()
    return db_device_type


@app.post("/devices/", response_model=DevicePydantic)
def create_device(device: DevicePydantic, db: Session = Depends(get_db)):
    db.add(device)
    db.commit()
    db.refresh(device)
    return device


@app.get("/devices/", response_model=list[DevicePydantic])
def read_devices(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(DevicePydantic).offset(skip).limit(limit).all()


@app.get("/devices/{device_id}", response_model=DevicePydantic)
def read_device(device_id: int, db: Session = Depends(get_db)):
    db_device = db.query(DevicePydantic).filter(DevicePydantic.device_id == device_id).first()
    if db_device is None:
        raise HTTPException(status_code=404, detail="Device not found")
    return db_device


@app.put("/devices/{device_id}", response_model=DevicePydantic)
def update_device(device_id: int, device: DevicePydantic, db: Session = Depends(get_db)):
    db_device = db.query(DevicePydantic).filter(DevicePydantic.device_id == device_id).first()
    if db_device is None:
        raise HTTPException(status_code=404, detail="Device not found")
    for field, value in device.dict().items():
        setattr(db_device, field, value)
    db.commit()
    db.refresh(db_device)
    return db_device


@app.delete("/devices/{device_id}", response_model=DevicePydantic)
def delete_device(device_id: int, db: Session = Depends(get_db)):
    db_device = db.query(DevicePydantic).filter(DevicePydantic.device_id == device_id).first()
    if db_device is None:
        raise HTTPException(status_code=404, detail="Device not found")
    db.delete(db_device)
    db.commit()
    return db_device



@app.post("/device_tags/", response_model=DeviceTagPydantic)
def create_device_tag(
    device_id: int, tag_id: int, db: Session = Depends(get_db)
):
    db_device = db.query(DevicePydantic).filter(DevicePydantic.device_id == device_id).first()
    db_tag = db.query(TagPydantic).filter(TagPydantic.tag_id == tag_id).first()

    if not db_device or not db_tag:
        raise HTTPException(status_code=404, detail="Device or Tag not found")

    device_tag = DeviceTagPydantic(device_id=device_id, tag_id=tag_id)
    db.add(device_tag)
    db.commit()
    db.refresh(device_tag)
    return device_tag


@app.delete("/device_tags/")
def delete_device_tag(
    device_id: int, tag_id: int, db: Session = Depends(get_db)
):
    device_tag = (
        db.query(DeviceTagPydantic)
        .filter(
            DeviceTagPydantic.device_id == device_id,
            DeviceTagPydantic.tag_id == tag_id,
        )
        .first()
    )

    if device_tag is None:
        raise HTTPException(
            status_code=404, detail="Device-Tag Relationship not found"
        )

    db.delete(device_tag)
    db.commit()
    return {"detail": "Device-Tag Relationship deleted"}



@app.post("/connection_types/", response_model=ConnectionTypePydantic)
def create_connection_type(connection_type: ConnectionTypePydantic, db: Session = Depends(get_db)):
    db.add(connection_type)
    db.commit()
    db.refresh(connection_type)
    return connection_type


@app.get("/connection_types/", response_model=list[ConnectionTypePydantic])
def read_connection_types(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(ConnectionTypePydantic).offset(skip).limit(limit).all()


@app.get("/connection_types/{connection_type_id}", response_model=ConnectionTypePydantic)
def read_connection_type(connection_type_id: int, db: Session = Depends(get_db)):
    db_connection_type = db.query(ConnectionTypePydantic).filter(ConnectionTypePydantic.connection_type_id == connection_type_id).first()
    if db_connection_type is None:
        raise HTTPException(status_code=404, detail="Connection Type not found")
    return db_connection_type


@app.put("/connection_types/{connection_type_id}", response_model=ConnectionTypePydantic)
def update_connection_type(connection_type_id: int, connection_type: ConnectionTypePydantic, db: Session = Depends(get_db)):
    db_connection_type = db.query(ConnectionTypePydantic).filter(ConnectionTypePydantic.connection_type_id == connection_type_id).first()
    if db_connection_type is None:
        raise HTTPException(status_code=404, detail="Connection Type not found")
    for field, value in connection_type.dict().items():
        setattr(db_connection_type, field, value)
    db.commit()
    db.refresh(db_connection_type)
    return db_connection_type


@app.delete("/connection_types/{connection_type_id}", response_model=ConnectionTypePydantic)
def delete_connection_type(connection_type_id: int, db: Session = Depends(get_db)):
    db_connection_type = db.query(ConnectionTypePydantic).filter(ConnectionTypePydantic.connection_type_id == connection_type_id).first()
    if db_connection_type is None:
        raise HTTPException(status_code=404, detail="Connection Type not found")
    db.delete(db_connection_type)
    db.commit()
    return db_connection_type



@app.post("/connections/", response_model=ConnectionPydantic)
def create_connection(connection: ConnectionPydantic, db: Session = Depends(get_db)):
    db.add(connection)
    db.commit()
    db.refresh(connection)
    return connection


@app.get("/connections/", response_model=list[ConnectionPydantic])
def read_connections(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(ConnectionPydantic).offset(skip).limit(limit).all()


@app.get("/connections/{connection_id}", response_model=ConnectionPydantic)
def read_connection(connection_id: int, db: Session = Depends(get_db)):
    db_connection = db.query(ConnectionPydantic).filter(ConnectionPydantic.connection_id == connection_id).first()
    if db_connection is None:
        raise HTTPException(status_code=404, detail="Connection not found")
    return db_connection


@app.put("/connections/{connection_id}", response_model=ConnectionPydantic)
def update_connection(connection_id: int, connection: ConnectionPydantic, db: Session = Depends(get_db)):
    db_connection = db.query(ConnectionPydantic).filter(ConnectionPydantic.connection_id == connection_id).first()
    if db_connection is None:
        raise HTTPException(status_code=404, detail="Connection not found")
    for field, value in connection.dict().items():
        setattr(db_connection, field, value)
    db.commit()
    db.refresh(db_connection)
    return db_connection


@app.delete("/connections/{connection_id}", response_model=ConnectionPydantic)
def delete_connection(connection_id: int, db: Session = Depends(get_db)):
    db_connection = db.query(ConnectionPydantic).filter(ConnectionPydantic.connection_id == connection_id).first()
    if db_connection is None:
        raise HTTPException(status_code=404, detail="Connection not found")
    db.delete(db_connection)
    db.commit()
    return db_connection





@app.post("/connection_details/", response_model=ConnectionDetailPydantic)
def create_connection_detail(connection_detail: ConnectionDetailPydantic, db: Session = Depends(get_db)):
    db.add(connection_detail)
    db.commit()
    db.refresh(connection_detail)
    return connection_detail


@app.get("/connection_details/", response_model=list[ConnectionDetailPydantic])
def read_connection_details(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(ConnectionDetailPydantic).offset(skip).limit(limit).all()


@app.get("/connection_details/{connection_detail_id}", response_model=ConnectionDetailPydantic)
def read_connection_detail(connection_detail_id: int, db: Session = Depends(get_db)):
    db_connection_detail = db.query(ConnectionDetailPydantic).filter(ConnectionDetailPydantic.connection_detail_id == connection_detail_id).first()
    if db_connection_detail is None:
        raise HTTPException(status_code=404, detail="Connection Detail not found")
    return db_connection_detail


@app.put("/connection_details/{connection_detail_id}", response_model=ConnectionDetailPydantic)
def update_connection_detail(connection_detail_id: int, connection_detail: ConnectionDetailPydantic, db: Session = Depends(get_db)):
    db_connection_detail = db.query(ConnectionDetailPydantic).filter(ConnectionDetailPydantic.connection_detail_id == connection_detail_id).first()
    if db_connection_detail is None:
        raise HTTPException(status_code=404, detail="Connection Detail not found")
    for field, value in connection_detail.dict().items():
        setattr(db_connection_detail, field, value)
    db.commit()
    db.refresh(db_connection_detail)
    return db_connection_detail


@app.delete("/connection_details/{connection_detail_id}", response_model=ConnectionDetailPydantic)
def delete_connection_detail(connection_detail_id: int, db: Session = Depends(get_db)):
    db_connection_detail = db.query(ConnectionDetailPydantic).filter(ConnectionDetailPydantic.connection_detail_id == connection_detail_id).first()
    if db_connection_detail is None:
        raise HTTPException(status_code=404, detail="Connection Detail not found")
    db.delete(db_connection_detail)
    db.commit()
    return db_connection_detail


@app.post("/user_log_history/", response_model=UserLogHistoryPydantic)
def create_user_log_history(user_log_history: UserLogHistoryPydantic, db: Session = Depends(get_db)):
    db.add(user_log_history)
    db.commit()
    db.refresh(user_log_history)
    return user_log_history


@app.get("/user_log_history/", response_model=list[UserLogHistoryPydantic])
def read_user_log_history(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(UserLogHistoryPydantic).offset(skip).limit(limit).all()


@app.get("/user_log_history/{log_id}", response_model=UserLogHistoryPydantic)
def read_user_log_by_id(log_id: int, db: Session = Depends(get_db)):
    db_user_log = db.query(UserLogHistoryPydantic).filter(UserLogHistoryPydantic.log_id == log_id).first()
    if db_user_log is None:
        raise HTTPException(status_code=404, detail="User Log not found")
    return db_user_log


@app.put("/user_log_history/{log_id}", response_model=UserLogHistoryPydantic)
def update_user_log_history(log_id: int, user_log_history: UserLogHistoryPydantic, db: Session = Depends(get_db)):
    db_user_log = db.query(UserLogHistoryPydantic).filter(UserLogHistoryPydantic.log_id == log_id).first()
    if db_user_log is None:
        raise HTTPException(status_code=404, detail="User Log not found")
    for field, value in user_log_history.dict().items():
        setattr(db_user_log, field, value)
    db.commit()
    db.refresh(db_user_log)
    return db_user_log


@app.delete("/user_log_history/{log_id}", response_model=UserLogHistoryPydantic)
def delete_user_log_history(log_id: int, db: Session = Depends(get_db)):
    db_user_log = db.query(UserLogHistoryPydantic).filter(UserLogHistoryPydantic.log_id == log_id).first()
    if db_user_log is None:
        raise HTTPException(status_code=404, detail="User Log not found")
    db.delete(db_user_log)
    db.commit()
    return db_user_log


    

@app.post("/alerts/", response_model=AlertPydantic)
def create_alert(alert: AlertPydantic, db: Session = Depends(get_db)):
    db.add(alert)
    db.commit()
    db.refresh(alert)
    return alert


@app.get("/alerts/", response_model=list[AlertPydantic])
def read_alerts(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(AlertPydantic).offset(skip).limit(limit).all()


@app.get("/alerts/{alert_id}", response_model=AlertPydantic)
def read_alert(alert_id: int, db: Session = Depends(get_db)):
    db_alert = db.query(AlertPydantic).filter(AlertPydantic.alert_id == alert_id).first()
    if db_alert is None:
        raise HTTPException(status_code=404, detail="Alert not found")
    return db_alert


@app.put("/alerts/{alert_id}", response_model=AlertPydantic)
def update_alert(alert_id: int, alert: AlertPydantic, db: Session = Depends(get_db)):
    db_alert = db.query(AlertPydantic).filter(AlertPydantic.alert_id == alert_id).first()
    if db_alert is None:
        raise HTTPException(status_code=404, detail="Alert not found")
    for field, value in alert.dict().items():
        setattr(db_alert, field, value)
    db.commit()
    db.refresh(db_alert)
    return db_alert


@app.delete("/alerts/{alert_id}", response_model=AlertPydantic)
def delete_alert(alert_id: int, db: Session = Depends(get_db)):
    db_alert = db.query(AlertPydantic).filter(AlertPydantic.alert_id == alert_id).first()
    if db_alert is None:
        raise HTTPException(status_code=404, detail="Alert not found")
    db.delete(db_alert)
    db.commit()
    return db_alert



@app.post("/alert_expressions/", response_model=AlertExpressionPydantic)
def create_alert_expression(alert_expression: AlertExpressionPydantic, db: Session = Depends(get_db)):
    db.add(alert_expression)
    db.commit()
    db.refresh(alert_expression)
    return alert_expression


@app.get("/alert_expressions/", response_model=list[AlertExpressionPydantic])
def read_alert_expressions(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(AlertExpressionPydantic).offset(skip).limit(limit).all()


@app.get("/alert_expressions/{expression_id}", response_model=AlertExpressionPydantic)
def read_alert_expression(expression_id: int, db: Session = Depends(get_db)):
    db_alert_expression = db.query(AlertExpressionPydantic).filter(AlertExpressionPydantic.expression_id == expression_id).first()
    if db_alert_expression is None:
        raise HTTPException(status_code=404, detail="Alert Expression not found")
    return db_alert_expression


@app.put("/alert_expressions/{expression_id}", response_model=AlertExpressionPydantic)
def update_alert_expression(expression_id: int, alert_expression: AlertExpressionPydantic, db: Session = Depends(get_db)):
    db_alert_expression = db.query(AlertExpressionPydantic).filter(AlertExpressionPydantic.expression_id == expression_id).first()
    if db_alert_expression is None:
        raise HTTPException(status_code=404, detail="Alert Expression not found")
    for field, value in alert_expression.dict().items():
        setattr(db_alert_expression, field, value)
    db.commit()
    db.refresh(db_alert_expression)
    return db_alert_expression


@app.delete("/alert_expressions/{expression_id}", response_model=AlertExpressionPydantic)
def delete_alert_expression(expression_id: int, db: Session = Depends(get_db)):
    db_alert_expression = db.query(AlertExpressionPydantic).filter(AlertExpressionPydantic.expression_id == expression_id).first()
    if db_alert_expression is None:
        raise HTTPException(status_code=404, detail="Alert Expression not found")
    db.delete(db_alert_expression)
    db.commit()
    return db_alert_expression




@app.post("/history/", response_model=HistoryPydantic)
def create_history(history: HistoryPydantic, db: Session = Depends(get_db)):
    db.add(history)
    db.commit()
    db.refresh(history)
    return history


@app.get("/history/", response_model=list[HistoryPydantic])
def read_history(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(History).offset(skip).limit(limit).all()


@app.get("/history/{history_id}", response_model=HistoryPydantic)
def read_history_by_id(history_id: int, db: Session = Depends(get_db)):
    db_history = db.query(HistoryPydantic).filter(HistoryPydantic.history_id == history_id).first()
    if db_history is None:
        raise HTTPException(status_code=404, detail="History not found")
    return db_history


@app.put("/history/{history_id}", response_model=HistoryPydantic)
def update_history(history_id: int, history: HistoryPydantic, db: Session = Depends(get_db)):
    db_history = db.query(HistoryPydantic).filter(HistoryPydantic.history_id == history_id).first()
    if db_history is None:
        raise HTTPException(status_code=404, detail="History not found")
    for field, value in history.dict().items():
        setattr(db_history, field, value)
    db.commit()
    db.refresh(db_history)
    return db_history


@app.delete("/history/{history_id}", response_model=HistoryPydantic)
def delete_history(history_id: int, db: Session = Depends(get_db)):
    db_history = db.query(HistoryPydantic).filter(HistoryPydantic.history_id == history_id).first()
    if db_history is None:
        raise HTTPException(status_code=404, detail="History not found")
    db.delete(db_history)
    db.commit()
    return db_history


@app.post("/action_types/", response_model=ActionTypePydantic)
def create_action_type(action_type: ActionTypePydantic, db: Session = Depends(get_db)):
    db.add(action_type)
    db.commit()
    db.refresh(action_type)
    return action_type


@app.get("/action_types/", response_model=list[ActionTypePydantic])
def read_action_types(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(ActionTypePydantic).offset(skip).limit(limit).all()


@app.get("/action_types/{action_type_id}", response_model=ActionTypePydantic)
def read_action_type(action_type_id: int, db: Session = Depends(get_db)):
    db_action_type = db.query(ActionTypePydantic).filter(ActionTypePydantic.action_type_id == action_type_id).first()
    if db_action_type is None:
        raise HTTPException(status_code=404, detail="Action Type not found")
    return db_action_type


@app.put("/action_types/{action_type_id}", response_model=ActionTypePydantic)
def update_action_type(action_type_id: int, action_type: ActionTypePydantic, db: Session = Depends(get_db)):
    db_action_type = db.query(ActionTypePydantic).filter(ActionTypePydantic.action_type_id == action_type_id).first()
    if db_action_type is None:
        raise HTTPException(status_code=404, detail="Action Type not found")
    for field, value in action_type.dict().items():
        setattr(db_action_type, field, value)
    db.commit()
    db.refresh(db_action_type)
    return db_action_type


@app.delete("/action_types/{action_type_id}", response_model=ActionTypePydantic)
def delete_action_type(action_type_id: int, db: Session = Depends(get_db)):
    db_action_type = db.query(ActionTypePydantic).filter(ActionTypePydantic.action_type_id == action_type_id).first()
    if db_action_type is None:
        raise HTTPException(status_code=404, detail="Action Type not found")
    db.delete(db_action_type)
    db.commit()
    return db_action_type




@app.post("/actions/", response_model=ActionPydantic)
def create_action(action: ActionPydantic, db: Session = Depends(get_db)):
    db.add(action)
    db.commit()
    db.refresh(action)
    return action


@app.get("/actions/", response_model=list[ActionPydantic])
def read_actions(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(ActionPydantic).offset(skip).limit(limit).all()


@app.get("/actions/{action_id}", response_model=ActionPydantic)
def read_action(action_id: int, db: Session = Depends(get_db)):
    db_action = db.query(ActionPydantic).filter(ActionPydantic.action_id == action_id).first()
    if db_action is None:
        raise HTTPException(status_code=404, detail="Action not found")
    return db_action


@app.put("/actions/{action_id}", response_model=ActionPydantic)
def update_action(action_id: int, action: ActionPydantic, db: Session = Depends(get_db)):
    db_action = db.query(ActionPydantic).filter(ActionPydantic.action_id == action_id).first()
    if db_action is None:
        raise HTTPException(status_code=404, detail="Action not found")
    for field, value in action.dict().items():
        setattr(db_action, field, value)
    db.commit()
    db.refresh(db_action)
    return db_action


@app.delete("/actions/{action_id}", response_model=ActionPydantic)
def delete_action(action_id: int, db: Session = Depends(get_db)):
    db_action = db.query(ActionPydantic).filter(ActionPydantic.action_id == action_id).first()
    if db_action is None:
        raise HTTPException(status_code=404, detail="Action not found")
    db.delete(db_action)
    db.commit()
    return db_action


@app.post("/action_history/")
def create_action_history(action_id: int, history_id: int, db: Session = Depends(get_db)):
    action = db.query(ActionPydantic).filter(ActionPydantic.action_id == action_id).first()
    history = db.query(HistoryPydantic).filter(HistoryPydantic.history_id == history_id).first()
    if action is None or history is None:
        raise HTTPException(status_code=404, detail="Action or History not found")

    # Check if the association already exists
    existing_association = (
        db.query(ActionHistoryPydantic)
        .filter(ActionHistoryPydantic.action_id == action_id, ActionHistoryPydantic.history_id == history_id)
        .first()
    )
    if existing_association:
        raise HTTPException(status_code=400, detail="Association already exists")

    new_association = ActionHistoryPydantic(action_id=action_id, history_id=history_id)
    db.add(new_association)
    db.commit()
    return {"message": "Association created successfully"}


@app.delete("/action_history/")
def delete_action_history(action_id: int, history_id: int, db: Session = Depends(get_db)):
    association = (
        db.query(ActionHistoryPydantic)
        .filter(ActionHistoryPydantic.action_id == action_id, ActionHistoryPydantic.history_id == history_id)
        .first()
    )
    if association is None:
        raise HTTPException(status_code=404, detail="Association not found")

    db.delete(association)
    db.commit()
    return {"message": "Association deleted successfully"}



@app.post("/action_alert/")
def create_action_alert(action_id: int, alert_id: int, db: Session = Depends(get_db)):
    action = db.query(ActionPydantic).filter(ActionPydantic.action_id == action_id).first()
    alert = db.query(AlertPydantic).filter(AlertPydantic.alert_id == alert_id).first()
    if action is None or alert is None:
        raise HTTPException(status_code=404, detail="Action or Alert not found")

    # Check if the association already exists
    existing_association = (
        db.query(ActionAlertPydantic)
        .filter(ActionAlertPydantic.action_id == action_id, ActionAlertPydantic.alert_id == alert_id)
        .first()
    )
    if existing_association:
        raise HTTPException(status_code=400, detail="Association already exists")

    new_association = ActionAlertPydantic(action_id=action_id, alert_id=alert_id)
    db.add(new_association)
    db.commit()
    return {"message": "Association created successfully"}


@app.delete("/action_alert/")
def delete_action_alert(action_id: int, alert_id: int, db: Session = Depends(get_db)):
    association = (
        db.query(ActionAlertPydantic)
        .filter(ActionAlertPydantic.action_id == action_id, ActionAlertPydantic.alert_id == alert_id)
        .first()
    )
    if association is None:
        raise HTTPException(status_code=404, detail="Association not found")

    db.delete(association)
    db.commit()
    return {"message": "Association deleted successfully"}
    
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
        .subquery("subq_alias")
    )

    query = (
        db.query(
            subq.c.row_number,
            subq.c.recorded_date_time,
            Device.device_id,
            Device.device_serial_number,
            Tag.description.label("tag_description"),
            History.value.label("tag_value")
        )
        .join(DeviceTag, DeviceTag.tag_id == subq.c.device_tag_id)
        .join(Tag, DeviceTag.tag_id == Tag.tag_id)
        .join(Device, DeviceTag.device_id == Device.device_id)
        .join(subq, subq.c.device_tag_id == History.device_tag_id)
        .filter(Device.is_active == True)
        .filter(subq.c.row_number == 1)
        .order_by(subq.c.recorded_date_time.desc())
        .all()
    )

    result = {}
    for _, device_id, device_serial_number, tag_description, tag_value in query:
        if device_id not in result:
            result[device_id] = {'device_serial_number': device_serial_number, 'tags': []}

        tag_info = {'description': tag_description, 'value': tag_value}
        result[device_id]['tags'].append(tag_info)

    return result

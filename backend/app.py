import sqlite3


# Establish a database connection
conn = sqlite3.connect('your_database.db')
cursor = conn.cursor()

# CREATE (Insert) operation for ADDRESSES table
def create_address(address_id, address_line1, address_line2, city, state, postal_code, country, latitude, longitude, created_by, created_at, updated_by, updated_at):
    cursor.execute("INSERT INTO ADDRESSES VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                   (address_id, address_line1, address_line2, city, state, postal_code, country, latitude, longitude, created_by, created_at, updated_by, updated_at))
    conn.commit()

# READ (Select) operation for ADDRESSES table
def read_address(address_id):
    cursor.execute("SELECT * FROM ADDRESSES WHERE address_id=?", (address_id,))
    return cursor.fetchone()

# UPDATE operation for ADDRESSES table
def update_address(address_id, new_address_line1):
    cursor.execute("UPDATE ADDRESSES SET address_line1=? WHERE address_id=?", (new_address_line1, address_id))
    conn.commit()

# DELETE operation for ADDRESSES table
def delete_address(address_id):
    cursor.execute("DELETE FROM ADDRESSES WHERE address_id=?", (address_id,))
    conn.commit()


# CREATE (Insert) operation for CONTACT_TYPES table
def create_contact_type(contact_type_id, description, created_by, created_at, updated_by, updated_at):
    cursor.execute("INSERT INTO CONTACT_TYPES VALUES (?, ?, ?, ?, ?, ?)",
                   (contact_type_id, description, created_by, created_at, updated_by, updated_at))
    conn.commit()

# READ (Select) operation for CONTACT_TYPES table
def read_contact_type(contact_type_id):
    cursor.execute("SELECT * FROM CONTACT_TYPES WHERE contact_type_id=?", (contact_type_id,))
    return cursor.fetchone()

# UPDATE operation for CONTACT_TYPES table
def update_contact_type(contact_type_id, new_description):
    cursor.execute("UPDATE CONTACT_TYPES SET description=? WHERE contact_type_id=?", (new_description, contact_type_id))
    conn.commit()

# DELETE operation for CONTACT_TYPES table
def delete_contact_type(contact_type_id):
    cursor.execute("DELETE FROM CONTACT_TYPES WHERE contact_type_id=?", (contact_type_id,))
    conn.commit()

# CREATE (Insert) operation for CONTACTS table
def create_contact(contact_id, contact_description, contact_type_id, created_by, created_at, updated_by, updated_at):
    cursor.execute("INSERT INTO CONTACTS VALUES (?, ?, ?, ?, ?, ?, ?)",
                   (contact_id, contact_description, contact_type_id, created_by, created_at, updated_by, updated_at))
    conn.commit()

# READ (Select) operation for CONTACTS table
def read_contact(contact_id):
    cursor.execute("SELECT * FROM CONTACTS WHERE contact_id=?", (contact_id,))
    return cursor.fetchone()

# UPDATE operation for CONTACTS table
def update_contact(contact_id, new_description):
    cursor.execute("UPDATE CONTACTS SET contact_description=? WHERE contact_id=?", (new_description, contact_id))
    conn.commit()

# DELETE operation for CONTACTS table
def delete_contact(contact_id):
    cursor.execute("DELETE FROM CONTACTS WHERE contact_id=?", (contact_id,))
    conn.commit()




# CREATE (Insert) operation for LOCATIONS table
def create_location(location_id, location_name, location_desc, location_type_id, location_root, latitude, longitude, address_id, contact_id, created_by, created_at, updated_by, updated_at):
    cursor.execute("INSERT INTO LOCATIONS VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                   (location_id, location_name, location_desc, location_type_id, location_root, latitude, longitude, address_id, contact_id, created_by, created_at, updated_by, updated_at))
    conn.commit()

# READ (Select) operation for LOCATIONS table
def read_location(location_id):
    cursor.execute("SELECT * FROM LOCATIONS WHERE location_id=?", (location_id,))
    return cursor.fetchone()

# UPDATE operation for LOCATIONS table
def update_location(location_id, new_location_name):
    cursor.execute("UPDATE LOCATIONS SET location_name=? WHERE location_id=?", (new_location_name, location_id))
    conn.commit()

# DELETE operation for LOCATIONS table
def delete_location(location_id):
    cursor.execute("DELETE FROM LOCATIONS WHERE location_id=?", (location_id,))
    conn.commit()

# CREATE (Insert) operation for LOCATION_CONTACTS table
def create_location_contact(location_id, contact_id):
    cursor.execute("INSERT INTO LOCATION_CONTACTS (location_id, contact_id) VALUES (?, ?)",
                   (location_id, contact_id))
    conn.commit()

# READ (Select) operation for LOCATION_CONTACTS table
def read_location_contact(location_id, contact_id):
    cursor.execute("SELECT * FROM LOCATION_CONTACTS WHERE location_id=? AND contact_id=?", (location_id, contact_id))
    return cursor.fetchone()

# UPDATE operation for LOCATION_CONTACTS table
def update_location_contact(location_id, contact_id, new_location_id, new_contact_id):
    cursor.execute("UPDATE LOCATION_CONTACTS SET location_id=?, contact_id=? WHERE location_id=? AND contact_id=?",
                   (new_location_id, new_contact_id, location_id, contact_id))
    conn.commit()

# DELETE operation for LOCATION_CONTACTS table
def delete_location_contact(location_id, contact_id):
    cursor.execute("DELETE FROM LOCATION_CONTACTS WHERE location_id=? AND contact_id=?", (location_id, contact_id))
    conn.commit()

# CREATE (Insert) operation for LOCATION_ADDRESSES table
def create_location_address(location_id, address_id):
    cursor.execute("INSERT INTO LOCATION_ADDRESSES (location_id, address_id) VALUES (?, ?)",
                   (location_id, address_id))
    conn.commit()

# READ (Select) operation for LOCATION_ADDRESSES table
def read_location_address(location_id, address_id):
    cursor.execute("SELECT * FROM LOCATION_ADDRESSES WHERE location_id=? AND address_id=?", (location_id, address_id))
    return cursor.fetchone()

# UPDATE operation for LOCATION_ADDRESSES table
def update_location_address(location_id, address_id, new_location_id, new_address_id):
    cursor.execute("UPDATE LOCATION_ADDRESSES SET location_id=?, address_id=? WHERE location_id=? AND address_id=?",
                   (new_location_id, new_address_id, location_id, address_id))
    conn.commit()

# DELETE operation for LOCATION_ADDRESSES table
def delete_location_address(location_id, address_id):
    cursor.execute("DELETE FROM LOCATION_ADDRESSES WHERE location_id=? AND address_id=?", (location_id, address_id))
    conn.commit()

# CREATE (Insert) operation for USERS table
def create_user(user_id, email, hex_password, contact_id, address_id, is_active, is_verified, created_by, created_at, updated_by, updated_at):
    cursor.execute("INSERT INTO USERS (user_id, email, hex_password, contact_id, address_id, is_active, is_verified, created_by, created_at, updated_by, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                   (user_id, email, hex_password, contact_id, address_id, is_active, is_verified, created_by, created_at, updated_by, updated_at))
    conn.commit()

# READ (Select) operation for USERS table
def read_user(user_id):
    cursor.execute("SELECT * FROM USERS WHERE user_id=?", (user_id,))
    return cursor.fetchone()

# UPDATE operation for USERS table
def update_user(user_id, new_email, new_hex_password, new_contact_id, new_address_id, new_is_active, new_is_verified, new_updated_by, new_updated_at):
    cursor.execute("UPDATE USERS SET email=?, hex_password=?, contact_id=?, address_id=?, is_active=?, is_verified=?, updated_by=?, updated_at=? WHERE user_id=?",
                   (new_email, new_hex_password, new_contact_id, new_address_id, new_is_active, new_is_verified, new_updated_by, new_updated_at, user_id))
    conn.commit()

# DELETE operation for USERS table
def delete_user(user_id):
    cursor.execute("DELETE FROM USERS WHERE user_id=?", (user_id,))
    conn.commit()

# CREATE (Insert) operation for USER_CONTACTS table
def create_user_contact(user_id, contact_id):
    cursor.execute("INSERT INTO USER_CONTACTS (user_id, contact_id) VALUES (?, ?)",
                   (user_id, contact_id))
    conn.commit()

# READ (Select) operation for USER_CONTACTS table
def read_user_contact(user_id, contact_id):
    cursor.execute("SELECT * FROM USER_CONTACTS WHERE user_id=? AND contact_id=?", (user_id, contact_id))
    return cursor.fetchone()

# UPDATE operation for USER_CONTACTS table
def update_user_contact(user_id, contact_id, new_user_id, new_contact_id):
    cursor.execute("UPDATE USER_CONTACTS SET user_id=?, contact_id=? WHERE user_id=? AND contact_id=?",
                   (new_user_id, new_contact_id, user_id, contact_id))
    conn.commit()

# DELETE operation for USER_CONTACTS table
def delete_user_contact(user_id, contact_id):
    cursor.execute("DELETE FROM USER_CONTACTS WHERE user_id=? AND contact_id=?", (user_id, contact_id))
    conn.commit()

# CREATE (Insert) operation for USER_ADDRESSES table
def create_user_address(user_id, address_id):
    cursor.execute("INSERT INTO USER_ADDRESSES (user_id, address_id) VALUES (?, ?)",
                   (user_id, address_id))
    conn.commit()

# READ (Select) operation for USER_ADDRESSES table
def read_user_address(user_id, address_id):
    cursor.execute("SELECT * FROM USER_ADDRESSES WHERE user_id=? AND address_id=?", (user_id, address_id))
    return cursor.fetchone()

# UPDATE operation for USER_ADDRESSES table
def update_user_address(user_id, address_id, new_user_id, new_address_id):
    cursor.execute("UPDATE USER_ADDRESSES SET user_id=?, address_id=? WHERE user_id=? AND address_id=?",
                   (new_user_id, new_address_id, user_id, address_id))
    conn.commit()

# DELETE operation for USER_ADDRESSES table
def delete_user_address(user_id, address_id):
    cursor.execute("DELETE FROM USER_ADDRESSES WHERE user_id=? AND address_id=?", (user_id, address_id))
    conn.commit()

# CREATE (Insert) operation for USER_GROUP table
def create_user_group(user_group_id, group_name, created_by, created_at, updated_by, updated_at):
    cursor.execute("INSERT INTO USER_GROUP (user_group_id, group_name, created_by, created_at, updated_by, updated_at) VALUES (?, ?, ?, ?, ?, ?)",
                   (user_group_id, group_name, created_by, created_at, updated_by, updated_at))
    conn.commit()

# READ (Select) operation for USER_GROUP table
def read_user_group(user_group_id):
    cursor.execute("SELECT * FROM USER_GROUP WHERE user_group_id=?", (user_group_id,))
    return cursor.fetchone()

# UPDATE operation for USER_GROUP table
def update_user_group(user_group_id, new_group_name, new_updated_by, new_updated_at):
    cursor.execute("UPDATE USER_GROUP SET group_name=?, updated_by=?, updated_at=? WHERE user_group_id=?",
                   (new_group_name, new_updated_by, new_updated_at, user_group_id))
    conn.commit()

# DELETE operation for USER_GROUP table
def delete_user_group(user_group_id):
    cursor.execute("DELETE FROM USER_GROUP WHERE user_group_id=?", (user_group_id,))
    conn.commit()


# CREATE (Insert) operation for USER_ROLE table
def create_user_role(role_id, role_name, created_by, created_at, updated_by, updated_at):
    cursor.execute("INSERT INTO USER_ROLE (role_id, role_name, created_by, created_at, updated_by, updated_at) VALUES (?, ?, ?, ?, ?, ?)",
                   (role_id, role_name, created_by, created_at, updated_by, updated_at))
    conn.commit()

# READ (Select) operation for USER_ROLE table
def read_user_role(role_id):
    cursor.execute("SELECT * FROM USER_ROLE WHERE role_id=?", (role_id,))
    return cursor.fetchone()

# UPDATE operation for USER_ROLE table
def update_user_role(role_id, new_role_name, new_updated_by, new_updated_at):
    cursor.execute("UPDATE USER_ROLE SET role_name=?, updated_by=?, updated_at=? WHERE role_id=?",
                   (new_role_name, new_updated_by, new_updated_at, role_id))
    conn.commit()

# DELETE operation for USER_ROLE table
def delete_user_role(role_id):
    cursor.execute("DELETE FROM USER_ROLE WHERE role_id=?", (role_id,))
    conn.commit()


# CREATE (Insert) operation for USER_GROUP_MEMBERSHIP table
def create_user_group_membership(user_id, user_group_id):
    cursor.execute("INSERT INTO USER_GROUP_MEMBERSHIP (user_id, user_group_id) VALUES (?, ?)",
                   (user_id, user_group_id))
    conn.commit()

# READ (Select) operation for USER_GROUP_MEMBERSHIP table
def read_user_group_membership(user_id, user_group_id):
    cursor.execute("SELECT * FROM USER_GROUP_MEMBERSHIP WHERE user_id=? AND user_group_id=?", (user_id, user_group_id))
    return cursor.fetchone()

# DELETE operation for USER_GROUP_MEMBERSHIP table
def delete_user_group_membership(user_id, user_group_id):
    cursor.execute("DELETE FROM USER_GROUP_MEMBERSHIP WHERE user_id=? AND user_group_id=?", (user_id, user_group_id))
    conn.commit()

    # CREATE (Insert) operation for USER_ROLE_ASSIGNMENT table
def create_user_role_assignment(user_id, role_id):
    cursor.execute("INSERT INTO USER_ROLE_ASSIGNMENT (user_id, role_id) VALUES (?, ?)",
                   (user_id, role_id))
    conn.commit()

# READ (Select) operation for USER_ROLE_ASSIGNMENT table
def read_user_role_assignment(user_id, role_id):
    cursor.execute("SELECT * FROM USER_ROLE_ASSIGNMENT WHERE user_id=? AND role_id=?", (user_id, role_id))
    return cursor.fetchone()

# UPDATE operation for USER_ROLE_ASSIGNMENT table
def update_user_role_assignment(user_id, role_id, new_user_id, new_role_id):
    cursor.execute("UPDATE USER_ROLE_ASSIGNMENT SET user_id=?, role_id=? WHERE user_id=? AND role_id=?",
                   (new_user_id, new_role_id, user_id, role_id))
    conn.commit()

# DELETE operation for USER_ROLE_ASSIGNMENT table
def delete_user_role_assignment(user_id, role_id):
    cursor.execute("DELETE FROM USER_ROLE_ASSIGNMENT WHERE user_id=? AND role_id=?", (user_id, role_id))
    conn.commit()




# CREATE (Insert) operation for ASSET_TYPES table
def create_asset_type(asset_type_id, description, created_by, created_at, updated_by, updated_at):
    cursor.execute("INSERT INTO ASSET_TYPES (asset_type_id, description, created_by, created_at, updated_by, updated_at) VALUES (?, ?, ?, ?, ?, ?)",
                   (asset_type_id, description, created_by, created_at, updated_by, updated_at))
    conn.commit()

# READ (Select) operation for ASSET_TYPES table
def read_asset_type(asset_type_id):
    cursor.execute("SELECT * FROM ASSET_TYPES WHERE asset_type_id=?", (asset_type_id,))
    return cursor.fetchone()

# UPDATE operation for ASSET_TYPES table
def update_asset_type(asset_type_id, new_description, new_updated_by, new_updated_at):
    cursor.execute("UPDATE ASSET_TYPES SET description=?, updated_by=?, updated_at=? WHERE asset_type_id=?",
                   (new_description, new_updated_by, new_updated_at, asset_type_id))
    conn.commit()

# DELETE operation for ASSET_TYPES table
def delete_asset_type(asset_type_id):
    cursor.execute("DELETE FROM ASSET_TYPES WHERE asset_type_id=?", (asset_type_id,))
    conn.commit()

# CREATE (Insert) operation for ASSETS table
def create_asset(asset_id, asset_type_id, created_by, created_at, updated_by, updated_at):
    cursor.execute("INSERT INTO ASSETS (asset_id, asset_type_id, created_by, created_at, updated_by, updated_at) VALUES (?, ?, ?, ?, ?, ?)",
                   (asset_id, asset_type_id, created_by, created_at, updated_by, updated_at))
    conn.commit()

# READ (Select) operation for ASSETS table
def read_asset(asset_id):
    cursor.execute("SELECT * FROM ASSETS WHERE asset_id=?", (asset_id,))
    return cursor.fetchone()

# UPDATE operation for ASSETS table
def update_asset(asset_id, new_asset_type_id, new_updated_by, new_updated_at):
    cursor.execute("UPDATE ASSETS SET asset_type_id=?, updated_by=?, updated_at=? WHERE asset_id=?",
                   (new_asset_type_id, new_updated_by, new_updated_at, asset_id))
    conn.commit()

# DELETE operation for ASSETS table
def delete_asset(asset_id):
    cursor.execute("DELETE FROM ASSETS WHERE asset_id=?", (asset_id,))
    conn.commit()



# CREATE (Insert) operation for RIGHTS table
def create_right(right_id, asset_id, create_right, edit_right, delete_right, read_data, view_right, created_by, created_at, updated_by, updated_at):
    cursor.execute("INSERT INTO RIGHTS (right_id, asset_id, create_right, edit_right, delete_right, read_data, view_right, created_by, created_at, updated_by, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                   (right_id, asset_id, create_right, edit_right, delete_right, read_data, view_right, created_by, created_at, updated_by, updated_at))
    conn.commit()

# READ (Select) operation for RIGHTS table
def read_right(right_id):
    cursor.execute("SELECT * FROM RIGHTS WHERE right_id=?", (right_id,))
    return cursor.fetchone()

# UPDATE operation for RIGHTS table
def update_right(right_id, new_create_right, new_edit_right, new_delete_right, new_read_data, new_view_right, new_updated_by, new_updated_at):
    cursor.execute("UPDATE RIGHTS SET create_right=?, edit_right=?, delete_right=?, read_data=?, view_right=?, updated_by=?, updated_at=? WHERE right_id=?",
                   (new_create_right, new_edit_right, new_delete_right, new_read_data, new_view_right, new_updated_by, new_updated_at, right_id))
    conn.commit()

# DELETE operation for RIGHTS table
def delete_right(right_id):
    cursor.execute("DELETE FROM RIGHTS WHERE right_id=?", (right_id,))
    conn.commit()


# CREATE (Insert) operation for USER_RIGHTS table
def create_user_right(user_id, right_id):
    cursor.execute("INSERT INTO USER_RIGHTS (user_id, right_id) VALUES (?, ?)",
                   (user_id, right_id))
    conn.commit()

# READ (Select) operation for USER_RIGHTS table
def read_user_right(user_id, right_id):
    cursor.execute("SELECT * FROM USER_RIGHTS WHERE user_id=? AND right_id=?", (user_id, right_id))
    return cursor.fetchone()

# DELETE operation for USER_RIGHTS table
def delete_user_right(user_id, right_id):
    cursor.execute("DELETE FROM USER_RIGHTS WHERE user_id=? AND right_id=?", (user_id, right_id))
    conn.commit()

# CREATE (Insert) operation for ROLE_RIGHTS table
def create_role_right(role_id, right_id):
    cursor.execute("INSERT INTO ROLE_RIGHTS (role_id, right_id) VALUES (?, ?)",
                   (role_id, right_id))
    conn.commit()

# READ (Select) operation for ROLE_RIGHTS table
def read_role_right(role_id, right_id):
    cursor.execute("SELECT * FROM ROLE_RIGHTS WHERE role_id=? AND right_id=?", (role_id, right_id))
    return cursor.fetchone()

# DELETE operation for ROLE_RIGHTS table
def delete_role_right(role_id, right_id):
    cursor.execute("DELETE FROM ROLE_RIGHTS WHERE role_id=? AND right_id=?", (role_id, right_id))
    conn.commit()


# CREATE (Insert) operation for TAGS table
def create_tag(tag_id, description, unit_of_measure, created_by, created_at, updated_by, updated_at):
    cursor.execute("INSERT INTO TAGS (tag_id, description, unit_of_measure, created_by, created_at, updated_by, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
                   (tag_id, description, unit_of_measure, created_by, created_at, updated_by, updated_at))
    conn.commit()

# READ (Select) operation for TAGS table
def read_tag(tag_id):
    cursor.execute("SELECT * FROM TAGS WHERE tag_id=?", (tag_id,))
    return cursor.fetchone()

# UPDATE operation for TAGS table
def update_tag(tag_id, updated_description, updated_unit_of_measure, updated_updated_by, updated_updated_at):
    cursor.execute("UPDATE TAGS SET description=?, unit_of_measure=?, updated_by=?, updated_at=? WHERE tag_id=?",
                   (updated_description, updated_unit_of_measure, updated_updated_by, updated_updated_at, tag_id))
    conn.commit()

# DELETE operation for TAGS table
def delete_tag(tag_id):
    cursor.execute("DELETE FROM TAGS WHERE tag_id=?", (tag_id,))
    conn.commit()


# CREATE (Insert) operation for DEVICE_TYPE table
def create_device_type(device_type_id, description, created_by, created_at, updated_by, updated_at):
    cursor.execute("INSERT INTO DEVICE_TYPE (device_type_id, description, created_by, created_at, updated_by, updated_at) VALUES (?, ?, ?, ?, ?, ?)",
                   (device_type_id, description, created_by, created_at, updated_by, updated_at))
    conn.commit()

# READ (Select) operation for DEVICE_TYPE table
def read_device_type(device_type_id):
    cursor.execute("SELECT * FROM DEVICE_TYPE WHERE device_type_id=?", (device_type_id,))
    return cursor.fetchone()

# UPDATE operation for DEVICE_TYPE table
def update_device_type(device_type_id, updated_description, updated_updated_by, updated_updated_at):
    cursor.execute("UPDATE DEVICE_TYPE SET description=?, updated_by=?, updated_at=? WHERE device_type_id=?",
                   (updated_description, updated_updated_by, updated_updated_at, device_type_id))
    conn.commit()

# DELETE operation for DEVICE_TYPE table
def delete_device_type(device_type_id):
    cursor.execute("DELETE FROM DEVICE_TYPE WHERE device_type_id=?", (device_type_id,))
    conn.commit()


# CREATE (Insert) operation for DEVICES table
def create_device(device_id, device_root_id, device_type_id, location_id, device_serial_number, description, model_number, brand_name, is_active, created_by, created_at, updated_by, updated_at):
    cursor.execute("INSERT INTO DEVICES (device_id, device_root_id, device_type_id, location_id, device_serial_number, description, model_number, brand_name, is_active, created_by, created_at, updated_by, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                   (device_id, device_root_id, device_type_id, location_id, device_serial_number, description, model_number, brand_name, is_active, created_by, created_at, updated_by, updated_at))
    conn.commit()

# READ (Select) operation for DEVICES table
def read_device(device_id):
    cursor.execute("SELECT * FROM DEVICES WHERE device_id=?", (device_id,))
    return cursor.fetchone()

# UPDATE operation for DEVICES table
def update_device(device_id, updated_device_serial_number, updated_description, updated_updated_by, updated_updated_at):
    cursor.execute("UPDATE DEVICES SET device_serial_number=?, description=?, updated_by=?, updated_at=? WHERE device_id=?",
                   (updated_device_serial_number, updated_description, updated_updated_by, updated_updated_at, device_id))
    conn.commit()

# DELETE operation for DEVICES table
def delete_device(device_id):
    cursor.execute("DELETE FROM DEVICES WHERE device_id=?", (device_id,))
    conn.commit()


# CREATE (Insert) operation for DEVICE_TAGS table
def create_device_tag(device_id, tag_id):
    cursor.execute("INSERT INTO DEVICE_TAGS (device_id, tag_id) VALUES (?, ?)",
                   (device_id, tag_id))
    conn.commit()

# READ (Select) operation for DEVICE_TAGS table
def read_device_tag(device_id, tag_id):
    cursor.execute("SELECT * FROM DEVICE_TAGS WHERE device_id=? AND tag_id=?", (device_id, tag_id))
    return cursor.fetchone()

# DELETE operation for DEVICE_TAGS table
def delete_device_tag(device_id, tag_id):
    cursor.execute("DELETE FROM DEVICE_TAGS WHERE device_id=? AND tag_id=?", (device_id, tag_id))
    conn.commit()



# CREATE (Insert) operation for CONNECTION_TYPES table
def create_connection_type(connection_type_id, description, created_by, created_at, updated_by, updated_at):
    cursor.execute("INSERT INTO CONNECTION_TYPES (connection_type_id, description, created_by, created_at, updated_by, updated_at) VALUES (?, ?, ?, ?, ?, ?)",
                   (connection_type_id, description, created_by, created_at, updated_by, updated_at))
    conn.commit()

# READ (Select) operation for CONNECTION_TYPES table
def read_connection_type(connection_type_id):
    cursor.execute("SELECT * FROM CONNECTION_TYPES WHERE connection_type_id=?", (connection_type_id,))
    return cursor.fetchone()

# UPDATE operation for CONNECTION_TYPES table
def update_connection_type(connection_type_id, new_description, new_updated_by, new_updated_at):
    cursor.execute("UPDATE CONNECTION_TYPES SET description=?, updated_by=?, updated_at=? WHERE connection_type_id=?",
                   (new_description, new_updated_by, new_updated_at, connection_type_id))
    conn.commit()

# DELETE operation for CONNECTION_TYPES table
def delete_connection_type(connection_type_id):
    cursor.execute("DELETE FROM CONNECTION_TYPES WHERE connection_type_id=?", (connection_type_id,))
    conn.commit()

# CREATE (Insert) operation for CONNECTIONS table
def create_connection(connection_id, connection_type_id, device_id, created_by, created_at, updated_by, updated_at):
    cursor.execute("INSERT INTO CONNECTIONS (connection_id, connection_type_id, device_id, created_by, created_at, updated_by, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
                   (connection_id, connection_type_id, device_id, created_by, created_at, updated_by, updated_at))
    conn.commit()

# READ (Select) operation for CONNECTIONS table
def read_connection(connection_id):
    cursor.execute("SELECT * FROM CONNECTIONS WHERE connection_id=?", (connection_id,))
    return cursor.fetchone()

# UPDATE operation for CONNECTIONS table
def update_connection(connection_id, new_connection_type_id, new_device_id, new_updated_by, new_updated_at):
    cursor.execute("UPDATE CONNECTIONS SET connection_type_id=?, device_id=?, updated_by=?, updated_at=? WHERE connection_id=?",
                   (new_connection_type_id, new_device_id, new_updated_by, new_updated_at, connection_id))
    conn.commit()

# DELETE operation for CONNECTIONS table
def delete_connection(connection_id):
    cursor.execute("DELETE FROM CONNECTIONS WHERE connection_id=?", (connection_id,))
    conn.commit()

# CREATE (Insert) operation for CONNECTION_DETAILS table
def create_connection_detail(connection_detail_id, connection_id, field_type, field_value, created_by, created_at, updated_by, updated_at):
    cursor.execute("INSERT INTO CONNECTION_DETAILS (connection_detail_id, connection_id, field_type, field_value, created_by, created_at, updated_by, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                   (connection_detail_id, connection_id, field_type, field_value, created_by, created_at, updated_by, updated_at))
    conn.commit()

# READ (Select) operation for CONNECTION_DETAILS table
def read_connection_detail(connection_detail_id):
    cursor.execute("SELECT * FROM CONNECTION_DETAILS WHERE connection_detail_id=?", (connection_detail_id,))
    return cursor.fetchone()

# UPDATE operation for CONNECTION_DETAILS table
def update_connection_detail(connection_detail_id, new_connection_id, new_field_type, new_field_value, new_updated_by, new_updated_at):
    cursor.execute("UPDATE CONNECTION_DETAILS SET connection_id=?, field_type=?, field_value=?, updated_by=?, updated_at=? WHERE connection_detail_id=?",
                   (new_connection_id, new_field_type, new_field_value, new_updated_by, new_updated_at, connection_detail_id))
    conn.commit()

# DELETE operation for CONNECTION_DETAILS table
def delete_connection_detail(connection_detail_id):
    cursor.execute("DELETE FROM CONNECTION_DETAILS WHERE connection_detail_id=?", (connection_detail_id,))
    conn.commit()


# CREATE (Insert) operation for USER_LOG_HISTORY table
def create_user_log_history(log_id, remote_host, identity, user_name, time_received, request_line, status_code, response_size, referer, user_agent, user_id, created_by, created_at, updated_by, updated_at):
    cursor.execute("INSERT INTO USER_LOG_HISTORY (log_id, remote_host, identity, user_name, time_received, request_line, status_code, response_size, referer, user_agent, user_id, created_by, created_at, updated_by, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                   (log_id, remote_host, identity, user_name, time_received, request_line, status_code, response_size, referer, user_agent, user_id, created_by, created_at, updated_by, updated_at))
    conn.commit()

# READ (Select) operation for USER_LOG_HISTORY table
def read_user_log_history(log_id):
    cursor.execute("SELECT * FROM USER_LOG_HISTORY WHERE log_id=?", (log_id,))
    return cursor.fetchone()

# UPDATE operation for USER_LOG_HISTORY table
def update_user_log_history(log_id, new_remote_host, new_identity, new_user_name, new_time_received, new_request_line, new_status_code, new_response_size, new_referer, new_user_agent, new_user_id, new_updated_by, new_updated_at):
    cursor.execute("UPDATE USER_LOG_HISTORY SET remote_host=?, identity=?, user_name=?, time_received=?, request_line=?, status_code=?, response_size=?, referer=?, user_agent=?, user_id=?, updated_by=?, updated_at=? WHERE log_id=?",
                   (new_remote_host, new_identity, new_user_name, new_time_received, new_request_line, new_status_code, new_response_size, new_referer, new_user_agent, new_user_id, new_updated_by, new_updated_at, log_id))
    conn.commit()

# DELETE operation for USER_LOG_HISTORY table
def delete_user_log_history(log_id):
    cursor.execute("DELETE FROM USER_LOG_HISTORY WHERE log_id=?", (log_id,))
    conn.commit()

# CREATE (Insert) operation for ALERTS table
def create_alert(alert_id, device_id, alert_description, created_by, created_at, updated_by, updated_at):
    cursor.execute("INSERT INTO ALERTS (alert_id, device_id, alert_description, created_by, created_at, updated_by, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
                   (alert_id, device_id, alert_description, created_by, created_at, updated_by, updated_at))
    conn.commit()

# READ (Select) operation for ALERTS table
def read_alert(alert_id):
    cursor.execute("SELECT * FROM ALERTS WHERE alert_id=?", (alert_id,))
    return cursor.fetchone()

# UPDATE operation for ALERTS table
def update_alert(alert_id, new_device_id, new_alert_description, new_updated_by, new_updated_at):
    cursor.execute("UPDATE ALERTS SET device_id=?, alert_description=?, updated_by=?, updated_at=? WHERE alert_id=?",
                   (new_device_id, new_alert_description, new_updated_by, new_updated_at, alert_id))
    conn.commit()

# DELETE operation for ALERTS table
def delete_alert(alert_id):
    cursor.execute("DELETE FROM ALERTS WHERE alert_id=?", (alert_id,))
    conn.commit()


# CREATE (Insert) operation for ALERT_EXPRESSIONS table
def create_alert_expression(expression_id, alert_id, expression, input_field_name, arithmetic_operator, constant_value, brace_value, logical_operator, description, created_by, created_at, updated_by, updated_at):
    cursor.execute("INSERT INTO ALERT_EXPRESSIONS (expression_id, alert_id, expression, input_field_name, arithmetic_operator, constant_value, brace_value, logical_operator, description, created_by, created_at, updated_by, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                   (expression_id, alert_id, expression, input_field_name, arithmetic_operator, constant_value, brace_value, logical_operator, description, created_by, created_at, updated_by, updated_at))
    conn.commit()

# READ (Select) operation for ALERT_EXPRESSIONS table
def read_alert_expression(expression_id):
    cursor.execute("SELECT * FROM ALERT_EXPRESSIONS WHERE expression_id=?", (expression_id,))
    return cursor.fetchone()

# UPDATE operation for ALERT_EXPRESSIONS table
def update_alert_expression(expression_id, new_expression, new_updated_by, new_updated_at):
    cursor.execute("UPDATE ALERT_EXPRESSIONS SET expression=?, updated_by=?, updated_at=? WHERE expression_id=?", 
                   (new_expression, new_updated_by, new_updated_at, expression_id))
    conn.commit()

# DELETE operation for ALERT_EXPRESSIONS table
def delete_alert_expression(expression_id):
    cursor.execute("DELETE FROM ALERT_EXPRESSIONS WHERE expression_id=?", (expression_id,))
    conn.commit()


# CREATE (Insert) operation for HISTORY table
def create_history(history_id, device_id, value, status, datetime, alert_id, created_by, created_at, updated_by, updated_at):
    cursor.execute("INSERT INTO HISTORY (history_id, device_id, value, status, datetime, alert_id, created_by, created_at, updated_by, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                   (history_id, device_id, value, status, datetime, alert_id, created_by, created_at, updated_by, updated_at))
    conn.commit()

# READ (Select) operation for HISTORY table
def read_history(history_id):
    cursor.execute("SELECT * FROM HISTORY WHERE history_id=?", (history_id,))
    return cursor.fetchone()

# UPDATE operation for HISTORY table
def update_history(history_id, new_status, new_updated_by, new_updated_at):
    cursor.execute("UPDATE HISTORY SET status=?, updated_by=?, updated_at=? WHERE history_id=?", 
                   (new_status, new_updated_by, new_updated_at, history_id))
    conn.commit()

# DELETE operation for HISTORY table
def delete_history(history_id):
    cursor.execute("DELETE FROM HISTORY WHERE history_id=?", (history_id,))
    conn.commit()

# CREATE (Insert) operation for ACTION_TYPES table
def create_action_type(action_type_id, description, created_by, created_at, updated_by, updated_at):
    cursor.execute("INSERT INTO ACTION_TYPES (action_type_id, description, created_by, created_at, updated_by, updated_at) VALUES (?, ?, ?, ?, ?, ?)",
                   (action_type_id, description, created_by, created_at, updated_by, updated_at))
    conn.commit()

# READ (Select) operation for ACTION_TYPES table
def read_action_type(action_type_id):
    cursor.execute("SELECT * FROM ACTION_TYPES WHERE action_type_id=?", (action_type_id,))
    return cursor.fetchone()

# UPDATE operation for ACTION_TYPES table
def update_action_type(action_type_id, new_description, new_updated_by, new_updated_at):
    cursor.execute("UPDATE ACTION_TYPES SET description=?, updated_by=?, updated_at=? WHERE action_type_id=?", 
                   (new_description, new_updated_by, new_updated_at, action_type_id))
    conn.commit()

# DELETE operation for ACTION_TYPES table
def delete_action_type(action_type_id):
    cursor.execute("DELETE FROM ACTION_TYPES WHERE action_type_id=?", (action_type_id,))
    conn.commit()

# CREATE (Insert) operation for ACTIONS table
def create_action(action_id, description, action_type_id, action_taken_datetime, created_by, created_at, updated_by, updated_at):
    cursor.execute("INSERT INTO ACTIONS (action_id, description, action_type_id, action_taken_datetime, created_by, created_at, updated_by, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                   (action_id, description, action_type_id, action_taken_datetime, created_by, created_at, updated_by, updated_at))
    conn.commit()

# READ (Select) operation for ACTIONS table
def read_action(action_id):
    cursor.execute("SELECT * FROM ACTIONS WHERE action_id=?", (action_id,))
    return cursor.fetchone()

# UPDATE operation for ACTIONS table
def update_action(action_id, new_description, new_action_type_id, new_action_taken_datetime, new_updated_by, new_updated_at):
    cursor.execute("UPDATE ACTIONS SET description=?, action_type_id=?, action_taken_datetime=?, updated_by=?, updated_at=? WHERE action_id=?", 
                   (new_description, new_action_type_id, new_action_taken_datetime, new_updated_by, new_updated_at, action_id))
    conn.commit()

# DELETE operation for ACTIONS table
def delete_action(action_id):
    cursor.execute("DELETE FROM ACTIONS WHERE action_id=?", (action_id,))
    conn.commit()

# CREATE (Insert) operation for ACTIONS_HISTORY table
def create_action_history(action_id, history_id):
    cursor.execute("INSERT INTO ACTIONS_HISTORY (action_id, history_id) VALUES (?, ?)",
                   (action_id, history_id))
    conn.commit()

# READ (Select) operation for ACTIONS_HISTORY table
def read_action_history(action_id, history_id):
    cursor.execute("SELECT * FROM ACTIONS_HISTORY WHERE action_id=? AND history_id=?", (action_id, history_id))
    return cursor.fetchone()

# DELETE operation for ACTIONS_HISTORY table
def delete_action_history(action_id, history_id):
    cursor.execute("DELETE FROM ACTIONS_HISTORY WHERE action_id=? AND history_id=?", (action_id, history_id))
    conn.commit()

# CREATE (Insert) operation for ACTIONS_ALERT table
def create_action_alert(action_id, alert_id):
    cursor.execute("INSERT INTO ACTIONS_ALERT (action_id, alert_id) VALUES (?, ?)",
                   (action_id, alert_id))
    conn.commit()

# READ (Select) operation for ACTIONS_ALERT table
def read_action_alert(action_id, alert_id):
    cursor.execute("SELECT * FROM ACTIONS_ALERT WHERE action_id=? AND alert_id=?", (action_id, alert_id))
    return cursor.fetchone()

# DELETE operation for ACTIONS_ALERT table
def delete_action_alert(action_id, alert_id):
    cursor.execute("DELETE FROM ACTIONS_ALERT WHERE action_id=? AND alert_id=?", (action_id, alert_id))
    conn.commit()



conn.close()
CREATE TABLE ADDRESSES (
    address_id INT PRIMARY KEY,
    address_line1 VARCHAR(255),
    address_line2 VARCHAR(255),
    city VARCHAR(255),
    state VARCHAR(255),
    postal_code VARCHAR(255),
    country VARCHAR(255),
    latitude DECIMAL(10, 7),
    longitude DECIMAL(10, 7),
    created_by VARCHAR(255),
    created_at DATETIME,
    updated_by VARCHAR(255),
    updated_at DATETIME
);


CREATE TABLE CONTACT_TYPES (
    contact_type_id INT PRIMARY KEY,
    description VARCHAR(255),
    created_by VARCHAR(255),
    created_at DATETIME,
    updated_by VARCHAR(255),
    updated_at DATETIME
);
CREATE TABLE CONTACTS (
    contact_id INT PRIMARY KEY,
    contact_description VARCHAR(255),
    contact_type_id INT,
    created_by VARCHAR(255),
    created_at DATETIME,
    updated_by VARCHAR(255),
    updated_at DATETIME,
    FOREIGN KEY (contact_type_id) REFERENCES CONTACT_TYPES(contact_type_id)
);

CREATE TABLE LOCATIONS (
    location_id INT PRIMARY KEY,
    location_name VARCHAR(255),
    location_desc VARCHAR(255),
    location_type_id INT,
    location_root INT,
    latitude DECIMAL(10, 7),
    longitude DECIMAL(10, 7),
    address_id INT,
    contact_id INT,
    created_by VARCHAR(255),
    created_at DATETIME,
    updated_by VARCHAR(255),
    updated_at DATETIME,
    FOREIGN KEY (location_root) REFERENCES LOCATIONS(location_id),
    FOREIGN KEY (address_id) REFERENCES ADDRESSES(address_id),
    FOREIGN KEY (contact_id) REFERENCES CONTACTS(contact_id)
);
CREATE TABLE LOCATION_CONTACTS (
    location_id INT,
    contact_id INT,
    PRIMARY KEY (location_id, contact_id),
    FOREIGN KEY (location_id) REFERENCES LOCATIONS(location_id),
    FOREIGN KEY (contact_id) REFERENCES CONTACTS(contact_id)
);
CREATE TABLE LOCATION_ADDRESSES (
    location_id INT,
    address_id INT,
    PRIMARY KEY (location_id, address_id),
    FOREIGN KEY (location_id) REFERENCES LOCATIONS(location_id),
    FOREIGN KEY (address_id) REFERENCES ADDRESSES(address_id)
);
CREATE TABLE USERS (
    user_id INT PRIMARY KEY,
    email VARCHAR(255),
    hex_password VARCHAR(255),
    contact_id INT,
    address_id INT,
    is_active BOOLEAN,
    is_verified BOOLEAN,
    created_by VARCHAR(255),
    created_at DATETIME,
    updated_by VARCHAR(255),
    updated_at DATETIME,
    FOREIGN KEY (contact_id) REFERENCES CONTACTS(contact_id),
    FOREIGN KEY (address_id) REFERENCES ADDRESSES(address_id)
);
CREATE TABLE USER_CONTACTS (
    user_id INT,
    contact_id INT,
    PRIMARY KEY (user_id, contact_id),
    FOREIGN KEY (user_id) REFERENCES USERS(user_id),
    FOREIGN KEY (contact_id) REFERENCES CONTACTS(contact_id)
);
CREATE TABLE USER_ADDRESSES (
    user_id INT,
    address_id INT,
    PRIMARY KEY (user_id, address_id),
    FOREIGN KEY (user_id) REFERENCES USERS(user_id),
    FOREIGN KEY (address_id) REFERENCES ADDRESSES(address_id)
);
CREATE TABLE USER_GROUP (
    user_group_id INT PRIMARY KEY,
    group_name VARCHAR(255),
    created_by VARCHAR(255),
    created_at DATETIME,
    updated_by VARCHAR(255),
    updated_at DATETIME
);
CREATE TABLE USER_ROLE (
    role_id INT PRIMARY KEY,
    role_name VARCHAR(255),
    created_by VARCHAR(255),
    created_at DATETIME,
    updated_by VARCHAR(255),
    updated_at DATETIME
);
CREATE TABLE USER_GROUP_MEMBERSHIP (
    user_id INT,
    user_group_id INT,
    PRIMARY KEY (user_id, user_group_id),
    FOREIGN KEY (user_id) REFERENCES USERS(user_id),
    FOREIGN KEY (user_group_id) REFERENCES USER_GROUP(user_group_id)
);
CREATE TABLE USER_ROLE_ASSIGNMENT (
    user_id INT,
    role_id INT,
    PRIMARY KEY (user_id, role_id),
    FOREIGN KEY (user_id) REFERENCES USERS(user_id),
    FOREIGN KEY (role_id) REFERENCES USER_ROLE(role_id)
);
CREATE TABLE ASSET_TYPES (
    asset_type_id INT PRIMARY KEY,
    description VARCHAR(255),
    created_by VARCHAR(255),
    created_at DATETIME,
    updated_by VARCHAR(255),
    updated_at DATETIME
);
CREATE TABLE ASSETS (
    asset_id INT PRIMARY KEY,
    asset_type_id INT,
    created_by VARCHAR(255),
    created_at DATETIME,
    updated_by VARCHAR(255),
    updated_at DATETIME,
    FOREIGN KEY (asset_type_id) REFERENCES ASSET_TYPES(asset_type_id)
);
CREATE TABLE RIGHTS (
    right_id INT PRIMARY KEY,
    asset_id INT,
    create_right BOOLEAN,
    edit_right BOOLEAN,
    delete_right BOOLEAN,
    read_data BOOLEAN,
    view_right BOOLEAN,
    created_by VARCHAR(255),
    created_at DATETIME,
    updated_by VARCHAR(255),
    updated_at DATETIME,
    FOREIGN KEY (asset_id) REFERENCES ASSETS(asset_id)
);
CREATE TABLE USER_RIGHTS (
    user_id INT,
    right_id INT,
    PRIMARY KEY (user_id, right_id),
    FOREIGN KEY (user_id) REFERENCES USERS(user_id),
    FOREIGN KEY (right_id) REFERENCES RIGHTS(right_id)
);
CREATE TABLE ROLE_RIGHTS (
    role_id INT,
    right_id INT,
    PRIMARY KEY (role_id, right_id),
    FOREIGN KEY (role_id) REFERENCES USER_ROLE(role_id),
    FOREIGN KEY (right_id) REFERENCES RIGHTS(right_id)
);
CREATE TABLE TAGS (
    tag_id INT PRIMARY KEY,
    description VARCHAR(255),
    unit_of_measure VARCHAR(255),
    created_by VARCHAR(255),
    created_at DATETIME,
    updated_by VARCHAR(255),
    updated_at DATETIME
);
CREATE TABLE DEVICE_TYPE (
    device_type_id INT PRIMARY KEY,
    description VARCHAR(255),
    created_by VARCHAR(255),
    created_at DATETIME,
    updated_by VARCHAR(255),
    updated_at DATETIME
);
CREATE TABLE DEVICES (
    device_id INT PRIMARY KEY,
    device_root_id INT,
    device_type_id INT,
    location_id INT,
    device_serial_number VARCHAR(255),
    description VARCHAR(255),
    model_number VARCHAR(255),
    brand_name VARCHAR(255),
    is_active BOOLEAN,
    created_by VARCHAR(255),
    created_at DATETIME,
    updated_by VARCHAR(255),
    updated_at DATETIME,
    FOREIGN KEY (device_root_id) REFERENCES DEVICES(device_id),
    FOREIGN KEY (device_type_id) REFERENCES DEVICE_TYPE(device_type_id),
    FOREIGN KEY (location_id) REFERENCES LOCATIONS(location_id)
);
CREATE TABLE DEVICE_TAGS (
    device_id INT,
    tag_id INT,
    PRIMARY KEY (device_id, tag_id),
    FOREIGN KEY (device_id) REFERENCES DEVICES(device_id),
    FOREIGN KEY (tag_id) REFERENCES TAGS(tag_id)
);
CREATE TABLE CONNECTION_TYPES (
    connection_type_id INT PRIMARY KEY,
    description VARCHAR(255),
    created_by VARCHAR(255),
    created_at DATETIME,
    updated_by VARCHAR(255),
    updated_at DATETIME
);
CREATE TABLE CONNECTIONS (
    connection_id INT PRIMARY KEY,
    connection_type_id INT,
    device_id INT,
    created_by VARCHAR(255),
    created_at DATETIME,
    updated_by VARCHAR(255),
    updated_at DATETIME,
    FOREIGN KEY (connection_type_id) REFERENCES CONNECTION_TYPES(connection_type_id),
    FOREIGN KEY (device_id) REFERENCES DEVICES(device_id)
);
CREATE TABLE CONNECTION_DETAILS (
    connection_detail_id INT PRIMARY KEY,
    connection_id INT,
    field_type VARCHAR(255),
    field_value VARCHAR(255),
    created_by VARCHAR(255),
    created_at DATETIME,
    updated_by VARCHAR(255),
    updated_at DATETIME,
    FOREIGN KEY (connection_id) REFERENCES CONNECTIONS(connection_id)
);
CREATE TABLE USER_LOG_HISTORY (
    log_id INT PRIMARY KEY,
    remote_host VARCHAR(255),
    identity VARCHAR(255),
    user_name VARCHAR(255),
    time_received DATETIME,
    request_line VARCHAR(255),
    status_code INT,
    response_size INT,
    referer VARCHAR(255),
    user_agent VARCHAR(255),
    user_id INT,
    created_by VARCHAR(255),
    created_at DATETIME,
    updated_by VARCHAR(255),
    updated_at DATETIME,
    FOREIGN KEY (user_id) REFERENCES USERS(user_id)
);
CREATE TABLE ALERTS (
    alert_id INT PRIMARY KEY,
    device_id INT,
    alert_description VARCHAR(255),
    created_by VARCHAR(255),
    created_at DATETIME,
    updated_by VARCHAR(255),
    updated_at DATETIME,
    FOREIGN KEY (device_id) REFERENCES DEVICES(device_id)
);
CREATE TABLE ALERT_EXPRESSIONS (
    expression_id INT PRIMARY KEY,
    alert_id INT,
    expression VARCHAR(255),
    input_field_name VARCHAR(255),
    arithmetic_operator VARCHAR(255),
    constant_value DECIMAL(10, 2),
    brace_value VARCHAR(255),
    logical_operator VARCHAR(255),
    description VARCHAR(255),
    created_by VARCHAR(255),
    created_at DATETIME,
    updated_by VARCHAR(255),
    updated_at DATETIME,
    FOREIGN KEY (alert_id) REFERENCES ALERTS(alert_id)
);
CREATE TABLE HISTORY (
    history_id INT PRIMARY KEY,
    device_id INT,
    value DECIMAL(10, 2),
    status VARCHAR(255),
    datetime DATETIME,
    alert_id INT,
    created_by VARCHAR(255),
    created_at DATETIME,
    updated_by VARCHAR(255),
    updated_at DATETIME,
    FOREIGN KEY (device_id) REFERENCES DEVICES(device_id),
    FOREIGN KEY (alert_id) REFERENCES ALERTS(alert_id)
);

CREATE TABLE ACTION_TYPES (
    action_type_id INT PRIMARY KEY,
    description VARCHAR(255),
    created_by VARCHAR(255),
    created_at DATETIME,
    updated_by VARCHAR(255),
    updated_at DATETIME
);
CREATE TABLE ACTIONS (
    action_id INT PRIMARY KEY,
    description VARCHAR(255),
    action_type_id INT,
    action_taken_datetime DATETIME,
    created_by VARCHAR(255),
    created_at DATETIME,
    updated_by VARCHAR(255),
    updated_at DATETIME,
    FOREIGN KEY (action_type_id) REFERENCES ACTION_TYPES(action_type_id)
);
CREATE TABLE ACTIONS_HISTORY (
    action_id INT,
    history_id INT,
    PRIMARY KEY (action_id, history_id),
    FOREIGN KEY (action_id) REFERENCES ACTIONS(action_id),
    FOREIGN KEY (history_id) REFERENCES HISTORY(history_id)
);
CREATE TABLE ACTIONS_ALERT (
    action_id INT,
    alert_id INT,
    PRIMARY KEY (action_id, alert_id),
    FOREIGN KEY (action_id) REFERENCES ACTIONS(action_id),
    FOREIGN KEY (alert_id) REFERENCES ALERTS(alert_id)
);

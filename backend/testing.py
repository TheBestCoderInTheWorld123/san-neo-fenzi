from mqtt_fetch import *
from mqtt_insert_pg import *
data = {
    0: [{'IMEI': '862174069140333'}, {'AQ': '10'}, {'status': '>'}, {'date_time': datetime(2023, 12, 17, 21, 9)}],
    1: [{'IMEI': '862174069140333'}, {'HUM': '51'}, {'status': ''}, {'date_time': datetime(2023, 12, 17, 21, 9)}],
    2: [{'IMEI': '862174069140333'}, {'TMP': '32'}, {'status': ''}, {'date_time': datetime(2023, 12, 17, 21, 9)}]
}
insert_alert(session, data)

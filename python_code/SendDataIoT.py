import json
import uuid
import pytz
import time
import pandas as pd

from datetime import datetime
from modules.Util import get_config_publisher
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

if __name__ == "__main__":
	# Get my config parameters
	my_env = get_config_publisher()
	
	tz = pytz.timezone(my_env.TIMEZONE)
	datetime_local = datetime.now(tz)

	# Create and Configure the IoT Client
	IoTclient = AWSIoTMQTTClient(my_env.CLIENT_NAME)
	IoTclient.configureEndpoint(my_env.BROKER_PATH, 8883)
	
	IoTclient.configureCredentials(
		my_env.ROOT_CA_PATH, 
		my_env.PRIVATE_KEY_PATH, 
		my_env.CERTIFICATE_PATH
	)
	
	# Allow the device to queue infinite messages
	IoTclient.configureOfflinePublishQueueing(-1)
	
	# Number of messages to send after a connection returns
	IoTclient.configureDrainingFrequency(2)  # 2 requests/second
	
	# How long to wait for a [dis]connection to complete (in seconds)
	IoTclient.configureConnectDisconnectTimeout(10)
	
	# How long to wait for publish/[un]subscribe (in seconds)
	IoTclient.configureMQTTOperationTimeout(5) 
	
	# Create an IoT connection
	IoTclient.connect()
	IoTclient.publish(my_env.TOPIC, "connected", 0)
	
	# Read the filename with Pandas
	df = pd.read_csv(my_env.PATH_FILE, sep=',')
	
	# Clean whitespaces in column names
	df.columns = df.columns.str.strip().str.replace(' ', '_').str.lower()
	
	# Read DF
	for index, row in df.iterrows():
		payload = json.dumps({
			"id": str(uuid.uuid4()),
			"device": "device-home-weather",
			"house_overall_kw": row['house_overall_[kw]'],
			"dishwasher_kw": row['dishwasher_[kw]'],
			"house_office_kw": row['home_office_[kw]'],
			"garage_doo_kwr": row['garage_door_[kw]'],
			"kitchen_kw": row['kitchen_12_[kw]'],
			"living_room_kw": row['living_room_[kw]'],
			"house_temperature": row['temperature'],
			"humidity": row['humidity'],
			"visibility": row['visibility'],
			"h"
			"pressure": row['pressure'],
			"windspeed": row['windspeed'],
			"datetime_read": datetime_local.strftime("%Y-%m-%d %H:%M:%S"),
			"timestamp": int(time.time())
		})
		
		print(payload)
		
		IoTclient.publish(my_env.TOPIC, payload, 0)
		time.sleep(5)
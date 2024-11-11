import time
from awsiot import mqtt_connection_builder
from awscrt import io, mqtt, auth, http

# Define endpoint and cert paths
endpoint = "a2w3ke0es02zef-ats.iot.eu-west-3.amazonaws.com"
root_ca_path = "/home/gateway/Desktop/PFE-2024/Cert/root-CA.crt"
cert_path = "/home/gateway/Desktop/PFE-2024/Cert/Raspberry_pi.cert.pem"
key_path = "/home/gateway/Desktop/PFE-2024/Cert/Raspberry_pi.private.key"

# Set up MQTT connection using the AWS IoT Device SDK v2
mqtt_connection = mqtt_connection_builder.mtls_from_path(
        endpoint=endpoint,
        cert_filepath=cert_path,
        pri_key_filepath=key_path,
        ca_filepath=root_ca_path,
        client_id="Raspberry_pi",
        clean_session=False,
        keep_alive_secs=6,
)

print("Connecting to AWS IoT...")
connect_future = mqtt_connection.connect()
connect_future.result()
print("Connected!")

# Publish a message
mqtt_connection.publish(
        topic="Raspberry-test",
        payload="{'Message':'Hello From Rpi to AWS'}",
        qos=mqtt.QoS.AT_LEAST_ONCE,
)
print("Published message to AWS IoT Core")

# Disconnect
disconnect_future = mqtt_connection.disconnect()
disconnect_future.result()
print("Disconnected!")

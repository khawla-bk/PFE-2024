import time
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import logging
logger = logging.getLogger("AWSIoTPythonSDK.core")
logger.setLevel(logging.DEBUG)
streamHandler = logging.StreamHandler()
logger.addHandler(streamHandler)


def test(self,params,packet):
        print("Recieved message from AWS Iot Core")
        print('Topic:'+packet.topic)
        print("Payload: ",(packet.payload))

myMQTTClient=AWSIoTMQTTClient("Raspberry_pi")
myMQTTClient.configureEndpoint("a2w3ke0es02zef-ats.iot.eu-west-3.amazonaws.com", 8883)

myMQTTClient.configureCredentials("/home/gateway/Desktop/PFE-2024/Cert/root-CA.crt",  "/home/gateway/Desktop/PFE-2024/Cert/Raspberry_pi.cert.pem", "/home/gateway/Desktop/PFE-2024/Cert/Raspberry_pi.private.key")  
myMQTTClient.configureOfflinePublishQueueing(-1) # Infinite offline Publish queueing
myMQTTClient.configureDrainingFrequency(2) # Draining: 2 Hz
myMQTTClient.configureConnectDisconnectTimeout(10) # 10 sec
myMQTTClient.configureMQTTOperationTimeout(50) # 50 sec
print ('Initiating connection...')
myMQTTClient.connect()
myMQTTClient.subscribe("Raspberry-test",1,test)
while True:
        time.sleep(5)
        print("Publishing to AWS IoT Core")
        myMQTTClient.publish(topic="Raspberry-test",QoS=1,payload="{'Message':'Hello From Rpi to AWS'}")
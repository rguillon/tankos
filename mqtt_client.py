import config

from umqtt.robust import MQTTClient

instance = MQTTClient("tankos_client", config.mqtt_broker)
instance.connect()


def publish(topic, msg):
    instance.publish(topic, msg)

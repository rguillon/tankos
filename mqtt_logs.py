# Tankos, aquarium monitoring and control for MicroPython
# Copyright (c) 2019 Renaud Guillon
# SPDX-License-Identifier: MIT

try:
    import io
except ImportError:
    import uio as io


class MqttLogs(io.IOBase):
    # Adapter class for sending logs over MQTT. Assumes the logging class will call write, once with the logger name and
    # severity, then with the message, and finally with a \n, the logger names and severity are transformed into
    # mqtt subtopics. The messages are pushed into a queue until beeing sent over mqtt with the update service.
    def __init__(self, mqtt_client, topic, max_msg):
        self.mqtt_client = mqtt_client
        self.topic = topic
        self.max_msg = max_msg
        self.logs = []
        self.current_log = b''
        self.current_topic = b''
        self.is_waiting_for_topic = True

    def write(self, msg):
        if msg == bytearray(b'\n'):
            # discard oldest messages if max umber if reached
            while len(self.logs) > self.max_msg:
                self.logs.pop()
            self.logs.insert(0, [self.current_topic, self.current_log])
            self.current_log = b''
            self.is_waiting_for_topic = True
        else:
            if self.is_waiting_for_topic:
                self.current_topic = msg.replace(':', '/')
                self.is_waiting_for_topic = False
            else:
                self.current_log = self.current_log + msg

    def update(self):
        while len(self.logs) > 0:
            sub_topic, msg = self.logs.pop()
            await self.mqtt_client.publish(self.topic + sub_topic, msg)

    def get_ms_until_next_update(self):
        return 100

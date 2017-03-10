import json

import paho.mqtt.client as mqtt


def connect(
    host, port, on_msg,
    username=None, password=None, subscriptions={}, on_disconnect=None):
    client = mqtt.Client()
    if username and password:
        client.username_pw_set(username, password)

    def on_conn(client, userdata, flags, rc):
        for topic, qos in subscriptions.items():
            client.subscribe(topic, qos=qos)

    client.on_disconnect = on_disconnect
    client.on_connect = on_conn
    client.on_message = on_msg
    client.connect(host, port, 60)
    client.loop_start()
    return client


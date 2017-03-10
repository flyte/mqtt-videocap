# -*- coding: utf-8 -*-
import json
import logging
import tempfile
import os
from time import sleep
from subprocess import check_call

import click
import requests
from celery import Celery

from .mqtt import connect


LOG = logging.getLogger("mqtt_videocap")
APP = Celery("mqtt_videocap.cli")


@APP.task
def post(path, url):
    LOG.info("Posting %r to %r..." % (path, url))
    with open(path, "rb") as payload:
        headers = {"content-type": "application/x-www-form-urlencoded"}
        requests.post(url, data=payload, verify=False, headers=headers)
    LOG.info("Post complete!")
    os.unlink(path)
    LOG.info("File deleted.")


@click.command()
@click.option("--ffmpeg", default="ffmpeg", help="Location of ffmpeg binary")
@click.option("--mqtt-host", default="localhost", help="MQTT host")
@click.option("--mqtt-port", default=1883, help="MQTT port")
@click.option("--mqtt-user", default=None, help="MQTT user")
@click.option("--mqtt-pass", default=None, help="MQTT password")
@click.option("--celery-broker", default="redis://localhost")
@click.option(
        "--default-device", default="/dev/video0",
        help="Device from which to capture if not specified in payload")
def main(**args):
    """
    Console script for mqtt_videocap
    """
    APP.conf.broker_url = args["celery_broker"]

    def on_msg(client, userdata, msg):
        """
        Handle incoming messages.
        """
        LOG.info("Message RX: (%s) %s" % (msg.topic, msg.payload))
        try:
            data = json.loads(msg.payload.decode("utf8"))
        except ValueError as err:
            LOG.error("Message payload was not valid JSON: %s" % err)
            return

        try:
            duration = float(data["duration"])
        except KeyError:
            LOG.error("Message payload did not include 'duration'.")
            return
        except ValueError:
            LOG.error("Duration did not parse as a float: %s" % data["duration"])
            return

        try:
            post_url = data["post_url"]
        except KeyError:
            LOG.error("No 'post_url' specified in message payload.")
            return

        device = data.get("device", args["default_device"])
        _, path = tempfile.mkstemp(".mp4")
        check_call([
            args["ffmpeg"], "-y", "-i", device, "-t", str(duration), path])

        post.delay(path, post_url)


    client = connect(
        args["mqtt_host"],
        args["mqtt_port"],
        on_msg,
        username=args["mqtt_user"],
        password=args["mqtt_pass"],
        subscriptions={"test/videocap": 0}
    )
    while True:
        sleep(1)

if __name__ == "__main__":
    main()

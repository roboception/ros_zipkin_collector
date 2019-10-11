#!/usr/bin/env python

from __future__ import absolute_import, print_function

import logging
import time
import json

import requests
import rospy
from std_msgs.msg import String


class RosZipkinCollector(object):
    def __init__(self):
        rospy.init_node('zipkin_collector', log_level=rospy.INFO)
        zipkin_port = rospy.get_param("~zipkin_port", 9411)
        zipkin_host = rospy.get_param("~zipkin_host", "localhost")
        self.zipkin_url = "http://{}:{}/api/v2/spans".format(zipkin_host, zipkin_port)

        rospy.loginfo("sending spans to {}".format(self.zipkin_url))
        rospy.Subscriber("/spans", String, self.spans_callback)

    def spin(self):
        rospy.spin()

    def spans_callback(self, msg):
        rospy.logdebug("got span: {}".format(msg.data))
        try:
            j = json.loads(msg.data)
        except ValueError as e:
            rospy.logerr("could not parse span: {}".format(e))
            return
        try:
            r = requests.post(self.zipkin_url, json=j, timeout=0.1)
        except (requests.RequestException, requests.exceptions.BaseHTTPError) as e:
            rospy.logwarn("Could not post zipkin span: {}".format(e))
            return
        if r.status_code != 202:
            rospy.logwarn("post spans failed: {}".format(r.text))


if __name__ == '__main__':
    try:
        collector = RosZipkinCollector()
        collector.spin()
    except rospy.ROSInterruptException:
        pass


'''
Copyright (c) 2019 Cisco and/or its affiliates.

This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.0 (the "License"). You may obtain a copy of the
License at

               https://developer.cisco.com/docs/licenses

All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.
'''

import configparser
import json
import os
import requests

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class CCP:
    def __init__(self, url, username,password):
        self.url = url
        self.username = username
        self.password = password
        self.cookie = None

    def login(self):

        headers = {
            'content-type': 'application/json',
        }

        response = requests.request("POST", self.url + "/2/system/login?username=" + self.username + "&password=" + self.password,  headers=headers, verify=False)

        if response:
            self.cookie = response.cookies

        return response


    def getClusters(self):

        response = requests.request("GET", self.url + "/2/clusters",cookies=self.cookie, verify=False)

        return response


    def deployNewClusterFromFile(self, newClusterDetails):

        try:
            with open(newClusterDetails) as json_data:
                data = json.load(json_data) 

            headers = {
                'content-type': 'application/json',
            }

            response = requests.request("POST", self.url + "/2/clusters", json=data,cookies=self.cookie, headers=headers, verify=False)

            return response

        except IOError as e:
            return "I/O error({0}): {1}".format(e.errno, e.strerror)


if __name__ == '__main__':
    
    config = configparser.ConfigParser()
    config.read('config.ini')

    CCP_URL = os.getenv('CCP_URL') or  config['DEFAULT']['CCP_URL']
    CCP_USERNAME = os.getenv('CCP_USERNAME') or  config['DEFAULT']['CCP_USERNAME']
    CCP_PASSWORD = os.getenv('CCP_PASSWORD') or  config['DEFAULT']['CCP_PASSWORD']
    NEW_CLUSTER_PROPERTIES = os.getenv('NEW_CLUSTER_PROPERTIES') or  config['DEFAULT']['NEW_CLUSTER_PROPERTIES']

    ccp = CCP(CCP_URL,CCP_USERNAME,CCP_PASSWORD)

    login =  ccp.login()

    if not login:
        print ("There was an issue with login: " + login.text)

    response = ccp.getClusters()
    
    if response:
        for cluster in response.json():
            print(cluster)
    else:
        print (response.text)

    response = ccp.deployNewClusterFromFile(NEW_CLUSTER_PROPERTIES)

    print(response.text)

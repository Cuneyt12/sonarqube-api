from pydoc import doc
from requests.auth import HTTPBasicAuth
import requests
from sonarqube import SonarQubeClient
import json
from math import *
import os
from genericpath import exists

import CreateDirectory

username = "admin"  # http://localhost:9000 kullanıcı adı
password = "cuneyt"  # http://localhost:9000  giriş şifresi


def listAllDetails(projectKey, type, path):
    i = 0
    count = 0
    pageCount = 5
    detayPath = path + "\\" + projectKey
    CreateDirectory.create(detayPath)
    detay = open(detayPath + "\\" + type + ".txt", "w")

    while i < pageCount:
       
        data = requests.get(
            'http://localhost:9000/api/issues/search?componentKeys=' + projectKey + '&s=FILE_LINE&resolved=false&types=' + type + '&p=' + str(
                (i + 1)) +
            '&ps=500&organization=default-organization&facets=severities%2Ctypes&additionalFields=_all',
            auth=HTTPBasicAuth(username, password))
        json_data = data.json()
        total_data = json_data["total"]
        pageCount = ceil(total_data / 500)

        if total_data == 0:
            return
        for j in range(500):
            if count < total_data:
                detay.write(str(count + 1) + "\n")
                detay.write(str(json_data["issues"][j]["message"]) + " | Severity: " + str(json_data["issues"][j]["severity"]) +
                            "\nComponent: " + str(json_data["issues"][j]["component"]) + "\n")
                count += 1
        if count == 10000:
            break
        i += 1
#https://github.com/google/guava.git
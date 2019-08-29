#!/usr/bin/env python3
# encoding: utf-8

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from pymemcache.client.base import Client
import json
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import time

client = Client(('127.0.0.1', 11211))

def misppullandset(dataType):
  headers={'Authorization':'<MISP API-KEY>','Accept':'application/json','Content-type':'application/json'}
  data=json.dumps({"returnFormat":"json","type":dataType,"tags":"Feed-%","to_ids":"yes","includeEventTags":"yes","includeContext":"yes"})
  try:
    response = requests.post('https://<MISP IP>/attributes/restSearch',headers=headers,data=data,verify=False)
    data=response.json()
    if data:
      for item in data["response"]["Attribute"]:
        client.set(str(item['type'] + '-' + item['value']), item['value'], 150)

  except Exception as e:
    with open('/var/log/misppullLog.txt','w') as file:
      file.write('misppull failed with error: ' + str(e) + '\n')


def ransomwarepullandset():
  url='https://ransomwaretracker.abuse.ch/downloads/RW_DOMBL.txt'
  try:
    response=requests.get(url)
    if(response):
      for line in response.text.splitlines():
        if(line.startswith('#') == False):
          client.set(str(line),'ransomwaretracker-domain', 150)
  except Exception as e:
    with open('/var/log/misppullLog.txt','w') as file:
      file.write('ransomwarepull failed with error: ' + str(e) + '\n')



if __name__ == '__main__':
  run_indefinitely = True
#  dataTypes={'domain', 'ip-%', 'md5', 'sha1','sha256'}
  dataTypes={'domain', 'ip-%'}
  while run_indefinitely:
    for dt in dataTypes:
      misppullandset(dt)
    ransomwarepullandset()
    time.sleep(60)

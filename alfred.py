#!/usr/bin/env python3
import subprocess
import json
import jq

class alfred:
  def __init__(self,socket):
    self.socket = socket

  def datastats(self):
    if len(self.socket) > 1:
      for i in range(len(self.socket)):
        databucket = json.loads(subprocess.check_output(["alfred-json","-s",self.socket[i],"-r","158","-f","json","-z"]).decode("utf-8"))
        statsbucket = json.loads(subprocess.check_output(["alfred-json","-s",self.socket[i],"-r","159","-f","json","-z"]).decode("utf-8"))

        if i == 0:
          output_data = databucket.copy()
          output_stats = statsbucket.copy()
        else:
          output_data.update(databucket)
          output_stats.update(statsbucket)
    else:
        output_data = json.loads(subprocess.check_output(["alfred-json","-s",self.socket[0],"-r","158","-f","json","-z"]).decode("utf-8"))
        output_stats = json.loads(subprocess.check_output(["alfred-json","-s",self.socket[0],"-r","159","-f","json","-z"]).decode("utf-8"))

    alfred_all = jq.jq(".[0] * .[1]").transform([output_data,output_stats])
    return alfred_all

  def aliases(self):
    alfred_data = self.datastats()

    alias = {}
    for mac,node in alfred_data.items():
      node_alias = {}
      if 'location' in node:
        try:
          node_alias['gps'] = str(node['location']['latitude']) + ' ' + str(node['location']['longitude'])
        except:
          pass

      try:
        node_alias['firmware'] = node['software']['firmware']['release']
      except KeyError:
        pass

      try:
        node_alias['clientcount'] = node['clients']['total']
      except KeyError:
        pass

      try:
        node_alias['hardware'] = node['hardware']['model']
      except:
        pass

      try:
        node_alias['autoupdater_state'] = node['software']['autoupdater']['enabled']
      except:
        pass

      try:
        node_alias['autoupdater_branch'] = node['software']['autoupdater']['branch']
      except:
        pass

      try:
        node_alias['uptime'] = str(node['uptime'])
      except:
        pass

      try:
        node_alias['batman'] = node['software']['batman-adv']['version']
      except:
        pass

      try:
        node_alias['gateway'] = node['gateway']
      except:
        pass

      try:
        node_alias['addresses'] = node['network']['addresses']
      except:
        pass

      try:
        node_alias['id'] = node['network']['mac']
      except KeyError:
        pass

      if 'hostname' in node:
        node_alias['name'] = node['hostname']
      elif 'name' in node:
        node_alias['name'] = node['name']
      if len(node_alias):
        alias[mac] = node_alias
    return alias

if __name__ == "__main__":
  ad = alfred()
  al = ad.aliases()
  print(al)

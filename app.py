import requests
import time
import os
import json
from prometheus_client import start_http_server
from prometheus_client.core import GaugeMetricFamily, REGISTRY

api_login = os.environ.get("api_login")
api_pass = os.environ.get("api_pass")

def get_metrics():
    domain_dict = list()
    mail_in = list()
    mail_out = list()
    r = requests.get(f'https://{os.environ.get("api_url")}/admin/api/v1/domains?page=1&paging=50', auth=(api_login, api_pass))
    result = json.loads(r.text)
    for i in range(0, len(result['results'])):
      r = requests.get(f'https://{os.environ.get("api_url")}/admin/api/v1/domains/{result["results"][i]["name"]}/stats', auth=(api_login, api_pass))
      domain_stats = list(json.loads(r.text).values())[-1]
      domain_dict.append({f'{result["results"][i]["name"]}_in':domain_stats["in"]})
      domain_dict.append({f'{result["results"][i]["name"]}_out':domain_stats["out"]})
    r = requests.get(f'https://{os.environ.get("api_url")}/admin/api/v1/boxes?page=1&paging=50000', auth=(api_login, api_pass))
    maillist = json.loads(r.text)
    for i in range(0, len(maillist['results'])):
      email = maillist['results'][i]["address"]
      r = requests.get(f'https://{os.environ.get("api_url")}/admin/api/v1/boxes/{email}/stats', auth=(api_login, api_pass))
      result = json.loads(r.text)
      stats = list(result.values())[-1]    
      mail_in.append({f'{email}_in':stats["in"]})
      mail_out.append({f'{email}_out':stats["out"]})
    return domain_dict, mail_in, mail_out    

class CustomCollector(object):
    def __init__(self):
        pass
    
    def collect(self):
      list_of_metrics = get_metrics()
      domains = GaugeMetricFamily(f'{os.environ.get("metric_name")}_domains', 'send/receive stats by domain', labels=["domains"])
      for keys in list_of_metrics[0]:
        for key in keys:
          domains.add_metric([key], keys[key])
      yield domains
      
      mail_in = GaugeMetricFamily(f'{os.environ.get("metric_name")}_mailbox_in', 'receive stats by mailbox', labels=["mailbox"])
      for keys in list_of_metrics[1]:
        for key in keys:
          mail_in.add_metric([key], keys[key])
      yield mail_in
    
      mail_out = GaugeMetricFamily(f'{os.environ.get("metric_name")}_mailbox_out', 'send stats by mailbox', labels=["mailbox"])
      for keys in list_of_metrics[2]:
        for key in keys:
          mail_out.add_metric([key], keys[key])
      yield mail_out

if __name__ == "__main__":
    start_http_server(8080)
    REGISTRY.register(CustomCollector())
    while True: 
      time.sleep(int(os.environ.get("update_freqency")))
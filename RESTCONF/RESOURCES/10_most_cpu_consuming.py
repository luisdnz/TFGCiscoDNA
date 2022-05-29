import json

from numpy import sort

with open(f"RESOURCES/cpu-resources.json", "r") as f:
        json = json.loads(f.read())

process_list = json["Cisco-IOS-XE-process-cpu-oper:cpu-usage"]["cpu-utilization"]["cpu-usage-processes"]["cpu-usage-process"]

ten_most_consuming = [None]*10
for process in process_list:
    inserted=False
    for i in range(0,10):
        if(ten_most_consuming[i]==None and not inserted):
                ten_most_consuming[i] = process
                inserted=True
        else:
            if inserted==False and int(process["avg-run-time"])>int(ten_most_consuming[i]["avg-run-time"]):
                ten_most_consuming[i] = process
                inserted=True

for p in ten_most_consuming:
    print(p)

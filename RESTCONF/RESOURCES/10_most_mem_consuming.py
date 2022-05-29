import json


with open(f"RESOURCES/mem-resources.json", "r") as f:
        json = json.loads(f.read())

process_list = json["Cisco-IOS-XE-process-memory-oper:memory-usage-processes"]["memory-usage-process"]

ten_most_consuming = [None]*10
for process in process_list:
    inserted=False
    for i in range(0,10):
        if(ten_most_consuming[i]==None and not inserted):
                ten_most_consuming[i] = process
                inserted=True
        else:
            if inserted==False and int(process["holding-memory"])>int(ten_most_consuming[i]["holding-memory"]):
                ten_most_consuming[i] = process
                inserted=True

for p in ten_most_consuming:
    print(p)
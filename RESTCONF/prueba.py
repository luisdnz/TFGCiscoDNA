import time
day, hour, min, secs = map(int, time.strftime("%d %H %M %S").split())
print(day)
print(hour)
print(min)
print(secs)
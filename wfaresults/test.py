import os
import datetime

path = "test/ADXMomentum_WFA_25_20210401_20210801_5_1h_e1000.csv"
ctime = os.path.getmtime(path)

print(ctime)
print(datetime.datetime.utcfromtimestamp(ctime).strftime("%Y-%m-%d %H:%M:%S"))



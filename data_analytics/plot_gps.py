import matplotlib.pyplot as plt
import csv
import math
import statistics

lats = []
longs = []
with open('./gpslogs.csv', 'r') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',')
    for row in spamreader:
        lats.append(float(row[0]))
        longs.append(float(row[1]))

point_x = []
point_y = []
for i in range(len(lats)-1):
    distance = math.sqrt((lats[i]-lats[i+1])**2 + (longs[i]-longs[i+1])**2)
    if distance < 1e-5:
        point_x.append(lats[i])
        point_y.append(longs[i])

dev_lat = statistics.stdev(lats)
dev_long = statistics.stdev(longs)
print("raw stddev: {}, {}".format(dev_lat, dev_long))

dev_lat_f = statistics.stdev(point_x)
dev_long_f = statistics.stdev(point_y)
print("filtered stddev: {}, {}".format(dev_lat_f, dev_long_f))

avg_lat = (statistics.mean(lats))
avg_long = statistics.mean(longs)
print("Raw Mean: {}, {}".format(avg_lat, avg_long))

avg_lat_filter = (statistics.mean(point_x))
avg_long_filter = statistics.mean(point_y)
print("Filtered Mean: {}, {}".format(avg_lat_filter, avg_long_filter))

plt.plot(
         lats, longs, 'b',
         point_x, point_y, 'y',
         avg_lat, avg_long, 'ro',
         avg_lat_filter, avg_long_filter, 'go'
        )
plt.show()

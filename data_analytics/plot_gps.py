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
# print("raw stddev: {}, {}".format(dev_lat, dev_long))


avg_lat = (statistics.mean(lats))
avg_long = statistics.mean(longs)
# print("Raw Mean: {}, {}".format(avg_lat, avg_long))


def g_h_filter(data, x0, dx, g, h, dt=1.):
    x_est = x0
    results = []
    for z in data:
        #prediction step
        x_pred = x_est + (dx*dt)
        dx = dx

        # update step
        residual = z - x_pred
        dx = dx    + h * (residual) / dt
        x_est  = x_pred + g * residual
        results.append(x_est)
    return results

filtered_lat = g_h_filter(lats, 1, 0, 0.3, 0.01)
filtered_lon = g_h_filter(longs, 1, 0, 0.3, 0.01)

# avg_lat_filter = (statistics.mean(point_x))
# avg_long_filter = statistics.mean(point_y)
# print("Filtered Mean: {}, {}".format(avg_lat_filter, avg_long_filter))

dev_lat_f = statistics.stdev(filtered_lat)
dev_long_f = statistics.stdev(filtered_lon)
# print("filtered stddev: {}, {}".format(dev_lat_f, dev_long_f))

points = zip(filtered_lat, filtered_lon)
for x in points:
    print("{},{}".format(x[0], x[1]))

plt.plot(
         lats, longs, 'b',
         # filtered_lat, filtered_lon, 'y',
         avg_lat, avg_long, 'ro',
         # avg_lat_filter, avg_long_filter, 'go',
         # [avg_lat, avg_lat+dev_lat], [avg_long, avg_long+dev_long], 'g'
        )
plt.show()

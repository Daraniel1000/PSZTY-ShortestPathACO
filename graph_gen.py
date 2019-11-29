import sys
import random as rd
import time

rd.seed(time.time())
size = 17
max_weight = 50
odds = 0.15
if len(sys.argv) > 1:
	size = int(sys.argv[1])
if len(sys.argv) > 2:
	max_weight = int(sys.argv[2])
if len(sys.argv) > 3:
	odds = float(sys.argv[3])

rd.seed()
start = rd.randint(1, size)
end = rd.randint(1, size)
while end == start:
	end = rd.randint(1, size)

fp = open("out.txt", "w")
fp.write("%d %d %d\n" % (start, end, size))

for i in range(1, size+1):
	for j in range(i, size+1):
		if i == j:
			continue
		if rd.random() < odds:
			fp.write("%d %d %d\n" % (i, j, rd.randint(1,max_weight)))
fp.close()
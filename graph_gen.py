import sys
import random as rd

size = 10
max_weight = 20
if len(sys.argv) > 1:
	size = int(sys.argv[1])
if len(sys.argv) > 2:
	max_weight = int(sys.argv[2])

rd.seed()
start = rd.randint(1, size)
end = rd.randint(1, size)
while end == start:
	end = rd.randint(1, size)

fp = open("out.txt", "w")
fp.write("%d %d %d\n" % (start, end, size))

for i in range(1, size):
	for j in range(1, size):
		if rd.random() < 0.33:
			fp.write("%d %d %d\n" % (i, j, rd.randint(1,max_weight)))
fp.close()
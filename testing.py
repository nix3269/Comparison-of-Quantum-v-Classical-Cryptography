import time;
import csv;

inp = input("Enter Number of rounds and filename")
rounds, filename = inp.split(" ")
name, ext= filename.split(".")
f = open(rounds+"_"+name+'_data.csv', 'w')
writer = csv.writer(f)
print(rounds, filename)
for i in range(int(rounds)):
	now = time.time()
	exec(open(filename).read())
	after = time.time()
	row = [now, after]
	writer.writerow(row)
f.close()
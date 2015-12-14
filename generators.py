mygenerator = (x*x for x in range(3))

for i in mygenerator:
	print(i)

# should NOT run again
for i in mygenerator:
	print(i)
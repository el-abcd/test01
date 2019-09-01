from pprint import pprint as pp

a = [1,3,5,7,9, None]
b = [x/2.0 for x in range(20)]
c = [2,4,6,8,10,20]

for x, y, z in zip(a,b,c):
    print "{}, {}, {}".format(x,y,z)

print "done!"


# zip with dicts:

d = dict(zip(a,b)) # Keys, Values
pp(d)

# reversed
list(reversed(a))
# returns an iterator!!!

# all:



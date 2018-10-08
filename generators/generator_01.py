

mygen = (x**2 for x in range(10))

print type(mygen)

# print len(mygen)

print "start run 1"
for i in mygen:
    print( dir(i))
    print i

print "start run 2"
for i in mygen:
    print i
print "end run 2"

def createGenerator():
    i = 0

    while (i < 10):
        i += 1
        yield i

a = createGenerator()
print a
for i in a:
    print i


import itertools

horses = [1,2,3,4]

races = itertools.permutations(horses)
print(races) # just prints the generator
print list(itertools.permutations(horses))


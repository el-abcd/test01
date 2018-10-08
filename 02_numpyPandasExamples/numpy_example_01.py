
# https://groups.google.com/a/google.com/forum/#!topic/python-tips/7U2jlkEloYk

import numpy as np
x = np.random.random(1000)

y = x + 1

x = np.random.rand(5,3)

#sub array
print x[2:4,2]

x.mean()

x = np.arange(4)
xx = x.reshape(4,1)
y = np.ones(5)
z = np.ones((3,4))

print (xx + y)

print "Example for z array"
print(x)
print(z)
print(x+z)

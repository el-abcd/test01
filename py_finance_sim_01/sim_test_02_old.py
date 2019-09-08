import simpy

"""
def sub(env):
   yield env.timeout(1)
   env.exit(23)

def parent(env):
   ret = yield env.process(sub(env))
   env.exit(23)

env = simpy.Environment()
env.run(env.process(parent(env)))
"""

# RESOURCES
import simpy
import pprint as pp

def resource_user(env, resource):
    request = resource.request()  # Generate a request event
    yield request                 # Wait for access
    print "Waiting {}".format(env.now)
    yield env.timeout(5)          # Do something
    print "Done waiting! {}".format(env.now)
    print dir(resource)
    pp.pprint(resource)
    print('%d of %d slots are allocated.' % (resource.count, resource.capacity))
    print('  Users:', resource.users)
    print('  Queued events:', resource.queue)
    resource.release(request)     # Release the resource

env = simpy.Environment()
res = simpy.Resource(env, capacity=1)
user = env.process(resource_user(env, res))
env.run()
print ("Done!!!")


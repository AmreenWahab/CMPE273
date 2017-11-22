'''
################################## slave.py #############################
# 
################################## slave.py #############################
'''
import grpc
import replicator_pb2
import argparse
import rocksdb

PORT = 3000

slavedb = rocksdb.DB("slavedb1.db", rocksdb.Options(create_if_missing=True))

class Slave():
    
    def __init__(self, host='0.0.0.0', port=PORT):
        self.channel = grpc.insecure_channel('%s:%d' % (host, port))
        self.stub = replicator_pb2.ReplicatorStub(self.channel)
        
    def run(self):
        
        action = self.stub.slaveConnector(replicator_pb2.SlaveRequest())
        

        for a in action:
            if a.action == 'put':
                print("# Put {} : {} to slave db".format(a.key, a.value))
                slavedb.put(a.key, a.value)
                print ("# Successfulyy added data to slavedb")
                print ("# Key in slave db : "+a.key.decode()+"     Value in slavedb : " + slavedb.get(a.key.decode()))

            elif a.action == 'delete':
                print ("# Delete {} from slave db".format(a.key))
                slavedb.delete(a.key)
                print ("# Successfully deleted")
    
if __name__ == "__main__":
    slave = Slave()
    slave.run()

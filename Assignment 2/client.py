'''
################################## client.py #############################
# 
################################## client.py #############################
'''
import grpc
import replicator_pb2
import argparse

PORT = 3000

class MainClient():
    
    def __init__(self, host='0.0.0.0', port=PORT):
        self.channel = grpc.insecure_channel('%s:%d' % (host, port))
        self.stub = replicator_pb2.ReplicatorStub(self.channel)

    def put(self, key, value):
        return self.stub.put(replicator_pb2.Request(key=key ,value=value))

    def delete(self, key):
        return self.stub.delete(replicator_pb2.DeleteRequest(key=key))

def main():
   
    client = MainClient()

    print ("# PUT Request 1 :  key = a   value = foo ")
    resp = client.put('a','foo')
    print ("# PUT Response: key = " +resp.key + "value = "+resp.value)
    
    print ("# PUT Request 2 :  key = b   value = bar ")
    resp1 = client.put('b','bar')
    print ("# PUT Response: key = " +resp1.key + "   value = "+resp1.value)

    print("# DELETE Request  1: ")
    resp2 = client.delete(resp.key)
    print("# DELETE Response: key deleted = " +resp2.key+"  value deleted = " +resp2.value) 


if __name__ == "__main__":
    main()
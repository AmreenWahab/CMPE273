'''
################################## server.py #############################
# Lab1 gRPC RocksDB Server 
################################## server.py #############################
'''
import time
import grpc
import replicator_pb2
import replicator_pb2_grpc
import rocksdb

import Queue
from concurrent import futures

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

class ReplicatorServicer(replicator_pb2.ReplicatorServicer):
    def __init__(self):
        self.db = rocksdb.DB("masterdb.db", rocksdb.Options(create_if_missing=True))
        #self.db = rocksdb.DB("slavedb.db", rocksdb.Options(create_if_missing=True))
        self.queue = Queue.Queue()

    def replicate(db_action):
        def wrapper(self, request, context):
            
            if(db_action.__name__=="delete"):
                value = (self.db.get(request.key.encode()))
                action = replicator_pb2.SlaveResponse(action = db_action.__name__, key=request.key.encode(), value=value)
            else:
                action = replicator_pb2.SlaveResponse(action = db_action.__name__, key=request.key.encode(), value=request.value.encode())
            
            self.queue.put(action)
            print ("DB queue sent to slave")
            return db_action(self, request, context)

        return wrapper

    @replicate
    def put(self, request, context):
        print ("put")
        #key = uuid.uuid4().hex
        self.db.put(request.key.encode(), request.value.encode())
        return replicator_pb2.Response(key=request.key,value=request.value)
    
    @replicate
    def delete(self, request, context):
        print ("delete")
        value = (self.db.get(request.key.encode())).decode()
        self.db.delete(request.key.encode())
        return replicator_pb2.Response(key=request.key, value=value)

    def slaveConnector(self, request, context):
        '''
        slave connects with master and master sends db_actions from queue to slave
        '''
        print ("Slave Connected")
        while True:
            while not self.queue.empty():
                    yield self.queue.get() 
                    print ("Successful replication of data on slave side") 


def run(host, port):
    '''
        Run the GRPC server
    '''
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    replicator_pb2_grpc.add_ReplicatorServicer_to_server(ReplicatorServicer(), server)
    server.add_insecure_port('%s:%d' % (host, port))
    server.start()

    try:
        while True:
            print ("Server started at...%d" % port)
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    run('0.0.0.0', 3000)
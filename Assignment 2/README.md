## Requirements

Implement a RocksDB replication in Python using the design from this [C++ replicator.](https://medium.com/@Pinterest_Engineering/open-sourcing-rocksplicator-a-real-time-rocksdb-data-replicator-558cd3847a9d)   

Differences form the replicator are:
Use GRPC Python server instead of Thrift server.
Explore GRPC sync, async, and streaming.

## Server - master.py
```sh
python master.py
```
## Client - client.py
```sh
python client.py
```
        
**Expected Output on Client**
```sh
# PUT Request 1 :  key = a   value = foo  
# PUT Response: key = avalue = foo 
# PUT Request 2 :  key = b   value = bar  
# PUT Response: key = bvalue = bar 
# DELETE Request  1:  
# DELETE Response: key deleted = a value deleted = foo
```
## Slave - slave.py 
```sh
python slave.py
```
**Expected Output on Slave**
```sh
# Put a:foo to slave db
# Successfully added data to slavedb 
# Key in slave db : a     Value in slavedb : foo

# Put b:bar to slave db 
# Successfully added data to slavedb 
# Key in slave db : b     Value in slavedb : bar

# Delete a from slave db
# Successfully deleted
```

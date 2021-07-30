import boto3
import json
import time

from modules.Util import get_config_consumer

if __name__ == "__main__":
    # Get my config parameters
    my_env = get_config_consumer()
    
    # Connection with kinesis
    kinesis = boto3.client('kinesis')

    # Get the shard with describe_stream
    response = kinesis.describe_stream(StreamName = my_env.STREAM_NAME)
    shard_id = response['StreamDescription']['Shards'][0]['ShardId']

    # Get the shard_iterator
    shard_iterator = kinesis.get_shard_iterator(
        StreamName = my_env.STREAM_NAME,
        ShardId = shard_id,
        ShardIteratorType = 'LATEST'
    )

    my_shard_iterator = shard_iterator['ShardIterator']

    record_response = kinesis.get_records(
        ShardIterator = my_shard_iterator,
        Limit = 1
    )

    # Go through all the records in the stream
    while 'NextShardIterator' in record_response:
        record_response = kinesis.get_records(
            ShardIterator = record_response['NextShardIterator'],
            Limit = 1
        )
        
        print("ShardIter : " + record_response['NextShardIterator'])
        
        try: 
            print(record_response['Records'][0]['Data'])
        except Exception:
            print("No hay datos.")
            
        time.sleep(5)
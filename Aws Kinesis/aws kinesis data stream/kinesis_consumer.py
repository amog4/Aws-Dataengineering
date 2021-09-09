import boto3,logging,sys,os,json


try:
    os.mkdir('logs')
except:
    pass

logging.basicConfig(filename="logs/get_records_consumer.txt",
                    format='%(levelname)s %(asctime)s :: %(message)s',
                    filemode='w',level=logging.INFO)


logging.info('Start program')


class shard(object):

    def __init__(self,shard,iterator):
        self.shard = shard
        self.iterator = iterator


def main(args):
    logging.info('Starting consumer')

    args1 = args[1]
  

    session = boto3.Session(profile_name='working-dev')
    kinesis = session.client('kinesis')

    # get all the shards and itterators
    get_iterator = []
    get_shards = kinesis.list_shards(StreamName = args1)
    has_shards = bool(get_shards['Shards'])

    while has_shards:
        for shards in get_shards['Shards']:
            shard_id =  shards['ShardId']

            response = kinesis.get_shard_iterator(StreamName=args1,
                                                      ShardId=shard_id,
                                                      ShardIteratorType='TRIM_HORIZON')

            

            get_iterator.append(shard(shard_id,response['ShardIterator']))

            if 'NextToken' in get_shards:
                get_shards = kinesis.list_shards(StreamName = args1,NextToken=get_shards['NextToken'])
                has_shards = bool(get_shards['Shards'])
            else:
                has_shards= False
          
    for iter in get_iterator:
     
        try:
            response = kinesis.get_records(
                ShardIterator=iter.iterator,
                Limit=123
            )

            for r in response['Records']:
                data = json.loads(r['Data'].decode('utf-8'))
                print(data)
            while True:
                if 'NextShardIterator' in response:
                    response = kinesis.get_records(
                    ShardIterator=response['NextShardIterator'],
                    Limit=123
                )

                for r in response['Records']:
                    data = json.loads(r['Data'].decode('utf8'))
                    print(data)
                else:
                    break
            
        
        except Exception as e:

            logging.error({'error':str(e),'iterator':iter})


if __name__ == '__main__':
    main(args=sys.argv)







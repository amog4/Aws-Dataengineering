import boto3,sys,json,time,os
from generate_data import get_orders
import logging

try:
    os.mkdir('logs')
except:
    pass

logging.basicConfig(filename="logs/put_record_produce.txt",
                    format='%(levelname)s %(asctime)s :: %(message)s',
                    filemode='w',level=logging.INFO)

logging.info('Start program')

def main(args):
    args1 = args[1]
    logging.info('Get args')
    session = boto3.Session(profile_name='working-dev')
    Kinesis = session.client('kinesis')
    logging.info('Connect to client')
    while True:
        logging.info('Get orders')
        orders = get_orders()

        try:
            put_records = Kinesis.put_record(StreamName=args1,
                        Data=json.dumps(orders).encode('utf8'),
                        PartitionKey=orders['order_id'])

            logging.info('Push Record {orders}')
            # returns 
            logging.info(f"sequence key:{put_records['SequenceNumber']} and shard id {put_records['ShardId']}")

        except Exception as e:
            logging.error({ 'error' :str(e),'order':orders })

    time.sleep(3)


if __name__ == '__main__':
    main(sys.argv)


    

        
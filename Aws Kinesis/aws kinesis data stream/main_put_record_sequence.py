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
        orders_list = []
        logging.info('Get orders')
        orders = get_orders()
        order_d = {'Data':json.dumps(orders).encode('utf8'),
                            'PartitionKey':orders['order_id']}

        orders_list.append((orders,order_d ))

        if len(orders_list) > 20:
            try:
                orders,records = zip(list,orders_list)
                put_records = Kinesis.put_records(StreamName=args1,
                            Records = records)
                for ind, r in put_records:
                    if r.get('ErrorCode'):

                        err_msg = r['ErrorMessage']
                        logging.error({ 'error' :str(e),'order':orders[ind] })
                    else:
                        logging.info('Push Record {orders}')
                        # returns 
                        logging.info(f"sequence key:{r['SequenceNumber']} and shard id {r['ShardId']}")

            except Exception as e:
                logging.error({ 'error' :str(e),'order':orders })
        orders_list.clear()
        time.sleep(0.3)


if __name__ == '__main__':
    main(sys.argv)


    

        
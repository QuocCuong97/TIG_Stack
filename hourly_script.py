import datetime
import logging
import os

import mysql.connector as mariadb
import numpy as np
import pymongo
from influxdb import InfluxDBClient

from config import config

ENV = os.environ.get('ENV', 'development')
CONF = config[ENV]

def get_mariadb_connect():
    mydb = mariadb.connect(host=CONF.MARIADB_HOST, 
                           user=CONF.MARIADB_USER, 
                           password=CONF.MARIADB_PASSWORD, 
                           database=CONF.MARIADB_DB_NAME)
    return mydb

def get_influxdb_connect():
    myinflux = InfluxDBClient(host=CONF.INFLUXDB_HOST, 
                              port=CONF.INFLUXDB_PORT, 
                              username=CONF.INFLUXDB_USER, 
                              password=CONF.INFLUXDB_PASSWORD,
                              database=CONF.INFLUXDB_DB_NAME)
    return myinflux

def calculate_data_transfer(start_time, end_time):
    try:
        mydb = get_mariadb_connect()
        mycursor = mydb.cursor()
    except:
        logging.error("Can't connect to OpenStack database")

    # Get list network WAN
    mycursor.execute("select id from networks where status='ACTIVE' and name like 'EXT_DIRECTNET%';")
    list_network_wan = []
    list_network_raw = mycursor.fetchall()
    for network in list_network_raw:
        list_network_wan.append(network[0])

    # Get list instance with TAP interface is WAN
    list_instance = []
    mycursor.execute("select id,device_id from ports where device_owner like 'compute%' and network_id in {}".format(str(tuple(list_network_wan))[:-1]+ ')'))
    list_port_raw = mycursor.fetchall()
    for port in list_port_raw:
        signal = False
        for instance in list_instance:
            if port[1] == instance['id']:
                instance['wan'].append('tap' + port[0][:11])
                signal = True
        if signal == False:
            list_instance.append({'id': port[1], 'wan': ['tap' + port[0][:11]]})
    mydb.close() # Close connection to MariaDB

    try:
        myinflux = get_influxdb_connect()
    except:
        logging.error("Can't connect to InfluxDB")

    list_total = []

    for instance in list_instance:
        total = 0
        try:
            for wan in instance['wan']:
                query = 'select * from instances where tags1=$tags1 and tags5=$tags5 and tags10=$tags10 and time >= $start_time and time < $end_time'
                bind_params = {'tags1': instance['id'], 
                               'tags5': 'data_transfer_out', 
                               'tags10': wan, 
                               'start_time': start_time, 
                               'end_time': end_time}
                list_tx_points = list(myinflux.query(query, bind_params=bind_params))[0]
                list_number = []
                for tx_point in list_tx_points:
                    list_number.append(tx_point['value'])
                i = 1
                reset_point = []
                while i < len(list_number):
                    if list_number[i] < list_number[i-1]:
                        reset_point.append(i)
                    i += 1
                point_arr = np.asarray(list_number)
                new_arr = np.split(point_arr, reset_point)
                result = 0
                if len(new_arr) == 1:
                    result += new_arr[0][-1] - new_arr[0][0]
                else:
                    for array in new_arr:
                        if array.size == 1:
                            result += array[0]
                        else:
                            result += (array[-1] - array[0])
                total += result

        except:
            #logging.warning('No record found for instance {}'.format(instance['id']))
            total = 0

        start_time_iso = datetime.datetime.fromtimestamp(start_time // 1000000000 + 30).isoformat()
        end_time_iso = datetime.datetime.fromtimestamp(end_time // 1000000000).isoformat()

        list_total.append({'time_from': start_time_iso, 'time_to': end_time_iso, "instance": instance['id'], "metric": total})

    myinflux.close() # Close connection to InfluxDB

    return list_total

def send_to_mongodb(data):
    client = pymongo.MongoClient(host=CONF.MONGODB_HOST,
                                 port=CONF.MONGODB_PORT,
                                 username=CONF.MONGODB_USER,
                                 password=CONF.MONGODB_PASSWORD,
                                 authSource=CONF.MONGO_DB_NAME
                                )
    try:
        mydb = client[CONF.MONGO_DB_NAME]
        mycol = mydb[CONF.COL_NAME_HOUR]
        mycol.insert_many(data)
    except:
        logging.error("Can't connect to MongoDB")

def hour_rounder(time):
    return (time.replace(second=0, microsecond=0, minute=0, hour=time.hour).timestamp())

if __name__ == '__main__':
    logging.basicConfig(filename='error.log', filemode='a', format='%(asctime)s  %(levelname)s  %(message)s')
    
    now = datetime.datetime.now()
    end_time = hour_rounder(now)
    start_time = end_time - 3630

    # Calculate data tranfer from InfluxDB
    list_metric = calculate_data_transfer(start_time * 1000000000, 
                                          end_time * 1000000000)

    # Send metric to MongoDB
    send_to_mongodb(list_metric)

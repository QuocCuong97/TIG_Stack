import logging
import numpy as np
from influxdb import InfluxDBClient

client = InfluxDBClient(host='localhost', port=8086, database='diamond')
logging.basicConfig(filename='error.log', filemode='a', format='%(asctime)s  %(levelname)s  %(message)s')

list_instance_raw = list(client.query("show tag values from instances with key=tags1",))[0]
list_instance = []
for item in list_instance_raw:
    instance = item['value']
    list_instance.append(instance)
    print(instance)

for instance in list_instance:
    try:
        list_tx_points = list(client.query("select * from instances where tags10 = '1500' and tags5 = 'data_transfer_out' and tags1 = '{}' and time >= now()-2h+30s".format(instance)))[0]
        list_number = []
        for tx_point in list_tx_points:
            list_number.append(tx_point['value'])
        point_arr = np.asarray(list_number)
        zero_point = np.where(point_arr == 0)
        new_arr = np.split(point_arr, zero_point[0])
        result = 0
        if len(new_arr) == 1:
            result += new_arr[0][-1] - new_arr[0][0]
        else:
            
            for array in new_arr:
                if array.size == 1:
                    result += array[0]
                else:
                    result += (array[-1] - array[0])
    except Exception as ex:
        logging.error('No record found!')

import datetime
import os

import pymongo

from config import config

ENV = os.environ.get('ENV', 'development')
CONF = config[ENV]

def convert_iso_time(time):
    return datetime.datetime.strptime(time, "%Y-%m-%dT%H:%M:%S")

if __name__ == '__main__':
    client = pymongo.MongoClient(host=CONF.MONGODB_HOST,
                                 port=CONF.MONGODB_PORT,
                                 username=CONF.MONGODB_USER,
                                 password=CONF.MONGODB_PASSWORD,
                                 authSource=CONF.MONGO_DB_NAME
                                )
    mydb = client["{}".format(CONF.MONGO_DB_NAME)]
    mycol = mydb["{}".format(CONF.COL_NAME_HOUR)]

    yesterday = (datetime.date.today() - datetime.timedelta(days=1)).strftime("%d-%m-%Y")
    list_instances = mycol.distinct("instance")
    data_list = []

    for instance in list_instances:
        total = 0
        for x in mycol.find({"instance": instance}):
            if convert_iso_time(x['time_from']).strftime("%d-%m-%Y") == yesterday:
                total += x['metric']
        data = {"time": str(yesterday), "instance": instance, "metric": total}
        data_list.append(data)
    mycol = mydb["{}".format(CONF.COL_NAME_DAY)]
    mycol.insert_many(data_list)

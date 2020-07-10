import pymongo
from pymongo.collection import Collection

client = pymongo.MongoClient(host='127.0.0.1', port=27017)
db = client['u2_douyin']


def handle_mongodb_save_data(item):
    # 抖音
    if item['item_type'] == 'douyin_info':
        douyin_data_collection = Collection(db, 'douyin_info')
        douyin_data_collection.insert(item)

    # 抖音
    if item['item_type'] == 'douyin_video':
        douyin_data_collection = Collection(db, 'douyin_video')
        douyin_data_collection.insert(item)

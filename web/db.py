import pymongo

# PATTERN
# "mongodb://your_mongo_username:your_mongo_password@database_container:27017/your_database_name"
client = pymongo.MongoClient("mongodb://root:rootpassword@db:27017/")

db = client["db"]
video = db["Video"]
result = db["Result"]


def add_new_video(json):
    record = video.insert_one(json)
    return record.inserted_id


def create_result_record(json):
    result.insert_one(json)
    return


def find_videos_by_name(title):
    return video.find({"title": {"$regex": title, "$options": "i"}})


def find_result_by_video_id(id):
    return result.find({"video_id": id})


def get_single_page(number):
    list = []
    for x in video.find().skip(10 * (int(number) - 1)).limit(10):
        print(x)
        for y in find_result_by_video_id(str(x['_id'])):
            del x['_id']
            del y['_id']
            del y['video_id']
            x.update(y)
            list.append(x)
    return list


def get_history_list(size):
    list = []
    for x in video.find().limit(int(size)):
        print(x)
        for y in find_result_by_video_id(str(x['_id'])):
            del x['_id']
            del y['_id']
            del y['video_id']
            x.update(y)
            list.append(x)
    return list


def get_search_results(title):
    list = []
    for x in find_videos_by_name(title):
        for y in find_result_by_video_id(str(x['_id'])):
            del x['_id']
            del y['_id']
            del y['video_id']
            x.update(y)
            list.append(x)
    return list


def drop():
    video.drop()
    result.drop()


if __name__ == '__main__':
    drop()

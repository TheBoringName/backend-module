import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017/")

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


def get_search_results(title):
    list = []
    for x in find_videos_by_name(title):
        for y in find_result_by_video_id(str(x['_id'])):
            del y['_id']
            list.append(y)
    return list


def drop():
    video.drop()
    result.drop()


if __name__ == '__main__':
    drop()

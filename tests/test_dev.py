import pytest
import mock

from session import session
import mongo


def test_area():
    resp = session.get("https://www.uoko.com/api/room/map?AreaId=3515&level=2&cityid=278")
    j = resp.json()
    mongo.collection.insert_many(j["data"])


def test_SubArea():
    """
db.getCollection('uoko').aggregate([
    { $group: {
        _id: "$AreaId",
        name: {$first:"$Name"},
        count: {$first:"$Count"},
    }}
 ])

    """

    for _id, Name in {AreaId["_id"]: AreaId["name"] for AreaId in mongo.collection.aggregate(pipeline=[
        {"$group": {
            "_id": "$AreaId",
            "name": {"$first": "$Name"},
            "count": {"$first": "$Count"},
        }},
    ])}.items():
        print(_id, Name)
        resp = session.get(f"https://www.uoko.com/api/room/map?cityid=278&level=3&AreaId=3515&SubAreaId={_id}")
        j = resp.json()
        mongo.collection.insert_many(j["data"])


def test_room():
    """
    https://www.uoko.com/api/room/list?CommunityIds=2ed6cfaf18de4d149ea999c0bf03b233&source=uoko&cityid=278&PageIndex=1

    :return:
    """

    for _id, Name in {AreaId["_id"]: AreaId["name"] for AreaId in mongo.collection.aggregate(pipeline=[
        {"$group": {
            "_id": "$Id",
            "name": {"$first": "$Name"},
        }},
    ])}.items():

        i = 1
        while i:
            print(_id, Name, i)
            resp = session.get(
                f"https://www.uoko.com/api/room/list?CommunityIds={_id}&source=uoko&cityid=278&PageIndex={i}")
            j = resp.json()

            if len(j["Items"]) == 0:
                break

            mongo.collection.insert_many(j['Items'])

            i += 1

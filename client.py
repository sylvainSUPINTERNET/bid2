import cv2
import os
import redis
from dotenv import load_dotenv
from PIL import Image
import numpy as np
load_dotenv()


r = redis.Redis(host=os.getenv('REDIS_URL'), port=os.getenv('REDIS_PORT'), db=0, username=os.getenv('REDIS_USER'), password=os.getenv('REDIS_PASSWORD'))



def read_frame()->None:
    # > Next entry ID that no consumer in this group has read
    # 0 last_id
    # $ next only
    last_id = "$"
    resp = r.xread(
                {"bid:leaderboard": last_id}, count=1, block=500
            )

    if resp:
        key, messages = resp[0]
        last_id, data = messages[0]
        
        
        # nparr = np.fromstring(data, np.uint8)
        # frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        # cv2.imshow('image', frame)
        
        
        data_dict = {k.decode("utf-8"): data[k] for k in data}
        
        d = np.frombuffer(data_dict["frame"], dtype="uint8")

        print(type(d))
        
        # cv2.imshow('frame', np.frombuffer(data_dict["frame"], dtype="uint8"))

        
        # data_dict["id"] = last_id.decode("utf-8")
        # data_dict["key"] = key.decode("utf-8")
        
        
        # print(type(data_dict["frame"]))
        # print(data_dict["frame"])
        # #cv2.imshow("image", Image.fromarray(data_dict["frame"]))        
        
        
        # # print("REDIS ID: ", last_id)
        # # # print("      --> ", bytes(data))
        # # print(data)
        # # cv2.imshow('frame', bytes(data))
        
        
    else:
        print("Nothing to read ...")


if __name__ == '__main__':
    while(True):
        read_frame()


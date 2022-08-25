import cv2
import os
import redis
import msgpack_numpy as m
from dotenv import load_dotenv
import base64
load_dotenv()
m.patch()


r = redis.Redis(host=os.getenv('REDIS_URL'), port=os.getenv('REDIS_PORT'), db=0, username=os.getenv('REDIS_USER'), password=os.getenv('REDIS_PASSWORD'))

# Nice: https://appdividend.com/2022/03/19/python-cv2-videocapture/
# cool : https://huogerac.hashnode.dev/using-redis-stream-with-python


if __name__ == '__main__':
    cap = cv2.VideoCapture('test.mp4')
    while( cap.isOpened() ):
        ret, frame = cap.read()
        cv2.imshow('frame', frame)
        print(frame.dtype)
        r.xadd("bid:leaderboard", {"frame": cv2.imencode('.jpg', frame)[1].tobytes()}, maxlen=1)
        print(frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
cap.release()
cv2.destroyAllWindows()
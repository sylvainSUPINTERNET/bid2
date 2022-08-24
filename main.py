import cv2
import os
import redis
from dotenv import load_dotenv
load_dotenv()

r = redis.Redis(host=os.getenv('REDIS_URL'), port=os.getenv('REDIS_PORT'), db=0, username=os.getenv('REDIS_USER'), password=os.getenv('REDIS_PASSWORD'))

# Nice: https://appdividend.com/2022/03/19/python-cv2-videocapture/



if __name__ == '__main__':
    cap = cv2.VideoCapture('test.mp4')
    while( cap.isOpened() ):
        ret, frame = cap.read()
        cv2.imshow('frame', frame)
        r.xadd("bid:leaderboard", {"frame": str(frame)}, maxlen=1)
        print(frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
cap.release()
cv2.destroyAllWindows()
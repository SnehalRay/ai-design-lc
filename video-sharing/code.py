'''
2254. Design Video Sharing Platform

You have a video sharing platform where users can upload and delete videos. Each video is a string of digits, where the ith digit of the string represents the content of the video at minute i. For example, the first digit represents the content at minute 0 in the video, the second digit represents the content at minute 1 in the video, and so on. Viewers of videos can also like and dislike videos. Internally, the platform keeps track of the number of views, likes, and dislikes on each video.

When a video is uploaded, it is associated with the smallest available integer videoId starting from 0. Once a video is deleted, the videoId associated with that video can be reused for another video.

Implement the VideoSharingPlatform class:

VideoSharingPlatform() Initializes the object.
int upload(String video) The user uploads a video. Return the videoId associated with the video.
void remove(int videoId) If there is a video associated with videoId, remove the video.
String watch(int videoId, int startMinute, int endMinute) If there is a video associated with videoId, increase the number of views on the video by 1 and return the substring of the video string starting at startMinute and ending at min(endMinute, video.length - 1) (inclusive). Otherwise, return "-1".
void like(int videoId) Increases the number of likes on the video associated with videoId by 1 if there is a video associated with videoId.
void dislike(int videoId) Increases the number of dislikes on the video associated with videoId by 1 if there is a video associated with videoId.
int[] getLikesAndDislikes(int videoId) Return a 0-indexed integer array values of length 2 where values[0] is the number of likes and values[1] is the number of dislikes on the video associated with videoId. If there is no video associated with videoId, return [-1].
int getViews(int videoId) Return the number of views on the video associated with videoId, if there is no video associated with videoId, return -1.




Video:
video_id
video_string
like_count
dislike_count
'''
import heapq
class Video:
    def __init__(self, video_id: int, video_string: str):
        self._video_id = video_id
        self._video_string = video_string
        self._like_count = 0
        self._dislike_count = 0
        self._view_count = 0

    @property
    def video_id(self) -> int:
        return self._video_id

    @property
    def video_string(self) -> str:
        return self._video_string

    @video_string.setter
    def video_string(self, value: str):
        self._video_string = value

    @property
    def like_count(self) -> int:
        return self._like_count

    @like_count.setter
    def like_count(self, value: int):
        if value < 0:
            raise ValueError("like_count cannot be negative")
        self._like_count = value

    @property
    def dislike_count(self) -> int:
        return self._dislike_count

    @dislike_count.setter
    def dislike_count(self, value: int):
        if value < 0:
            raise ValueError("dislike_count cannot be negative")
        self._dislike_count = value

    @property
    def view_count(self) -> int:
        return self._view_count

    @view_count.setter
    def view_count(self, value: int):
        if value < 0:
            raise ValueError("view_count cannot be negative")
        self._view_count = value


class VideoSharingPlatform:

    def __init__(self):
        self.video_map = {}
        self.vid_id = 0
        self.recycled_idx = [] #removed video idx

    def upload(self,video:str)->int:
        if self.recycled_idx:
            last_idx = heapq.heappop(self.recycled_idx)
        else:
            last_idx = self.vid_id
            self.vid_id+=1
        self.video_map[last_idx] = Video(last_idx, video)
        return last_idx

    def remove(self,videoId:int)->bool:
        if videoId not in self.video_map:
            return False
        del self.video_map[videoId]
        heapq.heappush(self.recycled_idx,videoId)
        return True
        

    def watch(self,videoId:int,startMinute:int, endMinute:int)->str:
        #increment the views
        #if end minute > len(video)-1: then clamp it the last index
        if videoId not in self.video_map:
            return None
        vid = self.video_map[videoId]
        if endMinute>=len(vid.video_string):
            endMinute = len(vid.video_string)-1
        req_vid = vid.video_string[startMinute:endMinute+1]
        vid.view_count = vid.view_count+1
        return req_vid
        

    def like(self,videoId:int)->None:
        if videoId not in self.video_map:
            return
        video = self.video_map[videoId]
        video.like_count+=1

    def dislike(self,videoId:int)->None:
        if videoId not in self.video_map:
            return
        video = self.video_map[videoId]
        video.dislike_count+=1
        

    def getLikeAndDislike(self,videoId:int)->list:
        #[like count, dislike count]
        if videoId not in self.video_map:
            return [-1,-1]
        video = self.video_map[videoId]

        like,dislike = video.like_count, video.dislike_count
        return [like,dislike]

    def get_views(self,videoId:int)->int:
        if videoId not in self.video_map:
            return -1
        video = self.video_map[videoId]
        return video.view_count


if __name__ == "__main__":
    vsp = VideoSharingPlatform()

    # Upload two videos
    id0 = vsp.upload("012345")   # id = 0
    id1 = vsp.upload("9876543")  # id = 1
    print(f"Uploaded IDs: {id0}, {id1}")  # 0, 1

    # Watch: clamp endMinute beyond length
    print(vsp.watch(id0, 0, 2))    # "012"
    print(vsp.watch(id0, 1, 100))  # "12345" (clamped)
    print(vsp.get_views(id0))      # 2

    # Like and dislike
    vsp.like(id1)
    vsp.like(id1)
    vsp.dislike(id1)
    print(vsp.getLikeAndDislike(id1))  # [2, 1]

    # Remove id0, then re-upload — should reuse id 0
    vsp.remove(id0)
    id2 = vsp.upload("111")
    print(f"Reused ID after remove: {id2}")  # 0

    # Operations on non-existent video
    print(vsp.watch(0, 0, 1))          # None  (id0 was deleted, id2 now holds slot 0 — watch id=99)
    print(vsp.watch(99, 0, 1))           # None
    print(vsp.getLikeAndDislike(99))     # [-1, -1]
    print(vsp.get_views(99))             # -1
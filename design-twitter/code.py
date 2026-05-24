'''

Design a simplified version of Twitter where users can post tweets, follow/unfollow another user, and is able to see the 10 most recent tweets in the user's news feed.

Implement the Twitter class:

Twitter() Initializes your twitter object.
void postTweet(int userId, int tweetId) Composes a new tweet with ID tweetId by the user userId. Each call to this function will be made with a unique tweetId.
List<Integer> getNewsFeed(int userId) Retrieves the 10 most recent tweet IDs in the user's news feed. Each item in the news feed must be posted by users who the user followed or by the user themself. Tweets must be ordered from most recent to least recent.
void follow(int followerId, int followeeId) The user with ID followerId started following the user with ID followeeId.
void unfollow(int followerId, int followeeId) The user with ID followerId started unfollowing the user with ID followeeId.
'''

import heapq
from collections import defaultdict
from typing import List

class Twitter:

    def __init__(self, max_feed_poll=10):
        self.follows = defaultdict(set) #user : users they follow
        self.posts = defaultdict(list) #user: posts in a list
        self.max_feed_poll = max_feed_poll
        self.count = 0

    def postTweet(self, userId: int, tweetId: int) -> None:
        #increment count
        self.posts[userId].append((self.count, tweetId))
        self.count+=1

    def getNewsFeed(self, userId: int) -> List:
        users = self.follows[userId] | {userId}
        heap = []
        for user in users:
            posts = self.posts[user]
            if posts:
                idx = len(posts) - 1
                count, tweetId = posts[idx]
                heapq.heappush(heap, (-count, tweetId, user, idx - 1))

        result = []
        while heap and len(result) < self.max_feed_poll:
            neg_count, tweetId, user, idx = heapq.heappop(heap)
            result.append(tweetId)
            if idx >= 0:
                count, next_tweetId = self.posts[user][idx]
                heapq.heappush(heap, (-count, next_tweetId, user, idx - 1))
        return result

    def follow(self,followerId: int, followeeId: int) -> bool:
        #followerId follows followee
        if followerId in self.follows and followeeId in self.follows[followerId]:
            return False
        self.follows[followerId].add(followeeId)
        return True

    def unfollow(self,followerId: int, followeeId: int) -> bool:
        if followeeId not in self.follows[followerId]:
            return False
        self.follows[followerId].remove(followeeId)
        return True


if __name__ == "__main__":
    t = Twitter()

    t.postTweet(1, 101)
    t.postTweet(2, 201)
    t.postTweet(2, 202)
    t.postTweet(1, 102)

    t.follow(3, 1)
    t.follow(3, 2)

    print("User 3 feed (follows 1 and 2):", t.getNewsFeed(3))
    # expected: [102, 202, 201, 101] — sorted by most recent globally

    print("User 1 feed (follows no one):", t.getNewsFeed(1))
    # expected: [102, 101] — own tweets only

    t.unfollow(3, 2)
    print("User 3 feed after unfollowing 2:", t.getNewsFeed(3))
    # expected: [102, 101] — only user 1's tweets now
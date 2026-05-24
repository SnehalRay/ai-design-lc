import unittest
from code import Twitter


class TestPostTweet(unittest.TestCase):

    def test_post_single_tweet(self):
        t = Twitter()
        t.postTweet(1, 101)
        self.assertEqual(t.getNewsFeed(1), [101])

    def test_post_multiple_tweets_same_user(self):
        t = Twitter()
        t.postTweet(1, 101)
        t.postTweet(1, 102)
        self.assertEqual(t.getNewsFeed(1), [102, 101])

    def test_post_multiple_tweets_ordering(self):
        t = Twitter()
        t.postTweet(1, 101)
        t.postTweet(1, 102)
        t.postTweet(1, 103)
        self.assertEqual(t.getNewsFeed(1), [103, 102, 101])


class TestFollow(unittest.TestCase):

    def test_follow_adds_to_feed(self):
        t = Twitter()
        t.postTweet(2, 201)
        t.follow(1, 2)
        self.assertIn(201, t.getNewsFeed(1))

    def test_follow_already_following(self):
        t = Twitter()
        t.follow(1, 2)
        result = t.follow(1, 2)
        self.assertFalse(result)

    def test_follow_self_no_duplicate(self):
        t = Twitter()
        t.postTweet(1, 101)
        t.follow(1, 1)
        self.assertEqual(t.getNewsFeed(1), [101])


class TestUnfollow(unittest.TestCase):

    def test_unfollow_removes_from_feed(self):
        t = Twitter()
        t.postTweet(2, 201)
        t.follow(1, 2)
        t.unfollow(1, 2)
        self.assertNotIn(201, t.getNewsFeed(1))

    def test_unfollow_not_following(self):
        t = Twitter()
        result = t.unfollow(1, 2)
        self.assertFalse(result)


class TestGetNewsFeed(unittest.TestCase):

    def test_feed_includes_own_tweets(self):
        t = Twitter()
        t.postTweet(1, 101)
        self.assertEqual(t.getNewsFeed(1), [101])

    def test_feed_empty_no_posts(self):
        t = Twitter()
        self.assertEqual(t.getNewsFeed(1), [])

    def test_feed_respects_max_feed_poll(self):
        t = Twitter(max_feed_poll=2)
        for i in range(5):
            t.postTweet(1, i)
        self.assertEqual(len(t.getNewsFeed(1)), 2)

    def test_feed_fewer_than_max(self):
        t = Twitter()
        t.postTweet(1, 101)
        feed = t.getNewsFeed(1)
        self.assertEqual(feed, [101])

    def test_feed_global_time_ordering(self):
        t = Twitter()
        t.postTweet(1, 101)
        t.postTweet(2, 201)
        t.postTweet(1, 102)
        t.postTweet(2, 202)
        t.follow(3, 1)
        t.follow(3, 2)
        self.assertEqual(t.getNewsFeed(3), [202, 102, 201, 101])

    def test_feed_multiple_from_same_user(self):
        t = Twitter(max_feed_poll=2)
        t.postTweet(2, 201)  # count=0, oldest
        t.postTweet(1, 101)  # count=1
        t.postTweet(1, 102)  # count=2
        t.postTweet(1, 103)  # count=3, newest
        t.follow(3, 1)
        t.follow(3, 2)
        # user 1's last two tweets (103, 102) are more recent than user 2's 201
        self.assertEqual(t.getNewsFeed(3), [103, 102])

    def test_feed_after_unfollow(self):
        t = Twitter()
        t.postTweet(1, 101)
        t.postTweet(2, 201)
        t.follow(3, 1)
        t.follow(3, 2)
        t.unfollow(3, 2)
        feed = t.getNewsFeed(3)
        self.assertIn(101, feed)
        self.assertNotIn(201, feed)


if __name__ == "__main__":
    unittest.main(verbosity=2)

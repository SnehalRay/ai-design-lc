import unittest
from code import VideoSharingPlatform


class TestUpload(unittest.TestCase):
    def setUp(self):
        self.vsp = VideoSharingPlatform()

    def test_first_upload_gets_id_zero(self):
        self.assertEqual(self.vsp.upload("123"), 0)

    def test_sequential_uploads_increment_id(self):
        id0 = self.vsp.upload("111")
        id1 = self.vsp.upload("222")
        id2 = self.vsp.upload("333")
        self.assertEqual([id0, id1, id2], [0, 1, 2])

    def test_reuses_smallest_freed_id(self):
        id0 = self.vsp.upload("aaa")
        id1 = self.vsp.upload("bbb")
        self.vsp.remove(id0)
        self.vsp.remove(id1)
        # heap should give back 0 first, then 1
        self.assertEqual(self.vsp.upload("ccc"), 0)
        self.assertEqual(self.vsp.upload("ddd"), 1)

    def test_reuse_prefers_smallest_id_not_fifo(self):
        self.vsp.upload("a")  # 0
        self.vsp.upload("b")  # 1
        self.vsp.upload("c")  # 2
        self.vsp.remove(2)
        self.vsp.remove(0)
        # min-heap → 0 comes back before 2
        self.assertEqual(self.vsp.upload("x"), 0)


class TestRemove(unittest.TestCase):
    def setUp(self):
        self.vsp = VideoSharingPlatform()

    def test_remove_existing_video(self):
        vid_id = self.vsp.upload("123")
        result = self.vsp.remove(vid_id)
        self.assertTrue(result)

    def test_remove_nonexistent_video(self):
        result = self.vsp.remove(99)
        self.assertFalse(result)

    def test_remove_makes_video_inaccessible(self):
        vid_id = self.vsp.upload("123")
        self.vsp.remove(vid_id)
        self.assertIsNone(self.vsp.watch(vid_id, 0, 2))

    def test_double_remove_second_returns_false(self):
        vid_id = self.vsp.upload("123")
        self.vsp.remove(vid_id)
        self.assertFalse(self.vsp.remove(vid_id))


class TestWatch(unittest.TestCase):
    def setUp(self):
        self.vsp = VideoSharingPlatform()
        self.vid_id = self.vsp.upload("0123456789")

    def test_watch_full_video(self):
        self.assertEqual(self.vsp.watch(self.vid_id, 0, 9), "0123456789")

    def test_watch_partial_range(self):
        self.assertEqual(self.vsp.watch(self.vid_id, 2, 5), "2345")

    def test_watch_clamps_end_minute(self):
        # endMinute > len-1, should return up to last char
        self.assertEqual(self.vsp.watch(self.vid_id, 0, 100), "0123456789")

    def test_watch_single_minute(self):
        self.assertEqual(self.vsp.watch(self.vid_id, 3, 3), "3")

    def test_watch_nonexistent_returns_none(self):
        self.assertIsNone(self.vsp.watch(99, 0, 5))

    def test_watch_increments_view_count(self):
        self.vsp.watch(self.vid_id, 0, 3)
        self.vsp.watch(self.vid_id, 0, 3)
        self.assertEqual(self.vsp.get_views(self.vid_id), 2)

    def test_watch_nonexistent_does_not_increment_views(self):
        self.vsp.watch(99, 0, 3)
        self.assertEqual(self.vsp.get_views(99), -1)


class TestLikeDislike(unittest.TestCase):
    def setUp(self):
        self.vsp = VideoSharingPlatform()
        self.vid_id = self.vsp.upload("hello")

    def test_like_increments(self):
        self.vsp.like(self.vid_id)
        self.vsp.like(self.vid_id)
        self.assertEqual(self.vsp.getLikeAndDislike(self.vid_id)[0], 2)

    def test_dislike_increments(self):
        self.vsp.dislike(self.vid_id)
        self.assertEqual(self.vsp.getLikeAndDislike(self.vid_id)[1], 1)

    def test_like_nonexistent_is_noop(self):
        self.vsp.like(99)  # should not raise
        self.assertEqual(self.vsp.getLikeAndDislike(99), [-1, -1])

    def test_dislike_nonexistent_is_noop(self):
        self.vsp.dislike(99)
        self.assertEqual(self.vsp.getLikeAndDislike(99), [-1, -1])

    def test_like_and_dislike_independent(self):
        self.vsp.like(self.vid_id)
        self.vsp.dislike(self.vid_id)
        self.vsp.dislike(self.vid_id)
        likes, dislikes = self.vsp.getLikeAndDislike(self.vid_id)
        self.assertEqual(likes, 1)
        self.assertEqual(dislikes, 2)


class TestGetLikeAndDislike(unittest.TestCase):
    def setUp(self):
        self.vsp = VideoSharingPlatform()

    def test_returns_zeros_on_fresh_video(self):
        vid_id = self.vsp.upload("abc")
        self.assertEqual(self.vsp.getLikeAndDislike(vid_id), [0, 0])

    def test_returns_sentinel_for_missing_video(self):
        self.assertEqual(self.vsp.getLikeAndDislike(99), [-1, -1])


class TestGetViews(unittest.TestCase):
    def setUp(self):
        self.vsp = VideoSharingPlatform()

    def test_returns_zero_on_fresh_video(self):
        vid_id = self.vsp.upload("abc")
        self.assertEqual(self.vsp.get_views(vid_id), 0)

    def test_returns_negative_one_for_missing(self):
        self.assertEqual(self.vsp.get_views(99), -1)

    def test_count_after_multiple_watches(self):
        vid_id = self.vsp.upload("abc")
        for _ in range(5):
            self.vsp.watch(vid_id, 0, 2)
        self.assertEqual(self.vsp.get_views(vid_id), 5)


if __name__ == "__main__":
    unittest.main()

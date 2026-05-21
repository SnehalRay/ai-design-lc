from code import LRUCache


def test_get_empty_cache():
    cache = LRUCache(2)
    assert cache.get(1) == -1

def test_get_missing_key():
    cache = LRUCache(2)
    cache.push(1, 10)
    assert cache.get(99) == -1

def test_push_then_get():
    cache = LRUCache(2)
    cache.push(1, 10)
    assert cache.get(1) == 10

def test_push_multiple_get_each():
    cache = LRUCache(3)
    cache.push(1, 10)
    cache.push(2, 20)
    cache.push(3, 30)
    assert cache.get(1) == 10
    assert cache.get(2) == 20
    assert cache.get(3) == 30

# --- Eviction ---

def test_evicts_least_recently_used():
    cache = LRUCache(2)
    cache.push(1, 10)
    cache.push(2, 20)
    cache.push(3, 30)   # evicts key 1 (oldest)
    assert cache.get(1) == -1
    assert cache.get(2) == 20
    assert cache.get(3) == 30

def test_eviction_order_multiple():
    cache = LRUCache(3)
    cache.push(1, 1)
    cache.push(2, 2)
    cache.push(3, 3)
    cache.push(4, 4)   # evicts key 1
    assert cache.get(1) == -1
    cache.push(5, 5)   # evicts key 2
    assert cache.get(2) == -1
    assert cache.get(3) == 3

# --- Recency promotion via get ---

def test_get_promotes_to_recent():
    cache = LRUCache(2)
    cache.push(1, 10)
    cache.push(2, 20)
    cache.get(1)        # key 1 is now most recent; key 2 becomes LRU
    cache.push(3, 30)   # evicts key 2
    assert cache.get(2) == -1
    assert cache.get(1) == 10
    assert cache.get(3) == 30

def test_get_saves_item_from_eviction():
    cache = LRUCache(3)
    cache.push(1, 1)
    cache.push(2, 2)
    cache.push(3, 3)
    cache.get(1)        # 1 is now MRU; LRU order: 2, 3, 1
    cache.push(4, 4)   # evicts key 2
    assert cache.get(2) == -1
    assert cache.get(1) == 1

# --- Recency promotion via push (overwrite) ---

def test_overwrite_updates_value():
    cache = LRUCache(2)
    cache.push(1, 10)
    cache.push(1, 99)
    assert cache.get(1) == 99

def test_overwrite_promotes_to_recent():
    cache = LRUCache(2)
    cache.push(1, 10)
    cache.push(2, 20)
    cache.push(1, 11)   # overwrite key 1 → it becomes MRU; key 2 is LRU
    cache.push(3, 30)   # evicts key 2
    assert cache.get(2) == -1
    assert cache.get(1) == 11
    assert cache.get(3) == 30

def test_overwrite_does_not_increase_size():
    cache = LRUCache(2)
    cache.push(1, 10)
    cache.push(1, 20)
    cache.push(1, 30)   # still only one unique key
    cache.push(2, 40)   # should NOT evict anything (size is 2, capacity is 2)
    assert cache.get(1) == 30
    assert cache.get(2) == 40

# --- Edge case: capacity = 1 ---

def test_capacity_one_basic():
    cache = LRUCache(1)
    cache.push(1, 10)
    assert cache.get(1) == 10

def test_capacity_one_evicts_on_new_key():
    cache = LRUCache(1)
    cache.push(1, 10)
    cache.push(2, 20)
    assert cache.get(1) == -1
    assert cache.get(2) == 20

def test_capacity_one_overwrite_no_eviction():
    cache = LRUCache(1)
    cache.push(1, 10)
    cache.push(1, 99)   # same key — no eviction
    assert cache.get(1) == 99

def test_capacity_one_repeated_evictions():
    cache = LRUCache(1)
    for i in range(1, 6):
        cache.push(i, i * 10)
    assert cache.get(5) == 50
    for i in range(1, 5):
        assert cache.get(i) == -1

# --- LeetCode canonical example ---

def test_leetcode_example():
    cache = LRUCache(2)
    cache.push(1, 1)
    cache.push(2, 2)
    assert cache.get(1) == 1      # returns 1
    cache.push(3, 3)               # evicts key 2
    assert cache.get(2) == -1     # not found
    cache.push(4, 4)               # evicts key 1
    assert cache.get(1) == -1     # not found
    assert cache.get(3) == 3      # returns 3
    assert cache.get(4) == 4      # returns 4


if __name__ == "__main__":
    tests = [
        test_get_empty_cache,
        test_get_missing_key,
        test_push_then_get,
        test_push_multiple_get_each,
        test_evicts_least_recently_used,
        test_eviction_order_multiple,
        test_get_promotes_to_recent,
        test_get_saves_item_from_eviction,
        test_overwrite_updates_value,
        test_overwrite_promotes_to_recent,
        test_overwrite_does_not_increase_size,
        test_capacity_one_basic,
        test_capacity_one_evicts_on_new_key,
        test_capacity_one_overwrite_no_eviction,
        test_capacity_one_repeated_evictions,
        test_leetcode_example,
    ]

    passed = 0
    failed = 0
    for t in tests:
        try:
            t()
            print(f"PASS  {t.__name__}")
            passed += 1
        except AssertionError as e:
            print(f"FAIL  {t.__name__}")
            failed += 1

    print(f"\n{passed} passed, {failed} failed")

from code import HashMap


# ---------------------------------------------------------------------------
# 1. Basic Functionality
# ---------------------------------------------------------------------------

def test_add_and_get():
    hm = HashMap()
    hm.add("a", 1)
    assert hm.get("a") == 1

def test_contains_true():
    hm = HashMap()
    hm.add("x", 99)
    assert hm.contains("x") == True

def test_delete_removes_key():
    hm = HashMap()
    hm.add("a", 1)
    hm.delete("a")
    assert hm.contains("a") == False
    assert hm.get("a") is None

def test_size_empty():
    hm = HashMap()
    assert hm.size() == 0

def test_size_after_add():
    hm = HashMap()
    hm.add("a", 1)
    hm.add("b", 2)
    hm.add("c", 3)
    assert hm.size() == 3

def test_size_after_delete():
    hm = HashMap()
    hm.add("a", 1)
    hm.add("b", 2)
    hm.add("c", 3)
    hm.delete("b")
    assert hm.size() == 2


# ---------------------------------------------------------------------------
# 2. Missing Key Edge Cases
# ---------------------------------------------------------------------------

def test_get_missing_key():
    hm = HashMap()
    assert hm.get("nope") is None

def test_contains_missing_key():
    hm = HashMap()
    assert hm.contains("nope") == False

def test_delete_missing_key():
    hm = HashMap()
    hm.delete("nope")  # should not raise


# ---------------------------------------------------------------------------
# 3. Overwrite / Update
# ---------------------------------------------------------------------------

def test_overwrite_value():
    hm = HashMap()
    hm.add("k", 1)
    hm.add("k", 2)
    assert hm.get("k") == 2

def test_size_stable_on_overwrite():
    hm = HashMap()
    hm.add("k", 1)
    hm.add("k", 2)
    assert hm.size() == 1


# ---------------------------------------------------------------------------
# 4. Hash Collision Handling
# Assumes internal bucket count of 10.
# Integer keys 0 and 10 both land in bucket 0 (key % 10 == 0).
# ---------------------------------------------------------------------------

def test_collision_both_retrievable():
    hm = HashMap()
    hm.add(0, "zero")
    hm.add(10, "ten")
    assert hm.get(0) == "zero"
    assert hm.get(10) == "ten"

def test_collision_delete_one():
    hm = HashMap()
    hm.add(0, "zero")
    hm.add(10, "ten")
    hm.delete(0)
    assert hm.get(0) is None
    assert hm.get(10) == "ten"

def test_collision_size():
    hm = HashMap()
    hm.add(0, "zero")
    hm.add(10, "ten")
    assert hm.size() == 2


# ---------------------------------------------------------------------------
# 5. Sequential / Mixed Operations
# ---------------------------------------------------------------------------

def test_add_delete_readd():
    hm = HashMap()
    hm.add("a", 1)
    hm.delete("a")
    hm.add("a", 99)
    assert hm.get("a") == 99

def test_multiple_keys_independent():
    hm = HashMap()
    pairs = [("a", 1), ("b", 2), ("c", 3), ("d", 4), ("e", 5)]
    for k, v in pairs:
        hm.add(k, v)
    for k, v in pairs:
        assert hm.get(k) == v

def test_size_through_sequence():
    hm = HashMap()
    hm.add("a", 1)
    hm.add("b", 2)
    hm.add("c", 3)
    hm.add("d", 4)
    hm.delete("a")
    hm.delete("b")
    hm.add("e", 5)
    assert hm.size() == 3


# ---------------------------------------------------------------------------
# 6. Value Type Variety
# ---------------------------------------------------------------------------

def test_integer_key():
    hm = HashMap()
    hm.add(42, "answer")
    assert hm.get(42) == "answer"

def test_none_as_value():
    # Storing None is valid; use contains() to distinguish "key exists with
    # value None" from "key not found".
    hm = HashMap()
    hm.add("k", None)
    assert hm.contains("k") == True
    assert hm.get("k") is None

def test_list_as_value():
    hm = HashMap()
    hm.add("k", [1, 2, 3])
    assert hm.get("k") == [1, 2, 3]


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------

def run_all():
    tests = [
        test_add_and_get,
        test_contains_true,
        test_delete_removes_key,
        test_size_empty,
        test_size_after_add,
        test_size_after_delete,
        test_get_missing_key,
        test_contains_missing_key,
        test_delete_missing_key,
        test_overwrite_value,
        test_size_stable_on_overwrite,
        test_collision_both_retrievable,
        test_collision_delete_one,
        test_collision_size,
        test_add_delete_readd,
        test_multiple_keys_independent,
        test_size_through_sequence,
        test_integer_key,
        test_none_as_value,
        test_list_as_value,
    ]
    passed = 0
    failed = 0
    for t in tests:
        try:
            t()
            print(f"  PASS  {t.__name__}")
            passed += 1
        except Exception as e:
            print(f"  FAIL  {t.__name__}: {e}")
            failed += 1
    print(f"\n{passed} passed, {failed} failed out of {len(tests)} tests")

if __name__ == "__main__":
    run_all()

import unittest
import importlib.util
import os

_spec = importlib.util.spec_from_file_location(
    "autocomplete",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "code.py")
)
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)
AutocompleteSystem = _mod.AutocompleteSystem


class TestInputChar(unittest.TestCase):

    def test_leetcode_example(self):
        ac = AutocompleteSystem(
            ["i love you", "island", "iroman", "i love leetcode"],
            [5, 3, 2, 2]
        )
        self.assertEqual(ac.input('i'), ['i love you', 'island', 'i love leetcode'])
        self.assertEqual(ac.input(' '), ['i love you', 'i love leetcode'])
        self.assertEqual(ac.input('a'), [])
        self.assertEqual(ac.input('#'), [])

    def test_hot_degree_ordering(self):
        ac = AutocompleteSystem(["abc", "abd", "abe"], [3, 1, 2])
        self.assertEqual(ac.input('a'), ['abc', 'abe', 'abd'])

    def test_ascii_tiebreak(self):
        ac = AutocompleteSystem(["abc", "abd"], [5, 5])
        self.assertEqual(ac.input('a'), ['abc', 'abd'])

    def test_fewer_than_3_returns_all(self):
        ac = AutocompleteSystem(["hello", "help"], [3, 2])
        self.assertEqual(ac.input('h'), ['hello', 'help'])

    def test_new_sentence_stored_via_hash(self):
        ac = AutocompleteSystem(["hello world"], [3])
        ac.input('h')
        ac.input('#')           # stores "h" with count 1
        result = ac.input('h')
        self.assertIn('hello world', result)
        self.assertIn('h', result)
        self.assertEqual(result[0], 'hello world')  # count 3 beats count 1

    def test_count_accumulates_across_sessions(self):
        ac = AutocompleteSystem(["hello"], [1])
        for _ in range(4):
            for ch in 'hello':
                ac.input(ch)
            ac.input('#')       # hello count goes 1 → 5
        result = ac.input('h')
        self.assertIn('hello', result)

    def test_dead_end_returns_empty(self):
        ac = AutocompleteSystem(["hello"], [1])
        ac.input('h')
        self.assertEqual(ac.input('x'), [])   # dead end
        self.assertEqual(ac.input('e'), [])   # stays dead

    def test_hash_resets_for_next_query(self):
        ac = AutocompleteSystem(["hello"], [1])
        ac.input('h')
        ac.input('#')
        result = ac.input('h')
        self.assertIn('hello', result)

    def test_only_top_3_returned(self):
        ac = AutocompleteSystem(["a1", "a2", "a3", "a4"], [4, 3, 2, 1])
        result = ac.input('a')
        self.assertEqual(len(result), 3)
        self.assertEqual(result, ['a1', 'a2', 'a3'])

    def test_sentence_with_spaces(self):
        ac = AutocompleteSystem(["new york", "new zealand", "new mexico"], [10, 7, 5])
        result = ac.input('n')
        self.assertEqual(result, ['new york', 'new zealand', 'new mexico'])


class TestInputWord(unittest.TestCase):

    def test_basic_prefix(self):
        ac = AutocompleteSystem(
            ["hi there", "hi theiry", "hi thereee", "hi"],
            [4, 2, 6, 9]
        )
        self.assertEqual(ac.input_word('hi'), ['hi', 'hi thereee', 'hi there'])

    def test_partial_word_prefix(self):
        ac = AutocompleteSystem(["hello", "help", "hero"], [3, 2, 1])
        self.assertEqual(ac.input_word('hel'), ['hello', 'help'])

    def test_dead_end_word(self):
        ac = AutocompleteSystem(["hello"], [1])
        self.assertEqual(ac.input_word('xyz'), [])

    def test_word_followed_by_input_char(self):
        ac = AutocompleteSystem(["hello world"], [3])
        ac.input_word('hello')
        self.assertEqual(ac.input(' '), ['hello world'])

    def test_hash_stores_typed_word(self):
        ac = AutocompleteSystem(["hello"], [1])
        ac.input_word('hi')
        ac.input_word('#')              # stores "hi" with count 1
        result = ac.input('h')
        self.assertIn('hello', result)
        self.assertIn('hi', result)

    def test_fewer_than_3_matches(self):
        ac = AutocompleteSystem(["abc"], [5])
        self.assertEqual(ac.input_word('ab'), ['abc'])


class TestEdgeCases(unittest.TestCase):

    def test_empty_init(self):
        ac = AutocompleteSystem([], [])
        self.assertEqual(ac.input('a'), [])

    def test_top3_evicts_lowest_after_new_entry(self):
        # abf starts outside top3; typing it enough times should push it in
        ac = AutocompleteSystem(["abc", "abd", "abe", "abf"], [5, 4, 3, 2])
        self.assertEqual(ac.input('a'), ['abc', 'abd', 'abe'])
        ac.input('#')  # reset

        for _ in range(4):           # abf: 2 + 4 = 6 → becomes hottest
            for ch in 'abf':
                ac.input(ch)
            ac.input('#')

        result = ac.input('a')
        self.assertEqual(result[0], 'abf')

    def test_dead_end_then_hash_stores_partial(self):
        ac = AutocompleteSystem(["hello"], [1])
        ac.input('h')
        ac.input('x')   # dead end
        ac.input('#')   # stores "hx" with count 1
        ac.input('h')
        result = ac.input('x')   # "hx" now in trie
        self.assertIn('hx', result)

    def test_single_character_sentence(self):
        ac = AutocompleteSystem(["a"], [5])
        self.assertEqual(ac.input('a'), ['a'])

    def test_full_sentence_as_prefix(self):
        ac = AutocompleteSystem(["hello"], [3])
        for ch in 'hello':
            result = ac.input(ch)
        self.assertEqual(result, ['hello'])


if __name__ == '__main__':
    unittest.main()

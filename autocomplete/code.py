'''
642. Design Search Autocomplete System

Design a search autocomplete system for a search engine. Users may input a sentence (at least one word and end with a special character '#').

You are given a string array sentences and an integer array times both of length n where sentences[i] is a previously typed sentence and times[i] is the corresponding number of times the sentence was typed. For each input character except '#', return the top 3 historical hot sentences that have the same prefix as the part of the sentence already typed.

Here are the specific rules:

The hot degree for a sentence is defined as the number of times a user typed the exactly same sentence before.
The returned top 3 hot sentences should be sorted by hot degree (The first is the hottest one). If several sentences have the same hot degree, use ASCII-code order (smaller one appears first).
If less than 3 hot sentences exist, return as many as you can.
When the input is a special character, it means the sentence ends, and in this case, you need to return an empty list.
Implement the AutocompleteSystem class:

AutocompleteSystem(String[] sentences, int[] times) Initializes the object with the sentences and times arrays.
List<String> input(char c) This indicates that the user typed the character c.
Returns an empty array [] if c == '#' and stores the inputted sentence in the system.
Returns the top 3 historical hot sentences that have the same prefix as the part of the sentence already typed. If there are fewer than 3 matches, return them all.


end with '#'
'''

from typing import List


class TrieNode:
    def __init__(self):
        self.children = {}
        self.top3 = []  # sentences sorted by (-count, sentence), max 3


class AutocompleteSystem:
    def __init__(self, sentences: List[str], times: List[int]):
        self.root = TrieNode()
        self.count = {}
        self.current_input = ""
        self.current_node = self.root

        for sentence, time in zip(sentences, times):
            self.count[sentence] = time
            self._insert(sentence)

    def _update_top3(self, node: TrieNode, sentence: str):
        node.top3 = [s for s in node.top3 if s != sentence]
        node.top3.append(sentence)
        node.top3.sort(key=lambda s: (-self.count[s], s))
        node.top3 = node.top3[:3]

    def _insert(self, sentence: str):
        node = self.root
        for ch in sentence:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
            self._update_top3(node, sentence)

    def input_word(self, word: str) -> List[str]:
        if word == '#':
            return self.input('#')
        
        curr = ""

        for ch in word:
            self.current_input += ch
            if self.current_node is not None and ch in self.current_node.children:
                self.current_node = self.current_node.children[ch]
            else:
                self.current_node = None

        return self.current_node.top3[:] if self.current_node is not None else []

    def input(self, c: str) -> List[str]:
        if c == '#':
            self.count[self.current_input] = self.count.get(self.current_input, 0) + 1
            self._insert(self.current_input)
            self.current_input = ""
            self.current_node = self.root
            return []

        self.current_input += c
        if self.current_node is not None and c in self.current_node.children:
            self.current_node = self.current_node.children[c]
            return self.current_node.top3[:]
        else:
            self.current_node = None
            return []


auto = AutocompleteSystem(["hi there","hi theiry","hi thereee", "hi"],[4,2,6,9])
print(auto.input('h'))
print(auto.input('i'))
print(auto.input('#'))
print(auto.input_word('hi'))


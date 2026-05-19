# initialize the main object
# hashmap should be able to
# 1. add a key-value pair
# 2. get the value for a key
# 3. delete a key-value pair
# 4. check if a key exists
# 5. get the size of the hashmap

#Rules: if no key, then it is going to be None

class HashMap:
    def __init__(self):
        self.bucket_size = 1000
        self.hash = [[] for _ in range(self.bucket_size)]
        self._size = 0

    def _hash(self, key):
        if isinstance(key, str):
            hash_val = 0
            for char in key:
                hash_val = hash_val * 31 + ord(char)
            return hash_val % self.bucket_size
        return key % self.bucket_size

    def add(self, key, value):
        hash_key = self._hash(key)
        for i, (k, v) in enumerate(self.hash[hash_key]):
            if k == key:
                self.hash[hash_key][i] = (key, value)
                return
        self.hash[hash_key].append((key, value))
        self._size += 1
        

    def get(self, key):
        hash_key = self._hash(key)
        for i, (k, v) in enumerate(self.hash[hash_key]):
            if k == key:
                return self.hash[hash_key][i][1]
        return None
        

    def delete(self, key):
        hash_key = self._hash(key)
        for i, (k, v) in enumerate(self.hash[hash_key]):
            if k == key:
                del self.hash[hash_key][i]
                self._size-=1
                return
        return

    def contains(self, key):
        hash_key = self._hash(key)
        for i, (k, v) in enumerate(self.hash[hash_key]):
            if k == key:
                return True
        return False
        

    def size(self):
        return self._size
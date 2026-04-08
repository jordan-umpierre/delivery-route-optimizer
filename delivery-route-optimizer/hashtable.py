# Custom hash table built with separate chaining for package lookup and updates.

class HashTable:
    # Separate chaining handles collisions while keeping lookup and insert fast.

    def __init__(self, capacity: int = 10):
        self.capacity = capacity

        self.table = [[] for _ in range(capacity)]

    def _hash(self, key: int) -> int:
        return key % self.capacity

    def insert(self, key: int, item) -> None:
        bucket_index = self._hash(key)
        bucket = self.table[bucket_index]

        for pair in bucket:
            if pair[0] == key:
                pair[1] = item
                return

        bucket.append([key, item])

    def lookup(self, key: int):
        bucket_index = self._hash(key)
        bucket = self.table[bucket_index]

        for pair in bucket:
            if pair[0] == key:
                return pair[1]

        return None

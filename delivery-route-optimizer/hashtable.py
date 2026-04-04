# WHAT: Define a custom hash table (built from scratch).
# WHY: Task 2 requires implementing our own hash table (not using Python's built-in dict as the hash table). This structure stores packages by package_id for fast lookup and updates during the day.

class HashTable:
    # WHAT: Custom hash table implemented using separate chaining (list-of-lists buckets).
    # WHY: Separate chaining handles collisions (multiple keys mapping to the same bucket index) while still keeping average-case lookup/insert near O(1).

    def __init__(self, capacity: int = 10):
        # WHAT: Initialize the hash table with a fixed number of buckets.
        # WHY: 10 buckets is a common, easy choice for 40 packages (IDs distribute cleanly with mod 10)
        self.capacity = capacity

        # WHAT: Create a list of empty buckets, where each bucket will hold [key, value] pairs.
        # WHY: We need our own storage structure instead of Python dict.
        self.table = [[] for _ in range(capacity)]

    def _hash(self, key: int) -> int:
        # WHAT: Compute the bucket index for a given key (package_id).
        # WHY: The key must map deterministically to a bucket so we can retrieve it later.
        # HOW: Modulo hashing is simple and standard for integer IDs.
        return key % self.capacity

    def insert(self, key: int, item) -> None:
        # WHAT: Insert or update a record by package_id (key).
        # WHY: Task 2A requires inserting package data into the custom hash table using package_id as the key.

        bucket_index = self._hash(key)
        bucket = self.table[bucket_index]

        # WHAT: If the key already exists in this bucket, update its stored value.
        # WHY: This supports overwriting/updating package records (example: status/time updates later).
        for pair in bucket:
            if pair[0] == key:
                pair[1] = item
                return

        # WHAT: If key does not exist, append a new [key, value] pair.
        # WHY: Separate chaining stores multiple pairs in the same bucket when collisions occur.
        bucket.append([key, item])

    def lookup(self, key: int):
        # WHAT: Look up and return the record stored under package_id (key).
        # WHY: Task 2B requires a lookup function that takes package_id as input and returns the package record.

        bucket_index = self._hash(key)
        bucket = self.table[bucket_index]

        # WHAT: Scan the bucket for a matching key.
        # WHY: With separate chaining, collisions place multiple keys in the same bucket list.
        for pair in bucket:
            if pair[0] == key:
                # WHAT: Return the stored value (Package object).
                # WHY: The Package object contains delivery address, deadline, city, zip, weight, and status/time.
                return pair[1]

        # WHAT: Return None if not found.
        # WHY: Allows caller to handle invalid package IDs gracefully.
        return None

import bitarray
import json

class BloomFilter():

    def __init__(self, size, number_hash_functions = 3):
        self.size = size

        self.bloom_filter = bitarray(self.size)
        self.bloom_filter.setall(0)

        self.number_hash_functions = number_hash_functions

    def _hash_djb2(self, s):
        hash = 5381
        for x in s:
            hash = ((hash << 5) + hash) + ord(x)
        return hash % self.size
    
    def _hash(self, item, K):
        return self._hash_djb2(str(K) + item)
    
    def add_to_filter(self, item):
        for i in range(self.number_hash_functions):
            self.bloom_filter[self._hash(item, i)] = 1

    def check_is_not_in_filter(self, item) -> bool: 
        for i in range(self.number_hash_functions):
            if self.bloom_filter[self._hash(item, i)] == 0:
                return True
        return False
    
    def load_items(self, items):
        for item in items:
            self.add_to_filter(item)

def init_bloom() -> BloomFilter:
    services = json.loads(open('json/services.json').read())

    bloom = BloomFilter(300)

    for service in services:
        bloom.load_items(service['keywords'])
    
    return bloom

def search_service_from_keywords(bloom: BloomFilter, words):
    results = []
    if any(bloom.check_is_not_in_filter(word) for word in words):
        return None
    services = json.loads(open('json/services.json').read())
    for service in services:
        if any(word not in service['keywords'] for word in words):
            continue
        results.append(service)
    return results
        

        
    
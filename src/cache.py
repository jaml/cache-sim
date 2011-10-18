import random

def is_power2(num):
    """Returns true if the number is a power of two."""
    return num != 0 and ((num & (num - 1)) == 0)

class Cache(object):
    """The root class for a cache. Handles all cache interaction."""
    def __init__(self, block_count, block_size):
        self.block_count = int(block_count)
        self.block_size = int(block_size)

        self.total_accesses = 0 
        self.total_hits = 0

        self.cache = []

        for i in range(self.block_count):
            line = []
            for j in range(self.block_size):
                line.append(-1)
            self.cache.append(line)

    def print_cache(self):
        """Outputs the contents of the cache to the command line."""
        print "\nCache Contents:"
        for block in self.cache:
            print "[ ",
            for word in block:
                if word == -1 or word == []:
                    output = '--'
                else:
                    output = word
                print "%s " % (str(output)),
            print "]"
    
    def print_hit_rate(self):
        """Outputs the hit rate percentage to the command line."""
        print "\nHit rate: %f%%" % \
               (100 * float(self.total_hits)/self.total_accesses)

    def store(self, address, verbose):
        raise NotImplementedError()

    def load(self, address, verbose):
        raise NotImplementedError()

    def _address_position(self, address):
        """The position that an address will be given in the cache."""
        block = (address / self.block_size) % self.block_count
        word = address % self.block_size 
        return block, word

    def _load_line(self, address, word):
        """Load the whole line that an address lies in."""
        return range(address-word, address-word+self.block_size)

class DirectMappedCache(Cache):
    """Represents a direct mapped cache."""
    def __init__(self, block_count, block_size):
        super(DirectMappedCache, self).__init__(block_count, block_size)

    def load(self, address, verbose):
        """Load an address into the cache."""
        block, word = self._address_position(address)
        self.total_accesses += 1
        
        # Did we get a hit?
        hit = self.cache[block][word] == address

        if hit:
            self.total_hits += 1

        self.cache[block] = self._load_line(address, word);

        if verbose:
            print "A read to address %d looked for word %d in block %d and was a %s." % (address,
                word, block, "hit" if hit else "miss")

    def store(self, address, verbose):
        """Store an address in the cache."""
        block, word = self._address_position(address)
        self.total_accesses += 1
        
        # Is it a hit?
        hit = self.cache[block][word] == address

        if hit:
            self.total_hits += 1

        # Evict the block.
        self.cache[block] = self._load_line(address, word)

        if verbose:
            print "A write to address %d looked for word %d in block %d and was a %s." % (address,
                word, block, "hit" if hit else "miss")
        

class AssociativeCache(Cache):
    """The base class for all associative caches."""
    def __init__(self, block_count, block_size, associativity):
        super(AssociativeCache, self).__init__(block_count, block_size)

        if not is_power2(associativity):
            error("Associativity is not a power of 2.")

        self.associativity = associativity

    def load(self, address, verbose):
        """Load an address into the cache."""
        block, word = self._assoc_address_position(address)
        self.total_accesses += 1
        
        # Did we get a hit?
        hit = False
        for i in range(self.associativity):
            if self.cache[block+i][word] == address:
                hit = True
                break

        if hit:
            self.total_hits += 1

        # Get the block to evict.
        evict_number = self._assoc_insert_address(address, block, word)

        if not evict_number == None:
            self.cache[evict_number] = self._load_line(address, word);

        if verbose:
            print "A read to address %d looked for word %d in the set starting with block %d and was a %s." % (address,
                word, block, "hit" if hit else "miss")

    def store(self, address, verbose):
        """Store an address in the cache."""
        block, word = self._assoc_address_position(address)
        self.total_accesses += 1
        
        # Did we get a hit?
        hit = False
        for i in range(self.associativity):
            if self.cache[block+i][word] == address:
                hit = True
                break

        if hit:
            self.total_hits += 1

        # Get the block to evict.
        evict_number = self._assoc_insert_address(address, block, word)

        if not evict_number == None:
            self.cache[evict_number] = self._load_line(address, word);

        if verbose:
            print "A write to address %d looked for word %d in the set starting with block %d and was a %s." % (address,
                word, block, "hit" if hit else "miss")

    def _assoc_address_position(self, address):
        block, word = self._address_position(address)
        return (block/self.associativity)*self.associativity, word

class RandomAssociativeCache(AssociativeCache):
    def __init__(self, block_count, block_size, associativity):
        super(RandomAssociativeCache, self).__init__(block_count, block_size, associativity)

    def _assoc_insert_address(self, address, block, word):
        # If our address is already cached then do nothing.
        for i in range(self.associativity):
            if self.cache[block+i][word] == address:
                return None

        # How full is the current cache block?
        for i in range(self.associativity):
            if self.cache[block+i][0] == -1:
                # Found an empty space.
                return block+i
        
        # We need to evict.
        return block + random.randrange(self.associativity)

class LRUsedAssociativeCache(AssociativeCache):
    def __init__(self, block_count, block_size, associativity):
        super(LRUsedAssociativeCache, self).__init__(block_count,
                block_size, associativity)

        self.last_used = []

    def _assoc_insert_address(self, address, block, word):
        # If our address is already cached then do nothing.
        for i in range(self.associativity):
            if self.cache[block+i][word] == address:
                self.last_used.remove(block+i)
                self.last_used.append(block+i)
                return None

        # How full is the current cache block?
        for i in range(self.associativity):
            if self.cache[block+i][0] == -1:
                # Found an empty space.
                if block+i in self.last_used:
                    self.last_used.remove(block+i)
                self.last_used.append(block+i)
                return block+i
        
        # We need to evict.
        current_block = range(block, block+self.associativity)

        for i in self.last_used:
            if i in current_block:
                oldest_offset = i
                break

        if oldest_offset in self.last_used:
            self.last_used.remove(oldest_offset)

        self.last_used.append(oldest_offset)

        return oldest_offset

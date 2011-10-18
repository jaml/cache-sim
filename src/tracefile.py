import re

from cache import *
from utils import *

class InvalidTraceFile(Exception):
    """Thrown when the trace file is invalid."""
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

class TraceFile(object):
    """A trace file of attributes and commands."""

    VALID_CACHE_TYPES = ['1', '2r', '2l', '4r', '4l']
    VALID_INSTRUCTIONS = ['l','s','v','h','p']

    def __init__(self, block_count, block_size, cache_type, commands):
        self.block_count = block_count.split()[0]
        self.block_size = block_size.split()[0]
        self.cache_type = cache_type.split()[0]
        self.commands = self._check_commands(commands)

        if not is_power2(int(self.block_count)):
            error("Block count is not a power of 2.")

        if not is_power2(int(self.block_size)):
            error("Block size is not a power of 2.")

        # Set up the cache.
        if self.cache_type not in TraceFile.VALID_CACHE_TYPES:
            raise InvalidTraceFile("Invalid Cache Type: %s" % self.cache_type)

        if self.cache_type == '1':
            self.cache = DirectMappedCache(self.block_count, self.block_size)
        elif self.cache_type == '2r':
            self.cache = RandomAssociativeCache(self.block_count,
                    self.block_size, 2)
        elif self.cache_type == '2l':
            self.cache = LRUsedAssociativeCache(self.block_count,
                    self.block_size, 2)
        elif self.cache_type == '4r':
            self.cache = RandomAssociativeCache(self.block_count,
                    self.block_size, 4)
        elif self.cache_type == '4l':
            self.cache = LRUsedAssociativeCache(self.block_count,
                    self.block_size, 4)

        # Verboseness is off by default.
        self.verbose = False

    def run(self):
        """Run through the file executing each command in turn."""
        for command in self.commands:
            if command[0] == 'v':
                self._toggle_verbose()
            elif command[0] == 'l':
                address = int(command[1])
                self.cache.load(address, self.verbose)
            elif command[0] == 's':
                address = int(command[1])
                self.cache.store(address, self.verbose)
            elif command[0] == 'p':
                self.cache.print_cache()
            elif command[0] == 'h':
                self.cache.print_hit_rate()

    def _toggle_verbose(self):
        """Toggle verbose mode on or off."""
        self.verbose = not self.verbose
    
    def _check_commands(self, commands):
        """Check that the command string is valid."""
        stripped_commands = []

        # Enumerate the commands so that we can get the line number of the
        # error.
        for command in enumerate(commands):
            if command[1] == "":
                continue

            # You split the command into a command and (optional) argument.
            split_command = command[1].split()[:2]

            # Check if the instructions is valid.
            if split_command[0] not in TraceFile.VALID_INSTRUCTIONS:
                raise InvalidTraceFile("Command '%s' on line %d is incorrect." \
                        % (split_command[0], command[0]+4))
            
            # Store the argument if there is one.
            if len(split_command) == 1:
                stripped_commands.append([split_command[0]])
            elif not re.match("\d+", split_command[1]):
                stripped_commands.append([split_command[0]])
            else:
                stripped_commands.append(split_command)
        
        return stripped_commands


def load_tracefile(filename):
    """Load the tracefile into the program."""
    # Open the file.
    try:
        tracefile = open(filename, 'r')
    except (IOError):
        error("Couldn't find tracefile: %s" % filename)

    # Read the file in and close it.
    lines = tracefile.read().split('\n')
    tracefile.close()

    block_count = lines[0]
    block_size = lines[1]
    cache_type = lines[2]
    commands = lines[3:]

    return TraceFile(block_count, block_size, cache_type, commands)

import sys

# Utility Functions
def error(message):
    """Prints an error string in red and then exits the program."""
    print "\033[1;31mERROR:\033[0m %s" % message
    sys.exit(1)

def is_power2(num):
    """Returns true if the number is a power of two."""
    return num != 0 and ((num & (num - 1)) == 0)


# -*- coding: utf-8 -*-

"""
Finger Counter
Entry point to the module.
"""

# Python built-in imports
import argparse

# Local imports

#-----------------------------------------------------------------------------#
#
# Arguments
#
#-----------------------------------------------------------------------------#
DES = "Counts the number of raised fingers"

PARSER = argparse.ArgumentParser(description=DES)

#-----------------------------------------------------------------------------#
#
# Main function: Entry point
#
#-----------------------------------------------------------------------------#
def main() -> None:
    """ Main function. Gets called when the module is called from the cmdline.
    """
    args = PARSER.parse_args()
    print("Press 'q' to quit the LiveFeed")

if __name__ == '__main__':
    main()

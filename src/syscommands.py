import os
import sys

# Function that reboots the bot
def reboot():
    os.execv(sys.executable, ['python'] + sys.argv)
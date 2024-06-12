import os
import sys
import traceback

#
# --- Execution ---
#

def get_args(verbose=True):
    if len(sys.argv) > 1:
        args = sys.argv[1:]
    else:
        args = None
    if verbose:
        info(f"Args: {args}")
    return args

def script_name():
    return os.path.basename(traceback.extract_stack()[0][0]).replace('.py', '')

#
# --- Qute Environment Variables ---
#

## All Mode
# Either hints (started via hints) or command (started via command or key binding).
QUTE_MODE = os.environ.get("QUTE_MODE")
# The currently set user agent, if customized.
QUTE_USER_AGENT = os.environ.get("QUTE_USER_AGENT")
# The FIFO or file to write commands to.
QUTE_FIFO = os.environ.get("QUTE_FIFO")
# Path of a file containing the HTML source of the current page.
QUTE_HTML = os.environ.get("QUTE_HTML")
# Path of a file containing the plaintext of the current page.
QUTE_TEXT = os.environ.get("QUTE_TEXT")
# Path of the directory containing qutebrowser’s configuration.
QUTE_CONFIG_DIR = os.environ.get("QUTE_CONFIG_DIR")
# Path of the directory containing qutebrowser’s data.
QUTE_DATA_DIR = os.environ.get("QUTE_DATA_DIR")
# Path of the downloads directory.
QUTE_DOWNLOAD_DIR = os.environ.get("QUTE_DOWNLOAD_DIR")
# Text currently in qutebrowser’s command line. Note this is only useful for userscripts spawned (e.g. via a keybinding) when qutebrowser is still in command mode. If you want to receive arguments passed to your userscript via :spawn, use the normal way of getting commandline arguments (e.g. $@ in bash or sys.argv / argparse / … in Python).
QUTE_COMMANDLINE_TEXT = os.environ.get("QUTE_COMMANDLINE_TEXT")
# The version of qutebrowser, as a string like "2.0.0". Note that this was added in v2.0.0, thus older versions can only be detected by the absence of this variable.
QUTE_VERSION = os.environ.get("QUTE_VERSION")

## Command Mode
if QUTE_MODE == "command":
    # The current page URL.
    QUTE_URL = os.environ.get("QUTE_URL")
    # The title of the current page.
    QUTE_TITLE = os.environ.get("QUTE_TITLE")
    # The text currently selected on the page.
    QUTE_SELECTED_TEXT = os.environ.get("QUTE_SELECTED_TEXT")
    # The count from the spawn command running the userscript.
    QUTE_COUNT = os.environ.get("QUTE_COUNT")
    # The current tab’s index.
    QUTE_TAB_INDEX = os.environ.get("QUTE_TAB_INDEX")

## Hint Mode
elif QUTE_MODE == "hints":
    # The URL selected via hints.
    QUTE_URL = os.environ.get("QUTE_URL")
    # The current page URL.
    QUTE_CURRENT_URL = os.environ.get("QUTE_CURRENT_URL")
    # The plain text of the element selected via hints.
    QUTE_SELECTED_TEXT = os.environ.get("QUTE_SELECTED_TEXT")
    # The HTML of the element selected via hints.
    QUTE_SELECTED_HTML = os.environ.get("QUTE_SELECTED_HTML")

#
# --- Qute Commands ---
#

def send_command(command, get_cmd=False):
    if get_cmd:
        return command
    with open(QUTE_FIFO, "w") as f:
        f.write(command + '\n')

def send_chained(commands, get_cmd=False):
    if not isinstance(commands, list):
        commands = [commands]
    command = ' ;; '.join(commands)
    return send_command(command, get_cmd)

#
# --- Logging ---
#

def log(message, level, clear, get_cmd=False):
    if level not in ['info', 'warning', 'error']:
        message = f'Unknown level: {level} for message: {message}'
        level = 'warning'
        clear = False

    commands = [f'message-{level} "{script_name()}: {message}"']
    if clear:
        commands.append('clear-messages')

    return send_chained(commands, get_cmd)

def info(message, clear=True, get_cmd=False):
    return log(message, 'info', clear, get_cmd)
def warning(message, clear=False, get_cmd=False):
    return log(message, 'warning', clear, get_cmd)
def error(message, clear=False, get_cmd=False):
    return log(message, 'error', clear, get_cmd)

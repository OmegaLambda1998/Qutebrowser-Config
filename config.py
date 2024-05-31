# Documentation:
#   qute://help/configuring.html
#   qute://help/settings.html

import os
import string
from urllib.parse import quote
from qutebrowser.utils import message

config.load_autoconfig()

HOME = os.environ.get('HOME')
CONFIG = os.environ.get('CONFIG')
BASE = os.environ.get('BASE')
DOWNLOAD = f'{BASE}/Downloads'
TERMINAL = os.environ.get('TERMINAL').split()
EDITOR = os.environ.get('EDITOR')
FILEMANAGER = os.environ.get('FILEMANAGER')

def mass_set(option, value, urls):
    for url in urls:
        config.set(option, value, url)

def bind_chained(key, *commands):
    config.bind(key, ' ;; '.join(commands))

default_urls = [
    'mail.google.com',
    'outlook.office365.com',
    'www.messenger.com',
    'app.slack.com',
    'discord.com',
    'calendar.google.com',
    'www.overleaf.com/project/*',
    'docs.google.com',
]

# Change the argument to True to still load settings configured via autoconfig.yml
config.load_autoconfig(False)

# Aliases for commands. The keys of the given dictionary are the
# aliases, while the values are the commands they map to.
c.aliases = {
    'q': 'close',
    'qa': 'quit',
    'w': 'session-save --only-active-window',
    'wq': 'quit --save',
    'wqa': 'quit --save',
    'e': 'config-edit',
    's': 'config-source',
}

# Do not restore open sites when qutebrowser is reopened
c.auto_save.session = True

#
### Bindings
#

# Movement
config.bind('<Ctrl-j>', 'tab-prev')
config.bind('<Ctrl-j>', 'tab-prev', mode='passthrough')
config.unbind('K')
config.bind('<Ctrl-k>', 'tab-next')
config.bind('<Ctrl-k>', 'tab-next', mode='passthrough')
config.unbind('J')
config.bind('<Ctrl-h>', 'back')
config.bind('<Ctrl-Shift-h>', 'back -t')
config.bind('<Ctrl-h>', 'back', mode='passthrough')
config.bind('<Ctrl-Shift-h>', 'back -t', mode='passthrough')
config.unbind('L')
config.bind('<Ctrl-l>', 'forward')
config.bind('<Ctrl-Shift-l>', 'forward -t')
config.bind('<Ctrl-l>', 'forward', mode='passthrough')
config.bind('<Ctrl-Shift-l>', 'forward -t', mode='passthrough')
config.unbind('H')

# Try to avoid accidental tab killing & provide more passthrough functionality
# Reload
config.bind('<Ctrl-r>', 'reload')
config.bind('<Ctrl-r>', 'reload', mode='passthrough')
config.unbind('r')
config.bind('<Ctrl-Shift-r>', 'reload -f')
config.bind('<Ctrl-Shift-r>', 'reload -f', mode='passthrough')
config.unbind('R')
# Tab-close
config.bind('<Ctrl-d>', 'tab-close')
config.bind('<Ctrl-d>', 'tab-close', mode='passthrough')
config.unbind('d')
config.bind('<Ctrl-Shift-d>', 'tab-close -o')
config.bind('<Ctrl-Shift-d>', 'tab-close -o', mode='passthrough')
config.unbind('D')
# Open cmd
config.bind('<Ctrl-;>', 'cmd-set-text :')
config.bind('<Ctrl-;>', 'cmd-set-text :', mode='passthrough')
# Tab-select
config.bind('<Ctrl-t>', 'cmd-set-text --space :tab-select ')
config.bind('<Ctrl-t>', 'cmd-set-text --space :tab-select ', mode='passthrough')
# Open
config.bind('<Ctrl-o>', 'cmd-set-text --space :open -s ')
config.bind('<Ctrl-o>', 'cmd-set-text --space :open -s ', mode='passthrough')
config.bind('<Ctrl-Shift-O>', 'cmd-set-text --space :open -s -t ')
config.bind('<Ctrl-Shift-o>', 'cmd-set-text --space :open -s -t ', mode='passthrough')

# Clean up persistent elements
bind_chained('<Escape>', 'download-clear', 'zoom', 'search', 'clear-keychain', 'clear-messages')
config.bind('<Escape>', 'mode-leave ;; jseval -q document.activeElement.blur()', mode='insert')

# Hints
config.bind('yc', 'hint code userscript code_select')


#
### Colours
#

# What colour should the background be if unset
c.colors.webpage.bg = 'black'

# Value to use for `prefers-color-scheme:` for websites
c.colors.webpage.preferred_color_scheme = 'dark'

# Do not render all web contents using a dark theme
c.colors.webpage.darkmode.enabled = True

# Which images to apply dark mode to
c.colors.webpage.darkmode.policy.images = 'never'

# Which pages to apply dark mode to
c.colors.webpage.darkmode.policy.page = 'smart'

#
### Completion
#

# What categories and in what order to show in the :open completion
c.completion.open_categories = ['searchengines', 'quickmarks', 'history']

#
### Content
#

# Do not automatically start playing `<video>` elements.
c.content.autoplay = False

# Limit fullscreen to browser window
c.content.fullscreen.window = True

# Allow any page to copy to clipboard via a button
c.content.javascript.clipboard = 'access'

# Allow websites to show notifications - default's to ask
mass_set('content.notifications.enabled', True, default_urls)

# Allow local documents to access remote urls
c.content.local_content_can_access_remote_urls = True

# Use both blocking methods
c.content.blocking.method = 'both'

# Use utf-8 encoding
c.content.default_encoding = 'utf-8'

# Automatically open pdf's using pdfjs
c.content.pdfjs = True

# Request reduced motion (minimise animations) to improve performance
c.content.prefers_reduced_motion = True

#
### Downloads
#

# Directory to download to
c.downloads.location.directory = DOWNLOAD 

# Do not remember last used download directory
c.downloads.location.remember = False

# Show download path and filename in download prompt
c.downloads.location.suggestion = 'both'

#
### Editor
#

# Change qutebrowser editor
c.editor.command = [*TERMINAL, EDITOR, '{file}', '-c', 'normal{line}G{column0}1']

#
### Fileselect
#

# Use custom commands for selecting folders and files
c.fileselect.handler = 'default'

# Command to select a folder
c.fileselect.folder.command = [*TERMINAL, FILEMANAGER, '--cwd-file {}']

# Command to select a single file
c.fileselect.single_file.command = [*TERMINAL, FILEMANAGER, '--chooser-file {}']

# command to select multiple files
c.fileselect.multiple_files.command = [*TERMINAL, FILEMANAGER, '--chooser-file {}']

#
### Hints
#

c.hints.selectors["code"] = [
    # Selects all code tags whose direct parent is not a pre tag
    ":not(pre) > code",
    "pre"
]

#
### Input
#

# Enter insert mode if an editable element is focused after loading the page
# c.input.insert_mode.auto_load = True

# Enter passthrough mode for the given urls
# mass_set('input.mode_override', 'passthrough', default_urls)

#
# TODO: Test
### QT
#

# Additional arguments to pass to Qt, without leading `--`.
#c.qt.args = [
#    'enable-gpu-rasterization',
#    'ignore-gpu-blacklist',
#    'enable-native-gpu-memory-buffers',
#    'enable-viz-display-compositor',
#    'num-raster-threads=4',
#    'use-gl=egl',
#    'enable-accelerated-video-decode',
#]

# Enable experimental web platform features
#c.qt.chromium.experimental_web_platform_features = 'always'

# Allow seperate visits to the same site to share an OS process, reducing memory consumption at the cost of security, robustness, and responsiveness
#c.qt.chromium.process_model = 'process-per-site'

# Define other environment variables
#c.qt.environ = {
#    'DRI_PRIME': '1', # Use dGPU
#}

# Force QT_QPA_PLATFORM=wayland-egl
#c.qt.force_platform = 'wayland-egl'

# Turn on High DPI scaling
#c.qt.highdpi = True

# Do not disable accelerated 2d canvas
#c.qt.workarounds.disable_accelerated_2d_canvas = 'never'

#
### Url
#

# If a search engine shortcut is invoked without parameters, open base url
c.url.open_base_url = True

# Search engines

#
### Allow duck duck go url parameters to be appended based on keys
#

# Take a string and identify the keys
def split_flags_and_search(search, possible_flags):
    flags = {}
    for elem in search:
        if '=' in elem:
            kv = elem.split('=')
            if len(kv) == 2:
                key, value = kv
                if key in possible_flags:
                    flags[key] = value
                    continue
        break
    search = ' '.join(search[len(flags):])
    return flags, search

# DDG search modifiers 
ddg_url_params = {
    'region': 'kl',
    'safesearch': 'kp',
    'header': 'ko',
    'ads': 'k1',
    'units': 'kaj',
    'filetype': 'filetype:',
    'f': 'filetype:',
    'site': 'site:',
    's': 'site:',
}

# Human readable values converted to DDG values
ddg_url_values = {
    'kl': {
        'none': 'wt-wt',
        'au': 'au-en',
        'us': 'us-en',
    },
    'kp': {
        'on': '1',
        'mod': '-1',
        'off': '-2',
    },
    'ko': {
        'floating': '1',
        'scrolling': '2',
        'instant': '-1',
        'off': '-2',
    },
    'k1': {
        'on': '1',
        'off': '-1',
    },
    'kaj': {
        'metric': 'm',
        'imperial': 'u',
    },
    'site:': {
        'r': 'reddit.com',
        'reddit': 'reddit.com',
        'arx': 'arxiv.org',
        'arxiv': 'arxiv.org',
        'ads': 'adsabs.harvard.edu',
        'arw': 'wiki.archlinux.org',
        'arch': 'wiki.archlinux.org',
        'gh': 'github.com',
        'github': 'github.com',
    }
}

# If these flags aren't defined, use these defaults
default_flags = {
    'region': 'none',
    'safesearch': 'off',
    'header': 'instant',
    'ads': 'off',
    'units': 'metric',
}

# Preprocess search string 
class DuckDuckGoSearchString(str):
    def format(self, *args, **kwargs):
        unquoted = str(kwargs['unquoted'])
        elements = unquoted.split()
        flags, search = split_flags_and_search(elements, list(ddg_url_params.keys()))
        append_str = ''
        for (k, v) in default_flags.items():
            if k not in list(flags.keys()):
                flags[k] = v
        for (k, v) in flags.items():
            param = ddg_url_params[k]
            value = ddg_url_values.get(param, {}).get(v, v)
            # In search modifiers
            if param[-1] == ':':
                search = f"{search} {param}{value}"
            else:
                append_str += f'&{param}={value}'
        s = self.__str__() + append_str
        return s.format(search, **kwargs)

# Define search engines
c.url.searchengines = {
    'DEFAULT': DuckDuckGoSearchString('https://duckduckgo.com/?q={}'),
    'g': 'https://google.com/search?q={}', # Google
    'sr': 'https://www.reddit.com/r/{}', # Subreddit
    'arx': 'https://arxiv.org/search/physics/?query={}&searchtype=all&abstract=show&size=200&order=', # Arxiv
    'ads': 'https://ui.adsabs.harvard.edu/search/q={}', # ADS
    'gh': 'https://github.com/search?q={}&type=repositories', # Github
    'arw': 'https://wiki.archlinux.org/index.php?search={}', # Arch Wiki
    'arp': 'https://archlinux.org/packages/?sort=&q={}&maintainer=&flagged=', # Arch Packages
    'aru': 'https://aur.archlinux.org/packages?O=0&K={}', # AUR
    'passthrough': '{}', # Go exactly to the given url
}

# Change blank and start page
c.url.default_page = f"file://{CONFIG}/qutebrowser/default_page/index.html"
c.url.start_pages = f"file://{CONFIG}/qutebrowser/default_page/index.html"

#
### Window
#

# Hide window decorations
c.window.hide_decoration = True

# Window and tabtitle format
c.window.title_format = '{current_title}{title_sep}({current_url})'
c.tabs.title.format = '{index}{perc}: ' + c.window.title_format

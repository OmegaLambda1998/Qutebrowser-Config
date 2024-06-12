#!/usr/bin/env python3

# External Packages
import os
import sys
import tldextract

# Internal Packages
from userscript_utils import *

def overleaf_project_id(url):
    extracts = tldextract.extract(url)
    scheme, parts = url.split('://')
    parts = parts.split('/')
    if extracts.domain == 'overleaf' and 'project' in parts:
        return parts[2]
    return None

def is_detacher(url):
    scheme, parts = url.split('://')
    parts = parts.split('/')
    return parts[-1] == "detacher"

def is_detached(url):
    scheme, parts = url.split('://')
    parts = parts.split('/')
    return parts[-1] == "detached"

def compile_project(project_id):
    #detacher_url = f'https://www.overleaf.com/project/{project_id}/detacher'
    #detached_url = f'https://www.overleaf.com/project/{project_id}/detached'
    delay = 0

    commands = [
        info(f'Compiling Project: {project_id}', clear=False, get_cmd=True),
        f'fake-key ":w<Return>"',
        f'cmd-later {str(delay := delay + 15000)} {info(f"Compilation hopefully finished, downloading pdf", clear=False, get_cmd=True)}',
        f'cmd-later {str(delay := delay + 1000)} mode-enter normal',
        f'cmd-later {str(delay := delay + 1000)} hint pdf',
        f'cmd-later {str(delay := delay + 1000)} fake-key -g "<Return>"',
        f'cmd-later {str(delay := delay + 1000)} fake-key -g "y"',
        f'cmd-later {str(delay := delay + 1000)} mode-enter passthrough',
        f'cmd-later {str(delay := delay + 10000)} download-clear',
    ]
    send_chained(commands)

def main(args):
    project_id = overleaf_project_id(QUTE_URL)
    if not project_id:
        info("Not an overleaf project, quitting")
        return None
    info(f"Overleaf Project ID: {project_id}")
    if args is not None:
        if 'download' in args:
            download_pdf(project_id)
        if 'compile' in args:
            compile_project(project_id)

if __name__ == "__main__":
    main(get_args())

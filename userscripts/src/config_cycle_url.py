#!/usr/bin/env python3

# External Packages
import os
import sys

# Internal Packages
from userscript_utils import *

def main(args):
    url = QUTE_URL

    scheme, *parts = url.split('://')

    parts = [p for p in '/'.join(parts).split('/') if p != '']

    info(f"{url}, {scheme}, {parts}")

    pattern = None

    # If it's a file, just store the full filepath
    if scheme == 'file':
        pattern = url
    # Get pattern for non http[s] urls
    # For example: qute://help/settings.html => qute://help
    elif scheme not in ['http', 'https']:
        pattern = f'{scheme}://{parts[0]}'
    # Otherwise we just want the {domain} part of {scheme}://{domain}/{path}
    else:
        pattern = parts[0]

    if pattern is not None:
        info(f"Cycling {args} for pattern: {pattern}", clear=False)
        send_command(f'config-cycle --pattern {pattern} {args}')

if __name__ == "__main__":
    args = get_args()
    if args is not None:
        args = ' '.join(args)
    main(args)

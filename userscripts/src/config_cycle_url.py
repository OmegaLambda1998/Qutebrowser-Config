#!/usr/bin/env python3

# External Packages
import os
import sys
import tldextract

# Internal Packages
from userscript_utils import *

def main(args):
    url = QUTE_URL
    extracts = tldextract.extract(url)
    scheme, parts = url.split('://')
    parts = parts.split('/')
    info(f"{url}, {extracts}, {scheme}, {parts}")

    pattern = None
    if scheme not in ['http', 'https']:
        pattern = f'{scheme}://{parts[0]}'
    else:
        extract_components = [
            str(extracts.subdomain),
            str(extracts.domain),
            str(extracts.suffix),
        ]
        pattern_components = [e for e in extract_components if len(e) > 0]
        if len(pattern_components) > 1:
            pattern = '.'.join(pattern_components)
        elif len(pattern_components) == 1:
            pattern = pattern_components[0]

    if pattern is not None:
        info(f"Cycling {args} for pattern: {pattern}", clear=False)
        send_command(f'config-cycle --pattern {pattern} {args}')

if __name__ == "__main__":
    args = get_args()
    if args is not None:
        args = ' '.join(args)
    main(args)

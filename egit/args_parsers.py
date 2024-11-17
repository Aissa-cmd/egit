import argparse

egit_parser = argparse.ArgumentParser(description="Enhanced Git CLI")
egit_parser.add_argument('-nf', '--no-fetch', default=False, dest='no_fetch', action='store_true', help="Don't check status of remote branch")
egit_parser.add_argument('-v', '--verbose', default=False, dest='verbose', action='store_true', help="Print status of remote branch")
egit_parser.add_argument('-i', '--interactive', default=False, dest='interactive', action='store_true', help="Interactive rebase")
egit_parser.add_argument('-no', '--no-origin', default=False, dest='no_origin', action='store_true', help="When found multile remotes, ask which one to use")
egit_parser.add_argument('-c', '--check', action="store", dest="check" , default=None, help="Run pre-hooks")
egit_parser.add_argument('-V', '--version', action="store_true", dest="version", default=False, help="Show version")

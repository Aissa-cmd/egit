import sys
import os
from egit.git_wrapper import GitWrapper
from egit.utils import get_repo, parse_argv
from egit.repository import Repository


"""
Exit codes:
0 - success
1 - Invalid git repository
2 - No arguments provided
3 - No Git arguments provided
"""


def main():
    try:
        cli_args = sys.argv[1:]
        argv_options = parse_argv(cli_args)
        cwd = os.getcwd()
        repo = get_repo(cwd)
        repository = Repository(repo)
        git_wrapper = GitWrapper(repository, argv_options)
        git_wrapper.run()
    except KeyboardInterrupt:
        print('Interrupted')

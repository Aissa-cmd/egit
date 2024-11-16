import sys
import argparse
import subprocess
from pathlib import Path
from git import Repo, exc
from rich.progress import Progress, SpinnerColumn, TextColumn
from egit.args_parsers import egit_parser
from egit.console import Console

class ArgvOptions:
    def __init__(self, egit_args: argparse.Namespace, git_args: list[str]):
        self.egit_args = egit_args
        self.git_command = git_args[0] if len(git_args) > 0 else None
        self.git_args = git_args

    def __str__(self):
        return f"""
        egit_args: {self.egit_args}
        git_args: {self.git_args}
        """
    
def print_help():
    help_text = """
    egit - Enhanced Git CLI (v0.1.0)
    
    Usage:
        egit [options] -- [git commands/options]
    
    Options:
        -h, --help            Show help
        -nf, --no-fetch       Don't check status of remote branch
        -v, --verbose         Print status of remote branch
        -i, --interactive     Interactive rebase
        -no, --no-origin      When found multile remotes, ask which one to use
        -c, --check           Run pre-hooks
    """
    print(help_text)

def parse_argv(args: list[str]) -> ArgvOptions:
    egit_args = []
    git_args = []
    split_index = len(args)
    if "--" in args:
        split_index = args.index('--')
    if len(args) > 0:
        egit_args = args[:split_index]
    if split_index + 1 < len(args):
        git_args = args[split_index + 1:]
    parsed_egit_args = egit_parser.parse_args(egit_args)
    parsed_options = ArgvOptions(parsed_egit_args, git_args)
    # called with no args (egit and git) or with -h/--help, print help and exit
    if (len(egit_args) == 0 or parsed_options.egit_args.help) and (len(git_args) == 0):
        print_help()
        sys.exit(0)
    return parsed_options

progress = Progress(
    SpinnerColumn(),
    TextColumn("[progress.description]{task.description}"),
    transient=True,
)

# * git helpers
def get_repo(path: str) -> Repo:
    try:
        base_path_to_repo = subprocess.check_output(
            ["git", "rev-parse", "--show-toplevel"],
            cwd=path,
        ).decode("utf-8").strip()
        return Repo(base_path_to_repo)
    except exc.InvalidGitRepositoryError:
        Console.error("Invalid git repository")
        sys.exit(1)

def file_path_relative_to_repo(file: Path, repo: Repo) -> str:
    """
    Returns the relative path of a file to the repo
    """
    return file.relative_to(Path(repo.working_dir).parent).as_posix()

def get_repo_remote_names(repo: Repo) -> list[str]:
    """
    Returns the list of remote names in the repo
    """
    result = subprocess.check_output(
        ["git", "remote", "show", "-n"],
        cwd=repo.working_dir,
    ).decode("utf-8").strip().split("\n")
    cleaned_result = filter(lambda remote_name: len(remote_name) > 0, result)
    return list(cleaned_result)

def fetch_remote(repo: Repo, remote_name: str):
    """
    Fetches the remote branch
    """
    subprocess.run(
        ["git", "fetch", remote_name],
        cwd=repo.working_dir,
    )

def is_repo_first_commit(repo: Repo) -> bool:
    """
    Returns True if the repo is first commit
    """
    try:
        subprocess.check_output(
            ["git", "rev-parse", "--verify", "HEAD"],
            cwd=repo.working_dir,
        )
        return False
    except subprocess.CalledProcessError:
        return True

def get_status(repo: Repo):
    """
    Get repo status
    """
    result = subprocess.check_output(
        ["git", "status"],
        cwd=repo.working_dir,
    ).decode("utf-8").strip()
    return result

def get_staged_file_names(repo: Repo) -> list[Path]:
    """
    Returns the list of staged files in the repo
    """
    result = subprocess.check_output(
        ["git", "diff", "--name-only", "--cached"],
        cwd=repo.working_dir,
    ).decode("utf-8").strip().split("\n")
    cleaned_result = filter(lambda file_name: len(file_name) > 0, result)
    return [Path(repo.working_dir, file_name) for file_name in cleaned_result]

def get_staged_file_diff(repo: Repo, file: Path) -> str:
    """
    Returns the diff of the file in the repo
    """
    result = subprocess.check_output(
        ["git", "diff", "--cached", "HEAD", file.relative_to(repo.working_dir).as_posix()],
        cwd=repo.working_dir,
    )
    return result.decode("utf-8")

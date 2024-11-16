import subprocess
import sys
from egit.repository import Repository
from egit.utils import ArgvOptions
from egit.exceptions import HookException
from egit.git_hooks import GitHooks
from egit.runner import Runner


class GitWrapper:
    def __init__(self, repo: Repository, args: ArgvOptions):
        self.repo = repo
        self.args = args
        self.runner = Runner(args)
        self.git_hooks = GitHooks(repo, args, self.runner)

    def _run_command(self, command: list[str]):
        self.runner.verbose(f'🚀 running command: {" ".join(command)}')
        return subprocess.run(" ".join(command), cwd=self.repo.working_dir, shell=True)

    def run(self):
        git_command = self.args.git_command
        # check for hooks
        if self.args.egit_args.check is not None:
            git_command = self.args.egit_args.check
        pre_hook = getattr(self.git_hooks, f'pre_{git_command}', None)
        if pre_hook is None:
            self.runner.verbose(f"No pre_{git_command} hook found")
        else:
            self.runner.verbose(f"Found pre_{git_command} hook")
        try:
            if pre_hook is not None:
                self.runner.verbose(f"Running pre-{git_command} hook")
                pre_hook()
        except HookException:
            if self.args.egit_args.check is None:
                self.runner.info('Git command did not run')
                sys.exit(0)
        except Exception as e:
            self.runner.error(f"Error pre-{git_command} hook: {e}")
            sys.exit(1)
        if self.args.egit_args.check is not None:
            self.runner.verbose(f"Running only pre-{git_command} hook")
            sys.exit(0)
        if git_command.startswith('-'):
            # no hooks for options, just run git
            subprocess.run(['git'] + self.args.git_args)
            return
        command_result = self._run_command(['git'] + self.args.git_args)
        if command_result.returncode != 0:
            sys.exit(1)
        post_hook = getattr(self.git_hooks, f'post_{git_command}', None)
        if post_hook is None:
            self.runner.verbose(f"No post_{git_command} hook found")
        else:
            self.runner.verbose(f"Found post_{git_command} hook")
        if pre_hook is not None:
            self.runner.verbose(f"Running post-{git_command} hook")
            post_hook()

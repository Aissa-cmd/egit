import sys
import re
from egit.repository import Repository
from egit.utils import (
    file_path_relative_to_repo,
    ArgvOptions,
    progress,
)
from egit.exceptions import (
    HookException,
    PreHookException,
    PostHookException,
)
from egit.runner import Runner

class GitHooks:
    def __init__(self, repo: Repository, args: ArgvOptions, runner: Runner):
        self.repo = repo
        self.args = args
        self.runner = runner

    # [!] utils
    def _pull_changes(self):
        remote_names = self.repo.remote_names
        remote_to_use = None
        if len(remote_names) == 0:
            self.runner.info('No remotes found')
            return
        if self.args.egit_args.no_origin == False and self.args.egit_args.interactive == False:
            if len(remote_names) > 1:
                self.runner.info(f'Found multiple remotes, using "origin"')
            else:
                self.runner.info(f'using "origin"')
            remote_to_use = "origin"
        else:
            remote_to_use = self.runner.ask(f"Found multiple remotes, which one to use?", choices=remote_names)
        with progress as progress_bar:
            progress_bar.add_task(f"fetching remote: {remote_to_use}", total=1)
            # fetch_remote(self.repo, remote_to_use)
            self.repo.fetch(remote_to_use)
        git_status = self.repo.status
        behind_patter = r"(Your branch is behind '.*?' by \d+ commit)"
        match = re.search(behind_patter, git_status, flags=re.IGNORECASE)
        if match is not None and len(match.groups()) > 0:
            self.runner.warning(match.groups()[0])
            self.runner.info('You can use "git pull" to update your branch, before comming your changes')
            sys.exit(0)

    def _check_no_comments(self) -> bool:
        found_comment = False
        for file in self.repo.staged_files:
            diff = self.repo.get_staged_file_diff(file)
            # check for '!NO_TRACK' in diff
            if re.search(r'!NO_TRACK', diff, flags=re.IGNORECASE):
                self.runner.rich_text([
                    ["⏮️ ", "white"],
                    ["!NO_TRACK", "bold yellow"],
                    [" found in ", "white"],
                    [file_path_relative_to_repo(file, self.repo.repo), "cyan underline"],
                ])
                found_comment = True
            # check for '!NO_COMMIT' in diff
            if re.search(r'!NO_COMMIT', diff, flags=re.IGNORECASE):
                self.runner.rich_text([
                    ["⏮️ ", "white"],
                    ["!NO_COMMIT", "bold yellow"],
                    [" found in ", "white"],
                    [file_path_relative_to_repo(file, self.repo.repo), "cyan underline"],
                ])
                found_comment = True
        return found_comment

    def _check_no_commit_comment(self) -> bool:
        found_comment = False
        for file in self.repo.staged_files:
            # check for '!NO_COMMIT' in diff
            diff = self.repo.get_staged_file_diff(file)
            # use re better that str.contains case-insensitive
            if re.search(r'!NO_COMMIT', diff, flags=re.IGNORECASE):
                self.runner.rich_text([
                    ["⏮️ ", "white"],
                    ["!NO_COMMIT", "bold yellow"],
                    [" found in ", "white"],
                    [file_path_relative_to_repo(file, self.repo.repo), "cyan underline"],
                ])
                found_comment = True
        return found_comment

    def _check_no_track_comment(self) -> bool:
        found_comment = False
        for file in self.repo.staged_files:
            # check for '!NO_TRACK' in diff 
            diff = self.repo.get_staged_file_diff(file)
            # use re better that str.contains case-insensitive
            if re.search(r'!NO_TRACK', diff, flags=re.IGNORECASE):
                self.runner.rich_text([
                    ["⏮️ ", "white"],
                    ["!NO_TRACK", "bold yellow"],
                    [" found in ", "white"],
                    [file_path_relative_to_repo(file, self.repo.repo), "cyan underline"],
                ])
                found_comment = True
        return found_comment

    def _check_todo_comment(self) -> bool:
        found_comment = False
        for file in self.repo.staged_files:
            # check for 'TODO' in diff
            diff = self.repo.get_staged_file_diff(file)
            if re.search(r'TODO', diff, flags=re.IGNORECASE):
                self.runner.rich_text([
                    ["⏮️ ", "white"],
                    ["TODO", "bold #FF8C00"],
                    [" found in ", "white"],
                    [file_path_relative_to_repo(file, self.repo.repo), "cyan underline"],
                ])
                found_comment = True
        if found_comment:
            result = self.runner.ask("Found TODOs, do you want to continue?", default="y", choices=["y", "n"])
            if result == "n":
                self.runner.info("Aborting")
                sys.exit(0)
            else:
                self.runner.info("Continuing")
        return found_comment
    
    # * pre_hooks
    def pre_commit(self):
        if self.args.egit_args.no_fetch:
            self.runner.info('Skipping fetch')
        else:
            self._pull_changes()
        # get staged file names
        found_coment = self._check_no_comments()
        self._check_todo_comment()
        if found_coment:
            raise PreHookException('found files with !NO_COMMIT or !NO_TRACK')

    def pre_add(self):
        pass

    # ...

    # * post_hooks
    def post_commit(self):
        print('⏭️ running post commit')

    def post_add(self):
        pass

    # ...
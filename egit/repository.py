from pathlib import Path
from git import Repo
from egit.utils import (
    get_repo_remote_names,
    get_staged_file_names,
    get_staged_file_diff,
    is_repo_first_commit,
    fetch_remote,
    get_status,
)

class Repository:
    def __init__(self, repo: Repo):
        self.repo = repo
        self._is_first_commit = None
        self._remote_names = None
        self._status = None
        self._staged_files = None
        self._staged_files_diff = {}

    @property
    def working_dir(self):
        return self.repo.working_dir

    @property
    def is_first_commit(self):
        if self._is_first_commit is None:
            self._is_first_commit = is_repo_first_commit(self.repo)
        return self._is_first_commit

    @property
    def remote_names(self) -> list[str]:
        if self._remote_names is None:
            self._remote_names = get_repo_remote_names(self.repo)
        return self._remote_names
    
    @property
    def status(self) -> str:
        if self._status is None:
            self._status = get_status(self.repo)
        return self._status

    @property
    def staged_files(self) -> list[Path]:
        if self._staged_files is None:
            self._staged_files = get_staged_file_names(self.repo)
        return self._staged_files

    def fetch(self, remote_name: str):
        fetch_remote(self.repo, remote_name)

    def get_staged_file_diff(self, file: Path) -> str:
        file_path = str(file.as_posix())
        if file_path not in self.staged_files:
            diff = get_staged_file_diff(self.repo, file)
            self._staged_files_diff[file_path] = diff
            return diff
        return self._staged_files_diff[file_path]

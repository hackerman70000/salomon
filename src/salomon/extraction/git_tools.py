import os
import subprocess
from pathlib import Path


def clone_repo(repo_url: str, target_dir: Path, branch: str = "main") -> Path:
    repo_name = repo_url.rstrip("/").split("/")[-1]
    if repo_name.endswith(".git"):
        repo_name = repo_name[:-4]

    repo_path = target_dir / repo_name

    token = os.getenv("GIT_TOKEN")

    result = repo_url.replace(
        "https://",
        f"https://x-access-token:{token}@",
        1,
    )

    cmd = [
        "git",
        "clone",
        "--depth", "1",
        "--branch", branch,
        "--single-branch",
        result,
        str(repo_path),
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        raise RuntimeError(result.stderr)

    return repo_path
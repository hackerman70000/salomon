import os
import subprocess
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


def _inject_token(repo_url: str) -> str:
    token = os.getenv("GIT_TOKEN")

    if not token:
        return repo_url

    if repo_url.startswith("https://"):
        return repo_url.replace(
            "https://",
            f"https://{token}@",
        )

    return repo_url


def clone_repo(repo_url: str, target_dir: Path) -> Path:
    repo_name = repo_url.rstrip("/").split("/")[-1]
    if repo_name.endswith(".git"):
        repo_name = repo_name[:-4]

    repo_path = target_dir / repo_name

    auth_url = _inject_token(repo_url)

    result = subprocess.run(
        ["git", "clone", "--depth", "1", auth_url, str(repo_path)],
        capture_output=True,
        text=True,
        check=False,
    )

    if result.returncode != 0:
        raise RuntimeError(f"Git clone failed:\n{result.stderr.strip()}")

    return repo_path
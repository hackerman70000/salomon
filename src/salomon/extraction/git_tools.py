from pathlib import Path
import subprocess

def clone_repo(repo_url: str, target_dir: Path) -> Path:
    repo_name = repo_url.rstrip("/").split("/")[-1]
    if repo_name.endswith(".git"):
        repo_name = repo_name[:-4]

    repo_path = target_dir / repo_name

    result = subprocess.run(
        ["git", "clone", "--depth", "1", repo_url, str(repo_path)],
        capture_output=True,
        text=True,
        check=False,
    )

    if result.returncode != 0:
        raise RuntimeError(f"Git clone failed:\n{result.stderr.strip()}")

    return repo_path

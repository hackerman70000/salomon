from pathlib import Path

from salomon.extraction.models import LanguageName, SourceFile

LANGUAGE_EXTENSIONS: dict[LanguageName, set[str]] = {
    "c" : {".c"},
    "cpp": {".cc", ".cpp", ".cxx", ".h", ".hh", ".hpp"},
    "python": {".py"}
}

SUPPORTED_EXTENSIONS: set[str] = {item for ext in LANGUAGE_EXTENSIONS.values() for item in ext}


IGNORED_DIR_NAMES = {
    ".git",
    ".venv",
    "venv",
    "__pycache__",
    "build",
    "cmake-build-debug",
    "cmake-build-release",
    "dist",
    "vendor",
    "third_party",
    "node_modules",
}


def should_skip_dir(dir_name: str) -> bool:
    return dir_name in IGNORED_DIR_NAMES


def detect_language(path: Path) -> LanguageName:
    suffix = path.suffix.lower()

    for lang, extensions in LANGUAGE_EXTENSIONS.items():
        if suffix in extensions:
            return lang

    raise ValueError(f"Unsupported file type: {suffix}")


def find_files(repo_dir: Path) -> list[SourceFile]:
    files: list[SourceFile] = []

    for path in repo_dir.rglob("*"):
        if not path.is_file():
            continue

        if any(should_skip_dir(part) for part in path.parts):
            continue

        if path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            continue

        files.append(
            SourceFile(
                path=str(path.relative_to(repo_dir)),
                language=detect_language(path),
            )
        )

    return sorted(files, key=lambda f: f.path)
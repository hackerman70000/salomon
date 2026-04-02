from __future__ import annotations

import tempfile
from pathlib import Path
from typing import Iterator

from tree_sitter import Parser
from tree_sitter_language_pack import get_language

from salomon.extraction.file_discovery import detect_language, find_files
from salomon.extraction.git_tools import clone_repo
from salomon.extraction.models import FunctionInfo, LanguageName


class FunctionExtractor:
    def __init__(self) -> None:
        self._parsers: dict[LanguageName, Parser] = {
            "c": self._make_parser("c"),
            "cpp": self._make_parser("cpp"),
            "python": self._make_parser("python"),
        }

    def from_code(
            self,
            code: str,
            *,
            language: LanguageName,
            file_path: str = "<memory>",
    ) -> list[FunctionInfo]:
        source = code.encode("utf-8")
        parser = self._parsers[language]
        tree = parser.parse(source)

        results: list[FunctionInfo] = []

        for node in self._walk(tree.root_node):
            if node.type != "function_definition":
                continue

            name = self._extract_function_name(source, node)
            if not name:
                name = "<unparsed>"

            results.append(
                FunctionInfo(
                    name=name,
                    file_path=file_path,
                    language=language,
                    start_line=node.start_point[0] + 1,
                    end_line=node.end_point[0] + 1,
                    signature=self._extract_signature(source, node),
                    code=self._node_text(source, node),
                )
            )

        return results

    def from_file(self, path: str | Path) -> list[FunctionInfo]:
        path = Path(path)
        code = path.read_text(encoding="utf-8", errors="replace")
        language = detect_language(path)

        return self.from_code(
            code,
            language=language,
            file_path=str(path),
        )

    def from_repo(self, repo_url: str) -> list[FunctionInfo]:
        all_functions: list[FunctionInfo] = []

        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            repo_path = clone_repo(repo_url, tmp_path)
            source_files = find_files(repo_path)

            for source_file in source_files:
                absolute_path = repo_path / source_file.path

                try:
                    file_functions = self.from_file(absolute_path)
                except Exception as exc:
                    print(f"Skipping {source_file.path}: {exc}")
                    continue

                for function in file_functions:
                    all_functions.append(
                        function.model_copy(
                            update={"file_path": source_file.path},
                        )
                    )

        return all_functions

    @staticmethod
    def _make_parser(language_name: LanguageName) -> Parser:
        parser = Parser()
        parser.language = get_language(language_name)
        return parser

    @staticmethod
    def _node_text(source: bytes, node) -> str:
        return source[node.start_byte:node.end_byte].decode(
            "utf-8",
            errors="replace",
        )

    def _walk(self, node) -> Iterator:
        yield node
        for child in node.children:
            yield from self._walk(child)

    def _extract_function_name(self, source: bytes, node) -> str | None:
        declarator = node.child_by_field_name("declarator")
        if declarator is None:
            return None

        stack = [declarator]

        while stack:
            current = stack.pop()

            if current.type in {"identifier", "field_identifier", "operator_name"}:
                return self._node_text(source, current)

            for child in reversed(current.children):
                stack.append(child)

        return None

    def _extract_signature(self, source: bytes, node) -> str:
        body = node.child_by_field_name("body")
        if body is None:
            return self._node_text(source, node).strip()

        return source[node.start_byte:body.start_byte].decode(
            "utf-8",
            errors="replace",
        ).strip()



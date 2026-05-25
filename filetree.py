import os
import fnmatch
import argparse
from pathlib import Path
from typing import List, Tuple, Optional, Set


class DirectoryTreeGenerator:
    """Generates a visual representation of the directory tree, respecting .gitignore."""

    def __init__(
        self,
        root_dir: str = ".",
        output_file: Optional[str] = None,
        max_depth: Optional[int] = None,
    ):
        self.root_dir = Path(root_dir).resolve()
        self.output_file = output_file
        self.max_depth = max_depth

        # Characters to draw the tree
        self.indent_prefix = "│  "
        self.branch_prefix = "├─ "
        self.last_prefix = "└─ "
        self.space_prefix = "   "

        # Using set for O(1) lookup
        self.ignore_names: Set[str] = {
            ".git",
            "__pycache__",
            "migrations",
            "venv",
            "env",
            ".venv",
            ".env",
        }
        self.ignore_rules = self._load_gitignore()

    def _load_gitignore(self) -> List[Tuple[str, bool]]:
        """Reads and processes .gitignore file rules, if it exists."""
        gitignore_path = self.root_dir / ".gitignore"
        if not gitignore_path.exists():
            return []

        rules = []
        for line in gitignore_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            negate = line.startswith("!")
            if negate:
                line = line[1:].strip()
            rules.append((line, negate))
        return rules

    def _is_ignored(self, path: Path) -> bool:
        """Checks if the current path should be ignored."""
        if path.name in self.ignore_names:
            return True

        if not self.ignore_rules:
            return False

        rel_path = path.relative_to(self.root_dir).as_posix()
        is_dir = path.is_dir()
        if is_dir and not rel_path.endswith("/"):
            rel_path += "/"

        ignored = False
        for pattern, negate in self.ignore_rules:
            if self._matches_gitignore_pattern(rel_path, pattern, is_dir):
                ignored = not negate
        return ignored

    def _matches_gitignore_pattern(
        self, rel_path: str, pattern: str, is_dir: bool
    ) -> bool:
        """Compares the file path with a gitignore pattern."""
        if pattern.endswith("/"):
            pattern = pattern.rstrip("/")
            if not is_dir:
                return False

        if pattern.startswith("/"):
            pattern = pattern[1:]
            return fnmatch.fnmatch(rel_path.rstrip("/"), pattern)

        if "/" in pattern:
            return fnmatch.fnmatch(rel_path.rstrip("/"), pattern) or fnmatch.fnmatch(
                rel_path, f"**/{pattern}"
            )

        return fnmatch.fnmatch(Path(rel_path).name, pattern) or fnmatch.fnmatch(
            rel_path, f"**/{pattern}"
        )

    def generate_tree(self) -> None:
        """Initiates the tree generation and manages output (console and/or file)."""
        tree_content = [f"{self.root_dir.name}/"]
        self._generate_tree_recursive(self.root_dir, [], tree_content, current_depth=0)

        output_text = "\n".join(tree_content)
        print(output_text)

        if self.output_file:
            with open(self.output_file, "w", encoding="utf-8") as f:
                f.write(output_text)
            print(f"\n[+] Directory structure saved to: '{self.output_file}'")

    def _generate_tree_recursive(
        self, directory: Path, prefix: List[str], output: List[str], current_depth: int
    ) -> None:
        """Recursively traverses directories building the tree lines."""
        if self.max_depth is not None and current_depth >= self.max_depth:
            return

        try:
            entries = [e for e in directory.iterdir() if not self._is_ignored(e)]
        except PermissionError:
            output.append("".join(prefix) + self.last_prefix + "[Access Denied]")
            return

        # Sort: folders first, then files (alphabetically)
        entries.sort(key=lambda x: (not x.is_dir(), x.name.lower()))

        for i, entry in enumerate(entries):
            is_last = i == len(entries) - 1
            current_prefix = self.last_prefix if is_last else self.branch_prefix

            line = "".join(prefix) + current_prefix + entry.name
            if entry.is_dir():
                line += "/"
            output.append(line)

            if entry.is_dir():
                new_prefix = prefix + [
                    self.space_prefix if is_last else self.indent_prefix
                ]
                self._generate_tree_recursive(
                    entry, new_prefix, output, current_depth + 1
                )


def main():
    parser = argparse.ArgumentParser(
        description="Generates a visual directory tree, respecting .gitignore."
    )
    parser.add_argument(
        "directory",
        nargs="?",
        default=".",
        help="Root directory to generate the tree (default: current directory).",
    )
    parser.add_argument(
        "-o", "--output", type=str, help="Saves output to the specified file."
    )
    parser.add_argument(
        "-d", "--depth", type=int, help="Maximum depth of folders to traverse."
    )

    args = parser.parse_args()

    try:
        tree_generator = DirectoryTreeGenerator(
            root_dir=args.directory, output_file=args.output, max_depth=args.depth
        )
        tree_generator.generate_tree()
    except Exception as e:
        print(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    main()

import os
import fnmatch
from pathlib import Path


class DirectoryTreeGenerator:
    def __init__(self, root_dir=".", output_file="directory_structure.txt"):
        self.root_dir = Path(root_dir)
        self.output_file = output_file
        self.indent_prefix = "│  "
        self.branch_prefix = "├─ "
        self.last_prefix = "└─ "
        self.ignore_names = [
            ".git",
            "__pycache__",
            "migrations",
            "venv",
            "env",
            ".venv",
            ".env",
        ]
        self.ignore_rules = self._load_gitignore()

    def _load_gitignore(self):
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

    def _is_ignored(self, path):
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

    def _matches_gitignore_pattern(self, rel_path, pattern, is_dir):
        if pattern.endswith("/"):
            pattern = pattern.rstrip("/")
            if not is_dir:
                return False

        if pattern.startswith("/"):
            pattern = pattern[1:]
            return fnmatch.fnmatch(rel_path.rstrip("/"), pattern)

        if "/" in pattern:
            return (
                fnmatch.fnmatch(rel_path.rstrip("/"), pattern)
                or fnmatch.fnmatch(rel_path, f"**/{pattern}")
            )

        return (
            fnmatch.fnmatch(Path(rel_path).name, pattern)
            or fnmatch.fnmatch(rel_path, f"**/{pattern}")
        )

    def generate_tree(self):
        tree_content = [f"{self.root_dir.name}/"]
        self._generate_tree_recursive(self.root_dir, [], tree_content)
        with open(self.output_file, "w", encoding="utf-8") as f:
            f.write("\n".join(tree_content))
        print("\n".join(tree_content))

    def _generate_tree_recursive(self, directory, prefix, output):
        entries = [e for e in directory.iterdir() if not self._is_ignored(e)]
        entries.sort(key=lambda x: (not x.is_dir(), x.name))
        for i, entry in enumerate(entries):
            is_last = i == len(entries) - 1
            current_prefix = self.last_prefix if is_last else self.branch_prefix
            line = "".join(prefix + [current_prefix + entry.name])
            if entry.is_dir():
                line += "/"
            output.append(line)
            if entry.is_dir():
                new_prefix = prefix + [self.indent_prefix if not is_last else "    "]
                self._generate_tree_recursive(entry, new_prefix, output)


def main():
    try:
        current_dir = os.getcwd()
        tree_generator = DirectoryTreeGenerator(current_dir)
        tree_generator.generate_tree()
        print(f"\nDirectory structure has been saved to 'directory_structure.txt'")
    except Exception as e:
        print(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    main()

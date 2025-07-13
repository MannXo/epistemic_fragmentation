import os

# Folders to ignore while walking the tree
IGNORED_DIRS = {'__pycache__', 'venv', '.git', '.mypy_cache', '.idea', '.pytest_cache'}

def print_tree(root_path, prefix=''):
    entries = sorted(os.listdir(root_path))
    entries = [e for e in entries if e not in IGNORED_DIRS and not e.startswith('.')]

    for i, entry in enumerate(entries):
        path = os.path.join(root_path, entry)
        connector = '└── ' if i == len(entries) - 1 else '├── '
        print(prefix + connector + entry)
        if os.path.isdir(path):
            extension = '    ' if i == len(entries) - 1 else '│   '
            print_tree(path, prefix + extension)

if __name__ == '__main__':
    project_root = '.'
    print_tree(project_root)

from pathlib import Path
import argparse
import sys


def find_empty(root: Path, recursive: bool = True):
    if root.exists() and root.is_file():
        return [root] if root.stat().st_size == 0 else []
    matches = []
    iterator = root.rglob('*') if recursive else root.iterdir()
    for p in iterator:
        try:
            if p.is_file() and p.stat().st_size == 0:
                matches.append(p)
        except OSError:
            continue
    return matches


def main():
    ap = argparse.ArgumentParser(
        description="Find (and optionally delete) empty files."
    )
    ap.add_argument('path', nargs='?', default='.',
                    help='directory or file to check')
    ap.add_argument('-n', '--no-recursive', action='store_true',
                    help='do not recurse into subdirectories')
    ap.add_argument('-d', '--delete', action='store_true',
                    help='delete found empty files')
    args = ap.parse_args()

    root = Path(args.path).resolve()
    if not root.exists():
        print(f"Path not found: {root}", file=sys.stderr)
        sys.exit(2)

    empties = find_empty(root, recursive=not args.no_recursive)
    if not empties:
        print(f"No empty files found.")
        return

    for f in empties:
        print(f)
        if args.delete:
            try:
                f.unlink()
            except Exception as e:
                print(f"Faield to delete {f}: {e}", file=sys.stderr)

    print(f"\n{len(empties)} empty file(s) {'deleted' if args.delete else 'found'}.")


if __name__ == "__main__":
    main()

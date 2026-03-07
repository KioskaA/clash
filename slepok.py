import os
import sys
import argparse


def generate_snapshot(start_path: str, output_file: str, ignore_dirs: set = None) -> None:
    if ignore_dirs is None:
        ignore_dirs = {'.git', 'venv', '__pycache__'}

    lines = []
    start_path = os.path.abspath(start_path)
    # Корневая папка как заголовок
    lines.append(f"# {os.path.basename(start_path)}/")

    def walk_dir(current_path: str, level: int) -> None:
        try:
            with os.scandir(current_path) as entries:
                dirs = []
                files = []
                for entry in entries:
                    if entry.is_dir(follow_symlinks=False):
                        if entry.name in ignore_dirs:
                            continue
                        dirs.append(entry.name)
                    else:
                        files.append(entry.name)

                dirs.sort()
                files.sort()

                for name in dirs:
                    indent = '  ' * level
                    lines.append(f"{indent}- **{name}/**")
                    full_path = os.path.join(current_path, name)
                    walk_dir(full_path, level + 1)

                for name in files:
                    indent = '  ' * level
                    lines.append(f"{indent}- {name}")

        except PermissionError:
            indent = '  ' * level
            lines.append(f"{indent}- *[Permission Denied]*")
        except Exception as e:
            indent = '  ' * level
            lines.append(f"{indent}- *[Error: {e}]*")

    walk_dir(start_path, 1)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

    print(f"Snapshot сохранён в {output_file}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", nargs="?", default=".", help="Путь к директории")
    parser.add_argument("output", nargs="?", default="snapshot.md", help="Имя выходного файла")
    args = parser.parse_args()

    if not os.path.isdir(args.directory):
        print(f"Ошибка: '{args.directory}' не является директорией.")
        sys.exit(1)

    generate_snapshot(args.directory, args.output)


if __name__ == "__main__":
    main()
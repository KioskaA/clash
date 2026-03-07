import os
from datetime import datetime
from pathlib import Path
from typing import Optional


class StorageCreator:
    """
    Класс для создания и проверки структуры файлового хранилища клана.
    По умолчанию папка storage создаётся в той же директории, где находится этот файл.
    """

    def __init__(self, storage_root: Optional[str] = None):
        """
        :param storage_root: путь к корневой папке storage.
            Если не указан, используется './storage' относительно расположения этого файла.
        """
        if storage_root is None:
            # Папка, где лежит текущий файл
            base_dir = Path(__file__).parent
            self.storage_root = base_dir / 'storage'
        else:
            self.storage_root = Path(storage_root)

    def ensure_clan_structure(self, clan_tag: str) -> None:
        """
        Создаёт всю необходимую структуру папок и timestamp-файлов для указанного клана.
        Если какие-то элементы уже существуют, они не перезаписываются (кроме случая,
        когда отсутствует timestamp-файл – он создаётся с текущим временем).

        :param clan_tag: тег клана (например, '#2PQR89VGU')
        """
        # Папка клана
        clan_dir = self.storage_root / f"clan_{clan_tag}"
        clan_dir.mkdir(parents=True, exist_ok=True)

        # Основной timestamp клана
        self._ensure_timestamp_file(clan_dir / "main_timestamp.txt")

        # Структура подпапок и соответствующие им timestamp-файлы
        subdirs_config = {
            "players/current_members": None,
            "players/left_players": None,
            "cw": "cw_timestamp.txt",
            "cwl": "cwl_timestamp.txt",
            "raids": "raids_timestamp.txt",
            "clan_games": "cg_timestamp.txt",
        }

        for subdir, timestamp_file in subdirs_config.items():
            dir_path = clan_dir / subdir
            dir_path.mkdir(parents=True, exist_ok=True)

            if timestamp_file:
                self._ensure_timestamp_file(dir_path / timestamp_file)

    def _ensure_timestamp_file(self, file_path: Path) -> None:
        """
        Вспомогательный метод: если файл не существует, создаёт его и записывает
        текущую дату и время в формате 'last_updated: YYYY-MM-DD HH:MM:SS'.
        """
        if not file_path.exists():
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            file_path.write_text(f'last_updated: {current_time}', encoding="utf-8")


# Пример использования:
if __name__ == "__main__":
    # Без аргументов – storage появится рядом с этим файлом
    creator = StorageCreator()
    creator.ensure_clan_structure("#2PQR89VGU")

    # Можно явно указать другой путь, например:
    # creator = StorageCreator("/absolute/path/to/storage")
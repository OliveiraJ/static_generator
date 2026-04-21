import shutil
import sys
from pathlib import Path

from generate_page import generate_pages_recursive

STATIC = "./static"
PUBLIC = "./docs"
TEMPLATE = "./template.html"
CONTENT = "./content"
DEFAULT_BASE_PATH = "/"


def main():
    base_path = DEFAULT_BASE_PATH
    if len(sys.argv) > 1:
        base_path = sys.argv[1]

    sync_folder(STATIC, PUBLIC)
    generate_pages_recursive(CONTENT, TEMPLATE, PUBLIC, base_path)


def sync_folder(source: str | Path, destination: str | Path) -> None:
    source = Path(source)
    destination = Path(destination)

    if not source.exists():
        raise FileNotFoundError(f"Pasta de origem não encontrada: {source}")

    if not source.is_dir():
        raise NotADirectoryError(f"Origem não é uma pasta: {source}")

    # Limpa o destino (ou cria se não existir)
    if destination.exists():
        shutil.rmtree(destination)
    destination.mkdir(parents=True)

    # Copia tudo da origem para o destino
    shutil.copytree(source, destination, dirs_exist_ok=True)


if __name__ == "__main__":
    main()

from pathlib import Path
from typing import List, Dict
from zipfile import ZipFile

from utils import Version

_default_install_location = Path.home() / "install"
_default_cache_location = Path.home() / ".ipm" / "cache"

Path.mkdir(_default_cache_location, parents=True, exist_ok=True)


def get_cache_destination(file):
    return _default_cache_location / file


def install():
    print("ASDF")


def unzip(a):
    with ZipFile(a, "r") as zf:
        zf.extractall(a)


def get_installed_packages(d=_default_install_location) -> Dict[str, List[Version]]:
    return {
        c.name: [Version(v.name) for v in c.iterdir() if Version.is_valid(v.name)]
        for c in d.iterdir()
    }


if __name__ == "__main__":
    print(get_installed_packages())

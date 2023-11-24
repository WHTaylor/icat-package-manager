from typing import Optional

from . import files
from . import repo
from .utils import Version


def do_list(component: Optional[str]):
    installed = files.get_installed_packages()

    if component:
        available_versions = repo.get_component_versions(component)
        installed_versions = installed.get(component, [])
        for v in available_versions:
            if v in installed_versions:
                print(f"{v} (installed)")
            else:
                print(v)
    else:
        available = repo.get_components()
        for package in available:
            if package in installed:
                current = max(installed[package])
                print(f"{package} (installed: {current})")
            else:
                print(package)


def do_install(
        component: str,
        version: Optional[Version] = None,
        allow_snapshots=False):
    installed = files.get_installed_packages().get(component, [])

    if version:
        if version in installed:
            print(f"{component} {version} is already installed")
            return
        install_version = version
    else:
        all_available = repo.get_component_versions(component)
        available = [v for v in all_available if
                     (allow_snapshots or not v.is_snapshot())]
        latest = max(available)
        if latest in installed:
            print(f"Latest available version, {latest}, is already installed")
            if latest != max(all_available):
                print(f"Newer snapshot, {max(all_available)}, is available")
            return
        install_version = latest

    repo.download_distro(component, install_version)
    dest = files.extract_distro(component, install_version)

    if not installed:
        print(
            f"Installed {dest}. No prior version existed, so configuration "
            "must be completed manually")
        return

    print(f"Copying config from existing install to {dest}")
    files.copy_config(component, max(installed), install_version)

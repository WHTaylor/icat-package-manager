import argparse
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
        all_available = repo.get_component_versions(args.component)
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


def run():
    parser = argparse.ArgumentParser(
        description="Find and install ICAT components")
    subparsers = parser.add_subparsers(required=True)

    list_parser = subparsers.add_parser(
        "list",
        help="Show available/installed components")
    list_parser.add_argument(
        "component",
        nargs="?",
        help="List available versions of a specific component")
    list_parser.set_defaults(func=do_list)

    install_parser = subparsers.add_parser(
        "install",
        help="Install an ICAT package"
    )
    install_parser.add_argument(
        "component",
        help="The component to install")
    install_parser.add_argument(
        "version",
        help="Specific version to install. Defaults to latest version if not specified",
        type=Version,
        nargs="?")
    install_parser.add_argument(
        "-s", "--allow-snapshots",
        action="store_true",
        help="Allow snapshot versions. If not set, only non -SNAPSHOT versions will be used"
    )
    install_parser.set_defaults(func=do_install)

    args = parser.parse_args()
    kwargs = {
        k: v for k, v in vars(args).items() if k != "func"
    }
    args.func(**kwargs)


if __name__ == "__main__":
    run()

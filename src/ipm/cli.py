from typing import Optional
import argparse
import repo
import files


def do_list(component: Optional[str]):
    installed = files.get_installed_packages()

    if component:
        available_versions = repo.get_package_versions(component)
        installed_versions = installed[component]
        for v in available_versions:
            if v in installed_versions:
                print(f"{v} (installed)")
            else:
                print(v)
    else:
        available = repo.get_packages()
        for package in available:
            if package in installed:
                current = max(installed[package])
                print(f"{package} (installed: {current})")
            else:
                print(package)


def do_install(component: str, version: Optional[str] = None):
    print(component)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Manage ICAT components")
    subparsers = parser.add_subparsers()

    list_parser = subparsers.add_parser('list')
    list_parser.add_argument('component', nargs="?")
    list_parser.set_defaults(func=do_list)

    args = parser.parse_args()
    args.func(args.component)

from typing import Optional
import argparse
import repo


def do_list(component: Optional[str]):
    if component:
        result = repo.get_package_versions(component)
    else:
        result = repo.get_packages()

    for r in result:
        print(r)


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

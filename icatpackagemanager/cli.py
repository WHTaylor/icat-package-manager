import argparse

from . import commands
from .utils import Version


def run():
    parser = argparse.ArgumentParser(
        description="Find and install ICAT components")
    subparsers = parser.add_subparsers()

    list_parser = subparsers.add_parser(
        "list",
        help="Show available/installed components")
    list_parser.add_argument(
        "component",
        nargs="?",
        help="List available versions of a specific component")
    list_parser.set_defaults(func=commands.do_list)

    install_parser = subparsers.add_parser(
        "install",
        help="Install an ICAT package"
    )
    install_parser.add_argument(
        "component",
        help="The component to install")
    install_parser.add_argument(
        "version",
        help="Specific version to install. Defaults to latest version if not "
             "specified",
        type=Version,
        nargs="?")
    install_parser.add_argument(
        "-s", "--allow-snapshots",
        action="store_true",
        help="Allow snapshot versions. If not set, only non -SNAPSHOT versions "
             "will be used"
    )
    install_parser.set_defaults(func=commands.do_install)

    args = parser.parse_args()
    if not hasattr(args, 'func'):
        print("Must provide a subcommand")
        parser.print_usage()
        exit(1)

    kwargs = {
        k: v for k, v in vars(args).items() if k != "func"
    }
    args.func(**kwargs)


if __name__ == "__main__":
    run()

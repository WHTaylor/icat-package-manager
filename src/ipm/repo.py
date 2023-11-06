from urllib.request import urlopen

import lxml.html

from src.ipm.utils import Version

_default_repo = "https://repo.icatproject.org/repo/org/icatproject/"


def _get_table_rows(page):
    parsed = lxml.html.fromstring(page)
    table_rows = parsed.xpath("body/table//tr")
    # First rows are headers/dividers, last is a divider
    package_rows = table_rows[3:-1]
    # Second column contains a link element, which has the package name
    return [r.getchildren()[1].getchildren()[0] for r in package_rows]


def get_packages(repo_url=_default_repo):
    with urlopen(repo_url) as f:
        if f.status != 200:
            raise Exception(f"Couldn't reach {repo_url}")
        page = f.read().decode()
        links = _get_table_rows(page)
        return [link.text.strip("/") for link in links]


def get_package_versions(package_name, repo_url=_default_repo):
    with urlopen(f"{repo_url}/{package_name}") as f:
        if f.status != 200:
            raise Exception(f"Couldn't reach {repo_url}")
        page = f.read().decode()
        links = _get_table_rows(page)
        version_strings = (link.text.strip("/") for link in links)
        return [Version(v) for v in version_strings if Version.is_valid(v)]


if __name__ == "__main__":
    print(get_packages())
    print(get_package_versions("icat.ear"))
    print(get_package_versions("icat.server"))

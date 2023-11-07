# ICAT Package Manager

## CLI

 - `list`, lists all components available from the repo, and which are installed
 - `list <component>`, lists available and installed versions of the component
 - `install <component>`:
   - Checks for installed versions of the component
   - Checks for available versions of the component
   - If there is no newer version, do nothing.
   - Otherwise, download latest distro, and unzips it into install directory
   - If there is no previous version, stop and prompt for configuration
   - Otherwise, copy config from previous version, and run setup script
 - `install <component> <version>`, installs specific version of a package
 - By default, install will not use snapshot versions, and won't install if the version already exists. Will have arguments to allow override both of these.

## Terminology

 - Repository, or repo, is a website hosting ICAT components. By default, this is the official `repo.icatproject.org`.
 - A component is one of the ICAT projects ie. `icat.server`, `authn.simple`, etc. Components can have many versions, in the format `x.y.z-<suffix>`.
 - A package is a specific version of a component. Packages are:
   - 'Available' if it exists in the repo
   - 'Installed' if it exists in the install directory
   - 'Deployed' if it's currently running on the application server
 - A distro is a zipfile containing a built package.
 - The distro cache is a directory containing distros downloaded from the repo.
 - The install directory is where distro's are unpacked so that they can be deployed.

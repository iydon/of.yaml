# Changelog

## [`v0.3`](https://github.com/iydon/of.yaml/tree/v0.3)

- Add partial support for OpenFOAM standard list
- Modify the YAML file to include multiple documents (meta, foam, static)
- ...


## [`v0.4`](https://github.com/iydon/of.yaml/tree/v0.4)

- Add command line tool with [click](https://github.com/pallets/click)
- Modify the original single file to Python package
- ...


## [`v0.5`](https://github.com/iydon/of.yaml/tree/v0.5)

- Add version information for YAML
- Modify project name
- ...


## [`v0.6`](https://github.com/iydon/of.yaml/tree/v0.6)

- Add real-time progress bar for most OpenFOAM solvers
- Add "other" document for YAML to hold uncategorized data
- Add script to convert Python package into a single file
- Add this changelog :)
- Modify `README.md` according to the [template](https://github.com/othneildrew/Best-README-Template)
- Remove the idea of rewriting the project using Rust


## [`v0.7`](https://github.com/iydon/of.yaml/tree/v0.7)

- Add more progress bar adapters for applications
- Add MkDocs support, which will be used to build documentation in the future
- Add post-processing sub-module for VTK
- Fix version comparison problem (major and minor)
- Fix typo: permision -> permission


## [`v0.8`](https://github.com/iydon/of.yaml/tree/v0.8)

- Add more cases
- Add more comments in source code
- Add more information about OpenFOAM (root, environ, foamSearch, etc.)
- Add post-processing (probes)
- Update program architecture


## [`v0.9`](https://github.com/iydon/of.yaml/tree/v0.9)

- Add `Array?D` data type
- Add draft conversion of OpenFOAM case to YAML format
- Add more cases
- Add third-party tutorials ([BasicOpenFOAMProgrammingTutorials](https://github.com/UnnamedMoose/BasicOpenFOAMProgrammingTutorials))
- Fix type hints error in standalone script (`t.Optional['Foam']`)
- Update program architecture (original `PostProcess` is renamed `VTK` and degraded to a sub-module of `PostProcess`)
- Update `Command::run` to allow `pipeline` to specify additional parameters


## [`v0.10`](https://github.com/iydon/of.yaml/tree/v0.10)

- Add the ability to import modules on demand
- Add support for multilingual documentation
- Add optional dependencies for package
- Publish `ifoam` package on [PyPi](https://pypi.org/project/ifoam) using Poetry


## [`v0.11`](https://github.com/iydon/of.yaml/tree/v0.11)

- Add third-party tutorials ([openfoam_tutorials](https://github.com/openfoamtutorials/openfoam_tutorials))
- Add [mypy](https://github.com/python/mypy) support for static types
- Add the ability to parse additional Foam files
- Add the ability to read remote case
- Add [typing-extensions](https://github.com/python/typing_extensions) support
- Compatible with python3.7
- Move cases to a new [repository](https://github.com/iydon/of.yaml-tutorial)
- Update program architecture (`Foam::_save_static`)


## `v0.12`

- Add extra sub-module for sending emails and timing
- Add namespace to package
- Update program architecture
    - `foam::base::type::{Data, Version}` -> `foam::util::object::{Data, Version}`
    - `foam::base::parse` -> `foam::parse`
    - `foam::extra` -> `foam::util::object`

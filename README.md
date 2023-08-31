<!-- Template from https://github.com/othneildrew/Best-README-Template -->
<div id="top"></div>



<!-- PROJECT SHIELDS -->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![GPL-3.0 License][license-shield]][license-url]



<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/iydon/of.yaml">
    🟢⬜🟩⬜🟩<br />
    ⬜⬜⬜⬜⬜<br />
    🟩⬜🟩⬜🟩<br />
    ⬜⬜⬜⬜⬜<br />
    🟩⬜🟩⬜🟩<br />
  </a>

  <h3 align="center">OpenFOAM.YAML</h3>

  <p align="center">
    Python Interface to OpenFOAM Case (Configured Using YAML)
    <br />
    <a href="https://ifoam.readthedocs.io"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    View <a href="https://github.com/iydon/of.yaml-template">Demo</a>/<a href="https://github.com/iydon/of.yaml-tutorial">Tutorial</a>
    ·
    <a href="https://github.com/iydon/of.yaml/issues">Report Bug</a>
    ·
    <a href="https://github.com/iydon/of.yaml/issues">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#installation">Installation</a></li>
        <li><a href="#demo">Demo</a></li>
      </ul>
    </li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About the Project

This repository was originally designed to solve the problem of complex OpenFOAM case structure, and the solution was to re-present the original cases using the common configuration file format YAML. Later, since there is a corresponding package for the YAML format in Python, I wrote this Python interface package for OpenFOAM, and then I added progress bars to most OpenFOAM solvers by analyzing log files in real time. Although there are still many details to be specified in this repository, its function of generating cases and calling solvers is ready for preliminary use, for example, I used this package to generate cases in batch in my own project. In the future I would like to integrate the post-processing steps into this interface package as well.

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

This project currently uses Poetry to manage Python dependencies. I've heard good things about [PDM](https://github.com/pdm-project/pdm) so far, and may provide PDM support subsequently.

### Installation

```sh
pip3 install ifoam[full]
```

### Demo

Save the following demo code as a separate file (e.g. `demo.py`).

```python
from foam import Foam

foam = Foam.fromDemo('cavity')
foam['foam']['system', 'controlDict', 'endTime'] = 1.0
foam.save('cavity')
foam.cmd.all_run()
```

Running the demo code in the virtual environment results in the following output.

```sh
$ python demo.py

Foam.fromPath('.../of.yaml/foam/demo/7/cavity.yaml', warn=False)
Running blockMesh on .../of.yaml/cavity using 1 processes if in parallel
Running icoFoam on .../of.yaml/cavity using 1 processes if in parallel
100%|█████████████████████████████████████| 1.0/1.0 [00:02<00:00,  2.24s/it]
```



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repository and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- LICENSE -->
## License

Distributed under the GPL-3.0 License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Iydon Liang - [@iydon](https://github.com/iydon) - liangiydon_AT_gmail.com

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
[contributors-shield]: https://img.shields.io/github/contributors/iydon/of.yaml.svg?style=for-the-badge
[contributors-url]: https://github.com/iydon/of.yaml/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/iydon/of.yaml.svg?style=for-the-badge
[forks-url]: https://github.com/iydon/of.yaml/network/members
[stars-shield]: https://img.shields.io/github/stars/iydon/of.yaml.svg?style=for-the-badge
[stars-url]: https://github.com/iydon/of.yaml/stargazers
[issues-shield]: https://img.shields.io/github/issues-closed/iydon/of.yaml.svg?style=for-the-badge
[issues-url]: https://github.com/iydon/of.yaml/issues
[license-shield]: https://img.shields.io/github/license/iydon/of.yaml.svg?style=for-the-badge
[license-url]: https://github.com/iydon/of.yaml/blob/master/LICENSE.txt

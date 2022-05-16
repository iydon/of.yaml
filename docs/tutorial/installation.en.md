To get a local copy up and running follow these simple example steps.

## Prerequisites

This project currently uses Poetry to manage Python dependencies. I've heard good things about [PDM](https://github.com/pdm-project/pdm) so far, and may provide PDM support subsequently. If Poetry is not installed, you can refer to [official installation guide](https://github.com/python-poetry/poetry#installation).


## Installation

1. Clone the repository
   ```sh
   git clone https://github.com/iydon/of.yaml.git
   ```
2. Install Python dependencies
   ```sh
   poetry install --extras full
   ```
3. Activate the virtual environment
   ```sh
   poetry shell
   ```
4. (Optional) Convert Python package into a single file
   ```sh
   make standalone
   ```

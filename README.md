# SLUMBER - Sleep Logging and Unsupervised Monitoring through BioElectrical Recordings

## Description

<!--
Provide a concise description of your project here.
Describe what it does, the problem it solves, and why it’s useful.
-->

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Testing](#testing)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Prerequisites

- Python 3.10
- Windows operating system

## Installation

1. Create a virtual environment and activate it

   ```
   python -m venv %VENV_PATH%
   %VENV_PATH%\Scripts\activate
   ```

4. Install [Poetry](https://python-poetry.org/docs/#installing-manually)
   ```
   pip install -U pip setuptools
   pip install poetry
   ```

5. Install dependencies
   ```
   poetry install
   ```

## Usage

After installing dependencies, you can start the application with:

```bash
poetry run slumber <condition-name>
```

### Scoring Sleep Stages from ZMax Data

To score sleep stages from ZMax data, use the following command:

```bash
poetry run score_zmax <data_dir> [options]
```

Required arguments:
- `data_dir`: Path to ZMax data directory containing EEG data files

Optional arguments:
- `--model-dir`: Path to directory containing U-Time model (default: models/utime_EEG_10)
- `--weight-file`: Name of specific weight file to use
- `--no-filter`: Do not apply a filter to the data
- `--epoch_duration`: Duration of epochs in seconds (default: 30)
- `--output-path`: Path to save output predictions (default: <data_dir>/utime_predictions.csv)


## Configuration

<!--
Detail any configuration options, environment variables, or settings that need to be set up.
-->

## Deployment

<!--
If applicable, describe the process for deploying the application to various environments (e.g., staging, production).
-->

## Contributing

To contribute, please follow these steps:

1. **Fork the Repository**: Start by forking the repository.
2. **Follow the Contribution Guidelines**: Please follow the instructions outlined in the [CONTRIBUTING.md](CONTRIBUTING.md) file for setting up your development environment, creating feature branches, and submitting pull requests.
3. **Create a Pull Request**: Go to the original repository and create a pull request from your forkd repository. Provide a detailed description of your changes and any relevant information.

### Reporting Issues

If you encounter any issues or bugs, please report them using the GitHub issue tracker. Provide as much detail as possible, including steps to reproduce the issue and any relevant information.

## License

This project is licensed under a **Modified GPL-3.0 License (Non-Commercial)**.  
You may use, modify, and distribute this software **for non-commercial purposes only**.  
For commercial use, please contact the author for permission.  
See the [LICENSE](./LICENSE) file for full details.

## Contact

<!--
Provide ways for others to reach out: email, Twitter handle, etc.
-->

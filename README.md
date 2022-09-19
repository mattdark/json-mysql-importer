
# JSON to MySQL Importer
A Python app that imports data from a dataset (JSON) into a MySQL DB


## Prerequisites
### MySQL
While this script could work with any MySQL variant, tests were run on Percona Server for MySQL. If you already have MySQL running on your system, skip this step.

For installing Percona Server for MySQL from the repositories on Debian and Ubuntu, follow the instructions below. For other operating systems check the [documentation](https://docs.percona.com/percona-server/latest/installation.html).

Before installing Percona Server for MySQL, make sure `curl` and `gnupg2` are installed.
```
$ sudo apt install gnupg2 curl
```

Then, install `percona-release`, a tool that allows users to automatically configure which Percona Software repositories are enabled or disabled.

Get the repository package:
```
$ wget https://repo.percona.com/apt/percona-release_latest.$(lsb_release -sc)_all.deb
```

Install the downloaded package with dpkg:
```
$ sudo dpkg -i percona-release_latest.$(lsb_release -sc)_all.deb
```

Enable the ps80 repository:
```
$ sudo percona-release setup ps80
```

Install percona-server-server, the package that provides the Percona Server for MySQL:
```
$ sudo apt install percona-server-server
```



```
$ sudo dpkg -i percona-release_latest.$(lsb_release -sc)_all.deb
```

### Conda
Before running the Python script that imports the data into a MySQL DB, you must install Conda through Anaconda or Miniconda. [Here](https://docs.conda.io/projects/conda/en/latest/user-guide/install/download.html#anaconda-or-miniconda) you can find more information on which one is better for you.

To install Anaconda, go to [anaconda.com/products/distribution](https://www.anaconda.com/products/distribution) and download the installer for your operating system.

If you're on Linux, run the following command after getting the installer:
```
$ bash Anaconda3-2022.05-Linux-x86_64.sh
```

Replacing the filename according to the version you're installing

It will prompt you to confirm some configuration details:
* Accepting license
* Confirming installation folder
* Initializing Anaconda (by the installer)

## Getting Started
### Clone this repository
```
git clone https://github.com/mattdark/json-mysql-importer.git
```

### Configure your Python environment
### virtualenv and pip

#### Conda
When you clone this repository to your local development environment, you will find an environment.yml file that contains information about the Python version and dependencies required by this project. This file is used by Conda to configure the virtual environment and install dependencies.



After installing Anaconda, change to the `json-mysql-importer` directory:
```
$ cd json-mysql-importer
```

Create the environment:
```
$ conda env create -f environment.yml
```

This command will create a virtual environment for your project, install Python 3.10 and dependencies specified in the `environment.yml` file.

Once the environment is created, you can activate it by running:
```
$ conda activate percona
```

Before running the script, don't forget to set `user`, `password` and `host` in the `base.py` module, required for connecting to your MySQL DB.


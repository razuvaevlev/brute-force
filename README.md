# Dictionary brute-force script 

![Static Badge](https://img.shields.io/badge/Python-3.9-blue) [![License: GPL v3](https://img.shields.io/badge/License-GPLv3-green.svg)](https://www.gnu.org/licenses/gpl-3.0)


> _Python script for dictionary attack on forms consisting of two fields: username and password_


## Requirements
>[!WARNING] 
>Python 3.9 (or later) needed
## Installation
```sh
git clone https://github.com/razuvaevlev/brute-force.git
cd brute-force
pip install requests
```
## Usage
```
usage: brute.py [-h] -d DICTIONARY [-u USERNAME] [-n WORKERS] [-t TIMEOUT] url

Bruteforce for simple html form

positional arguments:
  url                   URL to login page

options:
  -h, --help            show this help message and exit
  -d DICTIONARY, --dictionary DICTIONARY
                        Password dictionary file
  -u USERNAME, --username USERNAME
                        Username to bruteforce(default: "admin")
  -n WORKERS, --workers WORKERS
                        Number of workers to use(default:10)
  -t TIMEOUT, --timeout TIMEOUT
                        Timeout in milliseconds

```
## Example
```
$ python3.9 brute.py <url> -d top-500-passwords.txt
Password: SuperSecret
Execution time: 0.9264669418334961
```

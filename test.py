from bs4 import BeautifulSoup
import requests
import os
import threading
import logging
config_path="/Users/liexe/pt_saved/reload"
def python_version_reload():
    def thread():
        url=f"https://www.python.org/ftp/python/"
        try:
            with requests.get(url,verify=False) as r:
                bs = BeautifulSoup(r.content, "lxml")
                results = []
                for i in bs.find_all("a"):
                    if i.text[0].isnumeric():
                        results.append(i.text[:-1])
                if results:
                    sort_results(results)
        except Exception as e:
            logging.error(f"Python Version Reload Wrong:{e}")
    threadings=threading.Thread(target=thread)
    threadings.start()
class Version:
    def __init__(self, version_str: str):
        self.version = version_str.split('.')
        while len(self.version) < 3:
            self.version.append('0')

    def __lt__(self, other):
        for i in range(3):
            if (v1 := int(self.version[i])) < (v2 := int(other.version[i])):
                return True
            elif v1 > v2:
                return False
        else:
            return False
def sort_results(results: list):
    _results = results.copy()
    length = len(_results)
    for i in range(length):
        for ii in range(0, length - i - 1):
            v1 = Version(_results[ii])
            v2 = Version(_results[ii + 1])
            if v1 < v2:
                _results[ii], _results[ii + 1] = _results[ii + 1], _results[ii]
    print(_results)
    
python_version_reload()
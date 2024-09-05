# WeBrufo (WEB BRUte-FOrcer)

## Table of Contents

* [Introduction](#Introduction)
* [Dependencies](#Dependencies)
* [Usage](#Usage)



## Introduction
A simple script to bruteforce web forms. Uses CSS selector to locate the inputs and perform bruteforce. Both credential bruteforce and spraying can be performed using this script. And for the name, was too lazy to think and come up with some cool name soo...

## Dependencies
The script primarily requires Selenium to start a headless browser session and perform the bruteforce. Can be installed using  
``` python
pip install selenium
```
## Usage
The basic command to run the script is
```bash
python webrufo.py -u 'https://pentest-ground.com:81/login' -p '#form2Example2'::file.txt "#form2Example1"::"file.txt" --submit 'body > div > div > form > button'
```
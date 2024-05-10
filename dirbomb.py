import argparse
import requests
from colorama import init, Fore
import multiprocessing
import sys
import signal
import time

# Arguments
parse = argparse.ArgumentParser()
parse.add_argument("-u", "--url", type=str, help="URL example: https://example.com/")
parse.add_argument("-w", "--wordlist")
parse.add_argument("-t", "--threads", type=int)
args = parse.parse_args()
url = args.url
wordlist = []
threads = args.threads
with open(args.wordlist, 'r') as f:
    contents = f.readlines()
wordlist = [item.strip('\n') for item in contents]
chunks = int(len(wordlist) / threads)
chunked_list = [wordlist[i:i+chunks] for i in range(0, len(wordlist), chunks)]

# GET requests
def attack(w, u):
    n = 0
    for i in w:
        url = u + w[n]
        n += 1
        response = requests.get(url)
        if response.status_code == 200:
            print(Fore.GREEN + "[+] " + Fore.RESET + "Found directory:",Fore.CYAN + url + Fore.RESET + "\n")

init() # Init colorama
if __name__ == '__main__': # Main execute
    try:
        print(Fore.LIGHTMAGENTA_EX + "\nStarting search:\n" + Fore.RESET)
            
        processes = []
        
        n=0
        for i in range(threads):
            p = multiprocessing.Process(target = attack, args=(chunked_list[n], url))
            p.start()
            processes.append(p)
            n+=1
            
        # Joins all the processes 
        for p in processes:
            p.join()
        signal.pause()
    except KeyboardInterrupt:
        print ("\n! Received keyboard interrupt, quitting threads.\n")
        time.sleep(2)
        for p in processes:
            p.terminate()
            time.sleep(1)
        sys.exit()
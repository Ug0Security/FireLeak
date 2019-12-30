#!/usr/bin/env ../venv/bin/python3.5

import sys
import logging
import asyncio
from aiohttp import ClientSession, TCPConnector, client_exceptions
import socket
# from aiohttp.resolver import AsyncResolver
from time import time, localtime, strftime
from statistics import mean
import json
from setting import USER_AGENT, CONN_TIMEOUT, READ_TIMEOUT, URL_TEST, IPV4_ONLY
#from url_list import url_ltuple

wordlist = sys.argv[1]
try :
    wa = sys.argv[4]
except:
    wa = ""
try:
    wb = sys.argv[3]
except:
    wb = ""
my_list = """
"""

try :	
    offset = int(sys.argv[2])
except:
    offset = 0


    
    

url_list = my_list.split('\n')[1:-1]
url_list = set(url_list)                    # eleminate ducplicate in case of
url_ltuple = list()



with open (wordlist) as wl:
    for line in wl.readlines()[offset:]:
        ligne = line.rstrip()
        url_ltuple.append((0,"https://" + wb + ligne + wa + ".firebaseio.com/.json"))
        



sites = list()


client_headers = {'User-agent': USER_AGENT,
            'Accept-Language': 'en-US,en;q=0.8',
            'Accept': '*/*','Accept-Encoding': 'gzip,deflate,sdch'
            }



class Site(object):
    def __init__(self, id, url):
        self.id = id
        self.url = url
        self.status = None
        self.headers = None
        self.state = None
        self.resp_time = None
        self.test_time = None


for id, url in url_ltuple:
    sites.append(Site(id, url))



def mutlidict2string(multidict):
    lines = list()
    for key in multidict:
        line = ''.join((key, ': ', str(multidict[key]), '\n'))
        lines.append(line)

    text = ''.join(lines)
    return text


async def gethead(site, session, start_time, retesting=False):

    try:
        async with session.get(site.url) as response:
            site.status = str(response.status)
            html = await response.text()
            

            if site.status == "401":
                print(site.url + " == 401") 
                pass


            if site.status == "404":
                #print(site.url +" == 404")
                pass

            elif site.status == "200":  
                print ("\n" + site.url + " == " + site.status)
                truc = json.dumps(html, sort_keys=True, indent=4)
                size = len(truc)
                
                if size > 1000:
                    if size > 1000000:
                        size = size / 1000000
                        print(str(size) + "MB")
                    else:
                  
                        size = size / 1000
                        print(str(size) + "KB")
                else :
                    print(str(size) + "B")

               
                if "password" in truc.lower():
                    print ("----------- Password Leak (password)?")
                elif "pass" in truc.lower():
                    print ("----------- Password Leak (pass)?")


                elif "users" in truc.lower():
                   print ("----------- User Leak ?")

                elif "email" in truc.lower():
                    print ("----------- Email Leak ?")

                elif "token" in truc.lower():
                     print ("----------- Token Leak ?")

                elif "hash" in truc.lower():
                    print ("----------- Hash Leak ?")

                elif "iban" in truc.lower():
                    print ("----------- Iban Leak ?")

                elif "bank" in truc.lower():
                    print ("----------- Bank Leak ?")    
                elif "phone" in truc.lower():
                    print ("----------- Phone Leak ?")

                elif "auth" in truc.lower():
                    print ("----------- Auth Leak ?")

                elif "aws" in truc.lower():
                    print ("----------- AWS Leak ?")
             
                else :
                    print ("No Leak")
            #else: 
                #print(site.url) 
                #print(html)   


    except asyncio.TimeoutError:
        pass
    except ValueError:
        pass
    except client_exceptions.ClientConnectionError:
        pass
    except client_exceptions.ClientResponseError:
        pass
    except:
        pass

async def bound_gethead(sem, site, session, retesting=False):

    async with sem:
        start_time = time()
        await gethead(site, session, start_time=start_time, retesting=retesting)


async def run(sites, retesting=False):

    if IPV4_ONLY:
        connector = TCPConnector(verify_ssl=False, family=socket.AF_INET)
    else:
        connector = TCPConnector(verify_ssl=False)

    sem = asyncio.Semaphore(100)

    tasks = []
    if not retesting:
        read_timeout = READ_TIMEOUT
        conn_timeout = CONN_TIMEOUT
    else:
        read_timeout = READ_TIMEOUT + READ_TIMEOUT/2
        conn_timeout = CONN_TIMEOUT + CONN_TIMEOUT/2

    async with ClientSession(connector=connector, read_timeout=read_timeout,
                             conn_timeout=conn_timeout, headers=client_headers) as session:
        for site_ in sites:

            task = asyncio.ensure_future(bound_gethead(sem, site_, session, retesting=retesting))
            tasks.append(task)

        responses = await asyncio.gather(*tasks)


loop = asyncio.get_event_loop()
future = asyncio.ensure_future(run(sites=sites))
loop.run_until_complete(future)

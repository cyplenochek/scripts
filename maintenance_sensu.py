#!/usr/bin/python
import sys, getopt
import json
import urllib2
import time

def main(argv):
    url = ''
    reason = ''
    mode = ''
    try:
      opts, args = getopt.getopt(argv,"hu:r:m:",["ifile=","ofile="])
    except getopt.GetoptError:
      print 'clear.py -u <url> -r <reason> -m <mode clear|create>'
      sys.exit(2)
    for opt, arg in opts:
      if opt == '-h':
         print 'clear.py -u <url> -r <reason> -m <mode clear|create>'
         sys.exit()
      elif opt in ("-u"):
         url = arg
      elif opt in ("-r"):
         reason = arg
      elif opt in ("-m"):
         mode = arg

    print 'URL is "', url
    print 'reason is "', reason
    print 'mode is ', mode

    if mode == 'clear':
       url2 = 'http://'+url+'/silenced'
       print url2
       response = urllib2.urlopen(url2)
       json_obj = json.load(response)

       for i in json_obj:
          if i['reason'] == reason:
             print i['id']
             data = {}
             data['id'] = i['id']
             json_data = json.dumps(data)
             req = urllib2.Request('http://'+url+'/silenced/clear')
             req.add_header('Content-Type', 'application/json')
             response = urllib2.urlopen(req, json.dumps(data))
             time.sleep(2)

    if mode == 'create':
       url2 = 'http://'+url+'/clients'
       print url2
       response = urllib2.urlopen(url2)
       json_obj = json.load(response)

       for i in json_obj:
         print i['name']
         data = {}
         data['subscription'] = "client:"+i['name']
         data['reason'] = reason
         json_data = json.dumps(data)
         print json_data
         req = urllib2.Request('http://'+url+'/silenced')
         req.add_header('Content-Type', 'application/json')
         response = urllib2.urlopen(req, json.dumps(data))
         time.sleep(2)


if __name__ == "__main__":
   main(sys.argv[1:])



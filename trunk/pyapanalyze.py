#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

import sys
import getopt
import time

lst_ip=dict()
lst_files=dict()
lst_fext=dict()
lst_file_extension=dict( { ".php":0, ".png":0,".jpg":0,".js":0,".html":0} )
lst_by_days = dict()
bandwidth=0


months = {
    'Jan':'01',
    'Feb':'02',
    'Mar':'03',
    'Apr':'04',
    'May':'05',
    'Jun':'06',
    'Jul':'07',
    'Aug':'08',
    'Sep':'09',
    'Oct':'10',
    'Nov':'11',
    'Dec':'12'
    }


###TAKE from: http://code.google.com/p/apachelog/source/browse/trunk/apachelog.py   
def parse_date(date):
    """
    Takes a date in the format: [05/Dec/2006:10:51:44 +0000]
    (including square brackets) and returns a two element
    tuple containing first a timestamp of the form
    YYYYMMDDHH24IISS e.g. 20061205105144 and second the
    timezone offset as is e.g.;

    parse_date('[05/Dec/2006:10:51:44 +0000]')  
    >> ('20061205105144', '+0000')

    It does not attempt to adjust the timestamp according
    to the timezone - this is your problem.
    """
    date = date[1:-1]
    elems = [
        date[7:11],
        months[date[3:6]],
        date[0:2],
        date[12:14],
        date[15:17],
        date[18:20],
        ]
    return (''.join(elems),date[21:])



def parse_apache_log(line):
  global bandwidth
  global lst_by_days
  if( line[0] in lst_ip ):
    lst_ip[line[0]] = lst_ip[line[0]] + 1
  else:
    lst_ip[line[0]] = 0
    
  str_date = line[3].replace("[","[") + " " + line[4].replace("]","]")
  #s = time.strptime(str_date,"%d/%b/%Y:%H:%M:%S %Z")
  str_date = parse_date(str_date)
  #print str_date

  
  month = int(str_date[0][4:6])
  day   = int(str_date[0][6:8])
  
 
  bytes=0
  
  fileExtension=""
  
  if(line[5] == '"GET'):
    #fileName, fileExtension = os.path.splitext(line[6])
    #print fileName + " ~ " + fileExtension
    if( line[6] in lst_files ):
      lst_files[line[6]] = lst_files[line[6]] + 1   
    else:
      lst_files[line[6]] = 0
      
    if(line[8]=="200"):
      for k in lst_file_extension:
	if k in line[6]:
	  #print "Extension " + k + " in " + line[6]
	  if (line[9] != "-\n"):
	    bytes = int((line[9].replace("\n","")))
	    #print "\t bytes: " + str(bytes)
	    lst_file_extension[k] += bytes
	    bandwidth = bandwidth + bytes
      
    
    if( (month,day) in lst_by_days):
      #print lst_by_days[month]
      lst_by_days [ month, day ] += 1
    else:
      #print lst_by_days
      lst_by_days [ month,day ] = 1
      #print line
      #if(fileExtension != ""):
	#fileExtension = fileExtension.replace(".","")
	#if fileExtension.startswith("php"):
	  #fileExtension = "php"
	#print line
	#print "f: " + fileExtension
	#if(line[9].replace("\n","").isdigit()):
	  #if( fileExtension  in lst_file_extension ):
	    #lst_file_extension[ fileExtension ] += int((line[9].replace("\n","")))
	  #else:
	    #lst_file_extension[ fileExtension ] = int((line[9].replace("\n","")))
      
      
 


  
  
def main(argv=None):
  global fondo
  longitud=158
  anchura=104
  if argv is None:
    argv = sys.argv
    
  l_lines=list()
  
  for i,arg in enumerate(argv):
    if (i>0):
      print "Loading " + arg
      f_log = [line.split(' ') for line in open(arg)]
      for l_line in f_log:
	l_lines.append(l_line)
	#if l_line not in l_lines:
	  #l_lines.append(l_line)
  
  #f_log = [line.split(' ') for line in open("/home/dzayas/logAnal/ssl_access_log")]
  #for l_line in f_log:
    #if l_line not in l_lines:
      #l_lines.append(l_line)

  #f_log = [line.split(' ') for line in open("/home/dzayas/logAnal/ssl_access_log-20121014")]
  #for l_line in f_log:
    #if l_line not in l_lines:
      #l_lines.append(l_line)
  
  
  
  
  for l_line in l_lines:
    parse_apache_log(l_line)
  print "Hits by IP:"
  print lst_ip
  #print lst_files
  print "Bandwidth by file (bytes)"
  print lst_file_extension
  print "Total kbytes: " + str(bandwidth/1024)+"KB"
  print "Total hits (month,day)"
  print lst_by_days

if __name__ == "__main__":
  try:
      import psyco
      psyco.full()
  except ImportError:
      pass
  sys.exit(main())
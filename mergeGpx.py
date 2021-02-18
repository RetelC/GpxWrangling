###########################
## mergeGpx.py
## Name: Cas Retel
## E-mail: casretel@gmail.com
## Date: 2018.11.17
###########################
## This is a standalone Python script which allows the user to merge .gpx files. 
## These are text files consisting of gps datapoints, used to store information 
## on sports activities such as runs or bike rides. 
## Because some tracking devices (such as my Garmin watch) automatically
## shut off in a period that's shorter than my lunch break during bikerides, 
## I regularly end up with multiple "activities" executed consecutively. 
## In order to upload only one total activity to Strava, download the .gpx files 
## and merge them with this script. 

## Written in Python 2.7.10

##### Usage #####
## python mergeGpx.py file1.gpx file2.gpx file3.gpx output.gpx
## python mergeGpx.py file*.gpx output.gpx
## ! needs to be run from the folder containing inupt gpx files, throws an error otherwise !

import os 
import re
import sys

def checkPaths(infiles): 
  ## check if at least one input file is provided
  if len(infiles) < 2: 
    sys.exit("!! Error in mergeGpx.py: Script requires at least two input and one output filename !!")
  ## check if all infiles exist
  for infile in infiles: 
    if not os.path.isfile(infile): 
      sys.exit("!! Error in mergeGpx.py: " + infile + " doesn't exist !! ")

def writeFirstGpx(gpx_in, gpx_out):  
  ## read and write gpx_in to gpx_out, until </trkseq> is reached
  tail = False
  tail_stored = []
  with open(gpx_in, 'r') as infile: 
    gpx = infile.readlines()
    ## ! overwrite output file if it exists !
    with open(gpx_out, 'w') as outfile:
      for line in gpx:
        ## Break if end of trkseg is reached
        if re.search('/trkseg', line): 
          tail = True
        ## if all is well, write to file, else store for the end
        if not tail: 
          outfile.write(line)
        else: 
          # print line
          tail_stored.append(line)
  return tail_stored


def addGpx(gpx_in, gpx_out): 
  ## append trksegs of gpx_in to gpx_out, without header and tail
  header = True
  with open(gpx_in, 'r') as infile: 
    gpx = infile.readlines()
    ## append to output
    with open(gpx_out, 'a') as outfile: 
      for line in gpx: 
        ## check if end of header is reached, skip if not
        if re.search('<trkpt lat=', line): 
          header = False
        if header: 
          continue
        
        ## Break if end of trkseg is reached
        if re.search('</trkseg>', line): 
          break
        ## if all is well, write line to output file
        outfile.write(line)

##### Body #####
print "--- Running mergeGpx.py ---"

## Check that input files all exist
checkPaths(sys.argv[0:(len(sys.argv) - 1)])

## Write to output file
input_files = sys.argv[1:(len(sys.argv) - 1)]
last_file = sys.argv[len(sys.argv) - 1]

print "--- Files provided correctly, proceeding to merge ---"

tail = writeFirstGpx(input_files[0], last_file)
for addfile in input_files[1:len(input_files)]:
  addGpx(addfile, last_file)
with open(last_file, 'a') as outfile: 
  for el in tail: 
    outfile.write(el)

print "--- mergeGpx.py finished, output written to %s ---" %(last_file)


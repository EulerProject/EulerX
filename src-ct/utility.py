# Copyright (c) 2014 University of California, Davis
# 
# 
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
# 
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import os


def paddedBase10toN(num,n,size):
    """Change a  to a base-n number.
    Up to base-36 is supported without special notation."""
    num_rep={10:'a',
         11:'b',
         12:'c',
         13:'d',
         14:'e',
         15:'f',
         16:'g',
         17:'h',
         18:'i',
         19:'j',
         20:'k',
         21:'l',
         22:'m',
         23:'n',
         24:'o',
         25:'p',
         26:'q',
         27:'r',
         28:'s',
         29:'t',
         30:'u',
         31:'v',
         32:'w',
         33:'x',
         34:'y',
         35:'z'}
    new_num_string=''
    current=num
    while current!=0:
        remainder=current%n
        if 36>remainder>9:
            remainder_string=num_rep[remainder]
        elif remainder>=36:
            remainder_string='('+str(remainder)+')'
        else:
            remainder_string=str(remainder)
        new_num_string=remainder_string+new_num_string
        current=current/n
        
    while (len(new_num_string) < size):
        new_num_string = "0" + new_num_string
            
    return new_num_string


# this is necessary for windows paths - boo windows!
def quoteSpacesInPath(theString):
    
    result = ""
    newParts = []
    delim = "/"
    if (theString.find("\\") != -1):
        delim = "\\"
            
    parts = theString.split(delim)
    for part in parts:
        if (part.find(" ") != -1):
            part = "\"" + part + "\""
        newParts.append(part)
    result = delim.join(newParts)
    return result

def cleanOutputFileName(fileName):
    #newName = fileName.replace(" ","_")
    newName = fileName
    newName = newName.replace("{","")
    newName = newName.replace("}","")
    return newName
                              
def powerSet(list):
      result = []
      numCombinations = pow(2,len(list))
      for loop in range(0, numCombinations):
          newList = []
          binary = paddedBase10toN(loop,2,len(list))
          for inloop in range(0,len(binary)):
              if (binary[inloop] == "1"):
                  newList += [list[inloop]]          
          result.append(newList)          
      return result 
  
  ## returns the part of the filename before the first period
##
def getNameFromFile(fileName):
    slashes = fileName.split("/")
    realName = slashes[len(slashes)-1]
    if (realName.index(".") != -1):
        parts = realName.split(".")
        value = parts[0]

    return value

## compresses a file with gzip
def compressFile(fileName):
  status = "unknown"
  if os.path.exists(fileName):
    cmd = "gzip " + fileName
    status = os.system(cmd)
  return status

  
 

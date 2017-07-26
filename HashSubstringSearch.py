#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Implement a speed-optimized version of the Rabin-Karp algorithm to search
for a substring within a string, using polynomial hashing.  The main function
here is HashSearch

Copyright (C) 2017 J. Andrew Howe

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""


def PolyHash(thisStr,p,x):
  """
  Perform polynomial hashing of a string.
  ---
  Usage: hashCode = PolyHash(thisStr,p,x)
  ---
  thisStr: input string to hash
  p: prime integer sufficiently large to minimize the probability of collisions
  x: random integer in the inclusive range [0,p-1] for the polynomial
  hashCode: integer hash code of the string
  ---
  ex:
  print(PolyHash('andrew is cool',4241,42))
  
  JAH 20170617
  """
  
  # loop through the string
  hashCode = 0
  try:
    for (indx,char) in enumerate(thisStr):
      # convert the char to the unicode int, then hash it
      hashCode += ord(char) * (x**indx) % p
  except TypeError as err:
    raise TypeError('%s\nA parameter is the wrong type: %s'%(err,PolyHash.__doc__))

  return hashCode % p


def PrecomputePolyHash(thisStr,subLen,p,x):
  """
  Perform polynomial hashing of all substrings of a given length in a string
  using more efficient precomputation of the hashes.
  ---
  Usage: hashCodes = PrecomputePolyHash(thisStr,subLen,p,x)
  ---
  thisStr: input string to hash
  subLen: length of the individual substrings to hash
  p: prime integer sufficiently large to minimize the probability of collisions
  x: random integer in the inclusive range [0,p-1] for the polynomial
  hashCodes: list of length len(thisStr) - subLen + 1 of the hash codes of each
    individual substring of length subLen
  ---
  ex:
  PrecomputePolyHash('andrew',3,4241,42)
  
  JAH 20170617
  """
  
  try:
    lenS = len(thisStr)
    subs = lenS - subLen + 1
    xPow = x**subLen #precompute the highest power ox x
    
    # be sure sublen < len(thisStr)
    if (subLen > lenS):
      raise ValueError('%s\nsubLen (%d) must be < len(thisStr) (%d): %s'%(err,subLen,lenS,PrecomputePolyHash.__doc__))
    elif (subLen == lenS):
      # same length, so just return PolyHash
      return [PolyHash(thisStr,p,x)]
  except TypeError as err:
    raise TypeError('%s\nA parameter is the wrong type: %s'%(err,PrecomputePolyHash.__doc__))
  
  hashCodes = [0]*subs
  
  # first we should precompute all the unicode values
  uniCodes = [ord(c) for c in thisStr]
  
  # start with the last substring
  hashCodes[-1] = PolyHash(thisStr[-subLen:],p,x)
  # loop though substrings in thisStr of length subLen, from the end
  for indx in range(subs-2,-1,-1):
    # implement the proper recurrence relation:
    # multi next hash by x, add on the current value, subtract off the 
    # last value (but with an extra x), then add it all and mod p
    hashCodes[indx] = (x*hashCodes[indx+1] + uniCodes[indx] - \
    uniCodes[indx+subLen]*xPow)%p
  
  return hashCodes

    
def HashSearch(searchMe,findMe,p,x):
  """
  Use an efficient Rabin-Karp algorithm to search a string and return the starting
  indices of all instances of a specified substring
  ---
  Usage: indices = HashSearch(searchMe,findMe,p,x)
  ---
  searchMe: string to search
  findMe: substring to find
  p: prime integer sufficiently large to minimize the probability of collisions
  x: random integer in the inclusive range [0,p-1] for the polynomial
  indices: list of indices into searchMe of starting points of findMe
  ---
  ex:
  HashSearch('andrew is awesome','not',4241,41)
  
  JAH 20170617
  """

  lenFnd = len(findMe)
    
  # short circuit optimizations:
  # if len(findMe) is 1, just brute-force it
  if (lenFnd == 1):
    return [i for i in range(len(searchMe)) if searchMe[i] == findMe]
  # if 2 strings are equal length, just compare
  elif (lenFnd == len(searchMe)):
    if (findMe == searchMe):
      return [0]
    else:
      return []
  # if string sought is blank or longer, return blank
  elif ((lenFnd > len(searchMe)) or (lenFnd == 0)):
    return []
  
  # first of all, get the hash code of findMe
  findHash = PolyHash(findMe,p,x)
  
  # get all substring hashcodes of length len(findMe)
  lenFnd = len(findMe)
  hashes = PrecomputePolyHash(searchMe,lenFnd,p,x)
  
  # loop through all the substring hashcodes and check equality
  fndIndices = []
  for (i,cod) in enumerate(hashes):
    if (findHash == cod):
      # hashcodes same, so check equality
      if (findMe == searchMe[i:(i+lenFnd)]):
        fndIndices.append(i)
      else:
        print('Hash Collision! Use a larger value for p(%d)!'%p)

  return fndIndices

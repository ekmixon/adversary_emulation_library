#!/usr/bin/python3

# Python code to encrypt, compress, and base64 encode shellcode from a file

import argparse
import gzip
from base64 import b64encode
import os

def xor(data, key):
    # xor encrypt shellcode
    output_str = ""
    for i in range(len(data)):
        current = data[i]
        current_key = key[i%len(key)]
        output_str += chr((current) ^ ord(current_key))

    return bytearray(output_str, 'latin-1')

def getShellcode(fileName):
    # Open shellcode file and read bytes
    try:
        with open(fileName, 'rb') as shellcodeFileHandle:
            shellcodeBytes = shellcodeFileHandle.read()
            shellcodeFileHandle.close()
        print(f"--- Shellcode file -{fileName}- successfully loaded")
    except IOError:
        print(f"!!! Could not open and read -{fileName}-")
        quit()

    print(f"--- Shellcode size: {len(shellcodeBytes)} bytes")

    return shellcodeBytes

def encryptShellcode(shellcodeBytes, key):
    # XOR Encrypt Shellcode
    encryptedShellcode = xor(shellcodeBytes, key)
    print(f"--- Encrypted shellcode size: {len(encryptedShellcode)} bytes")
    try:
        with open("reverseencrypted.raw", "wb+") as f:
            f.write(encryptedShellcode)
    except:
        print("!!! Unable to write encrypted shellcode to file.")
        quit()

    return encryptedShellcode

def compressShellcode(encryptedShellcode):
    # Use gzip to compress shellcode
    try:
        compressedShellcode = gzip.compress(encryptedShellcode)
    except:
        print("!!! Unable to compress shellcode.")
        quit()

    return compressedShellcode

def writeEncodedToFile(compressedShellcode, outfile):
    # Base64 encode the shellcode and write out to file
    try:
        encodedShellcode = b64encode(bytearray(compressedShellcode))
    except:
        print("!!! Unable to encode shellcode.")
        quit()

    try:
        with open(outfile, "wb+") as f:
            numChars = f.write(encodedShellcode)
        print(f"--- Encoded shellcode written to {outfile}.")
    except IOError:
        print("!!! Could not write encoded shellcode to file.")
        
if __name__ == '__main__':
    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("shellcodeFileName", help="File name of the raw shellcode to be encrypted/compressed/encoded")
    parser.add_argument("key", help="Key to XOR encrypt the shellcode")
    parser.add_argument("outfile", help="Name of file where encrypted/compressed/encoded shellcode will be output")
    args = parser.parse_args() 
    
    shellcodeBytes = getShellcode(args.shellcodeFileName)
    encryptedShellcode = encryptShellcode(shellcodeBytes, args.key)
    compressedShellcode = compressShellcode(encryptedShellcode)    
    writeEncodedToFile(compressedShellcode, args.outfile)    
                
       

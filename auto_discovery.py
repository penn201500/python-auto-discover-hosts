#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import os
import platform

def read_hosts(filename):
    with open(filename) as f:
        lines = f.read().splitlines()
    return lines


def check_host_on(host_ip):  
    try:
        if (platform.system() == "Windows"):      
            cmd = ['ping',  
                   '%s' % host_ip,  
                   '-n',  
                   '1']
        elif (platform.system() == "Linux"):        
            cmd = ['ping',  
                   '%s' % host_ip,  
                   '-c',  
                   '1']                   
        #print cmd
        output = os.popen(' '.join(cmd)).readlines()  
        #print output
        for line in list(output):  
            if not line:  
                continue  
            if str(line).find('ttl') >= 0 or str(line).find('TTL') >= 0:  
                return True  
    except:  
        pass


def write_to_file(devices, filename):
    with open(filename, 'a') as discover_file:     
        writer = discover_file.write(devices + '\n')
        

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Discover info of network' +
                                                 'devices.')
    parser.add_argument('inputfile', help='file with hosts to probe')
    parser.add_argument('outputfile', help='file to write host ping status')
    args = parser.parse_args()

    hosts_to_scan = read_hosts(args.inputfile)
    print hosts_to_scan
    for ip in hosts_to_scan:
        if check_host_on(ip):
            write_to_file(ip, args.outputfile)
        else:
            continue

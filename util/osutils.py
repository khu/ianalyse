import os
import shutil          
import re 
import util.datetimeutils                             
from datetime import datetime

def touch(path):
    makedirs_p(os.path.dirname(path))
    f = open(path, 'w')
    f.close()

def makedirs_p(path):
    if not os.access(path, os.F_OK):
        os.makedirs(path)

def rmdir_p(path):
    shutil.rmtree(path)

def write_to_file(path, content):
    makedirs_p(os.path.dirname(path))
    f = open(path, 'w')
    try:
        f.write(content)
    finally:
        f.close() 
                                                                   
def list_matched_files(root, pattern):     
    files = []
    for file in os.listdir(root):
        m = re.match(pattern, file)
        if m != None:
            files.append(file)
    return files
    
def sort_by_rule(root, rule, order):   
    pattern = "log([0-9]*).*.xml"
    files = list();
    all_files = list_matched_files(root, pattern)
    return sorted(all_files, eval('compare_files_' + order)) 

def __compare_files(file1, file2, order):
    pattern = "log([0-9]*).*.xml"
    m1 = re.match(pattern, file1)
    date1 = datetime.strptime(m1.group(1), "%Y%m%d%H%M%S")
    m2 = re.match(pattern, file2)
    date2 = datetime.strptime(m2.group(1), "%Y%m%d%H%M%S")

    if order == 'desc':                                   
        return cmp(date2, date1)
    else:                                                  
        return cmp(date1, date2)
        
def compare_files_asc(file1, file2):
    return __compare_files(file1, file2, 'asc')

def compare_files_desc(file1, file2):
    return __compare_files(file1, file2, 'desc')                                      

    
    

os.write_to_file = write_to_file
os.touch = touch
os.makedirs_p = makedirs_p
os.rmdir_p = rmdir_p
os.sort_by_rule = sort_by_rule



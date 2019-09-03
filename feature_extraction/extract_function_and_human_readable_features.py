#!/usr/bin/env python

import json
import os

from feature_extraction.functions_and_human_readable import FunctionOccurences

#-------------------Run one time to find all the functions used----------------------------------------

func_list1 = []
rootdir_malicious = os.path.join("inputs", "malicious")
for root, subFolders, files in os.walk(rootdir_malicious):
    for _file in files:
        if _file.endswith(".php"):
            file_path = root + "/" + _file
            print file_path
            fo = FunctionOccurences(file_path)
            try:
                func_list1.extend(fo.get_all_function_used())
            except:
                print "Something went wrong with file {}".format(file_path)

func_list2 = []
rootdir_bening = os.path.join("inputs", "benign", "wordpress")
for root, subFolders, files in os.walk(rootdir_bening):
    for _file in files:
        if _file.endswith(".php"):
            file_path = root + "/" + _file
            print file_path
            fo = FunctionOccurences(file_path)
            try:
                func_list2.extend(fo.get_all_function_used())
            except:
                print "Something went wrong with file {}".format(file_path)

#-----------------------------------------------------------------------------

func_list = func_list1 + func_list2
func_list = list(set(func_list))

#------------------------------------------------------------------------------

func_dict = {}
rootdir_malicious = os.path.join("inputs", "malicious")
for root, subFolders, files in os.walk(rootdir_malicious):
    for _file in files:
        if _file.endswith(".php"):
            file_path = root + "/" + _file
            print file_path
            func_dict[file_path] = {}
            for func in func_list:
                func_dict[file_path][func] = 0
            fo = FunctionOccurences(file_path)
            try:
                occurences_per_func = fo.get_occurences_per_function()
                # feature_dict["label"] = 1
                for func, occs in occurences_per_func.iteritems():
                    func_dict[file_path][func] = occs
                human_readables = fo.find_human_readables()
                func_dict[file_path]["human_readable_percentage"] = human_readables
                func_dict[file_path]["label"] = -1
            except:
                func_dict.pop(file_path, None)
                print "Something went wrong with file {}".format(file_path)

#--------------------------Find the occurences of each function in each file------------------------------

rootdir_bening = os.path.join("inputs", "benign", "wordpress")
for root, subFolders, files in os.walk(rootdir_bening):
    for _file in files:
        if _file.endswith(".php"):
            file_path = root + "/" + _file
            print file_path
            func_dict[file_path] = {}
            for func in func_list:
                func_dict[file_path][func] = 0
            fo = FunctionOccurences(file_path)
            try:
                occurences_per_func = fo.get_occurences_per_function()
                for func, occs in occurences_per_func.iteritems():
                    func_dict[file_path][func] = occs
                human_readables = fo.find_human_readables()
                func_dict[file_path]["human_readable_percentage"] = human_readables
                func_dict[file_path]["label"] = 1
            except:
                func_dict.pop(file_path, None)
                print "Something went wrong with file {}".format(file_path)


with open(os.path.join("outputs", "features", "function_and_human_readable_features.json"), "w") as f:
    json.dump(func_dict, f, indent=2, separators=(",", ":"))

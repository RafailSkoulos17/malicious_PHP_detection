#!/usr/bin/env python

import json
import os

from feature_extraction.feature_extractor import FeatureExtractor

f_dict = {}
rootdir_bening = os.path.join("inputs", "benign", "wordpress")
# i = 0
prev = 0
for root, subFolders1, files in os.walk(rootdir_bening):
    for _file in files:
        if _file.endswith(".php"):
            file_path = root + "/" + _file
            print file_path
            # with open(file_path, "r") as fin:
            #     _file = fin.read()
            # with open(file_path, "a") as fin:
            #     if not _file.rstrip(" ").rstrip("\n").endswith("?>"):
            #         fin.write("?>")
            fe = FeatureExtractor(file_path)
            try:
                feature_dict = fe.extract_features()
                feature_dict["label"] = 1
                f_dict[file_path] = feature_dict
                f_dict[file_path]["number_of_lines"] -= prev
                prev += f_dict[file_path]["number_of_lines"]
                f_dict[file_path]["number_of_lines"] += 1
                chars = f_dict[file_path]["length_in_characters"]
                lines = f_dict[file_path]["number_of_lines"]
                f_dict[file_path]["characters_per_line"] = float(chars) / lines
                number_of_comments = f_dict[file_path]["number_of_comments"]
                f_dict[file_path]["average_comments_per_line"] = float(number_of_comments) / lines
            except:
                f_dict.pop(file_path, None)
                print "Something went wrong with file {}".format(file_path)

rootdir_malicious = os.path.join("inputs", "malicious")
prev = 0
for root, subFolders2, files in os.walk(rootdir_malicious):
    for _file in files:
        if _file.endswith(".php"):
            file_path = root + "/" + _file
            print file_path
            # with open(file_path, "r") as fin:
            #     _file = fin.read()
            # with open(file_path, "a") as fin:
            #     if not _file.rstrip(" ").rstrip("\n").endswith("?>"):
            #         fin.write("?>")
            fe = FeatureExtractor(file_path)
            try:
                feature_dict = fe.extract_features()
                feature_dict["label"] = -1
                f_dict[file_path] = feature_dict
                f_dict[file_path]["number_of_lines"] -= prev
                prev += f_dict[file_path]["number_of_lines"]
                f_dict[file_path]["number_of_lines"] += 1
                chars = f_dict[file_path]["length_in_characters"]
                lines = f_dict[file_path]["number_of_lines"]
                f_dict[file_path]["characters_per_line"] = float(chars) / lines
                number_of_comments = f_dict[file_path]["number_of_comments"]
                f_dict[file_path]["average_comments_per_line"] = float(number_of_comments) / lines
            except:
                f_dict.pop(file_path, None)
                print "Something went wrong with file {}".format(file_path)

with open(os.path.join("outputs", "features", "lexical_features.json"), "w") as f:
    json.dump(f_dict, f, indent=2, separators=(",", ":"))

# Malware detection with machine learning methods

Build a system which is able predict if a given php file is malicious or benign, by using machine learning methods. To achieve this I extracted several lexical features and we chose the best among of them. Also I experimented with several different classifiers found in literature, namely Support-Vector Machine(SVM), Stochastic Gradient Descent Classifier and Decision Tree.

## Description

The module contains the following 2 main directories:
* **machine_learning**: Contains all the implementation of the machine learning algorithms used among with a file for the 
preprocess of the features and some files used for the tuning of the algorithms.

* **feature_extraction**: Contains the files used for the extraction of the features described below.

Also there are three files which use the files of the feature_extraction directory to extract the features for all the 
php files of the "inputs" directory. These files are **extract_function_and_human_readable_features.py**
, **extract_function_percent_and_human_readable_features.py** and **extract_lexical_features.py**.

Finally there is also the **geometric_mean.py** file which is used to compute the geometric mean score.

## How to run one of the Machine Learning algorithms

There are 2 simple simple steps:
1. Run one of the files used to extract the features for all the sample files or use the features
 which are extracted already and are located in the "machine_outputs/features" directory

2. Run the machine Learning algorithm you want from the "machine_learning", after you have assigned to the 
"input_file" variable the path of the file which contains the features.

You can also perform a grid search for the tuning parameters of the SVM algorithm,
by running the **<algorithm_name>_grid_search.py** file after you have assigned the values you want 
to the variables used to define the parameters combination of the grid search.

## Features used

Currently I have experimented with 3 different sets of features for each PHP file.

* Lexical features:

      * length_in_characters
      * number_of_lines
      * percentage_of_words_not_in_comments
      * characters_per_line
      * number_of_comments
      * average_comments_per_line
      * percentage_of_whitespaces
      * average_string_length
      * number_of_function_calls
      * number_hex_octal_numbers
      * number_of_words
      * percentage_of_human_readables
      * average_argument_length
      * number_of_unicode_symbols
      * number_of_strings

* Number of occurences of each function among with the "percentage_of_human_readables" feature.

* Number of occurences of each function divided by the total number of function calls in the file among with the "percentage_of_human_readables" feature.



## Classifiers used

    * Decicion Tree
    * SVM
    * Stochastic Gradient Descent Classifier

## Inputs and Outputs

**Inputs** directory contains the malicious and benign sample files.  
**Outputs** directory contains the features extracted in JSON files and the classification results.

## Prerequisites

In order to be able to use this module you will need to have the following programs pre-installed to your computer:
	
    Python 2.7

You will also need the following python packages:

    * numpy
    * pandas
    * sklearn
    * scipy
    * phply
    * ply
    * imblearn

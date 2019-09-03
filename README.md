# Malware detection with machine learning methods

The aim of this project is to build a python module which will be able to predict with adequite precision if a given php file is malicious or benign, by using machine learning methods. To achieve this we extracted several lexical features and we chose the best among of them. Also we are going to experiment with several different classifiers found in literature. 

## Description

The module contains the following packages:
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
by running the **svn_grid_search.py** file after you have assigned the values you want 
to the variables used to define the parameters combination of the grid search.

## Features used

Currently we have experimented with 3 different sets of features for each php file.

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
    * SGD

## Inputs and Outputs

**Inputs** directory contains the malicious and benign sample files.  
**Outputs** directory contains the features extracted in JSON files. In the future the classification results will be there too.

## Feature ouptput example
Not existing yet.

## Classification output example 
Not existing yet.

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


Note: Soon a python script "setup.py" will be created which will install all the necessary python packages.

## Tests

Not implemented yet.

## Author

***Rafail Skoulos***

## License

Does not exist.

## Acknowledgments

* Hat tip to anyone who's code was used
* Inspiration
* etc


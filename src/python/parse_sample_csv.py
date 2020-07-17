
#!/usr/bin/python3

"""
Script to parse PGDx result csv files in one directory and output a file with aggregate results
"""

__author__ = "Yuta Sakai"


import argparse
import os
import sys


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i", dest="input_directory", required=True,
        help="Full path to the directory containing the csv file"
    )
    parser.add_argument(
        "-o", dest="output_directory", required=True,
        help="Full path to the directory to save the result file"
    )

    args = parser.parse_args()

    input_directory = os.path.normpath(args.input_directory)
    output_directory = os.path.normpath(args.output_directory)

    # Parse the csv file
    result_dict = parse_pgdx_csv(input_directory)

    print(result_dict)


def parse_pgdx_csv(input_directory):
    """
    Parses the PGDx Case Report csv file and store the information in a python dictionary
    :param input_directory:
    :return:
    """
    result_dict = {}
    csv_file_list = os.listdir(input_directory)
    for file in csv_file_list:
        sample_name = file.split(".")[0]
        csv_file = open(input_directory + "/" + file, "r")
        if sample_name not in result_dict.keys():
            result_dict[sample_name] = {}
        else:
            print("Sample: " + sample_name + " has already been analyzed. Exiting script")
            sys.exit()
        for line in csv_file:
            line = line.rstrip()
            # Skip blank lines
            if line == "":
                continue
            else:
                line_item = line.split(",")
                # Add each header as a key
                if line_item[0].startswith("["):
                    header = line_item[0]
                    # FIXME
                    # Stop after [Sample Contamination Detection QC]
                    if header == "[Sample Genomic Signatures]":
                        break
                    result_dict[sample_name][header] = {}
                    continue
                # Skip the "Metric,Value" line
                if line_item[0] == "Metric" and line_item[1] == "Value":
                    continue
                # Add all the items underneath the header inside each header key
                result_dict[sample_name][header][line_item[0]] = line_item[1]
        csv_file.close()
    return result_dict


if __name__ == "__main__":
    main()

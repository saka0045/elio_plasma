
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
    parser.add_argument(
        "-f", dest="metric_file_path", required=True,
        help="Full path to the metrics.csv file"
    )

    args = parser.parse_args()

    input_directory = os.path.normpath(args.input_directory)
    output_directory = os.path.normpath(args.output_directory)
    metric_file_path = os.path.abspath(args.metric_file_path)

    # Parse the csv file
    result_dict, sample_list = parse_pgdx_csv(input_directory)

    # Create aggregate result csv file
    make_aggregate_result_file(metric_file_path, output_directory, result_dict, sample_list)


def make_aggregate_result_file(metric_file_path, output_directory, result_dict, sample_list):
    """
    Aggregate the desired metrics and output into a csv file
    :param metric_file_path:
    :param output_directory:
    :param result_dict:
    :param sample_list:
    :return:
    """
    result_file = open(output_directory + "/elio_plasma_aggregate_results.csv", "w")
    # Make the header row with sample name
    for sample in sample_list:
        result_file.write("," + sample)
    result_file.write("\n")
    # Open the metric file to see which metrics needs to be written
    metric_file = open(metric_file_path, "r")
    for line in metric_file:
        line = line.rstrip()
        line_item = line.split(",")
        metric_header = line_item[0]
        metric_category = line_item[1]
        metric = line_item[2]
        result_file.write(metric_header)
        for sample in sample_list:
            result_file.write("," + result_dict[sample][metric_category][metric])
        result_file.write("\n")
    result_file.close()
    metric_file.close()


def parse_pgdx_csv(input_directory):
    """
    Parses the PGDx Case Report csv file and store the information in a python dictionary
    :param input_directory:
    :return:
    """
    result_dict = {}
    sample_list = []
    csv_file_list = os.listdir(input_directory)
    for file in csv_file_list:
        sample_name = file.split(".")[0]
        csv_file = open(input_directory + "/" + file, "r")
        if sample_name not in result_dict.keys():
            result_dict[sample_name] = {}
            sample_list.append(sample_name)
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
    return result_dict, sample_list


if __name__ == "__main__":
    main()

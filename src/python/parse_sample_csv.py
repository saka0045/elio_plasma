
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
    result_dict, sample_list = parse_pgdx_csv(input_directory)

    # Create aggregate result csv file
    make_aggregate_result_file(output_directory, result_dict)


def make_aggregate_result_file(output_directory, result_dict):
    """
    Aggregate the desired metrics and output into a csv file
    :param output_directory:
    :param result_dict:
    :return:
    """
    result_file = open(output_directory + "/elio_plasma_aggregate_results.csv", "w")
    # Make the header row
    result_file.write("Sample,"
                      "Percent of Bases Mapped to Genome (%),"
                      "Percent of Bases Mapped to ROI (%),"
                      "Average High Quality Distinct Coverage,"
                      "Average High Quality Total Coverage,"
                      "% Exons with > 525 Distinct Coverage,"
                      "Identified Sequences per Sample (%),"
                      "Cluster Density (K/mm2),"
                      "Contamination Status\n")
    # Iterate through the result_dict and pull information
    for sample in result_dict.keys():
        percent_bases_mapped_to_genome = result_dict[sample]["[Sample Information]"]["Bases Mapped to Genome (%)"]
        percent_bases_mapped_to_roi = result_dict[sample]["[Sample Information]"]["Bases Mapped to ROI (%)"]
        average_hq_distinct_cov = result_dict[sample]["[Sample Information]"]["Average High Quality Distinct Coverage"]
        average_hp_total_cov = result_dict[sample]["[Sample Information]"]["Average High Quality Total Coverage"]
        percent_exons = \
            result_dict[sample]["[Sample Information]"]["% exons with coverage >525 Redundant Distinct Coverage"]
        identified_sequences_per_sample = \
            result_dict[sample]["[Sample Quality Metrics]"]["Identified Sequences per Sample (%)"]
        cluster_density = result_dict[sample]["[Run Quality Metrics]"]["Cluster Density (K/mm2)"]
        contamination_status = result_dict[sample]["[Sample Contamination Detection QC]"]["Contamination Status"]
        line_to_write = [sample, percent_bases_mapped_to_genome, percent_bases_mapped_to_roi, average_hq_distinct_cov,
                         average_hp_total_cov, percent_exons, identified_sequences_per_sample, cluster_density,
                         contamination_status]
        result_file.write(",".join(line_to_write) + "\n")
    result_file.close()


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

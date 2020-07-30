#!/usr/bin/python3

"""
Script to generate sample sheet for NGS-Instrumentation from PGDx supplied sample sheet
"""

__author__ = "Yuta Sakai"


import argparse
import os


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i", dest="pgdx_sample_sheet", required=True,
        help="Full path to the PGDx sample sheet"
    )
    parser.add_argument(
        "-o", dest="output_directory", required=True,
        help="Full path to the output directory to save the instrumentation sample sheet"
    )

    args = parser.parse_args()

    pgdx_sample_sheet_path = os.path.abspath(args.pgdx_sample_sheet)
    output_directory = os.path.normpath(args.output_directory)

    # Parse the PGDx sample sheet
    pgdx_sample_dict = parse_pgdx_sample_sheet(pgdx_sample_sheet_path)
    print(pgdx_sample_dict)


def parse_pgdx_sample_sheet(pgdx_sample_sheet_path):
    """
    Parses the PGDx sample sheet to extract the sample and index names
    :param pgdx_sample_sheet_path:
    :return:
    """
    pgdx_sample_sheet = open(pgdx_sample_sheet_path, "r")
    pgdx_sample_dict = {}
    for line in pgdx_sample_sheet:
        # Skip to the [Data] section
        if line.startswith("[Data]"):
            line = pgdx_sample_sheet.readline()
            line = line.rstrip()
            # Get the header information
            header_line = line.split(",")
            for line in pgdx_sample_sheet:
                line = line.rstrip()
                line_item = line.split(",")
                # Get the sample name and index name
                sample_name = line_item[header_line.index("Sample Name")]
                if "_" in sample_name:
                    print("Detected underscores in sample: " + sample_name)
                    print("Cannot have underscores in smaple name, switching them to dashes")
                    sample_name = sample_name.replace("_", "-")
                index_name = line_item[header_line.index("Index Name")].split(" ")[2]
                pgdx_sample_dict[sample_name] = index_name
    pgdx_sample_sheet.close()
    return pgdx_sample_dict


if __name__ == "__main__":
    main()

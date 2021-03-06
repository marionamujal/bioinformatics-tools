#!/usr/bin/env python

# Read a fastq file of barcodes and produce a 
# list of counts of reads for each
# unique barcode sequence

import sys
import argparse
import operator

def get_barcode_counts_dict(filename):
    barcode_counts = {}
    line_counter = 0  # each read takes 4 lines, but we only care about line 2
    with open(filename, 'r') as fastq:
        for line in fastq:
            if line_counter == 4:
                line_counter = 1
            else:
                line_counter += 1
            if line_counter == 2:
                barcode = line.strip()
                if barcode in barcode_counts:
                    barcode_counts[barcode] += 1
                else:
                    barcode_counts[barcode] = 1
    return barcode_counts

def main():
    # Parse dem args
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--number', required=True)
    parser.add_argument('-f', '--fastq', required=True)
    parser.add_argument('--max', action='store_true')
    parser.add_argument('--middle', action='store_true')
    args = parser.parse_args()
    if not args.max and not args.middle:
        sys.stderr.write("Please choose --max or --middle\n")
        sys.exit()

    # Read fastq file, store counts for each barcode
    barcode_counts = get_barcode_counts_dict(args.fastq)

    # Get a sorted list of (barcode, count) tuples
    # Is there a smarter way to do this? TODO
    sorted_barcodes = sorted(barcode_counts.items(), key=operator.itemgetter(1),
            reverse=True)

    # Decide what to print
    if args.max:
        n = int(args.number)
        for barcode_tuple in sorted_barcodes[:n]:
            barcode = barcode_tuple[0]
            count = str(barcode_tuple[1])
            print(barcode + "\t" + count)
    elif args.middle:
        n = int(args.number)
        number_of_barcodes = len(sorted_barcodes)
        if n > number_of_barcodes:
            start_index = 0
            end_index = number_of_barcodes
        else:
            start_index = number_of_barcodes/2 - n/2
            end_index = start_index + n
        for barcode_tuple in sorted_barcodes[start_index:end_index]:
            barcode = barcode_tuple[0]
            count = str(barcode_tuple[1])
            print(barcode + "\t" + count)

##########################

if __name__ == '__main__':
    main()


# Description
We solve the donation analytics challenge for the Insight Data Engineering program.  The instructions for the challenge can be found at https://github.com/InsightDataScience/donation-analytics/ .

# Running the code
run.sh located in the root runs src/donation-analytics.py to give a list of repeat donor data.

donation-analytics.py requires three arguments: two input files (a stream and percentile) and one output file.

Example usage:  python ./src/donation-analytics.py ./input/itcont.txt ./input/percentile.txt ./output/repeat_donors.txt

donation-analytics.py only uses the Python Standard library (sys, math).  The code was written and tested in Python 3.6.3.

# About the algorithm
We read through the input file line by line, parsing the relevant data and skipping lines with invalid data.  We place these into a dictionary whose keys are donor ids, and whose values are lists of donation recipients/years/amounts, giving an O(1) lookup time on average.  We then query the dictionary at each line to find the appropriate repeat donors.  We output the percentage of repeat donors, their total donation amount, and their total number of donations on each line.

# Testing
We have included unit tests in the insight_testsuite folder, specifically to test the following behaviors:

- test_2_empty_stream: empty stream is handled
- test_2_invalid_percentage: percentage defaults to 50 when empty or invalid
- test_2_corrupted_name: names are stripped of leading/trailing spaces and periods
- test_2_negative_amt: negative transaction amounts are skipped
- test_decreasing_years: decreasing years do not create extra repeat donors

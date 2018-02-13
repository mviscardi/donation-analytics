# Description
We solve the donation analytics challenge for the Insight Data Engineering program.  Our directory structure is the same as the one in the instructions for the challenge at https://github.com/InsightDataScience/donation-analytics/ .

# Dependencies
Our solution is written in Python 3.6.3, and the only modules needed are sys and math.

# Method
We read through the input file line by line, parsing the relevant data and skipping lines with invalid data.  We place these into a dictionary of donor ids for fast lookup, then query the dictionary at each line to find the appropriate repeat donors.  We then output the percentage of repeat donors, their total donation amount, and their total number of donations on each line.

# Testing
We have included 4 unit tests in the insight_testsuite folder, which our program passes.

# Name: donation-analytics.py
# Description: Solution to Insight Data Engineering challenge on donation analytics
# Author: Michael Viscardi
# Date: 2/12/18
# GitHub: https://github.com/symplectic314/donation-analytics

import sys
import math

itcont_path     = sys.argv[1]
percentile_path = sys.argv[2]
output_path     = sys.argv[3]

itcont_file        = open(itcont_path,     'r')
percentile_file    = open(percentile_path, 'r')
repeat_donors_file = open(output_path,     'w')

# The percentile to be computed
try:
  percentile = int(percentile_file.readline())
except ValueError or percentile < 0 or percentile > 100:
  percentile = 50

# A dictionary of donations
# Keys: unique donor id = (name, zip_code)
# Values: list of donations by a given donor
# A donation = committee id,
#              transaction year,
#              transaction amount
donation_dictionary = {}

# Stream in data
for line in itcont_file:
  line_data = line.split('|')

  # Parse relevant data
  cmte_id         = line_data[0]
  name            = line_data[7].strip(' .')
  zip_code        = line_data[10][:5]         # first 5 digits of zipcode
  transaction_dt  = line_data[13]
  transaction_yr  = transaction_dt[-4:]       # 4 digit transaction year
  transaction_amt = line_data[14]
  other_id        = line_data[15]

  # Skip line if relevant data is invalid
  if (len(transaction_dt) < 8     or
      len(zip_code)       < 5     or
      not name                    or
      not cmte_id                 or
      not transaction_amt         or
      float(transaction_amt) < 0  or
      other_id):
    continue

  # A donor is uniquely identified by his or her name and zip code
  donor_id = (name, zip_code)

  # Track where/when/how much they donated
  donation = {'CMTE_ID':         cmte_id,
              'TRANSACTION_YR':  transaction_yr,
              'TRANSACTION_AMT': transaction_amt}

  if donor_id not in donation_dictionary:
    # Cannot be a repeat donor, so don't print anything
    donation_dictionary[donor_id] = [donation]
  else:
    donation_dictionary[donor_id].append(donation)

    # Check if this person donated in a prior calendar year
    previous_donations = [previous_donation for
                          previous_donation in donation_dictionary[donor_id] if
                          previous_donation['TRANSACTION_YR'] < transaction_yr]

    if previous_donations:
      # Repeat donor found, so now check for repeat donors for this recipient,
      # zipcode, and year
      repeat_donor_list = []

      for repeat_donor_id in donation_dictionary:
        if (repeat_donor_id[1] == donor_id[1] and
            len(donation_dictionary[repeat_donor_id]) > 1):
          for repeat_donation in donation_dictionary[repeat_donor_id]:
            if (repeat_donation['CMTE_ID']        == cmte_id and
                repeat_donation['TRANSACTION_YR'] == transaction_yr):
              repeat_donor_list.append(round(float(repeat_donation['TRANSACTION_AMT'])))

      # Calculate output quantities
      ordinal_rank       = math.ceil(percentile/100 * len(repeat_donor_list))
      running_percentile = str(sorted(repeat_donor_list)[ordinal_rank-1])
      total_amount       = str(sum(repeat_donor_list))
      total_number       = str(len(repeat_donor_list))

      output_line_data = [cmte_id, zip_code, transaction_yr,
                          running_percentile, total_amount, total_number]
      output_line = '|'.join(output_line_data)

      # Write output line
      repeat_donors_file.write(output_line + '\n')

itcont_file.close()
percentile_file.close()
repeat_donors_file.close()

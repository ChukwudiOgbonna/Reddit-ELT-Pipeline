import sys
import datetime

def validate_input(date_input):
  try:
    datetime.datetime.strptime(date_input, '%Y%m%d')
  except ValueError:
    raise ValueError("Input parameter should be YYYYMMDD")
    sys.exit(1)
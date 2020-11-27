#!/usr/bin/env python

"""pldt-home-data.py: Display the remaining PLDT Home PREPAID WIFI data"""

from urllib import request
from terminaltables import SingleTable
from bs4 import BeautifulSoup

import simple_chalk as chalk

__author__ = "Maverick G. Fabroa"
__copyright__ = "Copyright 2020, pldt-home-data-extractor"
__license__ = "MIT"
__version__ = "1.0.0"
__email__ = "maverickfabroa@gmail.com"
__status__ = "Production"

def main():    
    # URI Link
    URI = "http://dashboard.pldthome.com/HomeWifiLoad/Availment/_LoadBalance"
    
    # Get the data
    data = request.urlopen(URI).read()
    
    # Create a BeatifulSoup object
    soup = BeautifulSoup(data, "html.parser")
    
    # Retrieve Main Title from the page
    main_title = soup.find("h2", {"class": "hwd"}).getText()
    
    # Retrieve the parent of the significant data
    parent_element = soup.find("div", {"class": ["balance", "prepaid"]})
    
    # Retrieve significant data
    general_data = parent_element.findAll("div", {"class": ["row", "prepaid"]})

    rows = list()
    
    for row in general_data:
        # Title of data
        title = row.find("p", {"class": "family-pack"}).getText().title()

        # Value of data
        value = row.find("p", {"class": ["value", "bal-info"]}).getText()
        
        # Expiration date
        tmp_exp = row.find("p", {"class": "expiration"}).getText()

        if tmp_exp.startswith("Expires on "):
            exp = tmp_exp[11:]

        rows.append([title, value, exp])

    # Custom column name
    col_name = [ "Name", "Value", "Expiration" ]

    # insert column names to rows
    rows.insert(0, col_name)

    # Create a table
    table = SingleTable(rows)

    # Set table title
    table.title = chalk.yellow(main_title)

    # Print the table
    print(table.table)
        
if __name__ == "__main__":
    main()
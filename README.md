# LocaFacil

LocaFacil is a web scraping project designed to extract real estate data from different websites, currently supporting Viva Real and OLX.

## Overview

LocaFacil simplifies the process of gathering real estate information by scraping data from popular real estate websites. It currently supports two platforms: Viva Real and OLX.

## Features

- **Supported Websites:**
  - [Viva Real](https://www.vivareal.com.br/)
  - [OLX](https://www.olx.com.br/)

- **Extracted Data:**
  - Property details such as price, address, area, type, rooms, bathrooms, parking spaces, etc.

- **Ease of Use:**
  - Simply provide the necessary parameters and let LocaFacil do the scraping for you.

## Usage

1. Install the required dependencies:
   ```bash
   pip install beautifulsoup4 selenium

2. Run the LocaFacil script with appropriate parameters:
   ```bash
   python locafacil.py

3. Retrieve the extracted data in CSV format.


## Note

- **Respecting Website Terms:**
  - Make sure to respect the terms of use of the respective websites you are scraping. Familiarize yourself with the terms and conditions of Viva Real and OLX or any other websites you plan to add to LocaFacil.

- **Adjusting Parameters:**
  - Adjust scraping parameters based on your specific requirements. This includes adjusting the number of pages, price ranges, property types, and any other parameters relevant to your scraping needs.

- **ChromeDriver:**
  - LocaFacil uses Selenium, which requires ChromeDriver. Ensure that you have ChromeDriver installed and set up properly. You can download ChromeDriver from [here](https://sites.google.com/chromium.org/driver/).

- **Legal and Ethical Use:**
  - Ensure that your usage of LocaFacil complies with legal and ethical standards. Respect the privacy and policies of the websites you are scraping, and use the extracted data responsibly.

- **License:**
  - This project is licensed under the [MIT License](LICENSE). Make sure to review and comply with the terms specified in the license.

Feel free to reach out if you have any further questions or if there's anything else I can assist you with.

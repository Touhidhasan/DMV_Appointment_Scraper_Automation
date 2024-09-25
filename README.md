# DMV Appointment Scraper Automation

## Overview
The DMV Appointment Scraper Automation is a Python-based project designed to automate the process of scraping appointment slots from the DMV website, solving CAPTCHAs, and sending email notifications when new slots are available. This project leverages Selenium for web automation, Google Sheets for data storage, and SMTP for email communication.

## Features
- Scrapes available appointment slots from the DMV website.
- Automatically solves CAPTCHAs using the CapSolver API.
- Reads DMV ID, date, and location information from Google Sheets.
- Sends email notifications for newly available appointment slots.
- Stores previously scraped slots to avoid duplicate notifications.

## Prerequisites
Before you begin, ensure you have met the following requirements:
- Python 3.7 or higher
- Google Sheets API credentials (JSON file)
- Access to the CapSolver API

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/dmv-appointment-scraper.git
   cd dmv-appointment-scraper

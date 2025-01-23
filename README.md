# Automated User Management Script

This project automates the process of creating and deleting users via API, generating reports, and cleaning up old reports. It is designed to run daily (morning and evening) with a 10-minute delay between report cleanup and execution.

---

## Features

- **Create Users**: Reads user data from a CSV file and sends a signup request to the API.
- **Delete Users**: Automatically deletes created users via API using their user ID.
- **Report Generation**: Logs the status of user creation and deletion in a CSV report.
- **Report Cleanup**: Deletes reports older than 10 minutes from the system.
- **Scheduled Execution**: Automatically runs the script daily in the morning and evening.

---

## Project Structure

project/ │ 
├── user_management.py # Main Python script ├
── user_student.csv # Input file containing user data ├── user_report.csv # Generated report file ├── requirements.txt # Python dependencies └── README.md # Project documentation

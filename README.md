# PDF Table Extraction and Conversion to Excel

## Overview
This project is a web-based application built with Flask that extracts tables and account details from PDF documents and converts them into an Excel file. It allows users to upload a PDF file containing financial or transactional data, and it processes the extracted information into structured account details and transaction records.

## Features
- Extracts text from PDF files using PyMuPDF (fitz).
- Parses account details such as Bank Name, IFSC Code, MICR Code, and more.
- Detects and extracts transaction tables using regex patterns.
- Converts extracted data into an Excel file with two sheets:
  - **Account Details**
  - **Transactions**
- Provides a user-friendly web interface for file uploads.
- Generates an Excel file for download.

## Installation
### Prerequisites
Ensure you have the following installed:
- Python 3.x
- pip (Python package manager)

### Setup
1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd <project_directory>
   ```
2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the Flask application:
   ```bash
   python app.py
   ```
4. Open your browser and navigate to:
   ```
   http://127.0.0.1:5000/
   ```

## Project Structure
```
📁 Project Folder
├── app.py              # Flask backend logic
├── templates/
│   ├── index.html      # Frontend HTML page
├── requirements.txt    # Required dependencies
├── README.md           # Project documentation
```

## How It Works
1. The user uploads a PDF file containing bank statements or transaction tables.
2. The backend extracts text using PyMuPDF.
3. Regex patterns parse account details and transactions.
4. The extracted data is converted into an Excel file using Pandas.
5. The user downloads the generated Excel file.

## Technologies Used
- **Python** (Flask, Pandas, PyMuPDF, Regex)
- **Flask** (Web framework for handling requests and rendering templates)
- **Bootstrap** (For frontend design)
- **OpenPyXL** (For generating Excel files)

## Usage
1. Run the Flask application.
2. Upload a PDF file via the web interface.
3. Click "Convert & Download."
4. Extracted account details and transactions are saved in an Excel file.

## Contributing
Feel free to contribute by submitting issues or pull requests.

## License
This project is open-source and available under the MIT License.

## Contact
For any questions or suggestions, feel free to reach out!


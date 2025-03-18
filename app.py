from flask import Flask, render_template, request, send_file, redirect, url_for, flash
import fitz  # PyMuPDF
import pandas as pd
import re
from io import BytesIO

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Replace with a secure key

def extract_text_from_pdf_bytes(pdf_bytes):
    # Open the PDF from bytes using PyMuPDF
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    text = ""
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text += page.get_text("text")
    return text

def parse_account_details(text):
    account_details = {}
    # Define regex patterns to capture account details
    patterns = {
        "Bank Name": r"BANK NAME\s*:\s*(.+)",
        "Branch Name": r"BRANCH NAME\s*:\s*(.+)",
        "Address": r"ADDRESS\s*:\s*(.+)",
        "City": r"CITY\s*:\s*(.+)",
        "Pin Code": r"PIN CODE\s*:\s*(.+)",
        "State": r"STATE\s*:\s*(.+)",
        "IFSC Code": r"IFSC Code\s*:\s*(.+)",
        "MICR Code": r"MICR Code\s*:\s*(.+)",
        "Phone No": r"Phone no:\s*(.+)",
        "Account No": r"Account No\s*:\s*(.+)",
        "Account Name": r"A/C Name\s*:\s*(.+)",
        "Nomination Registered": r"Nomination Registered\s*:\s*(.+)",
        "Nominee Name": r"Nominee Name\s*:\s*(.+)",
        "Address2": r"Address\s*:\s*(.+)",  # Added different key to avoid conflict
        "City2": r"City\s*:\s*(.+)",
        "Pin Code2": r"Pin Code\s*:\s*(.+)",
        "Tel No": r"Tel No.\s*:\s*(.+)",
        "Sanction Limit": r"Sanction Limit\s*:\s*(.+)",
        "TOD Limit": r"TOD Limit\s*:\s*(.+)",
        "Interest Rate": r"Interest Rate\s*:\s*(.+)",
        "Open Date": r"Open Date\s*:\s*(.+)",
    }

    for key, pattern in patterns.items():
        match = re.search(pattern, text)
        if match:
            account_details[key] = match.group(1).strip()
    return account_details

def parse_transactions(text):
    transactions = []
    # Regex pattern to extract Date, Description, Amount, and Balance
    transaction_pattern = r"(\d{2}-\w{3}-\d{4})\s+(.+?)\s+([\d,]+\.\d{2})\s+([\d,]+\.\d{2}[A-Za-z]*)"
    matches = re.findall(transaction_pattern, text)
    for match in matches:
        transactions.append({
            "Date": match[0],
            "Description": match[1].strip(),
            "Amount": match[2],
            "Balance": match[3],
        })
    return transactions

def create_excel_file(account_details, transactions):
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        pd.DataFrame([account_details]).to_excel(writer, sheet_name="Account Details", index=False)
        pd.DataFrame(transactions).to_excel(writer, sheet_name="Transactions", index=False)
    output.seek(0)
    return output

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    if "pdf_file" not in request.files:
        flash("No file part")
        return redirect(request.url)
    file = request.files["pdf_file"]
    if file.filename == "":
        flash("No file selected")
        return redirect(request.url)
    try:
        pdf_bytes = file.read()
        text = extract_text_from_pdf_bytes(pdf_bytes)
        account_details = parse_account_details(text)
        transactions = parse_transactions(text)
        print("Account details extracted:", account_details)
        print("Number of transactions extracted:", len(transactions))
        excel_file = create_excel_file(account_details, transactions)
        return send_file(
            excel_file,
            mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            as_attachment=True,
            download_name="output.xlsx"
        )
    except Exception as e:
        print("Error processing PDF:", e)
        flash(f"An error occurred: {e}")
        return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True, port=5000)
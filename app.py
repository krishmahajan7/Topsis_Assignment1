from flask import Flask, render_template, request
import os, re
from topsisalgorithm import topsis
import smtplib
from email.message import EmailMessage

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
RESULT_FOLDER = "results"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

def send_email(to_email, file_path):
    msg = EmailMessage()
    msg['Subject'] = 'TOPSIS Result File'
    msg['From'] = "krishmahajan555@gmail.com"
    msg['To'] = to_email
    msg.set_content("Attached is your TOPSIS result file.")

    with open(file_path, 'rb') as f:
        msg.add_attachment(f.read(), maintype='application', subtype='octet-stream', filename="result.csv")

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login("krishmahajan555@gmail.com", "ofrqiftdrekaiirw")
        smtp.send_message(msg)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    file = request.files['file']
    weights = request.form['weights']
    impacts = request.form['impacts']
    email = request.form['email']

    # Validate email
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return render_template('index.html', msg="Invalid Email Format")

    weights = list(map(float, weights.split(',')))
    impacts = impacts.split(',')

    if len(weights) != len(impacts):
        return render_template('index.html', msg="Weights and Impacts count mismatch")

    for i in impacts:
        if i not in ['+','-']:
            return render_template('index.html', msg="Impacts must be + or -")

    input_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(input_path)

    result_path = os.path.join(RESULT_FOLDER, "result.csv")

    topsis(input_path, weights, impacts, result_path)

    send_email(email, result_path)

    return render_template('index.html', msg="Result sent to Email successfully!")

if __name__ == "__main__":
    app.run(debug=True)

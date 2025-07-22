from flask import Flask, request, jsonify
import mysql.connector
import os

app = Flask(__name__)

# Configure MySQL connection
db = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASS"),
    database=os.getenv("DB_NAME"),
    port=3306
)
cursor = db.cursor()

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    print(data)

    # Extract fields from JotForm JSON
    first_name = data['q1_name']['first']
    last_name = data['q1_name']['last']
    email = data['q2_email']
    dob = data['q4_dob']
    age = data['q5_age']
    gender = data['q6_gender']  
    bank_name = data['q7_nameOf']
    account_no = data['q8_accountNumber']
    ifsc = data['q9_ifseCode']
    pan = data['q10_panNumber']
    phone = data['q12_phoneNumber']['full']

    address = f"{data['q11_address']['addr_line1']}, {data['q11_address'].get('addr_line2', '')}, " \
              f"{data['q11_address']['city']}, {data['q11_address']['state']}, " \
              f"{data['q11_address']['postal']}"

    # Insert into MySQL
    insert_query = """
        INSERT INTO users (first_name, last_name, email, dob, age, gender, bank_name,
                           account_number, ifsc_code, pan_number, phone_number, address)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    values = (first_name, last_name, email, dob, age, gender,
              bank_name, account_no, ifsc, pan, phone, address)

    cursor.execute(insert_query, values)
    db.commit()

    return jsonify({'status': 'success'}), 200

if __name__ == '__main__':
    app.run(debug=True)

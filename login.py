from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

@app.route('/')
def dashboard():
    return render_template('main_dashboard.html')

@app.route('/main_login')
def mainlogin():
    return render_template('main_login.html')





#----------------------------------Patient signup-----------------------------------
@app.route('/patient_signup')
def patientsignup():
    return render_template('patient_signup.html')

# MySQL Configuration
db = mysql.connector.connect(
    host='localhost',
    user='root',
    password='Naveen*1234567890',
    database='mgmt'
)
cursor = db.cursor()

@app.route('/patientsignupverify', methods=['POST'])
def patientsignupverify():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Check if username or email already exists
        cursor.execute("SELECT * FROM user WHERE username = %s OR email = %s", (username, email))
        existing_user = cursor.fetchone()

        if existing_user:
            # Inform the user that username or email already exists
 #           return "Username or Email already exists. Please use a different one."
            message = "Username or Email already exists. Please use a different one."
            return render_template('error_signup.html', message=message)

        # Insert data into the MySQL database if username or email doesn't exist
        query = "INSERT INTO user (username, email, password) VALUES (%s, %s, %s)"
        cursor.execute(query, (username, email, password))
        db.commit()  # Commit changes to the database

        # Redirect to the login page upon successful data insertion
        return redirect(url_for('patientlogin'))
    else:
        return redirect(url_for('index'))  # Redirect back to login page if not a POST request


@app.route('/patient_login')
def patientlogin():
    return render_template('patient_login.html')

@app.route('/patientverify', methods=['POST'])
def patientverify():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Query to fetch user data from the database
        query = "SELECT * FROM user WHERE username = %s AND password = %s"
        cursor.execute(query, (username, password))
        user = cursor.fetchone()

        if user:
            return redirect(url_for('patientdashboard'))  # Redirect to success page upon successful login
        else:
            return redirect(url_for('index'))    # Redirect back to login page with an error message

@app.route('/patientdash')
def patientdashboard():
    return render_template('patient_dashboard.html')








@app.route('/doctor_login')
def doctorlogin():
    return render_template('doctor_login.html')

@app.route('/admin_login')
def adminlogin():
    return render_template('admin_login.html')
















@app.route('/adminverify', methods=['POST'])
def adminverify():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Query to fetch user data from the database
        query = "SELECT * FROM admin WHERE username = %s AND password = %s"
        cursor.execute(query, (username, password))
        user = cursor.fetchone()

        if user:
            return redirect(url_for('admindashboard'))  # Redirect to success page upon successful login
        else:
            return redirect(url_for('index'))    # Redirect back to login page with an error message

@app.route('/admindash')
def admindashboard():
    return render_template('admin_dashboard.html')

#@app.route('/getappointmentdetails')
#def getappointmentdetails():
#    return render_template('appointments_list.html')





#---------------To get appointment details and approve/decline in admin page--------------------
@app.route('/getappointmentdetails')
def get_appointment_details():
    try:
        # Fetch appointment data from the database table
        cursor.execute("SELECT * FROM appointment")
        appointment_data = cursor.fetchall()

        # Pass the appointment data to the HTML template for rendering
        return render_template('appointments_list.html', appointments=appointment_data)
    except mysql.connector.Error as err:
        return f"An error occurred: {err}"

@app.route('/approve/<int:appointment_id>')
def approve_appointment(appointment_id):
    try:
        # Update the appointment status to 'Approved' in the database
        cursor.execute("UPDATE appointment SET status = 'Approved' WHERE id = %s", (appointment_id,))
        db.commit()
        return redirect(url_for('get_appointment_details'))
    except mysql.connector.Error as err:
        return f"An error occurred: {err}"

@app.route('/decline/<int:appointment_id>')
def decline_appointment(appointment_id):
    try:
        # Update the appointment status to 'Declined' in the database
        cursor.execute("UPDATE appointment SET status = 'Declined' WHERE id = %s", (appointment_id,))
        db.commit()
        return redirect(url_for('get_appointment_details'))
    except mysql.connector.Error as err:
        return f"An error occurred: {err}"





#-----------Fetch appointment status in the patient dashboard---------------------
@app.route('/appointmentstatus')
def appointmentstatus():
    try:
        # Fetch approved and declined appointments from the database table
        cursor.execute("SELECT * FROM appointment WHERE status IN ('Approved', 'Declined')")
        approved_declined_data = cursor.fetchall()

        # Pass the data to the HTML template for rendering
        return render_template('appointment_status.html', appointments=approved_declined_data)
    except mysql.connector.Error as err:
        return f"An error occurred: {err}"





#-------------------------Add Doctor details from Admin page---------------------------
@app.route('/adddoctordetails', methods=['POST'])
def adddoctordetails():
    if request.method == 'POST':
        doctorname = request.form['doctorname']
        phonenumber = request.form['phonenumber']
        email = request.form['email']
        password = request.form['password']
        specialization = request.form['specialization']

        # Insert submitted data into the MySQL database
        query = "INSERT INTO doctor (doctorname, phonenumber, email, password, specialization) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(query, (doctorname, phonenumber, email, password, specialization))
        db.commit()  # Commit changes to the database

        # Redirect to success page upon successful data insertion
        return redirect(url_for('adminlogin'))
    else:
        return redirect(url_for('index'))  # Redirect back to login page if not a POST request









@app.route('/appointmentbooking')
def appointmentbooking():
    return render_template('appointment_booking.html')

@app.route('/confirmAppointment', methods=['POST'])
def confirmAppointment():
    if request.method == 'POST':
        username = request.form['username']
        phonenumber = request.form['phonenumber']
        email = request.form['email']
        doctorid = request.form['doctorid']
        doctorname = request.form['doctorname']
        appointmentdate = request.form['appointmentdate']
        appointmenttime = request.form['appointmenttime']
        symptoms = request.form['symptoms']

        # Insert submitted data into the MySQL database
        query = "INSERT INTO appointment (username, phonenumber, email, doctorid, doctorname, appointmentdate, appointmenttime, symptoms) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(query, (username, phonenumber, email, doctorid, doctorname, appointmentdate, appointmenttime, symptoms))
        db.commit()  # Commit changes to the database

        # Redirect to success page upon successful data insertion
        return redirect(url_for('successfulappointment'))
    else:
        return redirect(url_for('index'))  # Redirect back to login page if not a POST request

@app.route('/successful-appointment')
def successfulappointment():
    return render_template('successful_appointment.html')

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, render_template, request, redirect, url_for, session, flash
import config
import mysql.connector as connector
from werkzeug.utils import secure_filename
import os
from ultralytics import YOLO
import bcrypt
from collections import Counter
from dotenv import load_dotenv


load_dotenv()


app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')


def connect_to_db():
    try:
        connection = connector.connect(**config.mysql_credentials)
        return connection
    except connector.Error as e:
        print(f"Error connecting to database: {e}")
        return None


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get('name')
        password = request.form.get('password')
        email = request.form.get('email')
        vehicle_id = request.form.get('vehicleId')
        contact_number = request.form.get('phoneNumber')
        address = request.form.get('address')
        car_brand = request.form.get('carBrand')
        model = request.form.get('carModel')
        
        # print("DATA from form")
        # print(f"name : {name}")
        # print(f"email : {email}")
        # print(f"password : {password}")
        # print(f"vehicle_id : {vehicle_id}")
        # print(f"contact_number : {contact_number}")
        # print(f"address : {address}")
        # print(f"car_brand : {car_brand}")
        # print(f"model : {model}")

        if not all([name, password, email, vehicle_id, contact_number, address, car_brand, model]):
            flash("All fields are required!", "error")
            return render_template('signup.html')

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        connection = connect_to_db()
        if connection:
            try:
                with connection.cursor() as cursor:
                    query = '''
                    INSERT INTO user_info (name, password, email, vehicle_id, contact_number, address, car_brand, model)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    '''
                    cursor.execute(query, (name, hashed_password, email, vehicle_id, contact_number, address, car_brand, model))
                    connection.commit()
                flash("Signup successful!", "success")
                return redirect(url_for('dashboard'))
            except connector.IntegrityError as e:
                if 'Duplicate entry' in str(e):
                    flash("Email already exists. Please use a different email.", "error")
                else:
                    flash("An error occurred while signing up. Please try again.", "error")
            except connector.Error as e:
                print(f"Error executing query: {e}")
                flash("An error occurred while signing up. Please try again.", "error")
        else:
            flash("Database connection failed. Please try again later.", "error")
            
    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        print(f"Email : {email}")
        print(f"Password : {password}")

        if not email or not password:
            flash("Email and password are required!", "error")
            return render_template('login.html')

        connection = connect_to_db()
        if connection:
            try:
                with connection.cursor() as cursor:
                    query = "SELECT password FROM user_info WHERE email = %s"
                    cursor.execute(query, (email,))
                    result = cursor.fetchone()
                    if result and bcrypt.checkpw(password.encode('utf-8'), result[0].encode('utf-8')):
                        session['user_email'] = email  # Store user email in session
                        flash("Login successful!", "success")
                        return redirect(url_for('dashboard'))
                    else:
                        flash("Invalid email or password.", "error")
            except connector.Error as e:
                print(f"Error executing query: {e}")
                flash("An error occurred during login. Please try again.", "error")
        else:
            flash("Database connection failed. Please try again later.", "error")

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('user_email', None)  # Remove user email from session
    flash("You have been logged out.", "info")
    
    return redirect(url_for('login'))


# Load YOLO model
model_path = "D:/Vehicle Damage Detection/models/model weights/best.pt"
model = YOLO(model_path)


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if request.method == 'POST':
        file = request.files.get('image')
        if not file:
            flash('Please upload an image.', 'error')
            return render_template('dashboard.html')

        filename = secure_filename(file.filename)
        if not filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            flash('Invalid file type. Please upload an image.', 'error')
            return render_template('dashboard.html')
        
        # Save the uploaded image
        image_path = os.path.join('D:/Vehicle Damage Detection/static', 'uploaded_image.jpg')
        print("File uploaded successfully")
        
        file.save(image_path)
        # print(f"Upload image path : {image_path}")
        # Make predictions using YOLO
        result = model(image_path)
        detected_objects = result[0].boxes
        class_ids = [box.cls.item() for box in detected_objects]
        class_counts = Counter(class_ids)
        # print(f"Class counts : {class_counts}")
        # Save the image with detections
        detected_image_path = os.path.join('D:/Vehicle Damage Detection/static', 'detected_image.jpg')
        detected_image_path = result[0].save(detected_image_path)
        print(f"Detected image path : {detected_image_path}")
        # Get the user's email from session
        user_email = session.get('user_email')
        print(user_email)
        if not user_email:
            flash('You need to log in to get an estimate.', 'error')
            return redirect(url_for('login'))

        # Fetch part prices from the database
        part_prices = get_part_prices(user_email, class_counts)
        # print(f"Part prices : {part_prices}")
        return render_template('estimate.html', original_image='uploaded_image.jpg', detected_image='detected_image.jpg', part_prices=part_prices)

    return render_template('dashboard.html')


def get_part_prices(email, class_counts):
    connection = connect_to_db()
    if connection:
        try:
            with connection.cursor(dictionary=True) as cursor:
                # Get user's car brand and model
                cursor.execute("SELECT car_brand, model FROM user_info WHERE email = %s", (email,))
                user_data = cursor.fetchone()
                if not user_data:
                    print("User not found")
                    return {}

                car_brand = user_data['car_brand']
                car_model = user_data['model']

                # Fetch part prices
                prices = {}
                for class_id, count in class_counts.items():
                    part_name = get_part_name_from_id(class_id)
                    # print(f"Parts name: {part_name}")
                    if part_name:
                        cursor.execute(
                            "SELECT price FROM car_models WHERE brand = %s AND model = %s AND part = %s",
                            (car_brand, car_model, part_name)
                        )
                        price_data = cursor.fetchone()
                        # print(f"Price data : {price_data}")
                        if price_data:
                            price_per_part = price_data['price']
                            total_price = price_per_part * count
                            prices[part_name] = {'count': count, 'price': price_per_part, 'total': total_price}
                # print(f"Prices : {prices}")
                return prices
        except connector.Error as e:
            print(f"Error executing query: {e}")
            return {}
    print("Connection failed")
    return {}


def get_part_name_from_id(class_id):
    class_names = ['Bonnet', 'Bumper', 'Dickey', 'Door', 'Fender', 'Light', 'Windshield']
    if 0 <= class_id < len(class_names):
        return class_names[int(class_id)]
    return None


@app.route('/view_profile')
def view_profile():
    if 'user_email' not in session:
        flash('You need to login to view your profile.', 'error')
        return redirect(url_for('login'))

    connection = connect_to_db()
    if connection:
        try:
            with connection.cursor(dictionary=True) as cursor:
                # Fetch current user information
                cursor.execute("SELECT * FROM user_info WHERE email = %s", (session['user_email'],))
                user_info = cursor.fetchone()
                if not user_info:
                    flash('User not found.', 'error')
                    return redirect(url_for('dashboard'))
                return render_template('view_profile.html', user_info=user_info)
        except connector.Error as e:
            print(f"Error executing query: {e}")
            flash("An error occurred while fetching your profile. Please try again.", "error")
    else:
        flash("Database connection failed. Please try again later.", "error")

    return redirect(url_for('dashboard'))


@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    if 'user_email' not in session:
        flash('You need to login to edit your profile.', 'error')
        return redirect(url_for('login'))

    connection = connect_to_db()
    if connection:
        try:
            with connection.cursor(dictionary=True) as cursor:
                if request.method == 'POST':
                    # Update user information
                    query = '''
                    UPDATE user_info
                    SET name = %s, email = %s, vehicle_id = %s, contact_number = %s, 
                        address = %s, car_brand = %s, model = %s
                    WHERE email = %s
                    '''
                    cursor.execute(query, (
                        request.form['name'],
                        request.form['email'],
                        request.form['vehicleId'],
                        request.form['phoneNumber'],
                        request.form['address'],
                        request.form['carBrand'],
                        request.form['carModel'],
                        session['user_email']
                    ))
                    connection.commit()
                    flash('Profile updated successfully!', 'success')
                    session['user_email'] = request.form['email']  # Update session if email changed
                    return redirect(url_for('dashboard'))

                # Fetch current user information
                cursor.execute("SELECT * FROM user_info WHERE email = %s", (session['user_email'],))
                user_info = cursor.fetchone()
                return render_template('edit_profile.html', user_info=user_info)

        except connector.Error as e:
            print(f"Error executing query: {e}")
            flash("An error occurred while updating your profile. Please try again.", "error")
    else:
        flash("Database connection failed. Please try again later.", "error")

    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(debug=True)
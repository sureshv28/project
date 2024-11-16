import os
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from werkzeug.security import generate_password_hash,check_password_hash
import mysql.connector
from PIL import Image
import torchvision.transforms.functional as TF
import CNN
import numpy as np
import torch
import pandas as pd

disease_info = pd.read_csv('disease_info.csv' , encoding='cp1252')
supplement_info = pd.read_csv('supplement_info.csv',encoding='cp1252')

model = CNN.CNN(39)    
model.load_state_dict(torch.load("plant_disease_model_1_latest.pt"))
model.eval()

def prediction(image_path):
    image = Image.open(image_path)
    image = image.resize((224, 224))
    input_data = TF.to_tensor(image)
    input_data = input_data.view((-1, 3, 224, 224))
    output = model(input_data)
    output = output.detach().numpy()
    index = np.argmax(output)
    return index

app = Flask(__name__)
app.secret_key = 'your_secret_key'


db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="project"
)

cursor = db.cursor()

@app.route('/')
def home_page():
    return render_template("home.html")



@app.route('/register', methods=['GET', 'POST'])
def register1():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        if not username or not email or not password:
            return jsonify({'success': False, 'message': 'All fields are required'}), 400

        password_hash = generate_password_hash(password)

        try:
            cursor.execute("INSERT INTO users (username, password) VALUES (%s,%s)", (username,password))
            db.commit()
            return jsonify({'success': True, 'message': 'User registered successfully'}), 201
        except Exception as e:
            print(f"Error: {e}")
            return jsonify({'success': False, 'message': 'Registration failed. User might already exist'}), 500
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        print(user[1])

        if user and (user[1]== password):
            session['username'] = username
            return jsonify({'success': True}), 200
        else:
            return jsonify({'success': False, 'message': 'Invalid username or password'}), 401
    return render_template('login.html')


@app.route('/home')
def home():
    
    return render_template("home.html")
    



@app.route('/index')
def index():
    return render_template("index.html")

@app.route('/register')
def register():
    return render_template("register.html")


@app.route('/contact')
def contact():
    return render_template("contact.html")


@app.route('/submit', methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        image = request.files['image']
        filename = image.filename
        file_path = os.path.join('static/uploads', filename)
        image.save(file_path)
        print(file_path)
        pred = prediction(file_path)
        title = disease_info['disease_name'][pred]
        description =disease_info['description'][pred]
        prevent = disease_info['Possible Steps'][pred]
        image_url = disease_info['image_url'][pred]
        supplement_name = supplement_info['supplement name'][pred]
        supplement_image_url = supplement_info['supplement image'][pred]
        supplement_buy_link = supplement_info['buy link'][pred]
        return render_template('submit.html' , title = title , desc = description , prevent = prevent , 
                               image_url = '/static/uploads/'+filename , pred = pred ,sname = supplement_name , simage = supplement_image_url , buy_link = supplement_buy_link)


@app.route('/supplement', methods=['GET', 'POST'])
def supplement():
    return render_template('supplement.html', supplement_image = list(supplement_info['supplement image']),
                           supplement_name = list(supplement_info['supplement name']), disease = list(disease_info['disease_name']), buy = list(supplement_info['buy link']))



if __name__ == "__main__":
    app.run(debug=True)
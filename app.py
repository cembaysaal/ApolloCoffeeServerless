from flask import Flask, request, jsonify, render_template, send_from_directory,redirect, url_for, session
import firebase_admin
from firebase_admin import credentials, firestore, auth
import os
from pyrebase import pyrebase
import json
import datetime
import time
from modal import Stub, wsgi_app, Volume, NetworkFileSystem, Image, Mount
from modal import Stub, Image

api_data = {
    "apiKey": "AIzaSyD50zFI8rUgDRxlIYdBp4JMyraa1ueDjwc",
    "type": "service_account",
    "project_id": "webhw-10d51",
    "private_key_id": "5c703a9a630659e0da537b61071deeaf694f54b9",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCXREBiwK543Ue4\nCACsHsozpEeUK3SYIKfBD8S436HAnFk8V0RSJrOI40ZPvdLYcwUEW8BEORN0K3sF\n2cZHFhOXzp68WN3BTF2xOrpZ6TNMjORNGydw4tRE303Xl4yBbf5qm3fFVHFk/2GK\nOO6foy+1c80nkNt6kKF5d/Is6ujQLI17u9bNE5urE0UrZb/PRkbNCFv6uXRU1jJm\nLnv+CpLsW1ssomcyBbsa2nh4JmAaFvCd2cRZbXpGQnFDZQTJVcolOkJzZjnZrhEW\n+aDcl15mR9hB7Aqb6whXQqQLeUKt2fWkk36KB10aHpqPBws0O5E93flC8sJCrGj6\nU9TggsDDAgMBAAECggEABBar5i2kFEiS3KDt20dZjI9zq51PhPY8jTPyaBphF7Ke\nmUpRcNEA3Z5FrDEZAzvtiBCulTQm2BHTPO4UPGak9+3ZDb6Lm+LcXFSywjN9e05f\n0K+4Jng9vRt9J04+Y+1rOp+pPtBXxBEkJmVx4NG7LhyLOvcLik1hPw1PMM9Ia8ap\nbFyN2SJC4L8zog8ILy3ljlinS5x27S3+Mf0RxR02Ikl7pURbdyWXkcQ8YWnAY2Tm\nWKXO96C3s7R3elJSPNtm3uB6353kBHpdUXxp7Bu5icl8D5+FmmtPYfUglffVR4eP\n0vPVxETpj1juKiZI+uUKbCo1mFWrins3CAQvqYW9sQKBgQDFCxk7cPHl1kOAL6Kh\ni8HaApixyQZf8sXlb4PA3f+JibyqN3KwQFJOOFscq3hLaegiLi486jEuqadkpLmb\nrvAM8/GjtlC4fKGAo12nrH5vsBOwNwRD+/xyS8bigm/ZBwCES5GLboOMvLdmLuIe\n0c7ohhknOlGppD7tHGgdjDTNcwKBgQDEhsxPgA2SfLMRTujDM7qX/8H0xqth7dFI\nwEX4vHS1bX+GYn+yU7Nm8JN9YPY9oWBLKmYYTu7NJwXWuHiis0+UH/Jm9MpHlzw0\nbjA5LsR2vCAvwDNyfalLK1MNLWpJAp44EVnn+wEYxYv7p/5h2D6wK8hjSQ38Q14Z\nR34rMhdrcQKBgQCO351MHHlJzjLjn6asvEmzam6NetXEfKRB2LoP/uhrMhQ62Dmw\n0vLbBMIL58kx5XkMT6/3O1iuHRXjRA3RdOdafQeZTXj6TGROgiZGjiyfj2y3OS0+\nnlhOB+QOGcY/93PIeYLvNxLr2WqiDRyofDkrIRDcAM111EJMa2yTADbJQQKBgB3A\nDjPGvcc8K1tmZ6QNM6UI6ZKldJJJjxIFUVJbLQu9/L0aMhyLwS/HIXysbfpccJhQ\nXc42PL4/twmPOWvf2x8gSvC9A9YcldeWCqTNaJ5U0kaIQQGG9lbTwynOgzV0OQFh\n1wtgGwVl+k/pWX/0XWEL77Tf/Ub/58HJ6daeKZ9xAoGAd/KgTbmPDjgTp677hzXc\nxpTFuEqJIKaTZoLucWy7SAwaeCcLIEvv8uO62m9rVqFP0ocepKo+vzHbLkBaNxqi\n+3JWRZdnbkx7PzO+8pvIGNe7kw5cnmXYhzIm0bQj54XKS3TOTDG19RebO9WKmr6K\n8JEo64FpJGZ+X4G0zFDwFBw=\n-----END PRIVATE KEY-----\n",
    "client_email": "firebase-adminsdk-u1cl6@webhw-10d51.iam.gserviceaccount.com",
    "client_id": "104919999687899558888",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-u1cl6%40webhw-10d51.iam.gserviceaccount.com",
    "universe_domain": "googleapis.com"
  }
cred = credentials.Certificate(api_data)
firebase_admin.initialize_app(cred)
firebase_config = {
    "apiKey": "AIzaSyD50zFI8rUgDRxlIYdBp4JMyraa1ueDjwc",
    "authDomain": "webhw-10d51.firebaseapp.com",
    "databaseURL": "https://webhw-10d51-default-rtdb.firebaseio.com",
    "projectId": "webhw-10d51",
    "storageBucket": "webhw-10d51.appspot.com",
    "messagingSenderId": "372272369535",
    "appId": "1:372272369535:web:d71cf84523398b1445544a",
    "measurementId": "G-P324S81H82"
}

firebase = pyrebase.initialize_app(firebase_config)

auth1 = firebase.auth()

db = firestore.client()

stub = Stub("cem-hw5",
            image=Image.debian_slim().pip_install(
"blinker==1.7.0",
"CacheControl==0.13.1",
"cachetools==5.3.2",
"certifi==2023.11.17",
"cffi==1.16.0",
"charset-normalizer==3.3.2",
"click==8.1.7",
"colorama==0.4.6",
"cryptography==41.0.5",
"firebase-admin==6.2.0",
"firebase-token-generator==2.0.1",
"Flask==3.0.0",
"gcloud==0.18.3",
"google-api-core==2.14.0",
"google-api-python-client==2.108.0",
"google-auth==2.23.4",
"google-auth-httplib2==0.1.1",
"google-cloud-core==2.3.3",
"google-cloud-firestore==2.13.1",
"google-cloud-storage==2.13.0",
"google-crc32c==1.5.0",
"google-resumable-media==2.6.0",
"googleapis-common-protos==1.61.0",
"grpcio==1.59.3",
"grpcio-status==1.59.3",
"httplib2==0.22.0",
"idna==3.6",
"itsdangerous==2.1.2",
"Jinja2==3.1.2",
"jws==0.1.3",
"MarkupSafe==2.1.3",
"msgpack==1.0.7",
"oauth2client==4.1.3",
"proto-plus==1.22.3",
"protobuf==4.25.1",
"pyasn1==0.5.1",
"pyasn1-modules==0.3.0",
"pycparser==2.21",
"pycryptodome==3.19.0",
"PyJWT==2.8.0",
"pyparsing==3.1.1",
"Pyrebase4==4.7.1",
"python-jwt==2.0.1",
"requests==2.29.0",
"requests-toolbelt==0.10.1",
"rsa==4.9",
"six==1.16.0",
"sseclient==0.0.27",
"uritemplate==4.1.1",
"urllib3==1.26.18",
"Werkzeug==3.0.1"))



@stub.function(mounts=[Mount.from_local_dir("DATAS", remote_path="/root/DATAS")])
@wsgi_app()
def flask_app():
    app = Flask(__name__, template_folder='/root/DATAS/templates', static_folder='/root/DATAS/static')
    app.secret_key = os.urandom(24)

    @app.route('/user')
    def user_index():
        coffee_data = db.collection('products').get()
        coffees = [{'name': coffee.get('name'), 'description': coffee.get('description'), 'prices': coffee.get('prices'), 'product_id': coffee.get('product_id')} for coffee in coffee_data]
        return render_template('user/userindex.html', coffees=coffees)

    @app.route('/usercoffees')
    def user_coffees():
        products_data = db.collection('products').get()
        products = [
            {
                'id': product.id,
                'name': product.get('name'),
                'prices': product.get('prices'),
                'description': product.get('description'),
                'product_id': product.get('product_id') 
            } 
            for product in products_data
        ]

        return render_template('user/usercoffees.html', products=products)


    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/user/basket')
    def basket():
        user_id = session['user_id'] 
        orders = db.collection('current_order').where(field_path='user_id', op_string='==', value=user_id).get()
        order_data = [
            {
                'order_id': order.id,
                'user_name': order.get('user_name'),
                'user_id': order.get('user_id'),
                'productId': order.get('productId'),
                'size': order.get('size'),
                'quantity': order.get('quantity'),
                'description': order.get('description'),
                'delivery_time': order.get('deliveryTime')
            }
            for order in orders
        ]
        return render_template('user/basket.html', orders=order_data)



    @app.route('/user/orders')
    def user_orders():
        user_id = session['user_id']  
        orders = db.collection('current_order').where(field_path='user_id', op_string='==', value=user_id).stream()  
        order_data = [
            {
                'order_id': order.id,
                'user_name': order.get('user_name'),  
                'user_id': order.get('user_id'),
                'description': order.get('description')
            }
            for order in orders
        ]
        return render_template('user/userorders.html', orders=order_data)  
    @app.route('/admin/coffees')
    def admin_coffees():

        products_data = db.collection('products').get()
        products = [
            {
                'id': product.id,
                'name': product.get('name'),
                'prices': product.get('prices'),
                'description': product.get('description'),
                'product_id': product.get('product_id') 
            } 
            for product in products_data
        ]
        
        return render_template('admin/admincoffees.html', coffees=products)

    @app.route('/admin/orders')
    def admin_orders():
        last_ten_orders = db.collection('current_order').order_by('date_time', direction=firestore.Query.DESCENDING).stream()
        current_orders_list = [order.to_dict() for order in last_ten_orders]
        print(current_orders_list)
        return render_template('admin/adminorders.html', orders=current_orders_list)




    @app.route('/coffees')
    def coffees():
        products_data = db.collection('products').get()
        products = [
            {
                'id': product.id,
                'name': product.get('name'),
                'prices': product.get('prices'),
                'description': product.get('description'),
                'product_id': product.get('product_id') 
            } 
            for product in products_data
        ]
        return render_template('coffees.html', coffees=products)



    @app.route('/admin/panel', methods=['GET', 'POST'])
    def admin_panel():
        if request.method == 'POST':
            product_name = request.form.get('coffeeName')
            product_id = request.form.get('coffeeID')
            product_description = request.form.get('product_description')
            product_prices = {
                'small': request.form.get('smallPrice'),
                'medium': request.form.get('mediumPrice'),
                'large': request.form.get('largePrice')
            }

            db.collection('products').add({
                'name': product_name,
                'product_id': product_id, 
                'description': product_description,
                'prices': product_prices
            })

            return redirect(url_for('admin_panel'))

        return render_template('admin/admin.html')

    @app.route('/admin/index')
    def admin_index():
        return render_template('admin/adminindex.html')




    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            email = request.form.get('email')
            password = request.form.get('password')
            
            user_data_firebase = db.collection('users').where(field_path='email', op_string='==', value=email).stream()
            user_data_list = [user_data.to_dict() for user_data in user_data_firebase]
            if not user_data_list:
                return "User not found"
            print("AAAAAAAAA",user_data_list[0])
            user_role = user_data_list[0]['role']
            try:
                user = auth.get_user_by_email(email)
                if user:
                    auth1.sign_in_with_email_and_password(email, password)
                    session['user_role'] = user_role
                    session['user_id'] = user.uid
                    session['user_name'] = user_data_list[0]['username']
                    session['user_email'] = user_data_list[0]['email']
                    
                    if user_role == 'admin':
                        return redirect(url_for('admin_index'))
                    else:
                        return redirect(url_for('user_index'))
            except Exception as e:
                return f"Login failed: {e}"
            
            
            
        return render_template('login.html')


    @app.route('/signup', methods=['GET', 'POST'])
    def signup():
        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']
            username = request.form['username']
            fullname = request.form['fullname']
            confirm_password = request.form['confirmPassword']
            
            if password != confirm_password:
                return "Password and Confirm Password do not match"
            try:
                user = auth.create_user(
                    email=email,
                    email_verified=False,
                    password=password,
                    display_name=username
                )
                session['user_id'] = user.uid
                user_data = {
                    'uid': user.uid,
                    'username': username,
                    'email': email,
                    'password': password,
                    'fullname': fullname
                }
                
                db.collection('users').add(user_data)

                return redirect(url_for('login'))  
            except Exception as e:
                return f"Registration failed: {e}"

        return render_template('signup.html')
            
    
    @app.route('/add_to_cart', methods=['POST'])
    def add_to_cart():
        data = request.get_json()
        description = db.collection('products').document(data.get('productId')).get().get('description')
        now = datetime.datetime.now()
        date_time = now.strftime("%d/%m/%Y %H:%M:%S")

        current_order = {
            "productId": data.get('productId'),
            "size": data.get('size'),
            "quantity": data.get('quantity'),
            "deliveryTime": data.get('deliveryTime'),
            "user_name": session['user_name'],
            "user_id": session['user_id'],
            "description": description,
            'date_time': date_time
        }


        db.collection('current_order').add(current_order)

        return jsonify({"message": "Product added to cart successfully!"})

    @app.route('/logout')
    def logout():
        return redirect(url_for('index'))

    @app.route('/submit_product', methods=['POST'])
    def submit_product():
        return redirect(url_for('admin.html'))
    return app
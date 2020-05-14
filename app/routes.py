import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from app import app, db, bcrypt, mail
from app.forms import RegistrationForm, LoginForm, PropertyForm
from app.models import User, Property
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Mail, Message
from flask_migrate import Migrate, MigrateCommand
from flask_uploads import UploadSet,configure_uploads,IMAGES

images = UploadSet('images', IMAGES)

@app.route("/")
@app.route("/index")
def index():
    return render_template('index.html')

@app.route("/categories")
def categories():
    all_properties = Property.query.all()
    
    return render_template('categories.html',all_properties = all_properties)

@app.route('/property/<int:property_id>')
@login_required
def _property(property_id):
    _property = Property.query.get(id)
    return render_template('property.html',_property = _property)

@app.route('/property/new', methods = ['POST','GET'])
@login_required
def new_property():
    form = PropertyForm()
    if form.validate_on_submit():
       
        description = form.content.data
        rent = form.rent.data
        if rent < 20001:
            rent_category = '_0_to_20'
        elif rent < 40001:
            rent_category = '_20_to_40'
        elif rent < 60001:
            rent_category = '_40_to_60'
        else:
            rent_category = 'above_60'
        
        location = form.location.data 
        owner_id = current_user._get_current_object().id 
        new_property = Property(description=description, rent=rent, rent_category=rent_category, location=location, owner_id=owner_id)
        new_property.save()
        return redirect(url_for('new_property'))
        
    return render_template('create_property.html', form = form)   

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)
    
@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)   

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))

# def save_picture(form_picture):
#     random_hex = secrets.token_hex(8)
#     _, f_ext = os.path.splitext(form_picture.filename)
#     picture_fn = random_hex + f_ext
#     picture_path = os.path.join(app.root_path, 'static/images', picture_fn)

#     output_size = (1364, 900)
#     i = Image.open(form_picture)
#     i.thumbnail(output_size)
#     i.save(picture_path)

#     return picture_fn   
# 
@app.route('/property/<int:id>',methods= ['POST'])
@login_required
def property_pic(id):
    property = Property.query.filter_by(owner_id = id).first()
    if 'image' in request.files:
        filename = images.save(request.files['image'])
        path = f'images/{filename}'
        property.image_file = path
        db.session.commit()
    return redirect(url_for('categories'))  

   
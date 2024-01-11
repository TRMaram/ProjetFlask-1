from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
import os
import datetime

from werkzeug.security import check_password_hash

app = Flask(__name__)
app = Flask(__name__, static_folder='static')
# Configuration de la base de données MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:@localhost:3306/dbtest'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key'  # Clé secrète pour gérer la session

# Flask-Mail configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # Replace with your SMTP server
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'khaldiyasmine27@gmail.com'  # Your email username
app.config['MAIL_PASSWORD'] = 'hcjo ivsr zbrs pusv'  # Your email password
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
# Initialisation des extensions
db = SQLAlchemy(app)
mail = Mail(app)

# Modèle de données pour la table User
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    civility = db.Column(db.String(10))
    date_of_birth = db.Column(db.String(20))
class candidature(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100))
    prenom = db.Column(db.String(100))
    email = db.Column(db.String(100))
    tel = db.Column(db.String(10))
    date = db.Column(db.String(100))
    offre = db.Column(db.String(50))
    dn = db.Column(db.String(20))
    cv = db.Column(db.LargeBinary)
class jobs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String)
    Entreprise = db.Column(db.String)
    Emplacement = db.Column(db.String)
    Details = db.Column(db.String)
class voir_details(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    Date_d_expiration = db.Column(db.String)
    Exigences_de_l_emploi = db.Column(db.String)
    Description_de_l_emploi = db.Column(db.String)
    Langue = db.Column(db.String)
    Remuneration_proposee = db.Column(db.String)
    Niveau_d_etude = db.Column(db.String)
    Genre = db.Column(db.String)
    Experience = db.Column(db.String)
    Type_d_emploi_desire = db.Column(db.String)
    Postes_vacants = db.Column(db.String)
    datePostulation = db.Column(db.String)
    location = db.Column(db.String)
    company = db.Column(db.String)

@app.route('/')
def index():
    d2 = jobs.query.all()
    return render_template('Home1.html',d2=d2)
@app.route('/connexion')
def connexion():
    return render_template('index.html')

@app.route('/details/<int:post_id>')
def details(post_id):
    # Dummy function to fetch post details based on post_id (replace with actual database query)
    post = voir_details.query.get(post_id)
    print(post.title)
    return render_template('details.html', post=post)


@app.route('/postuler/<int:post_id>', methods=['POST'])
def postuler(post_id):
    job = voir_details.query.get(post_id)
    if request.method == 'POST':
        nom = request.form['nom']
        prenom=request.form['prenom']
        email = request.form['email']
        tel = request.form['tel']
        dn = request.form['dn']
        offre = job.title
        date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cv = request.files['cv'] if 'cv' in request.files else None


        # Création d'un nouvel utilisateur et enregistrement dans la base de données
        new_candidat = candidature(
            nom=nom,
            prenom=prenom,
            email=email,
            tel=tel,
            dn=dn,
            date=date,
            offre=offre,
            cv=cv.read()
            # Ajoutez d'autres champs au besoin
        )
        db.session.add(new_candidat)
        db.session.commit()
        # Perform your candidat creation logic here
        # ...

        # For now, let's just print the received data
        print(f"Name: {nom}")
        print(f"prenom: {prenom}")
        print(f"Email: {email}")
        print(f"Tel {tel}")
        print(f"Date : {date}")
        print(f"Offre : {offre}")
        print(f"Date of Birth: {dn}")
        if cv:
            cv_filename = cv.filename  # Retrieve the file name
            print(f"Uploaded CV: {cv_filename}")
        msg = Message('Postulation avec Succée',
                      sender='your-email@example.com',  # Replace with your email address
                      recipients=[email])
        msg.body = f"Dear {nom},\nYour post to {offre} on {date} has been successfully submitted! Thank you."
        mail.send(msg)
        flash('Your post was successfull')
        return redirect(url_for('index'))
    return render_template('index.html')




@app.route('/signup', methods=['POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirmPassword']
        civility = request.form['civility']
        date_of_birth = request.form['dateOfBirth']
        cv = request.files['cv'] if 'cv' in request.files else None

        # Création d'un nouvel utilisateur et enregistrement dans la base de données
        new_user = User(
            name=name,
            email=email,
            password=password,
            civility=civility,
            date_of_birth=date_of_birth
            # Ajoutez d'autres champs au besoin
        )
        db.session.add(new_user)
        db.session.commit()
        # Perform your account creation logic here
        # ...

        # For now, let's just print the received data
        print(f"Name: {name}")
        print(f"Email: {email}")
        print(f"Password: {password}")
        print(f"Confirm Password: {confirm_password}")
        print(f"Civility: {civility}")
        print(f"Date of Birth: {date_of_birth}")
        if cv:
            cv_filename = cv.filename  # Retrieve the file name
            print(f"Uploaded CV: {cv_filename}")





        send_confirmation_email(name, email)  # Send confirmation email
        return redirect(url_for('success'))

    return render_template('index.html')

def send_confirmation_email(name, email):
    msg = Message('Account Created Successfully',
                  sender='your-email@example.com',  # Replace with your email address
                  recipients=[email])
    msg.body = f"Dear {name},\nYour account has been successfully created! Thank you."
    mail.send(msg)

@app.route('/success')
def success():
    return render_template('success.html')


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email, password=password).first()

        if user :
            # Si l'utilisateur existe et que le mot de passe correspond, connectez l'utilisateur


                print(user.id)
                user = User.query.filter_by(id=user.id).first()

                print(user.email)
                cand = candidature.query.filter(candidature.email.ilike(f'%{user.email}')).all()

                print(cand)
                return render_template('Home.html', user=user, candidate=cand)
        else:
           return render_template('index.html')





@app.route('/search', methods=['GET', ''])
def search():
    # Retrieve the search query from the URL parameters
    search_query = request.args.get('q', '')

    # Perform a search in the database (replace with your actual database query)
    if search_query:
        d2 = jobs.query.filter(jobs.titre.ilike(f'%{search_query}'))

    else:
        d2 = jobs.query.all()

    return render_template('Home1.html', d2=d2, search_query=search_query)


if __name__ == '__main__':
    db.create_all()  # Création des tables dans la base de données
    app.run(debug=True)




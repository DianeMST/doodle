from flask import Flask, render_template, request, redirect, session, make_response
from pony.flask import Pony
from flask_mail import Mail, Message
from pony.orm import *
from datetime import datetime

app = Flask(__name__)
app.config.update(dict(
    SECRET_KEY = 'QQQQQQQQQQQQQQQQQQQQQ'
))

app.config.update(
MAIL_SERVER = "smtp.gmail.com",
MAIL_PORT = 465,
MAIL_USE_SSL = "MAIL_USE_SSL",
MAIL_USERNAME = "yoancourspromeo@gmail.com",
MAIL_PASSWORD = "oehfwyycnrbaxows",
)
mail = Mail(app)

#Database config

db = Database()
pony = Pony(app)
pony.db = db

class Formateur(db.Entity):
    id = PrimaryKey(int, auto=True)
    username = Required(str, unique=True)  # New field
    Nom = Required(str)
    Prenom = Required(str)
    mdp = Required(str)
    Mail = Required(str)
    RDVs = Set('RDV')  

class Centre(db.Entity):
    id = PrimaryKey(int, auto=True)
    Ville = Required(str)
    Adresse = Required(str)

class Formation(db.Entity):
    id = PrimaryKey(int, auto=True)
    Nom = Required(str)
    RDVs = Set('RDV')

class RDV(db.Entity):
    id = PrimaryKey(int, auto=True)
    Heure = Required(datetime)
    Duree = Required(int)
    Date = Required(datetime)
    Formateur = Required(Formateur)  
    Formation = Required(Formation)  
    Nom = Required(str)
    Prenom = Required(str)
    Mail = Required(str)
    Telephone = Required(str)
    Url_invitation = Optional(str)

db.bind(provider='mysql', host='localhost', user='doodle', password='doodle', database='doodle')
db.generate_mapping(create_tables=True)


#Route page index qui affiche directement ce connecter
@app.route('/')
def indexlogin():
    return render_template('login.jinja')
#ROute page d'accueil
@app.route('/index')
def index():
    return render_template('index.jinja')

@app.route('/validelogin')
def validelogin():
    return render_template('validelogin.jinja')

@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'mdp' in request.form:
        username = request.form['username']
        mdp = request.form['mdp']
        with db_session:
            print('valide')
            user = Formateur.get(username = username, mdp = mdp)
            if user:
                session['loggedin'] = True
                session['id'] = user.id
                session['username'] = user.username
                return make_response (redirect('validelogin'))
                
            else:
                msg = 'Incorrect username/mdp!'
    return render_template('login.jinja', msg=msg)

@app.route('/rdv_pris')
def rdv_pris():
    return render_template('rdv_pris.jinja')

@app.route('/rdv')
def rdv():
    return render_template('rdv.jinja')

@app.route('/contact')
def contact():
    return render_template('contact.jinja')

#Formulaire de contact qui envoie le mail
@app.route('/contact_mail', methods=['POST'])
def contact_mail():
    nom = request.form.get('nom')
    prenom = request.form.get('prenom')
    email = request.form.get('email')
    telephone = request.form.get('telephone')
    message = request.form.get('message')
    objet = request.form.get('objet')
    
    msg = Message(body=f"Object : {objet} \n email : {email} \n nom: {nom} \n prenom {prenom} \n Message :  {message}",
                 recipients=['f.yoan19@gmail.com'],
                 sender= 'yoancourspromeo@gmail.com',
                 subject=f"Message de {prenom} {nom}")

    mail.send(msg)
    return render_template('validation_contact_form.jinja')



#Formulaire de prise de rendez-vous : 
@app.route('/prendre_rdv_form', methods=['POST'])
def prendre_rdv_form():
    nom = request.form.get('nom')
    email = request.form.get('email')
    formateur = request.form.get('formateur')
    date = request.form.get('date')
    heure = request.form.get('heure')
    durer = request.form.get('durer')
    
    msg = Message(body=f"nom: {nom}  \n email : {email} \n Formateur : {formateur} \n Date : {date} \n Heure : {heure} \n Durée du rdv :  {durer}",
                 recipients=['f.yoan19@gmail.com'],
                 sender= 'yoancourspromeo@gmail.com',
                 subject=f"Récapitulatif de la prise de rendez-vous  de {nom} {email}")
    
    
    mail.send(msg)
    return render_template('validation_prendrerdv_form.jinja')

@app.route('/register')
def register():
    return render_template('register.jinja')

if __name__ == '__main__':
    app.run(debug=True)
    
    


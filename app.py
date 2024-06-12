from flask import Flask, render_template, request, redirect, session, make_response, flash
from pony.flask import Pony
from flask_mail import Mail, Message
from pony.orm import *
from datetime import datetime, date

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
    username = Required(str, unique=True)  
    Nom = Required(str)
    Prenom = Required(str)
    mdp = Required(str)
    Mail = Required(str)
    RDVs = Set('RDV') 

class Eleve(db.Entity):
    id = PrimaryKey(int, auto=True)
    username = Required(str, unique=True)  
    Nom = Required(str)
    Prenom = Required(str)
    mdp = Required(str)
    Mail = Required(str)
  

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
    Date = Required(date) 
    Formateur = Required(Formateur)  
    Formation = Required(Formation)  
    Nom = Required(str)
    Prenom = Required(str)
    Mail = Required(str)
    Telephone = Required(str)
    Url_invitation = Optional(str)


db.bind(provider='mysql', host='localhost', user='doodle', password='doodle', database='doodle')
db.generate_mapping(create_tables=True)



@app.route('/')
def index():
    username = session.get('username', None)
    return render_template('index.jinja', username=username)



@app.route('/validelogin')
def validelogin():
    return render_template('validelogin.jinja')

@app.route('/validelogout')
def validelogout():
    return render_template('validelogout.jinja')

@app.route('/loginFormateur', methods=['GET', 'POST'])
def loginFormateur():
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
                session['type'] = 'formateur'
                return make_response (redirect('validelogin'))
                
            else:
                msg = 'Incorrect username/mdp!'
    return render_template('loginFormateur.jinja', msg=msg)


@app.route('/loginEleve', methods=['GET', 'POST'])
def loginEleve():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'mdp' in request.form:
        username = request.form['username']
        mdp = request.form['mdp']
        with db_session:
            print('valide')
            user = Eleve.get(username=username, mdp=mdp)
            if user:
                session['loggedin'] = True
                session['id'] = user.id
                session['username'] = user.username
                session['Nom'] = user.Nom
                session['Prenom'] = user.Prenom
                session['Mail'] = user.Mail
                session['type'] = 'eleve'
                return make_response(redirect('validelogin'))
            else:
                msg = 'Incorrect username/mdp!'
    return render_template('loginEleve.jinja', msg=msg)

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('loggedin', None)
    session.pop('type', None)
    return redirect(('validelogout'))

@app.route('/rdv_pris')
def rdv_pris():
    if 'loggedin' in session and session.get('type') == 'formateur':
        return render_template('rdv_pris.jinja')
    else:
        flash('Role incorrect')
        return redirect((''))

@app.route('/rdv')
def rdv():
    if 'loggedin' in session and session.get('type') == 'eleve':
        with db_session:
            formateurs = Formateur.select()[:]
            formations = Formation.select()[:]
        return render_template('rdv.jinja', formateurs=formateurs, formations=formations)
    else:
        flash('Role incorrect')
        return redirect((''))
    

@app.route('/prendre_rdv_form', methods=['POST'])
def prendre_rdv_form():
    nom = request.form.get('nom')
    prenom = request.form.get('prenom')
    email = request.form.get('email')
    formateur_id = request.form.get('formateur')
    formation_id = request.form.get('formation')
    date_str = request.form.get('date')
    heure_str = request.form.get('heure')
    minute_str = request.form.get('minute')
    duree = request.form.get('durer')
    telephone = request.form.get('telephone')

    # Ajout de messages de débogage
    missing_fields = []
    for field_name, field_value in [('nom', nom), ('prenom', prenom), ('email', email), ('formateur_id', formateur_id),
                                    ('formation_id', formation_id), ('date', date_str), ('heure', heure_str), ('minute', minute_str),
                                    ('duree', duree), ('telephone', telephone)]:
        if not field_value:
            missing_fields.append(field_name)
    
    if missing_fields:
        flash(f'Veuillez remplir tous les champs : {", ".join(missing_fields)}')
        return redirect(request.referrer)
    
    datetime_str = f"{date_str} {heure_str}:{minute_str}:00"
    try:
        date_time = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')
        date_only = datetime.strptime(date_str, '%Y-%m-%d').date()  # Extract the date part only
    except ValueError:
        flash('Date ou heure incorrecte.')
        return redirect(request.referrer)
    
    with db_session:
        formateur = Formateur.get(id=formateur_id)
        formation = Formation.get(id=formation_id)
        RDV(
            Heure=date_time,
            Duree=int(duree),
            Date=date_only,  # Use the date part only
            Formateur=formateur,
            Formation=formation,
            Nom=nom,
            Prenom=prenom,
            Mail=email,
            Telephone=telephone
        )
    
    msg = Message(
        body=f"nom: {nom} \n email : {email} \n Formateur : {formateur.Prenom} {formateur.Nom} \n Date : {date_str} \n Heure : {heure_str}:{minute_str} \n Durée du rdv : {duree} minutes",
        recipients=['f.yoan19@gmail.com'],
        sender='yoancourspromeo@gmail.com',
        subject=f"Récapitulatif de la prise de rendez-vous de {prenom} {nom}"
    )
    
    mail.send(msg)
    return render_template('validation_prendrerdv_form.jinja')


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



@app.route('/register')
def register():
    return render_template('register.jinja')

if __name__ == '__main__':
    app.run(debug=True)
    
    


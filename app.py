from flask import Flask, render_template, request, redirect, session, make_response, flash, url_for
from pony.flask import Pony
from flask_mail import Mail, Message
from pony.orm import *
from datetime import datetime, date
from werkzeug.security import check_password_hash
import os
from dotenv import load_dotenv


load_dotenv()

app = Flask(__name__)
app.config.update(dict(
    SECRET_KEY=os.getenv('SECRET_KEY')
))

app.config.update(
    MAIL_SERVER=os.getenv('MAIL_SERVER'),
    MAIL_PORT=os.getenv('MAIL_PORT'),
    MAIL_USE_SSL=os.getenv('MAIL_USE_SSL'),
    MAIL_USERNAME=os.getenv('MAIL_USERNAME'),
    MAIL_PASSWORD=os.getenv('MAIL_PASSWORD'),
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


db.bind(provider=os.getenv('DB_PROVIDER'), host=os.getenv('DB_HOST'), user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'), database=os.getenv('DB_DATABASE'))
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
            user = Formateur.get(username=username)
            if user and check_password_hash(user.mdp, mdp):
                session['loggedin'] = True
                session['id'] = user.id
                session['type'] = 'formateur'
                return make_response(redirect('validelogin'))
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
            user = Eleve.get(username=username)
            if user and check_password_hash(user.mdp, mdp):
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
        with db_session:
            formateur_id = session['id']
            formateur = Formateur.get(id=formateur_id)
            rdvs = RDV.select(lambda r: r.Formateur.id == formateur_id)[:]
        return render_template('rdv_pris.jinja', rdvs=rdvs, formateur=formateur)
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
            Date=date_only,  
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

@app.route('/delete_rdv/<int:rdv_id>', methods=['POST'])
def delete_rdv(rdv_id):
    if 'loggedin' in session and session.get('type') == 'formateur':
        with db_session:
            rdv = RDV.get(id=rdv_id)
            if rdv and rdv.Formateur.id == session['id']:
                msg = Message(
                    subject="Annulation du rendez-vous",
                    sender="yoancourspromeo@gmail.com",
                    recipients=[rdv.Mail],
                    body=f"""Bonjour {rdv.Prenom} {rdv.Nom},

Votre rendez-vous avec le formateur {rdv.Formateur.Prenom} {rdv.Formateur.Nom} prévu le {rdv.Date.strftime('%Y-%m-%d')} à {rdv.Heure.strftime('%H:%M')} a été annulé.

Cordialement,
Proméo Formation"""
                )
                mail.send(msg)
                
                rdv.delete()
                commit()
                flash('Rendez-vous supprimé avec succès.')
                
                return redirect(url_for('rdv_pris'))
            else:
                flash('Action non autorisée.')
        return redirect(url_for('index'))
    else:
        flash('Role incorrect')
        return redirect(url_for('index'))

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
    
    


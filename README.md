La bdd est présente dans les fichiers

# Application Web Proméo Formation

Cette application web est celle du projet de M.Delpeche

## Fonctionnalités

### 1. Connexion Élève et Formateur

L'application fournit des routes de connexion distinctes pour les élèves et les formateurs, assurant une gestion de session appropriée et un contrôle d'accès basé sur le type d'utilisateur.

### 2. Prise de RDV

- **Restriction Graphique pour les Dates Passées** : Le sélecteur de date pour la planification d'un rendez-vous (RDV) ne permet pas aux utilisateurs de sélectionner une date passée, garantissant que tous les rendez-vous sont fixés pour des dates futures uniquement.
- **Formulaire Prérempli Basé sur la Session** : Lors de la planification d'un rendez-vous, le formulaire est prérempli avec les détails de l'utilisateur connecté (nom, email), et les formateurs et formations disponibles sont dynamiquement remplis à partir de la base de données.

### 3. Notification par Email

- **Création de Rendez-vous** : Lorsqu'un rendez-vous est planifié avec succès, un email de confirmation est envoyé à l'utilisateur.
- **Suppression de Rendez-vous** : Si un rendez-vous est supprimé, une notification par email est envoyée à l'utilisateur pour l'informer de l'annulation.

### 4. Contrôle d'Accès

Les URLs sensibles de l'application nécessitent une session valide pour y accéder. Les utilisateurs non autorisés sont redirigés, et des messages appropriés leur sont affichés pour les informer des restrictions d'accès.

### 5. Menus Dynamiques

Les menus de navigation de l'application sont mis à jour dynamiquement en fonction de l'état de la session :
- **Utilisateurs Connectés** : Un message de bienvenue personnalisé et les liens pertinents sont affichés.
- **Utilisateurs Déconnectés** : Les options de connexion pour les élèves et les formateurs sont fournies.



3. **Créer un Fichier .env** :
    Créez un fichier `.env` dans le répertoire racine et ajoutez les configurations suivantes :
    ```dotenv
    SECRET_KEY=votre_cle_secrete
    MAIL_SERVER=smtp.gmail.com
    MAIL_PORT=465
    MAIL_USE_SSL=True
    MAIL_USERNAME=votre_email@gmail.com
    MAIL_PASSWORD=votre_mot_de_passe_email
    DB_PROVIDER=mysql
    DB_HOST=localhost
    DB_USER=votre_utilisateur_db
    DB_PASSWORD=votre_mot_de_passe_db
    DB_DATABASE=nom_de_votre_db
    ```
    Le notre au cas ou: 

    ```
    SECRET_KEY=QQQQQQQQQQQQQQQQQQQQQ
    MAIL_SERVER=smtp.gmail.com
    MAIL_PORT=465
    MAIL_USE_SSL=True
    MAIL_USERNAME=yoancourspromeo@gmail.com
    MAIL_PASSWORD=oehfwyycnrbaxows
    DB_PROVIDER=mysql
    DB_HOST=localhost
    DB_USER=doodle
    DB_PASSWORD=doodle
    DB_DATABASE=doodle
    
```


## Utilisation

### Connexion en tant qu'Élève ou Formateur

- Rendez-vous sur `/loginEleve` pour vous connecter en tant qu'élève.
- Rendez-vous sur `/loginFormateur` pour vous connecter en tant que formateur.

### Planifier un Rendez-vous

- Après vous être connecté en tant qu'élève, naviguez vers la page de prise de rendez-vous.
- Remplissez les détails requis et sélectionnez une date future pour le rendez-vous.
- Soumettez le formulaire pour planifier le rendez-vous. Un email de confirmation sera envoyé à l'adresse email fournie.

### Gérer les Rendez-vous

- Les formateurs peuvent visualiser et gérer les rendez-vous planifiés.
- Pour supprimer un rendez-vous, les formateurs peuvent cliquer sur le bouton de suppression à côté du rendez-vous. Un email de notification sera envoyé à l'élève pour l'informer de l'annulation.

### Contrôle d'Accès

- Assurez-vous d'être connecté avec le rôle correct (élève ou formateur) pour accéder aux URLs spécifiques.
- Les tentatives d'accès non autorisé seront redirigées vers les pages appropriées avec un message flash indiquant la restriction d'accès.

### Menus Dynamiques

- Les menus de navigation seront mis à jour en fonction de l'état actuel de la session, affichant les options pertinentes et les messages personnalisés.

### Choses qui auraiet pu etre en plus

- Usage des centres 
- Deplacer le rdv impossible
- Usage des disponibilités
- Pas de CRUD



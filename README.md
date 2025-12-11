📚 Application de Gestion de Bibliothèque avec Quiz et Récompenses
🚀 Présentation du projet

Cette application web permet de gérer une bibliothèque en ligne avec un système innovant de quiz et de récompenses pour encourager la lecture.
Elle inclut la gestion des livres, la gestion des utilisateurs, les emprunts, les quiz, ainsi qu’un système de points et de badges.

Le projet a été initialement pensé en PHP/MySQL, mais ici la version est développée en Django (Python).

🛠️ Fonctionnalités principales

🔐 Authentification & Rôles

- Connexion et inscription des utilisateurs
- Système de rôles : Employés et Responsable IT
- Gestion sécurisée de l’accès selon les permissions

👥 Gestion des utilisateurs

- Ajouter / modifier / supprimer des utilisateurs
- Gestion du profil
- Consultation du score et de l’historique des quiz
- Suivi des emprunts

📚 Gestion des livres

- Ajouter un livre
- Modifier un livre
- Supprimer un livre
- Rechercher par titre, auteur, catégorie

📖 Emprunts & Retours

- Emprunter un livre
- Retourner un livre
- Historique des emprunts

❓ Système de quiz

- Création de quiz associés à des livres
- Participation des utilisateurs
- Correction automatique
- Calcul de score

🏆 Récompenses

- Attribution de points
- Badges / niveaux
- Système de progression utilisateur

📊 Tableau de bord administrateur

- Statistiques globales

🧰 Technologies utilisées:

⚙️ Backend / Framework

- Django
- Python 3

🎨 Frontend

- HTML / CSS
- Bootstrap via :
- django-crispy-forms
- crispy-bootstrap4 ou crispy-bootstrap5

🗄️ Base de données

- SQLite (par défaut Django)

📦 Packages installés
pip install django
pip install django-crispy-forms
pip install crispy-bootstrap4
pip install crispy-bootstrap5
pip install Pillow

🏗️ Installation et configuration
1️⃣ Cloner le projet
git clone <url-du-projet>
cd nom_du_dossier

2️⃣ Installer les dépendances
pip install -r requirements.txt

(ou installer manuellement les packages listés ci-dessus)

3️⃣ Lancer les migrations
python manage.py makemigrations
python manage.py migrate

4️⃣ Lancer le serveur
python manage.py runserver

➡️ Accès via : http://127.0.0.1:8000/

📂 Structure du projet (exemple)
📁 project/
├── 📁 app_users/ # gestion des utilisateurs
├── 📁 app_books/ # gestion des livres
├── 📁 app_quiz/ # système de quiz
├── 📁 static/ # fichiers css/js/images
├── 📁 templates/ # templates HTML
├── manage.py
└── README.md

📝 Fonctionnement du système de récompenses :
Action Points obtenus
Quiz réussi +10 pts

Niveau atteint Badge automatiquement attribué

👤 Auteur
Projet réalisé dans le cadre d'un développement d’application web éducative pour la gestion d’une bibliothèque.

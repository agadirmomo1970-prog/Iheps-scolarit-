# IHEPS AGADIR — Application de Scolarité

Application web de gestion de la scolarité pour **IHEPS AGADIR**, entièrement en français et utilisable sur ordinateur, tablette et mobile.

Elle couvre la gestion des filières de l'institut, des étudiants et des professeurs, les emplois du temps hebdomadaires, les appels et présences, le suivi des heures, le pointage entrée/sortie et les remarques confidentielles.

---

## 1. Fonctionnalités

### Responsable de la Scolarité (administrateur)

- Tableau de bord : effectifs, séances du jour, taux de présence, remarques non lues, heures.
- Étudiants : création, modification, suppression, fiche détaillée, filtres par filière, niveau, année et statut, export CSV.
- Professeurs : comptes individuels, identifiants, mots de passe, spécialité, heures contractuelles, activation/désactivation.
- Filières et niveaux : filières personnalisables, niveaux, couleurs et ordre d'affichage.
- Matières : catalogue par filière, niveau facultatif, volume horaire.
- Emploi du temps : grille hebdomadaire par filière et niveau, création/modification/suppression de créneaux, détection des conflits (professeur, salle, classe), duplication de la semaine précédente, impression/PDF, export PowerPoint `.pptx`.
- Présences : séances par date, professeur, filière et état ; fiche d'appel avec statuts **Présent / Absent / Retard / Excusé**, observations, validation des heures.
- Suivi des heures : contrat, heures planifiées, heures effectuées, solde, progression, détail par mois et par séance.
- Pointage : registre d'entrée/sortie des professeurs, ajout et correction manuels.
- Remarques confidentielles : lecture, marquage lu/non lu, suppression, filtres.
- Paramètres : profil du responsable (nom, genre M./Mme, identifiant), informations de l'établissement, année académique, mot de passe.

### Professeur

- Tableau de bord personnel : cours du jour, prochaines séances, heures, pointage, assiduité.
- Emploi du temps personnel par semaine.
- Séances et appels : appel des cours passés ou du jour, soumission des heures à la scolarité, historique.
- Pointage entrée/sortie en un clic, note de journée.
- Remarques confidentielles : rédaction pour un étudiant, suivi de lecture, retrait possible tant que la scolarité ne les a pas lues.
- Profil : coordonnées et changement de mot de passe.

---

## 2. Stack technique

| Élément | Choix |
|---|---|
| Framework | Flask 3.1 |
| ORM | Flask-SQLAlchemy 3.1 |
| Authentification | Flask-Login, mots de passe hachés |
| Base locale | SQLite (`instance/iheps.db`) |
| Base production | PostgreSQL (`DATABASE_URL`) |
| Serveur production | Gunicorn |
| Export PowerPoint | python-pptx |
| Frontend | HTML/Jinja, CSS et JavaScript natifs, aucune dépendance CDN |

Sécurité incluse : protection CSRF sur tous les formulaires, cookies `HttpOnly` / `SameSite=Lax`, en-têtes `X-Content-Type-Options`, `X-Frame-Options`, `Referrer-Policy`, `Permissions-Policy`, décorateurs de rôle et validation serveur.

---

## 3. Installation locale

Prérequis : **Python 3.11 ou supérieur**.

```powershell
# 1. Se placer dans le dossier du projet
cd "C:\Users\HP\OneDrive\Bureau\Scolarité"

# 2. Créer et activer un environnement virtuel
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# 3. Installer les dépendances
pip install -r requirements.txt

# 4. Créer la configuration locale
Copy-Item .env.example .env
# Générez SECRET_KEY :
#   python -c "import secrets; print(secrets.token_hex(32))"
# puis collez la valeur dans .env (ADMIN_PASSWORD peut rester vide en local).

# 5. Créer la base et le compte administrateur
python seed.py

# 6. Démarrer le serveur
python run.py
```

L'application est disponible sur **http://127.0.0.1:5000**.

### Première connexion

La base est créée vide : seuls les paramètres de l'établissement et le compte administrateur sont initialisés.

| Rôle | Identifiant | Mot de passe |
|---|---|---|
| Responsable de la Scolarité | `responsable` | défini par `ADMIN_PASSWORD`, sinon généré et affiché au premier `init-db` |

> Aucun mot de passe par défaut n'est codé en dur. En production, `ADMIN_PASSWORD` est **obligatoire**. En local, s'il est vide, un mot de passe aléatoire est généré et affiché une seule fois par `init-db`. Le changement de mot de passe est imposé à la première connexion. Les filières, niveaux, matières, professeurs et étudiants sont ensuite créés depuis l'interface.

### Commandes utiles

```powershell
# Créer les tables, les paramètres et le compte admin (idempotent)
flask --app wsgi init-db

# Réinitialisation complète (destructive) : base vide + admin
flask --app wsgi reset-db --force

# Vérification de santé
curl http://127.0.0.1:5000/sante
```

---

## 4. Variables d'environnement

| Variable | Description | Défaut |
|---|---|---|
| `SECRET_KEY` | Clé de signature des sessions. **Obligatoire**, 32 caractères minimum, jamais une valeur d'exemple. | aucune (démarrage refusé) |
| `DATABASE_URL` | URL SQLAlchemy. Vide = SQLite local. | SQLite `instance/iheps.db` |
| `SESSION_COOKIE_SECURE` | `1` pour forcer HTTPS sur les cookies (session et « rester connecté »). | `0` |
| `ADMIN_USERNAME` | Identifiant du compte admin initial. | `responsable` |
| `ADMIN_PASSWORD` | Mot de passe du compte admin initial. **Obligatoire en production.** | généré en local |
| `HOST` / `PORT` | Écoute du serveur de développement. | `127.0.0.1` / `5000` |
| `FLASK_DEBUG` | Mode debug Flask. Doit rester `0` hors développement. | `0` |

> `DATABASE_URL` accepte les formats Render/Heroku `postgres://` et `postgresql://` : ils sont automatiquement convertis en `postgresql+psycopg://`.

---

## 5. Déploiement

### 5.1 Render (recommandé)

Le fichier `render.yaml` crée automatiquement le service web et la base PostgreSQL.

1. Poussez le projet sur un dépôt GitHub/GitLab.
2. Sur Render : **New → Blueprint**, sélectionnez le dépôt.
3. Render lit `render.yaml`, crée `iheps-db` et le service `iheps-scolarite`.
4. Renseignez `ADMIN_PASSWORD` (variable secrète) dans le tableau de bord Render.
5. Au premier démarrage, `flask --app wsgi init-db` crée les tables, les paramètres et le compte administrateur.
6. Ouvrez l'URL du service et connectez-vous avec `responsable` / le mot de passe choisi. Le changement de mot de passe est imposé à la première connexion.

> En production, gardez `SESSION_COOKIE_SECURE=1`.

### 5.2 PythonAnywhere

1. Téléversez le projet (ou clonez le dépôt) dans `/home/<utilisateur>/iheps`.
2. Créez un virtualenv et installez `requirements.txt`.
3. Créez une base MySQL/PostgreSQL ou utilisez SQLite (moins recommandé en production).
4. Dans l'onglet **Web**, créez une application Flask :
   - **Source code** : `/home/<utilisateur>/iheps`
   - **Working directory** : `/home/<utilisateur>/iheps`
   - **WSGI configuration file** : remplacez son contenu par :

```python
import sys
path = "/home/<utilisateur>/iheps"
if path not in sys.path:
    sys.path.insert(0, path)

from wsgi import app as application
```

5. Ajoutez les variables d'environnement (`SECRET_KEY`, `DATABASE_URL`, `ADMIN_PASSWORD`, `SESSION_COOKIE_SECURE=1`).
6. Dans un **Bash console** :

```bash
cd ~/iheps
source .venv/bin/activate
flask --app wsgi init-db
```

7. Rechargez l'application web.

### 5.3 VPS Linux (Ubuntu/Debian) avec Gunicorn + Nginx

```bash
sudo apt update
sudo apt install -y python3-venv python3-pip nginx postgresql

cd /var/www/iheps
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

cp .env.example .env
nano .env   # SECRET_KEY, DATABASE_URL, SESSION_COOKIE_SECURE=1, ADMIN_PASSWORD

flask --app wsgi init-db
```

Service systemd `/etc/systemd/system/iheps.service` :

```ini
[Unit]
Description=IHEPS AGADIR Scolarité
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/iheps
EnvironmentFile=/var/www/iheps/.env
ExecStart=/var/www/iheps/.venv/bin/gunicorn wsgi:app --bind 127.0.0.1:8000 --workers 3 --timeout 120
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now iheps
```

Configuration Nginx `/etc/nginx/sites-available/iheps` :

```nginx
server {
    listen 80;
    server_name scolarite.iheps-agadir.ma;

    client_max_body_size 10M;

    location /static/ {
        alias /var/www/iheps/app/static/;
        expires 7d;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

```bash
sudo ln -s /etc/nginx/sites-available/iheps /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx
```

Activez HTTPS avec Certbot :

```bash
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d scolarite.iheps-agadir.ma
```

---

## 6. Organisation du projet

```text
Scolarité/
├── app/
│   ├── __init__.py          # Fabrique Flask, contexte, filtres, erreurs, CLI
│   ├── admin.py             # Espace Responsable de la Scolarité
│   ├── professeur.py        # Espace professeur
│   ├── auth.py              # Connexion / déconnexion
│   ├── models.py            # Modèles SQLAlchemy
│   ├── seed.py              # Paramètres et compte administrateur
│   ├── utils.py             # Dates FR, heures, CSRF, décorateurs de rôle
│   ├── static/
│   │   ├── css/style.css    # Design responsive et impression
│   │   ├── js/app.js        # Menu, filtres, appels, confirmations
│   │   └── icons.svg        # Sprite d'icônes SVG
│   └── templates/
│       ├── base.html
│       ├── _macros.html
│       ├── auth/            # Connexion
│       ├── admin/           # Interface administratives
│       ├── professeur/      # Interface professeurs
│       └── partials/        # Grille d'emploi du temps, fiche d'appel
├── instance/iheps.db        # Base SQLite locale (non versionnée)
├── run.py                   # Serveur de développement
├── wsgi.py                  # Point d'entrée Gunicorn / PythonAnywhere
├── seed.py                  # Initialisation (admin + paramètres)
├── requirements.txt
├── Procfile
├── render.yaml
└── .env.example
```

### Modèle de données principal

- `Utilisateur` : administrateur ou professeur, rôle, identifiant, mot de passe haché, contrat.
- `Filiere` → `Niveau`, `Matiere`, `Etudiant`.
- `Etudiant` : matricule, identité, contacts, filière, niveau, année, statut.
- `Creneau` : emploi du temps d'une **semaine précise** (`semaine` = lundi), jour, horaires, salle.
- `Seance` : occurrence datée d'un créneau (ou séance exceptionnelle), statut brouillon/validée.
- `Presence` : statut et observation par étudiant et par séance.
- `Pointage` : entrée/sortie d'un professeur pour une journée.
- `Remarque` : observation confidentielle d'un professeur, indicateur de lecture.
- `Parametre` : établissement, année académique et réglages.

---

## 7. Sauvegarde et maintenance

### SQLite

```powershell
Copy-Item instance\iheps.db "sauvegarde_iheps_$(Get-Date -Format yyyyMMdd).db"
```

### PostgreSQL

```bash
pg_dump "$DATABASE_URL" > sauvegarde_iheps_$(date +%Y%m%d).sql
```

Restauration :

```bash
psql "$DATABASE_URL" < sauvegarde_iheps_20260101.sql
```

### Mise à jour de l'application

```bash
git pull
source .venv/bin/activate
pip install -r requirements.txt
flask --app wsgi init-db
sudo systemctl restart iheps
```

`init-db` est idempotent : il ne duplique ni les paramètres ni le compte administrateur.

---

## 8. Checklist avant mise en ligne

- [ ] `SECRET_KEY` aléatoire et long (64 caractères hexadécimaux), différente de toute valeur d'exemple.
- [ ] `ADMIN_PASSWORD` défini comme variable secrète (obligatoire en production).
- [ ] `FLASK_DEBUG=0`.
- [ ] `DATABASE_URL` PostgreSQL renseignée.
- [ ] `SESSION_COOKIE_SECURE=1` et HTTPS actif.
- [ ] Mot de passe administrateur changé depuis **Paramètres → Sécurité**.
- [ ] Base vide de toute donnée de test ou de démonstration.
- [ ] Sauvegarde automatique de la base planifiée.
- [ ] Test d'impression / export PDF et PowerPoint.
- [ ] Vérification des accès : un professeur ne doit jamais pouvoir ouvrir `/admin/...`.

---

## 9. Notes d'utilisation

- **Semaine** : chaque créneau appartient à une semaine identifiée par son lundi. Modifier une semaine ne modifie pas les autres. Le bouton « Dupliquer la semaine préc. » recopie les créneaux utiles.
- **Heures effectuées** : le professeur valide l'appel, puis la scolarité **confirme les heures**. Seules les séances dont les heures sont confirmées sont comptabilisées. Le solde = heures contractuelles − heures effectuées.
- **Pointage** : un seul relevé par professeur et par jour. La scolarité peut corriger un oubli.
- **Remarques** : le professeur ne voit que ses propres remarques ; l'administration voit tout. Une remarque lue ne peut plus être supprimée par le professeur.
- **Impression** : les pages d'emploi du temps et les fiches d'appel disposent d'une mise en page dédiée (A4 paysage pour les grilles).

---

## 10. Licence et contact

Application interne développée pour **IHEPS AGADIR — Institut des Hautes Études Paramédicales**, Agadir, Maroc.

Pour toute question technique : `scolarite@iheps-agadir.ma`.

from app import create_app
from app.models import db, User
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    # Vérifier si l'admin existe déjà
    existing = User.query.filter_by(email="papaseydou.wane@unchk.edu.sn").first()
    if existing:
        print("❌ Cet utilisateur existe déjà.")
    else:
        admin = User(
            nom="WANE",
            prenom="Papa Seydou",
            email="papaseydou.wane@unchk.edu.sn",
            mot_de_passe=generate_password_hash("Qqmkl@8345", method='pbkdf2:sha256'),
            is_admin=True
)

        db.session.add(admin)
        db.session.commit()
        print("✅ Compte administrateur créé avec succès.")

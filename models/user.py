from flask_sqlalchemy import SQLAlchemy

# Create DB instance
db = SQLAlchemy()


class User(db.Model):
    # Fields
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(64), nullable=False)
    age = db.Column(db.Integer, nullable=False)

    # toString
    def toString(self):
        print(f"{self.user_id}: {self.first_name} ({self.age})")
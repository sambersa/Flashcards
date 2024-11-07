from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flashcards.db'  # Use your preferred database URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Set the secret key for session management
app.secret_key = 'sbersa'  # Replace with a unique secret key

db = SQLAlchemy(app)

class Quiz(db.Model):
    __tablename__ = 'quizzes'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    flashcards = db.relationship('Flashcard', backref='quiz', lazy=True, cascade="all, delete-orphan")

class Flashcard(db.Model):
    __tablename__ = 'flashcards'
    id = db.Column(db.Integer, primary_key=True)
    term = db.Column(db.String(100), nullable=False)
    definition = db.Column(db.String(255), nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id', ondelete='CASCADE'), nullable=False)

# Create the database tables
with app.app_context():
    db.create_all()  # Create tables if they don't exist

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/my_flashcards', methods=['GET'])
def my_flashcards():
    quizzes = Quiz.query.all()  # Fetch all quizzes from the database
    return render_template('my_flashcards.html', quizzes=quizzes)

@app.route('/create_quiz', methods=['GET', 'POST'])
def create_quiz():
    if request.method == 'POST':
        title = request.form.get('title')
        new_quiz = Quiz(title=title)  # Create a new Quiz instance
        db.session.add(new_quiz)
        db.session.commit()
        return redirect(url_for('my_flashcards'))
    return render_template('create_quiz.html')

@app.route('/add_flashcards/<int:quiz_id>', methods=['GET', 'POST'])
def add_flashcards(quiz_id):
    if request.method == 'POST':
        term = request.form.get('term')
        definition = request.form.get('definition')
        new_flashcard = Flashcard(term=term, definition=definition, quiz_id=quiz_id)  # Create a new Flashcard instance
        db.session.add(new_flashcard)
        db.session.commit()
        return redirect(url_for('view_flashcards', quiz_id=quiz_id))
    return render_template('add_flashcards.html', quiz_id=quiz_id)

@app.route('/view_flashcards/<int:quiz_id>', methods=['GET'])
def view_flashcards(quiz_id):
    quiz = Quiz.query.get(quiz_id)
    if quiz is None:
        flash('Quiz not found', 'error')  # Flash a message if quiz not found
        return redirect(url_for('my_flashcards'))

    flashcards = Flashcard.query.filter_by(quiz_id=quiz.id).all()  # Fetch associated flashcards
    return render_template('view_flashcards.html', quiz=quiz, flashcards=flashcards)

@app.route('/delete_quiz/<int:quiz_id>', methods=['POST'])
def delete_quiz(quiz_id):
    quiz = Quiz.query.get(quiz_id)
    if quiz:
        db.session.delete(quiz)  # Delete the quiz and its associated flashcards
        db.session.commit()
        flash('Quiz and associated flashcards deleted successfully.')
    else:
        flash('Quiz not found.')
    return redirect(url_for('my_flashcards'))

if __name__ == '__main__':
    app.run(debug=True)

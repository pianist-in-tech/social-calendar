import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

#Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app) #Allow frontend to make requests

#Use the DATABASE_URL from .env
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv('DATABASE_URL')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(255), nullable=False)
    date = db.Column(db.String(10), nullable=False)
    time = db.Column(db.String(5), nullable=False)

with app.app_context(): #ensures that Flask knows which application it should use while running db.create_all().
    db.create_all()

@app.route("/posts", methods=['GET'])
def get_posts():
    posts = Post.query.all()
    return jsonify([{'id': p.id, 'content': p.content, 'date': p.date, 'time': p.time} for p in posts])

@app.route('/posts', methods=['POST'])
def add_post():
    data = request.json
    new_post = Post(content=data['content'], date=data['date'], time=data['time'])
    db.session.add(new_post)
    db.session.commit()
    return jsonify({"message": "Post added!"}), 201

@app.route('/posts/,<int:id>', methods=['DELETE'])
def delete_post(id):
    post = Post.query.get(id)
    if post:
        db.session.delete(post)
        db.session.commit()
        return jsonify({'message': "Post deleted!"})
    return jsonify({'error': "Post not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)

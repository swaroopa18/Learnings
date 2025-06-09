from flask import Flask, request, jsonify, redirect
from flask_cors import CORS
from sqlalchemy import create_engine, Column, String, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import shortuuid
import os
from dotenv import load_dotenv
from datetime import datetime
import re

load_dotenv()

app = Flask(__name__)
# Configure CORS to allow requests from the frontend
CORS(app, resources={
    r"/*": {
        "origins": ["http://localhost:3000"],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

# Database configuration
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///urls.db')
engine = create_engine(DATABASE_URL)
Base = declarative_base()
Session = sessionmaker(bind=engine)

class URL(Base):
    __tablename__ = 'urls'
    
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    original_url = Column(String, nullable=False)
    short_code = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

# Drop all tables and recreate them
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

def generate_short_code():
    # Generate a 6-character alphanumeric code
    while True:
        code = shortuuid.uuid()[:6]
        if re.match("^[a-zA-Z0-9]{6}$", code):
            return code

@app.route('/api/shorturls', methods=['POST'])
def create_short_url():
    data = request.get_json()
    title = data.get('title')
    original_url = data.get('originalUrl')
    
    if not title or not original_url:
        return jsonify({'error': 'Title and originalUrl are required'}), 400
    
    session = Session()
    
    # Check if URL already exists
    existing_url = session.query(URL).filter_by(original_url=original_url).first()
    if existing_url:
        return jsonify({
            'shortUrl': f'http://localhost:8080/s/{existing_url.short_code}'
        })
    
    # Generate short code
    short_code = generate_short_code()
    
    # Create new URL entry
    new_url = URL(
        title=title,
        original_url=original_url,
        short_code=short_code
    )
    session.add(new_url)
    session.commit()
    
    return jsonify({
        'shortUrl': f'http://localhost:8080/s/{short_code}'
    })

@app.route('/api/shorturls', methods=['GET'])
def get_all_short_urls():
    session = Session()
    urls = session.query(URL).order_by(URL.created_at.desc()).all()
    
    return jsonify([{
        'title': url.title,
        'shortUrl': f'http://localhost:8080/s/{url.short_code}'
    } for url in urls])

@app.route('/s/<short_code>', methods=['GET'])
def redirect_to_url(short_code):
    session = Session()
    url_entry = session.query(URL).filter_by(short_code=short_code).first()
    
    if url_entry:
        return redirect(url_entry.original_url, code=301)
    return jsonify({'error': 'URL not found'}), 404

if __name__ == '__main__':
    app.run(debug=True, port=8080) 
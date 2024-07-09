from flask import Flask, request, jsonify, render_template
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database setup
DATABASE_URL = 'sqlite:///vacan.db'
engine = create_engine(DATABASE_URL)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

# Define the Job model
class Job(Base):
    __tablename__ = 'vacan'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    url = Column(String)
    company = Column(String)
    description = Column(Text)

class JobResult(Base):
    __tablename__ = 'vacan_result'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    url = Column(String)
    company = Column(String)
    description = Column(Text)

Base.metadata.create_all(engine)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['GET'])
def search():
    title = request.args.get('title', '')
    company = request.args.get('company', '')

    results = session.query(Job).filter(Job.title.ilike(f'%{title}%'), Job.company.ilike(f'%{company}%')).all()

    jobs = []
    for job in results:
        jobs.append({
            'id': job.id,
            'title': job.title,
            'url': job.url,
            'company': job.company,
            'description': job.description
        })
        # Сохранение результата в таблицу vacan_result
        result = JobResult(title=job.title, url=job.url, company=job.company, description=job.description)
        session.add(result)

    session.commit()
    return jsonify(jobs)

if __name__ == '__main__':
    app.run(debug=True)

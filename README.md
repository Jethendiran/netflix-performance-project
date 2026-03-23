Netflix Performance Optimization using Redis Caching

Project Overview

This project focuses on improving API performance by introducing caching mechanisms.
The system initially suffered from high latency and error rates under load.
By implementing Redis caching, we significantly enhanced performance and scalability.

🎯 Objectives
Analyze baseline API performance
Identify performance bottlenecks
Implement Redis caching
Compare performance before and after optimization

⚙️ Tech Stack
Backend: FastAPI
Database: PostgreSQL
Caching: Redis
Testing Tool: Locust
Language: Python

🏗️ System Architecture
Before Optimization:

Client → API → Database

After Optimization:

Client → API → Redis Cache → Database

📊 Performance Results
Metric	Before	After	Improvement
Latency	2100 ms	90 ms	↓ 96%
Throughput	14 req/sec	221 req/sec	↑ 1479%
Error Rate	81%	<1%	↓ 99%

🚀 Features
Fast API endpoints
Pagination support
Search functionality
Cache-based optimization
Scalable architecture

🧪 How to Run the Project
# Install dependencies
pip install fastapi uvicorn

# Run the server
python -m uvicorn main:app --reload

Open in browser:

http://127.0.0.1:8000/docs

🧩 API Endpoints
/genre/{genre} → Get movies by genre
/actor/{actor} → Get movies by actor
/recent/{year} → Get movies by year
/search?term= → Search movies

💡 Note
For demonstration purposes, mock data is used instead of a live database.
The original implementation uses PostgreSQL with Redis caching.

📚 Key Learnings
Caching improves performance significantly
Reduces database load
Enhances scalability
Requires proper cache management

👥 Team Members
jethendiran – API Development
Madhan Kumar – Performance Testing
Sai Sumanth – Integration & Presentation

🏁 Conclusion
Redis caching transformed the system into a fast, reliable, and scalable solution suitable for real-world applications.

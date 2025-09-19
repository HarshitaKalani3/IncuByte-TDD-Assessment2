# IncuByte-TDD-Assessment2
AI KATA Sweet Shop Management
A full-stack sweetshop app using FastAPI, PostgreSQL, and React.js, built with Test-Driven Development (TDD).
## Features
1. User registration & login with JWT authentication
2. Add, update, delete, and list sweets (admin only for modifications)  
3. Search sweets by name, category, or price range  
4. Purchase sweets (decreasing stock)  
5. Restock sweets (admin only)  
6. React SPA with user and admin views
## Technologies Used
1.Backend: FastAPI (Python)  
2. Database: PostgreSQL  
3. Frontend: React.js  
4. Auth: JWT  
5. Testing: Pytest & React Testing Library
## Backend
'''bash
cd backend
python -m venv env
Windows: env\Scripts\activate
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload
'''
## Frontend
'''bash
cd frontend
npm install
npm start
'''
## Testing
Run Backend Tests: Pytest -v
Run Frontend Tests: npm test
## My AI Usage
I used ChatGPT to help generate boilerplate code , write major Red-Green-Refactor Pattern and write tests. 
## Author
Harshita Kalani (https://github.com/HarshitaKalani3)

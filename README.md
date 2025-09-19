# IncuByte-TDD-Assessment2
## AI KATA Sweet Shop Management
This project is a basic full-stack sweetshop management system using FastAPI in Python, PostgreSQL as database, and React.js for frontend, built with Test-Driven Development (TDD). It allows users to register, login, search, purchase and for admins to manage inventory.
## Features
1. User registration & login with JWT authentication
2. Add, update, delete, and list sweets (admin only for modifications)  
3. Search sweets by name, category, or price range  
4. Purchase sweets (decreasing stock)  
5. Restock sweets (admin only)  
6. React SPA with user and admin views
## Technologies Used
1. Backend: FastAPI (Python)  
2. Database: PostgreSQL  
3. Frontend: React.js  
4. Auth: JWT  
5. Testing: Pytest & React Testing Library
6. Editor: Visual Studio Code
## Clone Repo
git clone https://github.com/HarshitaKalani3/IncuByte-TDD-Assessment2.git
cd IncuByte-TDD-Assessment2
## Backend SetUp Run
'''bash
cd backend
python -m venv env
Windows: env\Scripts\activate
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload
'''
## Frontend SetUp Run
'''bash
cd frontend
npm install
npm start
'''
## Testing
Run Backend Tests: Pytest -v
Run Frontend Tests: npm test
## My AI Usage
I used ChatGPT to help generate boilerplate code , write major Red-Green-Refactor Pattern, structuring API endpoints and write tests. I asked Chatgpt how to make even the boiler plate and basic commands to initialize like in vs code that I have used for my project which actually helped me to save time and settings of the above directory structure. I used it to actually solve all the errors of my code i.e. error handling. It helped me to reduce the amount of repetitive coding and it gave helpful suggestions in every step of my project.
## Screenshots
https://github.com/HarshitaKalani3/IncuByte-TDD-Assessment2/tree/main/Screenshots
## Author
Harshita Kalani (https://github.com/HarshitaKalani3)

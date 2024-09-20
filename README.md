# Watsonx.ai IBM hackathon 2024: <Project Name>

## Development
### How to run 
Run flask backend
```
git clone <project_url>
cd backend
pip install -r requirements.txt
python init_db.py #run sqlite db
python run.py
```
(Recommended) Use python virtual enviroment
For the backend dont forget to add you IBM watsonx API in CONSTANTS.py
```
g_cloud_apikey = ""
project_id = ''
```

Run react backend
```
cd frontend
npm install
npm start
```


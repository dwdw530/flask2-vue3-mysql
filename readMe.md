pip freeze > requirements.txt
venv\Scripts\python.exe -m pip install -r requirements.txt
sqlacodegen mysql+pymysql://root:root@localhost/hr_domain --outfile models/models.py
split_models.py

# Streamlit Heroku Template with Azure AD login

Prerequisites:

- [cookiecutter](https://github.com/cookiecutter/cookiecutter) CLI
- [pipenv](https://pipenv.pypa.io/en/latest/)
- A Heroku app
- A Microsoft web app as shown [here](https://learn.microsoft.com/en-us/azure/active-directory/develop/web-app-quickstart?tabs=windows&pivots=devlang-python)

The redirect URI will be the URI for streamlit when running locally (eg http://localhost:8501/) and the link to the app for prod (something in the format https://YOURAPPNAMEHERE.herokuapp.com/)

Have the tenant_id, client_id and client_secret at the ready when running this cookiecutter

Usage:

- Navigate to the directory where you wanna create the project folder. Run the following command and follow the prompt:
```bash
cookiecutter https://github.com/Artificial-Collective/cookiecutter-streamlit-heroku
```


- Head inside the folder and install the pipenv environment:
```bash
pipenv install
```

- Start the strealit app:
```bash
pipenv run streamlit run app.py
```

- DO NOT commit .env to version control

- To make CI/CD work, go to your [heroku account](https://dashboard.heroku.com/account) and create an API key. Then add HEROKU_API_TOKEN and HEROKU_API_KEY to your github repo secrets. Intstruction to add [here](https://docs.github.com/en/actions/security-guides/encrypted-secrets#creating-encrypted-secrets-for-a-repository)


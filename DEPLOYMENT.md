# Deployment

This project is split into:

- `frontend/` for Vercel
- the Django project root for PythonAnywhere

## PythonAnywhere backend

Set these environment variables in the PythonAnywhere WSGI file before the Django app loads:

```python
import os

os.environ['DJANGO_DEBUG'] = '0'
os.environ['DJANGO_SECRET_KEY'] = 'replace-this-with-a-long-secret-key'
os.environ['DJANGO_ALLOWED_HOSTS'] = 'yourusername.pythonanywhere.com'
os.environ['CORS_ALLOWED_ORIGINS'] = 'https://your-vercel-project.vercel.app'
```

Then run:

```bash
python manage.py migrate
python manage.py collectstatic
```

Your API endpoint will be:

```text
https://yourusername.pythonanywhere.com/api/register/
```

## Vercel frontend

In `frontend/config.js`, replace the local backend URL:

```js
API_BASE_URL: 'http://127.0.0.1:8000',
```

with your PythonAnywhere URL:

```js
API_BASE_URL: 'https://yourusername.pythonanywhere.com',
```

Deploy `frontend/` as the Vercel root directory.

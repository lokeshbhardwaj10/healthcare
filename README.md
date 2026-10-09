# Healthcare Backend (Django + DRF + PostgreSQL + JWT)

## Setup
```bash
python -m venv venv && source venv/bin/activate     # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env                                 # then edit values
createdb healthcare_db                               # or create it via psql / pgAdmin
python manage.py makemigrations accounts patients doctors mappings
python manage.py migrate
python manage.py runserver
```
Generate a secret key: `python -c "from django.core.management.utils import get_random_secret_key as g; print(g())"`

## Endpoints
All endpoints except register/login need the header `Authorization: Bearer <access_token>`.

| Method | URL | Description |
|---|---|---|
| POST | /api/auth/register/ | `{name, email, password}` |
| POST | /api/auth/login/ | `{email, password}` -> `access`, `refresh` |
| POST | /api/auth/token/refresh/ | `{refresh}` -> new `access` (bonus) |
| POST/GET | /api/patients/ | Create / list **own** patients |
| GET/PUT/DELETE | /api/patients/<id>/ | Own patients only (others -> 404) |
| POST/GET | /api/doctors/ | Create / list all doctors |
| GET/PUT/DELETE | /api/doctors/<id>/ | Anyone authenticated can read; only creator can edit/delete |
| POST | /api/mappings/ | `{patient, doctor}` |
| GET | /api/mappings/ | Mappings for your patients |
| GET | /api/mappings/<patient_id>/ | Doctors assigned to that patient |
| DELETE | /api/mappings/<id>/ | Remove a mapping by its id |

## Sample requests
```bash
curl -X POST localhost:8000/api/auth/register/ -H "Content-Type: application/json" \
  -d '{"name":"Alice","email":"alice@example.com","password":"StrongPass#123"}'

curl -X POST localhost:8000/api/auth/login/ -H "Content-Type: application/json" \
  -d '{"email":"alice@example.com","password":"StrongPass#123"}'

curl -X POST localhost:8000/api/patients/ -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"name":"John Doe","age":40,"gender":"M","phone":"9999999999","address":"Delhi","medical_history":"Diabetes"}'

curl -X POST localhost:8000/api/doctors/ -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"name":"Dr. Smith","email":"smith@hospital.com","specialization":"Cardiology","experience_years":12}'

curl -X POST localhost:8000/api/mappings/ -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"patient":1,"doctor":1}'
```

## Design notes
- Email is stored as the username, so login is by email + password.
- Patient data is scoped per user (queryset filtering), so one user can't see or touch another's patients.
- Mapping rules: you can only assign doctors to your own patients; duplicate pairs are rejected (DB unique constraint + serializer check).
- `GET /api/mappings/<patient_id>/` and `DELETE /api/mappings/<id>/` share one URL shape per the spec; the id means patient id for GET and mapping id for DELETE.
- Secrets/DB credentials come from `.env` (never commit it).

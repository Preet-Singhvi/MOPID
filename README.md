# Django DRF Event Booking Project

This is a minimal Django + DRF project implementing an event reservation system with concurrency-safe booking.

## Quickstart (local)
1. Create a virtualenv: `python -m venv venv && source venv/bin/activate`
2. Install: `pip install -r requirements.txt`
3. Run migrations: `python manage.py migrate`
4. Create a superuser (optional): `python manage.py createsuperuser`
5. Run: `python manage.py runserver`

## Tests
Run tests with: `python manage.py test`

## Notes on concurrency
The reservation endpoint uses an atomic conditional UPDATE to increment `seats_reserved` only when it's below `capacity` and wraps the update + reservation creation in a transaction so overbooking is prevented even under concurrency.

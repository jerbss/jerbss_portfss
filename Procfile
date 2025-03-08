web: mkdir -p staticfiles && python manage.py collectstatic --noinput && python manage.py migrate && gunicorn jerbss_portfss.wsgi:application --bind 0.0.0.0:$PORT
build: bash build.sh
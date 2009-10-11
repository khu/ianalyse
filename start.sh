python manage.py runserver &
echo $! > iAnalyse.pid
sleep 2
open http://localhost:8000

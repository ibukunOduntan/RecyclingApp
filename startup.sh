apt-get update && apt-get install -y libgl1-mesa-glx libgl1-mesa-dri

gunicorn --bind=0.0.0.0 --timeout 1800 application:application

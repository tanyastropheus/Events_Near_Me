# launch elasticsearch server and flask to start the event web app
sudo service elasticsearch start
python3 -m event_app.app

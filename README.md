# TheFoobarHome

This projects aims at providing the required tools to monitor my home's metrics such as electricity production and consumption, heating system, ....

# Install

This project has been tested with Python 3.9.2 and TimeScaleDB 14.

1. Install TimescaleDB by following this [procedure](db/README.md).

2. Install the required packages.
```bash
sudo apt install python3-pip python3-dev libpq-dev python3-venv
```
3. Create a python virtual environment in the project folder.
```bash
cd TheFoobarHome
python3 -m venv venv
```
4. Activate the virtual environment you just created.
```bash
source venv/bin/activate
```
5. Install the project's python requirements.
```bash
pip3 install -r requirements.txt
```

# Config

Create a configuratin file call `config.ini` in the project's folder using the following template:

```ini
[db]
#TimescaleDB connection pool minimum number of connections
min_conn = 1
#TimescaleDB connection pool maximum number of connections
max_conn = 5 
#TimescaleDB connection username
user = 
#TimescaleDB connection password
password = 
#TimescaleDB hostname or IP address
host = 
#TimescaleDB port (5432 by default)
port = 5432
#TimescaleDB database name
database = 

[plenticore]
#Plenticore inverter hostname or IP address
host = 192.168.1.107
#Plenticore inverter owner's password
password = 
```

# How to run 

## As a python script
The main python module is `main.py` which can be run as any standard python script:
```bash
python3 main.py
```
## As a Linux `systemd` service
1. Copy the file `thefoobarhome.service` into `/etc/systemd/system/`
```bash
sudo cp thefoobarhome.service /etc/systemd/system/
```
2. Make sure the `User`, `WorkingDirectory` and `ExecStart` have the correct paths set. 
```ini
#The user the program will be run with
User=pi
#The project's root folder
WorkingDirectory=/home/pi/TheFoobarHome
#The python3 binary located in the virutal enviroment folder and the absolute path to the main.py script
ExecStart=/home/pi/TheFoobarHome/venv/bin/python3 /home/pi/TheFoobarHome/main.py
```
3. Start the service
```bash
sudo systemctl start thefoobarhome.service
```
4. You can check if the service is running properly
```bash
sudo systemctl status thefoobarhome.service
```
5. If you want to have the service automatically started on boot
```bash
sudo systemctl enable thefoobarhome.service
```
6. To stop the service
```bash
sudo systemctl stop thefoobarhome.service
```

# Acknowledgments
- [Hywan](https://github.com/Hywan) for the [LaMaisonVivante](https://github.com/Hywan/LaMaisonVivante) project and his knowledge sharing.
- [stegm](https://github.com/stegm) for the [pykoplenti](https://github.com/stegm/pykoplenti) project


# License

The license is [WTFPL](https://en.wikipedia.org/wiki/WTFPL).

```
       DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
                Version 2, December 2004

Copyright (C) 2022- Denis Moret

Everyone is permitted to copy and distribute verbatim or modified
copies of this license document, and changing it is allowed as long
as the name is changed.

           DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
  TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION

 0. You just DO WHAT THE FUCK YOU WANT TO.
```
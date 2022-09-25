# Database
TimescaleDB install procedure for **Raspberry Pi OS Lite 64-bit**

## Install [TimescaleDB](https://www.timescale.com/)

As `root`, add the PostgreSQL third party repository to get the latest PostgreSQL packages.
```bash
apt install gnupg postgresql-common apt-transport-https lsb-release wgets
```

Run the PostgreSQL repository setup script.
```bash
/usr/share/postgresql-common/pgdg/apt.postgresql.org.sh
```

Add the TimescaleDB third party repository.
```bash
echo "deb https://packagecloud.io/timescale/timescaledb/debian/ $(lsb_release -c -s) main" > /etc/apt/sources.list.d/timescaledb.list
```

Install Timescale GPG key.
```bash
wget --quiet -O - https://packagecloud.io/timescale/timescaledb/gpgkey | sudo sh -c "gpg --dearmor > /etc/apt/trusted.gpg.d/timescaledb.gpg"
```

Update your local repository list.
```bash
apt update
```

Install TimescaleDB.
```bash
apt install timescaledb-2-postgresql-14
```

Run `timescaledb-tune` script.
```bash
timescaledb-tune --quiet --yes
```

Install the `postgresql-client` package.
```bash
sudo apt-get install postgresql-client
```

Restart the TimescaleDB service.
```bash
systemctl restart postgresql
```

Connect to the PostgreSQL instance as the `postgres` superuser.
```bash
su postgres -c psql
```

At the `psql` prompt, create an empty database. Our database is called `the_foobar_home`
```sql
CREATE database the_foobar_home;
```

Connect to the database you just created.
```bash
\c example
```

Add the TimescaleDB extension.
```sql
CREATE EXTENSION IF NOT EXISTS timescaledb;
```

You can now connect to your database using this command.
```bash
su postgres -c 'psql -d the_foobar_home'
```


## References
https://docs.timescale.com/install/latest/self-hosted/installation-debian/
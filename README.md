# Spinup

This python3 script facilitates the creation and deletion of nginx virtual servers
and hosts file entries.

### Motivation

It is annoying to set up new virtual servers and hosts file entries by hand
every time I take on a new client.

## Install

### To install from pypi

```bash
sudo pip install spinup
```

### To install for development

```bash
git clone git@github.com:eatonphil/spinup
cd spinup
pyvenv .env
. .env/bin/activate
pip install -e ./
```

## Usage

### Create

This one-liner creates a new virtual host at `/etc/hosts/sites-enabled/mysite.com`
that forwards mysite.com to localhost:3000 and serves static files from ./static.
Additionally, this adds an entry in your hosts file so mysite.com points to
localhost.

The location of the nginx config file and the location of the hosts file are
both configurable either via command line args or a config file in your home
directory.

```bash
sudo spinup mysite.com 3000 ./static
```

### Delete

This one-line deletes the previously created config file and removes the entry
from the hosts file.

Note: a port argument is required because I can't figure out a good way to
make it optional dependent on the ["-d", "--delete"] flags existence.

```bash
sudo spinup mysite.com 3000 -d
```

## Args

* positional:
    1. domain_name: the domain name to create an entry and config file for
    2. port: the port that nginx should forward the domain to
    3. static_root [optional]: the directory to serve static files from
* flags:
    * -d, --delete: flag that deletes the site config and hosts entry
    * --nginx_conf_dir [default="/etc/nginx/sites-enabled/"]: the nginx config directory
    * --hosts_file [default="/etc/hosts"]: the hosts file location

## Config file

If you are on an unsupported system (Mac, FreeBSD, etc.) you can create a
~/.spinup.conf file to store your configurations. Here is an example of my
~/.spinup.conf file on FreeBSD:

```
[spinup]
nginx_conf_dir = /usr/local/etc/nginx/conf.d
hosts_file = /etc/hosts # Not necessary, just an example
```

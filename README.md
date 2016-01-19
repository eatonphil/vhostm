# vhostm (previously spinup)

This python3 script facilitates the creation and deletion of nginx virtual servers
and hosts file entries.

### Motivation

It is annoying to set up new virtual servers and hosts file entries by hand
every time I take on a new client.

## Install

### To install from pypi

```bash
sudo pip install vhostm
```

### To install for development

```bash
git clone git@github.com:eatonphil/vhostm
cd vhostm
pyvenv .env
. .env/bin/activate
pip install -e ./
```

## Usage

Vhostm differs slightly from spinup and provides a much more useful interface
for viewing existing vhosts.

### Setup

The following defaults are used:

"""json
{
    "nginx_conf_dir": "/etc/nginx/sites-enabled",
    "hosts_file": "/etc/hosts",
    "vhosts_file": "/etc/vhostm/vhosts.conf"
}
"""

To override any of these settings per user, copy the json with the settings
you wish to override into ~/.vhostm.conf and change the value of the key.

For instance, on FreeBSD, the config (~/.vhostm.conf) may look like this:

"""json
{
    "nginx_conf_dir": "/usr/local/etc/nginx/conf.d",
    "vhosts_file": "/usr/local/etc/vhostm/vhosts.conf"
}
"""

You may also override either of these per command by using the flags
(--nginx_conf_dir, --vhosts_file, --hosts_file).

### List

```bash
sudo vhostm list
```

### Create

This one-liner creates a new vhost at `/etc/nginx/sites-enabled/mysite.com`
that forwards mysite.com to localhost:3000 and serves static files from
./static. Additionally, this adds an entry in your hosts file so mysite.com
points to localhost.

```bash
sudo vhostm add -d mysite.com -p 3000 -s ./static
```

### Delete

This one-line deletes the previously created config file and removes the
entry from the hosts file.

```bash
sudo vhostm del -d mysite.com
```
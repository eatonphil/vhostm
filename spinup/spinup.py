#!/usr/bin/env python3

"""This script facilitates the creation and deletion of nginx virtual servers
and hosts file entries.
"""

import argparse
import configparser
import logging
import os
import subprocess
import sys

DESCRIPTION = """Spinup is a simple tool to create and destroy nginx virtual
servers."""

BASE_TEMPLATE = """
upstream {domain_name} {{
    server 127.0.0.1:{port};
}}

server {{
    listen 80;
    listen [::]:80;
    server_name {domain_name};

    location / {{
        proxy_set_header        Host $host;
        proxy_set_header        X-Real-IP $remote_addr;
        proxy_set_header        X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header        X-Forwarded-Proto $scheme;

        proxy_read_timeout  90;

        proxy_pass http://{domain_name};
    }}

    {static}
}}
"""

STATIC_TEMPLATE = """
    # Media: images, icons, video, audio, HTC
    location ~* \.(?:jpg|jpeg|gif|png|ico|cur|gz|svg|svgz|mp4|ogg|ogv|webm|htc|mst|otf|ttf|woff)$ {{
        root {static_root};
        # expires 1M;
        access_log off;
        add_header Cache-Control "public";
    }}

    # CSS and Javascript
    location ~* \.(?:css|js)$ {{
        root {static_root};
        # expires 1y;
        access_log off;
        add_header Cache-Control "public";
    }}
"""


def delete_config(nginx_conf_file):
    if os.path.isfile(nginx_conf_file):
        os.remove(nginx_conf_file)


def delete_hosts_entry(hosts_file, domain_name):
    f = open(hosts_file, "r")
    hosts_file_data = list(f)
    f.close()
    with open(hosts_file, "w") as f:
        for line in hosts_file_data:
            if domain_name not in line.split()[1:]:
                f.write(line)


def create_config(nginx_conf_file, args):
    if args["static_root"] is not None:
        args["static_root"] = os.path.abspath(args["static_root"])
        args["static"] = STATIC_TEMPLATE.format(static_root=args["static_root"])
    else:
        args["static"] = ""

    nginx_conf = BASE_TEMPLATE.format(**args)

    if os.path.isfile(nginx_conf_file):
        logging.error("Domain name already defined. (File {} exists.)"
                      "".format(nginx_conf_file))

    with open(nginx_conf_file, "w") as f:
        f.write(nginx_conf)


def add_hosts_entry(hosts_file, domain_name):
    with open(hosts_file, "a") as f:
        f.write("127.0.0.1\t{}".format(domain_name))


def main():
    """Use user config file in home directory if it exists. If it does not,
    default to sensible system defaults. Command line arguments override both.
    """

    if os.getuid() != 0:
        sys.exit("Must be run as root or sudoer")

    sudo_user = os.getenv("SUDO_USER")
    user_config = "/home/{}/.spinup.conf".format(sudo_user)
    if sudo_user == "root":
        user_config = "/root/.spinup.conf"

    nginx_conf_dir = None
    hosts_file = None

    if os.path.isfile(user_config):
        config = configparser.ConfigParser()
        config.read(user_config)
        config = config["spinup"]
        hosts_file = config.get("hosts_file")
        nginx_conf_dir = config.get("nginx_conf_dir")

    # Use system defaults
    if hosts_file is None:
        hosts_file = "/etc/hosts"

    if nginx_conf_dir is None:
        uname = os.uname()[0].lower()
        if uname == "linux":
            nginx_conf_dir = "/etc/nginx/sites-enabled"

    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument("--delete", "-d", action="store_true")
    parser.add_argument("domain_name")
    parser.add_argument("port", type=int)
    parser.add_argument("static_root", default=None, nargs="?")
    parser.add_argument("--nginx_conf_dir", type=str,
                        default=nginx_conf_dir)
    parser.add_argument("--hosts_file", type=str, default=hosts_file)
    args = parser.parse_args()

    if args.nginx_conf_dir is None and nginx_conf_dir is None:
        exit("System not supported by default, must specify --nginx_conf_dir"
             "and --hosts_file.")

    args.nginx_conf_dir = os.path.abspath(args.nginx_conf_dir)
    args.hosts_file = os.path.abspath(args.hosts_file)

    nginx_conf_file = os.path.join(args.nginx_conf_dir, args.domain_name)

    if args.delete:
        delete_config(nginx_conf_file)
        delete_hosts_entry(args.hosts_file, args.domain_name)
    else:
        create_config(nginx_conf_file, vars(args))
        add_hosts_entry(args.hosts_file, args.domain_name)

    assert(subprocess.call(["nginx", "-t"]) == 0)

    assert(subprocess.call(["service", "nginx", "reload"]) == 0)


if __name__ == "__main__":
    main()

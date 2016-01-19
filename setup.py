from setuptools import setup

setup(
    name="vhostm",
    packages=["vhostm"],
    version="0.1",
    description="Manage nginx virtual servers and hosts file entries.",
    author="Phil Eaton",
    author_email="me@eatonphil.com",
    url="https://github.com/eatonphil/vhostm",
    download_url="https://github.com/eatonphil/vhostm/tarball/0.1",
    keywords=["nginx", "virtual", "hosts"],
    install_requires=[
        "jinja2>=2.8"
    ],
    entry_points={
        "console_scripts": [
            "vhostm = vhostm.vhostm:main"
        ]
    }
)

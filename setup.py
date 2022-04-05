from setuptools import setup

setup(
    name="django-passwords",
    version=__import__("passwords").__version__,
    author="Donald Stufft",
    author_email="donald@e.vilgeni.us",
    description=("A Django reusable app that provides validators and a form "
                 "field that checks the strength of a password"),
    long_description=open("README.rst").read(),
    url="http://github.com/dstufft/django-passwords/",
    license="BSD",
    packages=[
        "passwords",
    ],
    include_package_data=True,
    install_requires=[
        "Django >= 2.2",
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Utilities",
        "Framework :: Django",
    ],
)

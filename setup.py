from setuptools import setup, find_packages

setup(
    name="atm_machine",
    version="0.1.0",
    description="Simple ATM Machine Simulation",
    long_description="This package provides a simple ATM machine simulation.",
    author="Your Name",
    author_email="gumusyigit101@gmail.com",
    packages=find_packages(where="atm_machine"),
    package_dir={"": "atm_machine"},
    install_requires=[
        "requests",
        "flask",
        "flask_cors",
        "customtkinter"
    ],
    python_requires=">=3.7",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)

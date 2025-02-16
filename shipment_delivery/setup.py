from setuptools import setup, find_packages

setup(
    name="shipment_delivery",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "temporalio",
    ],
) 
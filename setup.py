"""Setup for clickaware XBlock."""


import os

from setuptools import setup


def package_data(pkg, roots):
    """Generic function to find package_data.

    All of the files under each of the `roots` will be declared as package
    data for package `pkg`.

    """
    data = []
    for root in roots:
        for dirname, _, files in os.walk(os.path.join(pkg, root)):
            for fname in files:
                data.append(os.path.relpath(os.path.join(dirname, fname), pkg))

    return {pkg: data}


setup(
    name="clickaware-xblock",
    author="edSPIRIT",
    description="clickaware XBlock",
    version="0.1",
    license="MIT",
    packages=[
        "clickaware",
    ],
    install_requires=[
        "XBlock==1.6.2",
    ],
    entry_points={
        "xblock.v1": [
            "clickaware = clickaware:ClickAwareXBlock",
        ]
    },
    package_data=package_data(
        "clickaware", ["static", "public", "locale", "translations"]
    ),
)

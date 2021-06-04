from setuptools import setup

setup(
    name="phishpond",
    version="0.0.1",
    packages=["phishpond"],
    entry_points={"console_scripts": ["phishpond = phishpond.__main__:main"]},
)

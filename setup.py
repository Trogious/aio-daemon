import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="aio_daemon",  # Replace with your own username
    version="0.1",
    author="Trog",
    author_email="trog@swmud.net",
    description="Helper module for running async daemons.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Trogious/aio-daemon",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)

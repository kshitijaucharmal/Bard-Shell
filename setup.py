import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="geminishell",
    version="1.0.0",
    author="Kshitij Aucharmal",
    author_email="kshitijaucharmal21@gmail.com",
    description="A Python package for geminishell.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kshitijaucharmal/Gemini-Shell",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
)

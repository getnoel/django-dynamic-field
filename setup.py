import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="django-dynamic-field",
    version="0.0.1",
    author="Noel Puru",
    author_email="noel@noelcodes.com",
    description="Create dynamic fields from django admin.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/noelpuru/django-dynamic-field",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

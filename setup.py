import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sisense",
    version="0.0.18",
    author="Bluemetrics",
    author_email="equipe@bluemetrics.com.br",
    description="Sisense API interface in Python.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Bluemetrics/sisense",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
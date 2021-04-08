import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sckernel", # Replace with your own username
    version="0.1.1",
    author="Andrew Davis",
    author_email="andrewdavis33@gmail.com",
    description="A SuperCollider kernel for Jupyter Notebooks",
    long_description=long_description,
    url="https://github.com/andrewdavis33/sckernel",
    packages=setuptools.find_packages(),
    install_requires=[
        'jupyter_client', 'IPython', 'ipykernel'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)

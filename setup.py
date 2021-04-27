import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sckernel", # Replace with your own username
    version="0.3.2",
    author="Andrew Davis",
    author_email="andrewdavis33@gmail.com",
    description="A SuperCollider kernel for Jupyter Notebooks",
    long_description= long_description,
    long_description_content_type = "text/markdown",
    url="https://github.com/andrewdavis33/sckernel",
    install_requires=[
        'jupyter_client', 'IPython', 'ipykernel'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    python_requires='>=3.7',
    include_package_data=True,
)

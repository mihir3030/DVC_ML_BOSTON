from setuptools import setup

with open("README.md", "r", encoding="utf-8") as f:
    long_discription = f.read()


setup(
    name = 'src',
    version = '0.0.1',
    author = 'mihir3030',
    author_email='mihirdholakia777@gmail.com',
    description= 'simple DVC pipeline ',
    long_discription = long_discription,
    long_discription_content_type = "text/markdown",
    url = 'https://github.com/mihir3030/DVC_SIMPLE_MLOPS.git',
    packages=["src"],
    python_requires = ">=3.7",
    install_requires = [
        'dvc',
        'pandas',
        'scikit-learn'
    ]
)
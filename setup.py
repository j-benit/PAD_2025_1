from setuptools import setup, find_packages

setup(
    name="edu_pad",
    version="0.0.1",
    author="Jhon Benitez",
    author_email="jhon.benitez@est.iudigital.edu.co",
    description="ETL para análisis de datos de mercado libre",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "pandas",
        "openpyxl",
        "requests",
        "beautifulsoup4",
        "altair>=5.0.0",
        "streamlit>=1.28.0", 
        "tabulate",
    ],
)

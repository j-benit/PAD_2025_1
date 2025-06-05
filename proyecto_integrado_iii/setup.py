from setuptools import setup, find_packages

setup(
    name="edu_pad",
    version="0.0.1",
    author="Jhon Benitez",
    author_email="jhon.benitez@est.iudigital.edu.co",
    description="ETL para análisis de datos de mercado libre",
    py_modules=["actividad1", "actividad2", "actividad3"],
    install_requires=[
        "pandas",
        "openpyxl",
        "requests",
        "beautifulsoup4",
        "altair>=5.0.0",
        "streamlit>=1.28.0"
    ]
)
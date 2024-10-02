from setuptools import find_packages,setup

setup(
    name='mcqgenerator',
    version='0.0.1',
    author='Chhavi Dhiman',
    author_mail='dhimanchhavi5@gmail.com',
    install_requirements=["g4f","langchain","streamlit","python-dotenv","PyPDF2"],
    #finding local packages
    packages=find_packages()
)
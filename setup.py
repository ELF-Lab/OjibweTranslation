from setuptools import setup, find_packages

setup(
    name="ojibwe_translation",
    version="0.1.0",
    author="Minh Nguyen",
    packages=find_packages(),
    python_requires='>=3.12',
    install_requires=['pandas >= 2.2.3, <2.3', 
                      'pyinflect >= 0.5.1, < 0.6', 
                      'fst-runtime >= 0.1.0, < 0.2',
                      'numpy >= 1.26.4, < 2.0'
                      ],
    url="https://github.com/ELF-Lab/OjibweTranslation"    
)
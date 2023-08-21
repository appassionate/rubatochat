import setuptools

setuptools.setup(
    name="rubatochat",
    version="0.0.1",
    author="untitled",
    author_email="xk@fake.cn",
    description=" a llm chat demo based on fastapi for multi users",
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    python_requires='>=3.8',
    install_requires=[

  ],
    entry_points={
        'console_scripts': [
            'rubato=rubato.main:main']
        }
)

import setuptools

# with open('requirements.txt') as f:
#     requirements = f.read().splitlines()

setuptools.setup(
    name="chandra_bot",
    version="0.0.1",
    install_requires=[
        "aiohttp==3.9.3",
        "aiosignal==1.3.1",
        "asyncio==3.4.3",
        "attrs==23.2.0",
        "certifi==2024.2.2",
        "chardet==5.2.0",
        "charset-normalizer==3.3.2",
        "cssselect2==0.7.0",
        "freetype-py==2.4.0",
        "frozenlist==1.4.1",
        "idna==3.6",
        "lxml==5.1.0",
        "multidict==6.0.5",
        "nest-asyncio==1.6.0",
        "pillow==10.2.0",
        "py-cord==2.5.0",
        "pycairo==1.26.0",
        "reportlab==4.1.0",
        "requests==2.31.0",
        "rlPyCairo==0.3.0",
        "scrython==1.11.0",
        "svglib==1.5.1",
        "tinycss2==1.2.1",
        "urllib3==2.2.1",
        "webencodings==0.5.1",
        "yarl==1.9.4",
        "pytest"
    ]
    ,
    author="Jaroslav Nemec",
    author_email="jnemec.appetizer802@passmail.net",
    description="Discord bot for fetching card data from Scryfall API.",
    long_description="",
    long_description_content_type="text/markdown",
    url="https://github.com/jnemec91/chandra-bot",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: GNU GPL v.3 License",
        "Operating System :: OS Independent",
    ],
)
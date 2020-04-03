import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

version = __import__('pelican_embed_svg').__version__

setuptools.setup(
    name="pelican-embed-svg",
    version=version,
    author="Kevin Houlihan",
    author_email="kevin@hyperlinkyourheart.com",
    description="A pelican plugin for embedding SVG images/icons in HTML. Includes support for FontAwesome <i> tags.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/khoulihan/pelican-embed-svg",
    packages=setuptools.find_packages(),
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing',
    ],
    python_requires='>=3.6',
)

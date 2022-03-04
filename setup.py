import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


def requirements():
    """Build the requirements list for this project."""
    requirements_list = []

    with open("requirements.txt") as requirements:
        for install in requirements:
            requirements_list.append(install.strip())
    return requirements_list


requirements = requirements()

setuptools.setup(
    name="cleverbot-scraper",
    version="0.2",
    author="Matheus Fillipe",
    author_email="mattf@tilde.club",
    description="Free cleverbot without headless browser",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/matheusfillipe/cleverbot_scraper",
    packages=setuptools.find_packages(),
    install_requires=requirements,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Communications :: Chat",
        "Topic :: Internet",
    ],
    python_requires=">=3.4",
)

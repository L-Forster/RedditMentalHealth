from setuptools import setup

setup(
    name="RedditMentalDisorders",
    version="1.0.0",
    author="Louis Forster",
    description="Sentiment Analysis on scraped Reddit users",
    packages=[""],
    install_requires=[
        "requests==2.25.1",
        "Flask==2.0.1",
    ],
)

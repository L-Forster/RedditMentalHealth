from setuptools import setup

setup(
    name='RedditMentalDisorders',
    version='1.0.0',
    packages=['RedditMentalDisorders'],
    url='',
    license='',
    author='Louis Forster',
    author_email='',
    description='Sentiment analysis on scraped Reddit users.',
    install_requires=[],
    scripts=[
        "scripts/classify_facade",
        "scripts/classify_user",
        "scripts/interface",
        "scripts/scraper",
        "scripts/scraper_facade",
        "scripts/subreddits",
        "scripts/training",
        "scripts/training_facade",

    ]
)

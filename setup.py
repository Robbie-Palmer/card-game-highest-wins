from pathlib import Path

from setuptools import setup, find_packages

requirements = Path('requirements.txt').read_text()

setup(
    name='highest_wins',
    version='0.1.0',
    packages=find_packages(exclude=['*tests*']),
    description='A CLI tool which simulates a game of cards between two players',
    install_requires=requirements,
    entry_points=dict(console_scripts=['play-highest-wins = highest_wins:main']),
    url='https://github.com/Robbie-Palmer/card-game-highest-wins',
    setup_requires=['wheel']
)

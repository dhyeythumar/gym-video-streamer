import os
import gym_video_streamer
from setuptools import setup

description = "Wrapper to live stream OpenAI's gym agents training process from Google Colab to Twitch/YouTube server."

README_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'README.md')
if os.path.exists(README_path):
    with open(README_path, encoding='utf-8') as f:
        long_description = f.read()
    long_description_content_type = 'text/markdown'
else:
    print("No Readme.md")
    long_description = description
    long_description_content_type = 'text/plain'

VERSION = gym_video_streamer.__version__
BASE_DEPENDENCIES = [
    "gym>=0.17.3",
    "pyvirtualdisplay>=2.2",
]

setup(
    name="gym-video-streamer",
    author="Dhyey Thumar",
    author_email="dhyeythumar@gmail.com",
    version=VERSION,
    install_requires=BASE_DEPENDENCIES,
    packages=["gym_video_streamer"],

    url="https://github.com/dhyeythumar/gym-video-streamer",
    description=description,
    long_description=long_description,
    long_description_content_type=long_description_content_type,

    keywords=["OpenAI", "Gym", "Gym Wrapper", "Video Streamer", "Google Colab"],
    classifiers=[
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries"],
)

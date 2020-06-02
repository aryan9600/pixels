# Pixels

Pixels is a fun social media website for users to share images with their friends.
Pixels is powered by Django and follows the best practices that the documentation describes. (Although the templating
part of it might be a bit sloppy :grimacing: ). 
 ---

## Features 
Users can:
- register themselves and login.
- create and edit a profile.
- upload posts with images and captions.
- follow other users on the platform.
- view an activity feed for all users that they follow.
- like the posts of other users

## Usage
:warning: This repository is still under development, so stuff might not work as expected.

To use this on your system, follow the following steps:

Clone the repository : `git clone https://github.com/aryan9600/pixels.git`

`cd pixels`

`pip install -r requirements.txt`

Redis is used for caching posts ranks, etc. Please make sure that you have installed redis on your system.

`redis-server`

`python manage.py makemigrations`

`python manage.py migrate`

`python manage.py runserver`
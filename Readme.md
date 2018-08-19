# Picture Frame

Some code I wrote to use my old Raspberry Pi zero as a picture frame (using my smugmug account)

***XXX still not working XXXX***

## Deployment

### Prerequisites
Need to have the following packages installed:
* git
* python >= 3
* python3-pip
* apache2
* libapache2-mod-wsgi

Once Python is installed, since I'm running this on a Pi-Zero device
I don't care if I'm not using a virtual environment.

Install the packages using the Pipfile.

Now, create the config file using the example in config.template.json

When that's done: need to run the collection script:
* `$ python collect_images.py`

Now you can start the gunicorn webserver (TODO: add config to run as daemon)

Finally, need to install the crontab, so the image list will be collected daily.
* `crontab /home/pi/picture_frame/crontab`


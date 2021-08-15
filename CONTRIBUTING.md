# Contributing

Before we begin, thank you for considering to contribute to this repo. I am sure we can make this better for the world 😀.

The entire setup procedure required to run this project have been dealt in the [README file](./README.md) but in order to contribute to this repo, you might want to set it up locally, so as to easily test every minor change that you make to the code, while developing and testing stages. Here we will deal with the setting this repo locally.

## Setting up locally

Once you have the repo running by following the procedure in the [README file](./README.md), there is just a few more steps to get it running locally and begin experimenting.


### 1. Creating a Config file

As we will be running the scripts locally, we would require a local `config.py` file. We will be keying in the API credentials here.

Use the following format to create your own :

```python
# District ID for the location to be pinged
DISTRICT_ID = ""

# Twitter Consumer Credentials
TWITTER_CONSUMER_KEY = ""
TWITTER_CONSUMER_SECRET = ""

# Twitter Access Credentials
TWITTER_ACCESS_KEY = ""
TWITTER_ACCESS_SECRET = ""

# Twitter Username
TWITTER_RECIPIENT_USER_NAME = ""
```


### 2. Changes in the main Python script

As we will be using the credentials in the config file, we would have to use this. The code to perform this has already been included in the file. You would just have to comment out the portions using the `os.environ` and uncomment the portions using `config.` to use the credentials from the config file. Refer to the lines `For Development` and `For Deployment` which marks the places that needs this modification.


With these changes done, you are ready to experiment, but replace the code to use the credentials from the `environment variables` before pushing the code to your github repository so that it can utilize the credentials stored in your Github Repository Secrets.


Once your changes are ready, just raise a Pull Request from your fork through your browser or terminal. I will then review 🧐 your changes to add them to the main repository.

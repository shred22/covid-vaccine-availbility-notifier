## Python Based Vaccine Tracker

This is my personal  covid vaccine tracker. It tracks the availability of covid vaccines through the COWIN publid API's and if any slots are available,
it will send an email to desired email receivers.

The configuration and ccredentials is externalised and configparser  parses and uses the configurationn provided.

Usage.

Dependency and requirements areoutlined requirements .txt

Run Below  to Install Dependencies and you are good to go.<br>

`python -m pip install -r requirements.txt`

### Technical Requirements

- Python 3.6+

  Run below command on system and verify the python version

  `python --version `

- Clone the Project:

  `git clone git@github.com:shred22/covid-vaccine-availbility-notifier.git`

- `cd` into project directory and run: 

  ​    `pip install -r requirements.txt`

   - pip is the package manager for python, install pip as well if not already installed.

- run the project with below command

  `python src/main/python/vaccine_api_client.py`



### External Configuration

The application will read configuration from external `config.ini` file placed under `conf` directory. Under the checkout directory  create a folder named `conf` and add a file `config.ini`add the following key value pairs in the file .



```[mail]
[mail]
senderid= xxx@gmail.com
senderpassword = xxx
receiverids=xxx,xxx,xxx
```



As the application relies on google's SMTP server you need to use a *gmail* account to send notification emails.  Fill  in valid values for the above keys and you should be up  and running.



### Tracking Vaccine Availability

The  CoWIN API's are restricted at 100 API calls per 5 minutes, and it  is desired to run the script in a scheduled manner, however scheduling it to runn too frequently (e.g. once per 5 seconds) is not recommended as the calls  from the script will then start getting blocked  the CoWIN Server.



To run the command use below command:

`watch -n 50 python src/main/python/vaccine_api_client.py`

Application logs will  get printed in `app.log` file.


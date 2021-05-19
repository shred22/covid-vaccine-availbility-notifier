
import requests
import configparser
import logging
import urllib3
import json
import email_sender
from datetime import datetime, timedelta
import configparser
import  os

config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), '../../../conf', 'config.ini'))

#Setup the Logger
logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
rootLogger = logging.getLogger()

fileHandler = logging.FileHandler("app.log")
consoleHandler = logging.StreamHandler()

fileHandler.setFormatter(logFormatter)
consoleHandler.setFormatter(logFormatter)

#Add Console and File Handlers both to Root Logger
rootLogger.addHandler(consoleHandler)
rootLogger.addHandler(fileHandler)
rootLogger.setLevel(logging.INFO)

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
logging.getLogger("requests").setLevel(logging.ERROR)
logging.getLogger("urllib3").setLevel(logging.ERROR)

finalVaccinationSlotsList = []  
vaccineSlot = {}
reqHeaders = {'Authorization': 'Bearer zxxx',
              "Accept-Language": "hi_IN",
              "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
              "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
              }
tomorrowDate = datetime.now() + timedelta(1)
tomorrow = tomorrowDate.strftime('%d-%m-%Y')
serviceUrl = ['https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode=452016&date='+tomorrow, 'https://cdn-api.co-vin.in/api/v2/appointment/sessions/calendarByDistrict?district_id=314&date='+tomorrow]
for url in serviceUrl: 
    searchCriteria = 'Pin' if url.__contains__('Pin') else 'District'
    logging.info(f'Searching by {searchCriteria} : ' + url)
    response = requests.get(url, headers=reqHeaders, verify=False)
    jsonResponse = json.loads(response.text)

    for center in jsonResponse['centers']:
        for session in center['sessions']:
            if session['available_capacity_dose1'] > 0 or session['available_capacity_dose2'] > 0 or session['available_capacity'] > 0:
                vaccineSlot = {
                'name' : center['name'],
                'available_capacity_dose1' : session['available_capacity_dose1'],
                'available_capacity_dose2': session['available_capacity_dose2'],
                'available_capacity': session['available_capacity'],
                'vaccine' : session['vaccine']
                }
                finalVaccinationSlotsList.append(vaccineSlot)
            
    if len(finalVaccinationSlotsList) > 0: #
        emailBody = json.dumps(finalVaccinationSlotsList, indent = 4)
        email_sender.EmailSender.sendEmail(emailBody)
        print('EmailBody Below')
        print(emailBody)
    else:
        logging.info("Not Sending Emails as No Slots vaccant")

    
    

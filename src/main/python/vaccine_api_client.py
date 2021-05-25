
import requests
import configparser
import logging
import urllib3
import json
import email_sender
import configparser
import os
import time
import sys
from datetime import datetime, timedelta
from telegram_sender import telegram_alert
from metadata_collector import getDistrictApiUrls

config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), '../../../conf', 'config.ini'))

#Setup the Logger
logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s] [%(filename)s]  %(message)s")
rootLogger = logging.getLogger()

fileHandler = logging.FileHandler("app.log")
consoleHandler = logging.StreamHandler()

fileHandler.setFormatter(logFormatter)
consoleHandler.setFormatter(logFormatter)

#Add Console and File Handlers both to Root Logger
rootLogger.addHandler(consoleHandler)
rootLogger.addHandler(fileHandler)
rootLogger.setLevel(logging.DEBUG)

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
logging.getLogger("requests").setLevel(logging.ERROR)
logging.getLogger("urllib3").setLevel(logging.ERROR)

finalVaccinationSlotsList = []  
vaccineSlot = {}
reqHeaders = {
              "Accept-Language": config.get('mail', 'acceptLanguage'),
              "user-agent": config.get('mail', 'userAgent'),
              "accept": config.get('mail', 'accept')
              }

tomorrowDate = datetime.now() + timedelta(1)
tomorrow = tomorrowDate.strftime('%d-%m-%Y')
defaultState= 'Madhya Pradesh'
state = defaultState if len(sys.argv[1]) == 0 else sys.argv[1]


stateDistrictMap = getDistrictApiUrls(state)

logging.info('Metadata is ready. Ready to Track Vaccines')

telegram_conf = ''
pincode = ''


for state, districts in stateDistrictMap.items():
    logging.debug('State : '+state)
    logging.debug('districts : '+json.dumps(districts, indent=4))
    for district in districts:
        logging.debug('District : '+json.dumps(district, indent=4))
        districtApiUrl = config.get('mail', 'cowinDistrictApiUrl')
        
        districtApiUrl = districtApiUrl.replace('<dist_id>', str(district['district_id']))
        districtApiUrl = districtApiUrl.replace('<date>', tomorrow)
        logging.debug('DISTRICT API URL : '+districtApiUrl)
        try:
            response = requests.get(districtApiUrl, headers=reqHeaders, verify=False)
            jsonResponse = json.loads(response.text)
            for center in jsonResponse['centers']:
                for session in center['sessions']:
                    if session['available_capacity_dose1'] > 0 or session['available_capacity_dose2'] > 0 or session['available_capacity'] > 0:
                        vaccineSlot = {
                        'name' : center['name'],
                        'pincode': center['pincode'],
                        'available_capacity_dose1' : session['available_capacity_dose1'],
                        'available_capacity_dose2': session['available_capacity_dose2'],
                        'available_capacity': session['available_capacity'],
                        'vaccine' : session['vaccine']
                        }
                        finalVaccinationSlotsList.append(vaccineSlot)
                        telegram_alert(session['available_capacity_dose1'], session['available_capacity_dose2'], center['pincode'],
                                    center['name'], district['channel_url'] )

        except Exception as e:
            logging.error(e)
            
if len(finalVaccinationSlotsList) > 0: #
        
    emailBody = json.dumps(finalVaccinationSlotsList, indent = 4)
    email_sender.EmailSender.sendEmail(emailBody)
        
        
else:
    logging.info("Not Sending Emails as No Slots vaccant")


# for apiUrl in stateDistrictMap: #.split(","):
#     searchCriteria = 'Pin' if apiUrl.__contains__('Pin') else 'District'
#     apiUrl = apiUrl.replace('<date>', tomorrow)
#     logging.info(f'Searching by {searchCriteria} : ' + apiUrl)
#     try:
#         response = requests.get(apiUrl, headers=reqHeaders, verify=False)
#         jsonResponse = json.loads(response.text)
        
#         if searchCriteria.__contains__('pincode'):
#             pincode = apiUrl[apiUrl.index('=')+1:apiUrl.rindex('&')]
#             telegram_conf = config.get('mail', 'indorechannel') if(pincode == '45') else config.get('mail', 'punechannel')
#         else:
#             district = apiUrl[apiUrl.index('=')+1:apiUrl.rindex('&')]
#             telegram_conf = config.get('mail', 'indorechannel') if(district == '314') else config.get('mail', 'punechannel')
#         for center in jsonResponse['centers']:
#             for session in center['sessions']:
#                 if session['available_capacity_dose1'] > 0: #or session['available_capacity_dose2'] > 0 or session['available_capacity'] > 0:
#                     vaccineSlot = {
#                     'name' : center['name'],
#                     'pincode': center['pincode'],
#                     'available_capacity_dose1' : session['available_capacity_dose1'],
#                     'available_capacity_dose2': session['available_capacity_dose2'],
#                     'available_capacity': session['available_capacity'],
#                     'vaccine' : session['vaccine']
#                     }
#                     finalVaccinationSlotsList.append(vaccineSlot)
#                     if searchCriteria.__contains__('Pin'):
#                         telegram_alert(dose1=session['available_capacity_dose1'], dose2=session['available_capacity_dose2'],
#                                   pincode=center['pincode'], name=center['name'], telegram_conf=telegram_conf)
#     except Exception as e:
#         logging.error(e)
            
#     if len(finalVaccinationSlotsList) > 0: #
#         emailBody = json.dumps(finalVaccinationSlotsList, indent = 4)
#         email_sender.EmailSender.sendEmail(emailBody)
        
#     else:
#         logging.info("Not Sending Emails as No Slots vaccant")

    
    

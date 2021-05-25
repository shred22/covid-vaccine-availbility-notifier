
import requests
import configparser
import logging
import urllib3
import json
import configparser
import os


#ConfigParser
metaDataConfig = configparser.ConfigParser()
metaDataConfig.read(os.path.join(os.path.dirname(__file__), '../../../conf', 'config.ini'))
channelConfig = configparser.ConfigParser()

# Logging Configuration
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
logging.getLogger("requests").setLevel(logging.ERROR)
logging.getLogger("urllib3").setLevel(logging.ERROR)


def getDistrictApiUrls(stateName='Madhya Pradesh'):
 
            reqHeaders = {
                        "Accept-Language": metaDataConfig.get('mail', 'acceptLanguage'),
                        "user-agent": metaDataConfig.get('mail', 'userAgentMac'),
                        "accept": metaDataConfig.get('mail', 'accept')
                        }
            
            stateMetaDataUrl = metaDataConfig.get('metadata', 'statesApi')
            response = requests.get(stateMetaDataUrl, headers=reqHeaders, verify=False)
            jsonResponse = json.loads(response.text)
            stateToDistrictMap = {}
            districts = []
            channelUrl = ''
            logging.debug('State is '+stateName)
            for state in jsonResponse['states']:
                
                districtsApiUrl = metaDataConfig.get('metadata', 'districtsApi')
                channelConfig.read(os.path.join(os.path.dirname(__file__), '../../../conf/telegram-channels', 
                                                'tele-conf-'+str(state['state_id'])+'.ini'))
                if state['state_name'] == stateName:
                    response = requests.get(districtsApiUrl.replace('<state_id>', str(state['state_id'])),
                                            headers=reqHeaders, 
                                            verify=False)
                    jsonResponse = json.loads(response.text)
                    
                    for district in jsonResponse['districts']:
                        try: 
                            channelUrl =  channelConfig.get(state['state_name'], district['district_name'].lower())
                        except Exception as e:
                            channelUrl = ''
                    
                        if len(channelUrl) > 0:
                            dist = {
                                'district_id' : district['district_id'],
                                'district_name' : district['district_name'],
                                'channel_url' : channelUrl
                                }
                            districts.append(dist)
                    if len(districts) > 0:
                        stateToDistrictMap[str(state['state_id'])+':'+state['state_name']] = districts
                districts = []
            logging.debug(json.dumps(stateToDistrictMap, indent=4))
            return stateToDistrictMap
        
    

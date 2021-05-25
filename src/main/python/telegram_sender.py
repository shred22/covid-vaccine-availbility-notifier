import requests
import configparser
import os
    
def telegram_alert(dose1, dose2, pincode, name, channel_url):
    config = configparser.ConfigParser()
    config.read(os.path.join(os.path.dirname(__file__), '../../../conf', 'config.ini'))
    reqHeaders = {
              "Accept-Language": config.get('mail', 'acceptLanguage'),
              "user-agent": config.get('mail', 'userAgent'),
              "accept": config.get('mail', 'accept')
    }
    telegramMessage = f'''
    Vaccine Available.. \n
    Name: {name}
    Available Cap Dose 1 : {dose1}
    Availble Cap Dose 2 : {dose2}
    Pincode : {pincode}
    '''
    requests.get(channel_url.replace('<MSG>', telegramMessage), headers=reqHeaders, verify=False)
   
    


        
        
    



import os, shutil, sys, requests, json, requests, time
from Bounding_Box.WGS84_box import Bounding_Box
from Abbreviations.abb import abbrev
from xml.etree import ElementTree

'''
Example:    http://dev.virtualearth.net/REST/v1/Traffic/Incidents/45.219,-122.325,47.610,-122.107/false?severity=1,2,3,4&type=1,2,3,4,5,6,7,8,9,10,11&key=YOUR_API_KEY
'''
#Return coordinates in s, w, n, e bounding box
#Example: bounding_box = Bounding_Box(LATITUDE, LONGITUDE, RADIUS_IN_KM)
bounding_box = Bounding_Box(41.8784523,-87.6277754,3)
#Traffic API key
bing_key = os.environ["bing_api_key"]
#Text-To-Speech API key
tts_key = os.environ["tts_key"]

#Create folder to hold audio files
audio_folder = (os.getcwd() + "\\audio")
if os.path.isdir(audio_folder) == True:
    shutil.rmtree(audio_folder)
    os.mkdir(audio_folder)
else:
    os.mkdir(audio_folder)


def json_req():
    r = requests.get("http://dev.virtualearth.net/REST/v1/Traffic/Incidents/{}/{}?severity={}&type={}&key={}".format(bounding_box,'false', '3,4', '1,2,3,4,8,9,10,11', bing_key))
    if r.status_code == 200:
        #Do json parsing logic here
        json_load = json.loads(r.text)
        if json_load['authenticationResultCode'] == 'ValidCredentials':
            print('Successful Login!')
            if json_load['resourceSets'][0]['estimatedTotal']:
                print("\nThere are {} traffic incidents found in your area".format(json_load['resourceSets'][0]['estimatedTotal']) + "\n")
                estimated_total = (json_load['resourceSets'][0]['estimatedTotal'])
                for i in range(0, estimated_total):
                    traffic_incident = json_load['resourceSets'][0]['resources'][i]['description']
                    traffic_lat = json_load['resourceSets'][0]['resources'][i]['point']['coordinates'][0]
                    traffic_long = json_load['resourceSets'][0]['resources'][i]['point']['coordinates'][1]
                    traffic_coordinates = str(traffic_lat) + ", " + str(traffic_long)
                    
                    print(str(i + 1) + ") " + traffic_incident + "\n" + "Coordinates: " + traffic_coordinates)
                    
                    #Create the Text-To-Speech
                    timestr = time.strftime("%Y%m%d-%H%M")
                    access_token = None

                    #URL for the API
                    fetch_token_url = "https://westus.api.cognitive.microsoft.com/sts/v1.0/issueToken"

                    #Create the header
                    headers = {
                    'Ocp-Apim-Subscription-Key': tts_key
                    }

                    #Get the access token using the fetch_token_url & header above
                    response = requests.post(fetch_token_url, headers=headers)
                    access_token = str(response.text)

                    #Define the base url that the text will be sent to
                    base_url = 'https://westus.tts.speech.microsoft.com/'

                    #Define the Azure directory that the text will be sent to
                    path = 'cognitiveservices/v1'

                    #Concatenate the url
                    constructed_url = base_url + path

                    #Construct new headers from the documentation found on the Azure website
                    headers = {
                        'Authorization': 'Bearer ' + access_token,
                        'Content-Type': 'application/ssml+xml',
                        'X-Microsoft-OutputFormat': 'riff-24khz-16bit-mono-pcm',
                        'User-Agent': 'PySpeech'
                    }

                    #Documentation requires a specially crafted XML document called SSML be POST to the constructed_url using the headers above
                    xml_body = ElementTree.Element('speak', version='1.0')
                    xml_body.set('{http://www.w3.org/XML/1998/namespace}lang', 'en-us')
                    voice = ElementTree.SubElement(xml_body, 'voice')
                    voice.set('{http://www.w3.org/XML/1998/namespace}lang', 'en-US')
                    #Set the region and voice font
                    '''
                    en-US 	English (US) 	Female 	"Microsoft Server Speech Text to Speech Voice (en-US, ZiraRUS)"
                                            Female 	"Microsoft Server Speech Text to Speech Voice (en-US, JessaRUS)"
                                            Male 	"Microsoft Server Speech Text to Speech Voice (en-US, BenjaminRUS)"
                                            Female 	"Microsoft Server Speech Text to Speech Voice (en-US, Jessa24kRUS)"
                                            Male 	"Microsoft Server Speech Text to Speech Voice (en-US, Guy24kRUS)"
                    '''
                    voice.set('name', 'Microsoft Server Speech Text to Speech Voice (en-US, Guy24kRUS)')
                    #Need to replace the '/' in tts variable with ' and '
                    text_to_bing = abbrev(traffic_incident)
                    voice.text = text_to_bing
                    body = ElementTree.tostring(xml_body)
                    #Create a POST request that will send a file back based on response codes
                    try:
                        response = requests.post(constructed_url, headers=headers, data=body)
                    except TimeoutError:
                        print("Failure to connect to Azure Server! Please try again")
                        sys.exit()
                    if response.status_code == 200:
                        tts_file = text_to_bing.replace(" ", "-")
                        tts_filename = abbrev(tts_file)
                        with open(audio_folder + "\\" + timestr + "-" + tts_filename + '.wav', 'wb') as audio:
                            audio.write(response.content)
                            print("\nSUCCESS: The speech file is ready!\n")
                    else:
                        print("\nSomething went wrong: " + str(response.status_code))
        else:
            print('failure to send login credentials!')
            sys.exit()
    else:
        print("Please check supplied api-url and try again")
        sys.exit()

if __name__ == '__main__':
    json_req()
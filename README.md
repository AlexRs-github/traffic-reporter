# Traffic Reporter

This traffic reporter is designed to give you all the traffic in a bounding box. It will provide the traffic in the form of audio files. 

It relies on azure to provide the traffic data and audio processing!

# Requirements!
  - Python 3
  - An Azure account! Which can be created for free (at the time of this writing)!
  - 'Ocp-Apim-Subscription-Key' from [Azure for Text-to-Speech][tts].
  - An Azure Maps API Key to get the traffic. More info [here][maps].
 
# Usage
## Set environment variables
Set your Azure Maps & Text-to-Speech API Key to an environment variable:
```
Windows:
C:\Users\You> set bing_api_key=YOUR_AZURE_MAPS_API_KEY
C:\Users\You> set tts_key=YOUR_OCP_APIM_KEY
```
## Modify bounding box parameters
In order to change the traffic area the bounding box covers you can change this line:
```
bounding_box = Bounding_Box(41.8784523,-87.6277754,3)
```
 to your desired location and bounding box size like so:
 ```
bounding_box = Bounding_Box(LATITUDE,LONGITUDE,SIZE)
```

# Execution
```
Windows:
C:\Users\You> python traffic-reporter-orig.py
```



   [tts]: https://docs.microsoft.com/en-us/azure/cognitive-services/speech-service/rest-text-to-speech
   [maps]: https://docs.microsoft.com/en-us/rest/api/maps/traffic/gettrafficincidentdetail
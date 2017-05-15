# TextDirections

I wanted to play around with the Twilio and Google Maps API. This quick script lets users text an origin and destination location, and receive the directions in an SMS text message.

## Setup
- Set up a Twilio account and buy a phone number
- Set up a web hook (like ngrok) and add it to the "Manage Numbers" page 
   - [Twilio Youtube QuickStart tutorial](https://www.youtube.com/watch?v=knxlmCVFAZI)
- Get a Google Maps API Key and fill out credentials in receive_sms.py

And finally,  

```
python receive_sms.py
```

Thanks for checking this out :rabbit:

import tweepy 
import json

class postToTwitter:
    def __init__(self):
        with open('TwitterKeys.json', 'r') as keysJson:
            keys = json.load(keysJson)
        auth = tweepy.OAuthHandler(keys[0]['consumer_key'], keys[0]['consumer_secret'])
        auth.set_access_token(keys[0]['access_token'], keys[0]['access_token_secret']) 
        
        self.api = tweepy.API(auth) 

    def postWithImage(self, imagePath, text=""):
        imgstatus = self.api.media_upload(imagePath)
        media_id = [imgstatus.__dict__['media_id']]
        self.api.update_status(status=text, media_ids=media_id)

if __name__ == "__main__":
    postToTwitter()
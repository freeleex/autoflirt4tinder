# AutoFlirt AI bot for Tinder
This is a bot that basically flirts for you on tinder. It uses the api of https://www.haystack.ai/ to identify the attractiveness of the girls (or boys).

Created by [Alex Maza](http://alejandromaza.net)

## How it works
* Download the photo of the girl
* Send it to this endpoint: [API Endpoint](https://api.haystack.ai/api/image/analyze?apikey={YOUR_API_KEY}&output=json&model=attractiveness)
    * If the endpoint can give a punctuation it returns a JSON like this:
        ```
        {
            "result":"success",
            "people":[{
                "index":0,
                "attractiveness":9.962,
                "location":{
                    "x":379,
                    "y":213,
                    "width":222,
                    "height":223
                }
            }]
        }   
        ```
        * And then if the punctuation is more than a 7 it gives like, if not, dislike
        
    * If it doesn't recognize any face it returns a JSON like this:
        ```
        {"result":"success","people":[]}
        ```
        * If it doesn't work, it passes to the next photo and start over again
        * If it is in the last photo and still not recognizing a face, there's a probability of 70% to give like and 30% to give dislike
        
## Set up
* To run this you need to have the **Requests** and the **Selenium** packages installed.
* You have to download the Chrome (or Firefox) webdriver and put it into the same folder.
* Create a **Secrets** file and inside create 3 variables:
    * user --> With your user
    * password --> With your password
    * url --> With the endpoint url of the api with your key
* Then create a **Pickups** file with an array called *pickups* and put all the pickups inside

##### And finally you're ready to go! Have fun!
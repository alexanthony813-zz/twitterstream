# Deployed at https://rocky-atoll-27122.herokuapp.com/

Send GET requests to https://rocky-atoll-27122.herokuapp.com/get_sentiment/<lat>/<lon>/<radius>

Use the latitude, longitude, and radius (in kilometers) parameters to query the database. Response is formatted as such:

{
            “tweets”: 100, // number of tweets
            “average_polarity”: 0.4, // TextBlob provides a polarity value for sentiment analysis
            “most_positive”: { // tweet at this location with highest polarity
                        “text”: “what a great day!”,
                        "coordinates": [-75.14310264, 40.05701649]
            },
            “most_negative”: { // tweet at this location with lowest polarity
                        “text”: “worst lunch ever!”,
                        "coordinates": [-75.14311344, 40.05701716]
            }
}

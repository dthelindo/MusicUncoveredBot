## MusicUncovered (@MusicUncovered_)

### What is MusicUncovered?
MusicUncovered is a twitter bot that collects data using the Spotipy API, bringing users new, popular music daily.
Currently, MusicUncovered is guided to collect data for new, popular tracks in hip hop, pop, country and edm.

Follow @MusicUncovered_ on Twitter for daily updates.

### How does it work?
The bot parses through Spotify's data for new releases. For the daily _Hot Pick_ a random track with high popularity is chosen from the collection. For _Hip Hop Hot Pick_ , _Pop Hot Pick_, etc. the bot searches for tracks with the relative genres. Follow for follow capability now supported.

Once data is collected, it is posted through the Tweepy python package.

### Built With
* Python - language used
* Spotipy - Collecting song data
* Tweepy - Send tweets
* Heroku server

### Author
* Daniel Lindo - https://github.com/Dlindo28

#### What's New? (10/4/17)
* Added country and edm genre support
* Follow for follow functionality

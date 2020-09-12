## MusicUncovered (@MusicUncovered_)

### What is MusicUncovered?
MusicUncovered is a twitter bot that collects data using the Spotipy API, bringing users new, popular music weekly.
Currently, MusicUncovered is guided to collect data for new, popular tracks in hip hop, pop, country and edm.

Follow @MusicUncovered_ on Twitter for weekly updates.

### How does it work?
The bot parses through Spotify's data for new releases. For the weekly _Hot Pick_ a random track with high popularity is chosen from the collection. For _Hip Hop Hot Pick_ , _Pop Hot Pick_, etc. the bot searches for tracks with the relative genres.

Once data is collected, it is posted through the Tweepy python package.

### Built With
* Python - language used
* Spotipy - Collecting song data
* Tweepy - Send tweets
* Heroku server

### Contributors
* Daniel Lindo - https://github.com/Dlindo28 - https://www.linkedin.com/in/daniel-lindo/

#### What's New?
* Added country and edm genre support (10/4/17)
* Album of the week (11/1/17)

#### To-Do
* ~~Clean up code for less repetition~~
* Probihibit posting same song multiple times
* Revise follow for follow capabilities
* Generate tweet for rising artists

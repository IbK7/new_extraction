## News Extraction

The `/scrapper/news_scrapper.py` file extracts the news headlines from the sources. Running the script will launch a controlled browser that will open each of the sources itereatively.

Once each source is open, the script will pause for 5 seconds to allow the user to hanle the cookies popup, as each source had a different cookies popup and could not be handled automatically. 

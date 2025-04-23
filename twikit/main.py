import asyncio
import os
from twikit import Client

# Initialize client
client = Client('en-US')


async def get_user_tweets(username: str):
    await client.login(
        auth_info_1=os.getenv('TWITTER_USERNAME'),
        auth_info_2=os.getenv('EMAIL'),
        password=os.getenv('TWITTER_PASSWORD'),
        cookies_file='cookies.json'
    )
    
    user_id = await client.get_user_by_screen_name(username)
    tweets = await client.get_user_tweets(user_id, 'Tweets')

    await client.logout()
    return tweets
    
## Login
tweets = asyncio.run(get_user_tweets(username='MohsinHijazee'))


print (tweets)
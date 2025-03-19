import tweepy
import random
import time
from datetime import datetime

# ======================= #
# TWITTER AUTHENTICATION  #
# ======================= #

bearer_token = "AAAAAAAAAAAAAAAAAAAAAPztzwEAAAAAvBGCjApPNyqj9c%2BG7740SkkTShs%3DTCpOQ0DMncSMhaW0OA4UTPZrPRx3BHjIxFPzRyeoyMs2KHk6hM"
api_key = "uKyGoDr5LQbLvu9i7pgFrAnBr"
api_secret = "KGBVtj1BUmAEsyoTmZhz67953ItQ8TIDcChSpodXV8uGMPXsoH"
access_token = "1901441558596988929-WMdEPOtNDj7QTJgLHVylxnylI9ObgD"
access_token_secret = "9sf83R8A0MBdijPdns6nWaG7HF47htcWo6oONPmMS7o98"

client = tweepy.Client(
    bearer_token=bearer_token,
    consumer_key=api_key,
    consumer_secret=api_secret,
    access_token=access_token,
    access_token_secret=access_token_secret
)

# ======================= #
#     TRIVIA QUESTIONS    #
# ======================= #

TRIVIA_QUESTIONS = [
    {
        "question": "Who is the only player to record a 40-point triple-double in an NBA Finals game?",
        "answer": "LeBron James"
    },
    {
        "question": "Which player has the most combined points + rebounds + assists in a single playoff game over the last 50 years?",
        "answer": "LeBron James"
    },
    {
        "question": "Who is the only player to have a 30-20-10 stat line in a playoff game since 2000?",
        "answer": "Nikola Jokic"
    },
    {
        "question": "Which player has the most 50-point games in NBA playoff history?",
        "answer": "Michael Jordan"
    },
    {
        "question": "Who holds the record for the most assists in a single NBA Finals game?",
        "answer": "Magic Johnson"
    },
    {
        "question": "Who is the only player to average a triple-double in an entire NBA Finals series?",
        "answer": "LeBron James"
    },
    {
        "question": "Which player had a 35-point, 20-rebound, 10-assist game in the playoffs in the 2020s?",
        "answer": "Nikola Jokic"
    },
    {
        "question": "Who has the most career playoff triple-doubles?",
        "answer": "LeBron James"
    },
    {
        "question": "Which player has the most career points in NBA playoff history?",
        "answer": "LeBron James"
    },
    {
        "question": "Who is the only player with multiple 20-rebound games in the 2023 NBA Playoffs?",
        "answer": "Kevon Looney"
    }
]

# ======================= #
#     TWEET FORMATTER     #
# ======================= #

def build_tweet(question_text):
    return (
        "🏀 STAT KINGS TRIVIA 👑\n\n"
        f"{question_text}\n\n"
        "Reply with your guess ⬇️\n"
        "#NBATrivia #StatKingsHQ"
    )

# ======================= #
#       POST TRIVIA       #
# ======================= #

def post_trivia():
    trivia = random.choice(TRIVIA_QUESTIONS)
    tweet_text = build_tweet(trivia["question"])

    try:
        response = client.create_tweet(text=tweet_text)
        tweet_id = response.data["id"]
        print("✅ Trivia posted!")
        print("📊 Question:", trivia["question"])
        print("🔐 Answer:", trivia["answer"])
        return tweet_id
    except Exception as e:
        print("❌ Failed to post trivia:", e)
        return None

# ======================= #
#    LIKE REPLIES LATER   #
# ======================= #

def like_replies_to(tweet_id, delay=60):
    print(f"⏳ Waiting {delay} seconds before checking for replies...")
    time.sleep(delay)

    try:
        # Get replies by searching for tweets that mention @StatKingsHQ AND are replying to tweet_id
        query = f"to:StatKingsHQ conversation_id:{tweet_id} -is:retweet"
        response = client.search_recent_tweets(
            query=query,
            max_results=20,
            tweet_fields=["in_reply_to_user_id"]
        )
        if not response.data:
            print("😶 No replies found yet.")
            return

        for tweet in response.data:
            try:
                client.like(tweet.id)
                print(f"💙 Liked reply: {tweet.id}")
                time.sleep(1)
            except Exception as e:
                print(f"❌ Error liking tweet {tweet.id}: {e}")

    except Exception as e:
        print("❌ Failed to fetch replies:", e)

# ======================= #
#        MAIN BOT         #
# ======================= #

def run_trivia_bot():
    print(f"🚀 Running Stat Kings Trivia Bot at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    tweet_id = post_trivia()
    if tweet_id:
        like_replies_to(tweet_id, delay=90)

if __name__ == "__main__":
    run_trivia_bot()

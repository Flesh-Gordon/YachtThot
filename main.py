from reddit_client import reddit
from comment_handler import handle_comment
import time

SUBREDDIT = "MorganBrennanFanClub"

def main():
    subreddit = reddit.subreddit(SUBREDDIT)
    print(f"Monitoring r/{SUBREDDIT}...")

    for comment in subreddit.stream.comments(skip_existing=True):
        handle_comment(comment)
        time.sleep(1)  # simple rate limit

if __name__ == "__main__":
    main()
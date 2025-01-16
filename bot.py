import os
from groq import Groq
import praw
import requests
import schedule
import time
from dotenv import load_dotenv
from datetime import datetime
load_dotenv()

# Reddit API setup
reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    username=os.getenv("REDDIT_USERNAME"),
    password=os.getenv("REDDIT_PASSWORD"),
    user_agent=os.getenv("REDDIT_USER_AGENT"),
)

# Groq API setup
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Call an LLM through Groq API to generate a comment for some post based on the post's title and content
def get_llm_response_for_comment(title, content):
    
    client = Groq(api_key=GROQ_API_KEY)

    instructions = (
        "Write a thoughtful and engaging comment based on the following post. "
        "Ensure the comment is friendly, relevant, and adds value to the discussion."
        "Make sure the comment is short, it should not exceed 150 words."
    )

    post_details = f"Title: {title}\n\nContent: {content}"
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"{instructions}\n\n{post_details}",
            }
        ],
        model="llama-3.3-70b-versatile",
    )

    return chat_completion.choices[0].message.content

# Call an LLM through Groq API to generate content for a post on the topic given by user
def get_llm_response(topic):
    client = Groq(
        api_key=GROQ_API_KEY
    )
    
    instructions = (
        "Please write an article on the given topic. "
        "The content should be between 200-300 words, "
        "informative, and structured into paragraphs."
    )

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"{instructions}\n\nTopic: {topic}",
            }
        ],
        model="llama-3.3-70b-versatile",
    )

    return chat_completion.choices[0].message.content

# Fetch posts from a subreddit and comments on them and handle rate limits
def comment_on_posts(subreddit_name, num_posts):
    try:
        # Fetch posts from the subreddit
        subreddit = reddit.subreddit(subreddit_name)
        posts = subreddit.hot(limit=num_posts)  # Fetch top 'num_posts' hot posts

        for post in posts:
            title = post.title
            content = post.selftext.strip()

            # If content is empty, display this short message to user
            if not content:
                content = "No content provided. This seems to be a link or a short post."

            print(f"Processing post: {title}")     # Display the post title
            print(f"Content: {content[:200]}...")  # Display starting few lines of the content

            # Generate a comment by calling the LLM
            comment = get_llm_response_for_comment(title, content)
            print(f"Generated comment: {comment}") # Display the generated comment 

            try:
                # Post the comment
                post.reply(comment)
                print(f"Commented on post: {title}")

            except praw.exceptions.RedditAPIException as e:
                for sub_error in e.items:
                    if sub_error.error_type == "RATELIMIT": # If RATE_LIMIT_ERROR is there, then wait for some time and then retry posting the comment
                        
                        # Extract the wait time from the error message
                        wait_time = int(
                            ''.join(filter(str.isdigit, sub_error.message.split("minute")[0])) or "1"
                        ) * 60
                        print(f"Rate limit hit. Waiting for {wait_time} seconds...")
                        time.sleep(wait_time + 5)  
                        post.reply(comment)  # Retry after the wait time
                        print(f"Successfully commented after waiting on post: {title}")
                        break

    except Exception as e:
        print(f"Error commenting on posts: {e}")

# Post the LLM-Generated content 
def post_to_reddit(topic, response):
    subreddit_name = "test"  
    title = f"Insights on {topic}"

    try:
        reddit.subreddit(subreddit_name).submit(title, selftext=response)
        print(f"Posted to r/{subreddit_name}: {title}")
    except Exception as e:
        print(f"Error posting to Reddit: {e}")
    
# Schedule the task of posting to a user-specified time
def schedule_task_at_time(post_time, topic, response):
    def job():
        post_to_reddit(topic, response)
    
    # Schedule the job
    schedule.every().day.at(post_time).do(job)
    print(f"Post scheduled at {post_time}. Waiting to execute...")
    
    while True:
        schedule.run_pending()
        time.sleep(1)

def main():
    print("Welcome to the Reddit Bot!")
    choice = input("Choose an option:\n1. Post content\n2. Comment on posts\nEnter your choice (1 or 2): ")
    
    if choice == "1":
        topic = input("Enter the topic: ")
        response = get_llm_response(topic)
        post_time = input("Enter the time to post (in HH:MM 24-hour format, e.g., 14:30): ")

        try:
            datetime.strptime(post_time, "%H:%M")
            schedule_task_at_time(post_time, topic, response)
        except ValueError:
            print("Invalid time format. Please enter the time in HH:MM 24-hour format.")
    
    elif choice == "2":
        subreddit_name = input("Enter the subreddit name to comment on: ")
        num_posts = int(input("Enter the number of posts to comment on: "))
        comment_on_posts(subreddit_name, num_posts)

if __name__ == "__main__":
    main()

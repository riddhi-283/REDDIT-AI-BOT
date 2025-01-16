# Reddit Bot: Automated Content and Comment Generator

This project is a Python-based Reddit bot that automates posting and commenting on Reddit using the **Groq API** for LLM-based text generation. The bot can generate engaging comments for posts and create informative posts on user-specified topics. It also supports scheduling posts at a specific time.

## Features
- **Commenting on Posts**: Fetches posts from a subreddit and generates thoughtful comments using the Groq LLM.
- **Content Generation**: Creates structured posts on user-provided topics using Groq LLM.
- **Scheduling**: Allows scheduling posts to Reddit at a specific time.
- **Rate Limit Handling**: Automatically handles Reddit API rate limits. If a rate limit is encountered, it waits for the required time before retrying.

# Working
- **POST GENERATION**
![Screenshot 2025-01-16 143721](https://github.com/user-attachments/assets/2b785cca-fca8-46bd-93bd-a6f09d180b98)
![Screenshot 2025-01-16 143809](https://github.com/user-attachments/assets/149fbea9-a47c-4922-8286-5f91fd3ff9a6)

- **COMMENTING ON OTHER POSTS**
![Screenshot 2025-01-16 143945-cropped](https://github.com/user-attachments/assets/dd3f329a-a6b4-4d9c-b30a-086809f9e36e)

![Screenshot 2025-01-16 144053](https://github.com/user-attachments/assets/a656eec0-e70f-4a07-aaf6-fe4d88801335)

  
## Pre-requisites

Before running the bot, ensure you have the following:

1. Python 3.8+
2. Reddit API credentials ([Create a Reddit app](https://www.reddit.com/prefs/apps)).
3. Groq API key ([Sign up for Groq](https://www.groq.com)).
4. Install necessary Python libraries listed in the **Requirements** section.


## Libraries Used

The bot uses the following Python libraries:

- **praw**: For interacting with Reddit's API.
- **requests**: For making HTTP requests.
- **schedule**: For scheduling tasks.
- **python-dotenv**: For loading environment variables.
- **datetime**: For working with date and time.
- **groq**: For interacting with Groq API.


## Setup Instructions

Follow these steps to set up and run the bot:

### 1. Clone the Repository
``` sh
git clone https://github.com/yourusername/reddit-bot.git
```

### 2. Install Dependencies
``` sh
pip install -r requirements.txt
```

### 3. Configure Environment Variables
Create a \`.env\` file in the project directory and add the following:
``` sh
REDDIT_CLIENT_ID=<your-reddit-client-id>
REDDIT_CLIENT_SECRET=<your-reddit-client-secret>
REDDIT_USERNAME=<your-reddit-username>
REDDIT_PASSWORD=<your-reddit-password>
REDDIT_USER_AGENT=<your-user-agent>
GROQ_API_KEY=<your-groq-api-key>
```

### 4. Run the Bot
Start the bot by running:
```sh
python bot.py
```

## Usage

### 1. Post Content to Reddit
- Choose the "Post content" option.
- Provide a topic.
- Specify the time to schedule the post (24-hour format).

### 2. Comment on Posts
- Choose the "Comment on posts" option.
- Enter the subreddit name.
- Specify the number of posts to comment on.


## Contribution Guidelines

Feel free to fork this repository, submit issues, or make pull requests to improve the bot.

1. Fork the repository.
2. Create a new branch for your feature/bugfix.
3. Commit your changes with clear messages.
4. Submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.


## Disclaimer

Use this bot responsibly and comply with Reddit's [API Terms of Use](https://www.redditinc.com/policies/data-api-terms-of-service). Spamming or violating community guidelines may result in account suspension.

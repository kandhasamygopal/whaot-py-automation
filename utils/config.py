#Base URL and authentication tokens

BASE_URL = "https://api-dev.whaot.com"  # Replace with your API base URL
API_KEY = "your-api-key"  # Replace with your actual API key, if required

# Authentication Token
BEARER_TOKEN = "9ab6c59281c57b7db7929f978255788d8514da143bc63a00ebeae4b2fc2b2ee5eff7381e83f789cd67373135ca906ba72926c5dfc7146bad2d2438af4d2584ba740d402e52fc4ae3655d98147763498af7ea88adfa71ab7a95daad100785b2c6ed47057a53c5aa1b86441d2ae1f7bd7d6ca460b2155198cd1df77e9e5b20c3c6dca3ca18812054e901dc9b0a05919d460c454b4d6641852220830f4bc585a525"
AUTH_HEADERS = {
    "Authorization": f"Bearer {BEARER_TOKEN}",
    "Content-Type": "application/json",
}
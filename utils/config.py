#Base URL and authentication tokens

BASE_URL = "https://api-dev.whaot.com"  # Replace with your API base URL
API_KEY = "your-api-key"  # Replace with your actual API key, if required

# Authentication Token
BEARER_TOKEN = "9ab6c59281c57b7db7929f978255788d8514da143bc63a00ebeae4b2fc2b2ee5eff7381e83f789cd67373135ca906ba72926c5dfc7146bad2d2438af4d2584bab2d9f7c1f5ba9a74c25a8781df72dfa339c872670df2261256f9a4c3d8d8317a410cdb7c24fb83aa6403a74afeeba8f92370d5672b842c89d2f5d9a84f1d4e2c92a8f5737d368609b14f60a7e0dfcac4d946b618f82f002c41ac04aab135d986"
AUTH_HEADERS = {
    "Authorization": f"Bearer {BEARER_TOKEN}",
    "Content-Type": "application/json",
}
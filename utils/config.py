#Base URL and authentication tokens

BASE_URL = "https://api-dev.whaot.com"  # Replace with your API base URL
API_KEY = "your-api-key"  # Replace with your actual API key, if required

# Authentication Token
BEARER_TOKEN = "9ab6c59281c57b7db7929f978255788d8514da143bc63a00ebeae4b2fc2b2ee5eff7381e83f789cd67373135ca906ba72926c5dfc7146bad2d2438af4d2584ba8e57b4d7c77c3ea0cc1318f68ef7caec5b17191bb527dea90875ae48b1166528107314f2d46da97c945d153c13909915fdfda2a27ae7364e576a7ab26ec7ae1a982c7d7258f47eb2cf4977695c340659f545d980ae1a952c937983dc2382a098"
AUTH_HEADERS = {
    "Authorization": f"Bearer {BEARER_TOKEN}",
    "Content-Type": "application/json",
}
# add-recipe-api

## Technologies Used
- Node.js
- Python
- RabbitMQ
- [recipe-scrapers](https://github.com/hhursev/recipe-scrapers)

## Setup
1. Install dependencies via npm and pip (package.json and requirements.txt have listed dependencies)
2. Install RabbitMQ server based on OS and preferences (https://www.rabbitmq.com/docs/download)

## Usage
1. In client.js, set msg variable to a valid hyperlink to a recipe
2. Run server.py with ```python server.py```
3. Run client.js with ```node client.js```
4. client.js will eventually receive the recipe details and print to the console a stringified JSON object with the recipe name, ingredient list, and instructions

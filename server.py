#!/usr/bin/env python

# Citation for server.py format for both sending and receiving
# 08/09/2024
# Copied from RabbitMQ Python Hello World tutorial
# Source URL: https://www.rabbitmq.com/tutorials/tutorial-one-python

import pika, sys, os, json
from recipe_scrapers import scrape_html



def sendRecipeDetails(recipeObj):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='recipeDetails')
    channel.basic_publish(exchange='', routing_key='recipeDetails', body=recipeObj)
    print("[server.py] Sent recipe details!")
    
    connection.close()


def getRecipeDetails(recipeLink):
    url = recipeLink.decode(encoding="utf-8") ;
    scraper = scrape_html(html=None, org_url=url, online=True);

    recipeName = scraper.title()
    recipeIngredients = scraper.ingredients()
    recipeInstruct = scraper.instructions()

    recipeObj = '{"name":  "%s",  "ingredients": %s, "instructions": %s}' % (recipeName, recipeIngredients, recipeInstruct) 
    sendRecipeDetails(recipeObj)


def receiveRecipe():
    # establish connection with RabbitMQ server
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    # create queue named 'recipe' if it doesn't exist already
    channel.queue_declare(queue='recipeLink')

    def callback(ch, method, properties, body):
        print(f" [server.py] Received {body}")
        getRecipeDetails(body)

    # check the recipe queue for message
    channel.basic_consume(queue='recipeLink', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    try:
        receiveRecipe()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
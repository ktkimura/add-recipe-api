#!/usr/bin/env node

// Citation for client.js format for both sending and receiving
// 08/09/2024
// Copied from RabbitMQ JavaScript Hello World tutorial
// Source URL: https://www.rabbitmq.com/tutorials/tutorial-one-javascript

var amqp = require('amqplib/callback_api');

function sendRecipeLink(){
    amqp.connect('amqp://localhost', function(error0, connection) {
        if (error0) {
            throw error0;
        }
        connection.createChannel(function(error1, channel) {
            if (error1) {
                throw error1;
            }
            // queue will only be created if it doesn't exist already 
            var queue = 'recipeLink';
            var msg = 'https://www.allrecipes.com/recipe/21014/good-old-fashioned-pancakes/';   // encoded as a byte arr

            channel.assertQueue(queue, {
                durable: false
            });
            channel.sendToQueue(queue, Buffer.from(msg));

            console.log(" [client.js] Sent %s", msg);
        });
        setTimeout(function() {
            connection.close();
            process.exit(0);
        }, 500);
    });
};

function receiveRecipeDetails(){
    var amqp = require('amqplib/callback_api');

amqp.connect('amqp://localhost', function(error0, connection) {
    if (error0) {
        throw error0;
    }
    connection.createChannel(function(error1, channel) {
        if (error1) {
            throw error1;
        }

        var queue = 'recipeDetails';

        channel.assertQueue(queue, {
            durable: false
        });

        console.log(" [client.js] Waiting for messages in %s. To exit press CTRL+C", queue);

        channel.consume(queue, function(msg) {
            // note: ingredients and instructions will be passed in as arrays
            console.log(" [client.js] Received %s", msg.content.toString());
        }, {
            noAck: true
        });
    });
});
};

sendRecipeLink();
setTimeout(() => {}, 3000);
receiveRecipeDetails();

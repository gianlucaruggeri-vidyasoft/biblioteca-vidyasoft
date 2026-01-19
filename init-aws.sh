#!/bin/bash
echo "Sto creando il Topic SNS (email-notifications-topic)..."
awslocal sns create-topic --name email-notifications-topic

sleep 2

echo "Sto creando la Coda SQS..."
awslocal sqs create-queue --queue-name prenotazioni-queue

sleep 2

echo "Sto collegando SNS a SQS..."
awslocal sns subscribe \
  --topic-arn arn:aws:sns:us-east-1:000000000000:email-notifications-topic \
  --protocol sqs \
  --notification-endpoint arn:aws:sqs:us-east-1:000000000000:prenotazioni-queue

echo "🚀 Configurazione completata!"
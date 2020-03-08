#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pika
import requests
import json
import sys


def get_params():
	cred = pika.PlainCredentials('admin', 'admin')

	params = pika.ConnectionParameters(
		host='127.0.0.1',
		port=5672,
		virtual_host='/',
		credentials=cred
	)

	return params

connection = pika.BlockingConnection(get_params())

channel = connection.channel()

channel.queue_declare(queue='pentaho_notification', durable=True)
channel.exchange_declare(exchange='direct_pentaho', exchange_type='direct')


aplicacao = ' '.join(sys.argv[1:2]) or "Aplicação que enviou a mensagem não foi informada"
message = ' '.join(sys.argv[2:]) or "A mensagem da notificação não foi informada"


dados = {
	"APPLICATION": aplicacao,
	"MESSAGE": message
}

json_dados = json.dumps(dados)

channel.basic_publish(
	exchange='direct_pentaho', 
	routing_key='direct_pentaho', 
	body=json_dados
)

print(" [x] Sent %r" % (json_dados))
connection.close()
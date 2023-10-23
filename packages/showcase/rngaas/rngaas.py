import simplejson as json
from random import seed
from random import random

def get_default_random(event, context):
   clientip = get_client_ip(event)
   requestId = context.request_id

   seed(hash(clientip) + hash(requestId))
   return random()

def get_client_ip(event):
   http = event.get("http", None)
   if http:
      headers = http.get("headers", None)
      if headers:
         ip = headers.get("cf-connecting-ip", None) or headers.get("x-forwarded-for", None)
         if ip:
            return ip
   
   return "unknown"

def main(event, context):
   name = event.get("name", "stranger")
   
   body = {
      "context": {
               "activationId": context.activation_id,
               "apiHost": context.api_host,
               "apiKey": context.api_key,
               "deadline": context.deadline,
               "functionName": context.function_name,
               "functionVersion": context.function_version,
               "namespace": context.namespace,
               "requestId": context.request_id,
         },
      "event": event
   }

   print(json.dumps(body))

   return {
      "body": get_default_random(event, context),
      "statusCode": 200
   }



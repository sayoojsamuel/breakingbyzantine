#!/usr/bin/env python3

import grpc
from concurrent import futures
import time

# import the grpc classes
import byzantine_pb2
import byzantine_pb2_grpc

# import byzantine functionalities
import byzantine

class ByzantineServicer(byzantine_pb2_grpc.ByzantineServicer):
    def getDecision(self, request, context):
        response = byzantine_pb2.Acknowledge()
        response.value = Byzantine.SendDecision(request.value)
        return response

def client():
    # Generate a random personal choice
    personal_choice = decide()
    timestamp = time.time()
    encoded_message = encodeMessage(personal_choice, timestamp)
    generated_hmac = generateHMAC(encoded_message)
    callGeneral(7001, encoded_message, timestamp, generated_hmac)
    callGeneral(7002, encoded_message, timestamp, generated_hmac)	


def callGeneral(port, encoded_message, timestamp, generated_hmac):
    # open a gRPC channel
    channel = grpc.insecure_channel('localhost:{}'.format(port))

    # create a stub (client)
    stub = byzantine_pb2_grpc.ByzantineStub(channel)

    # create a valid request message
    decision = byzantine_pb2.Decision(encoded_message=encoded_message,time=timestamp,mac=generated_hmac)

    # make the call
    response = stub.getDecision(decision)

    print(response.value)


# create a gRPC server
server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

# use the generated function `add_ByzantineServicer_to_server`
# to add the defined class to the server
byzantine_pb2_grpc.add_ByzantineServicer_to_server(
                ByzantineServicer(), server)

# listen on port 7003
print('Starting server. General3 listening on port 7003.')
server.add_insecure_port('[::]:7003')
server.start()

# since server.start() will not block,
# a sleep-loop is added to keep alive
try:
    while True:
        time.sleep(86400)
except KeyboardInterrupt:
    server.stop(0)

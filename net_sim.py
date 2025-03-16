import csv
import argparse
from queue import Queue


def simulateOneServer(filename):
    server = Server()

    try:
        with open(filename, 'r') as file:
            reader = csv.reader(file)
            requests = [Request(row[0], row[1], row[2]) for row in reader]
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return

    for request in requests:
        server.current_time = max(server.current_time, request.timestamp)
        server.add_request(request)
        server.process_next_request()

    return server.get_average_wait_time()


def simulateManyServers(filename, num_servers):
    servers = [Server() for _ in range(num_servers)]

    try:
        with open(filename, 'r') as file:
            reader = csv.reader(file)
            requests = [Request(row[0], row[1], row[2]) for row in reader]
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return

    for index, request in enumerate(requests):
        server = servers[index % num_servers]
        server.current_time = max(server.current_time, request.timestamp)
        server.add_request(request)
        server.process_next_request()

    total_wait_time = sum(server.total_wait_time for server in servers)
    total_requests = sum(server.processed_requests for server in servers)
    return total_wait_time / total_requests if total_requests > 0 else 0


class Request:
    def __init__(self, timestamp, resource, processing_time):
        self.timestamp = int(timestamp)
        self.resource = resource
        self.processing_time = int(processing_time)


class Server:
    def __init__(self):
        self.queue = Queue()
        self.current_time = 0
        self.total_wait_time = 0
        self.processed_requests = 0

    def add_request(self, request):
        self.queue.put(request)

    def process_next_request(self):
        if not self.queue.empty():
            request = self.queue.get()
            wait_time = self.current_time - request.timestamp
            self.total_wait_time += wait_time
            self.processed_requests += 1
            self.current_time += request.processing_time

    def get_average_wait_time(self):
        if self.processed_requests == 0:
            return 0
        return self.total_wait_time / self.processed_requests


def main():
    parser = argparse.ArgumentParser(description='Simulate a network request queue.')
    parser.add_argument('--file', required=True, help='Path to the request log file')
    parser.add_argument('--servers', type=int, default=1, help='Number of servers (default: 1)')
    args = parser.parse_args()

    if args.servers == 1:
        avg_wait_time = simulateOneServer(args.file)
    else:
        avg_wait_time = simulateManyServers(args.file, args.servers)

    if avg_wait_time is not None:
        print(f"Simulation Complete! The network processed the requests successfully.")
        print(f"Number of servers used: {args.servers}")
        print(f"Average Wait Time: {avg_wait_time:.2f} seconds")


if __name__ == "__main__":
    main()


import sys

class Queue:
	def __init__(self):
		self.items = []
	
	def is_empty(self):
		return self.items == []
	
	def enqueue(self, item):
		self.items.insert(0,item)
	
	def dequeue(self):
		return self.items.pop()
	
	def size(self):
		return len(self.items)


class Server:
	def __init__(self):
		self.current_request = None
		self.time_remaining = 0
	
	def tick(self):
		if self.current_request != None:
			self.time_remaining = self.time_remaining - 1
			if self.time_remaining <= 0:
				self.current_request = None
	
	def busy(self):
		if self.current_request != None:
			return True
		else:
			return False
	
	def start_next(self,new_request):
		self.current_request = new_request
		self.time_remaining = new_request.processtime

class Request:
	def __init__(self, time, process_time, filename):
		self.timestamp = time
		self.processtime = process_time
		self.request_file = filename
	
	def get_stamp(self):
		return self.timestamp
	
	def get_process_time(self):
		return self.process_time
	
	def wait_time(self, current_time):
		return current_time - self.timestamp

def simulateManyServers(filename, num_servers = 1):
	server_list = []
	for i in range(0, num_servers):
		server_list.append(Server())
	
	server_num = 0
	server = Server()
	server_queue = Queue()
	waiting_times = []
	
	req_file = open(filename, 'r')
	lines = req_file.readlines()
	
	num_requests = len(lines)
	request_count = 0
	current_second = 0
	
	end = False
	while(not(end)):
		while(request_count < num_requests):
			data = lines[request_count].split(',')
			request_time = int(data[0])
			requestfile = data[1]
			processingtime = int(data[2])
		
			if request_time == current_second:
				request = Request(current_second, processingtime, requestfile)
				server_queue.enqueue(request)
			else:
				break
		
			request_count = request_count + 1
		

		while(not server_queue.is_empty()):
			server_num = server_num % num_servers
			if(not server_list[server_num].busy()):
				next_request = server_queue.dequeue()
				waiting_times.append(next_request.wait_time(current_second))
				server_list[server_num].start_next(next_request)
				server_num = server_num + 1
			else:
				break
					
		current_second = current_second+1
		for server in server_list:
			server.tick()
			
		if (request_count >= num_requests) and (server_queue.is_empty()):
			end = True
			
	average_wait = sum(waiting_times) / len(waiting_times)
	print ("Average Wait %6.2f secs %3d requests remaining."%(average_wait, server_queue.size()))


def simulateOneServer(filename):
	server = Server()
	server_queue = Queue()
	waiting_times = []
	
	req_file = open(filename, 'r')
	lines = req_file.readlines()
	
	num_requests = len(lines)
	request_count = 0
	current_second = 0
	
	end = False
	while(not(end)):
		while(request_count < num_requests):
			data = lines[request_count].split(',')
			request_time = int(data[0])
			requestfile = data[1]
			processingtime = int(data[2])
		
			if request_time == current_second:
				request = Request(current_second, processingtime, requestfile)
				server_queue.enqueue(request)
			else:
				break
		
			request_count = request_count + 1
			
		if (not server.busy()) and (not server_queue.is_empty()):
			next_request = server_queue.dequeue()
			waiting_times.append(next_request.wait_time(current_second))
			server.start_next(next_request)
			
		current_second = current_second+1
		server.tick()
		
		if (request_count >= num_requests) and (server_queue.is_empty()):
			end = True
		
		
	average_wait = sum(waiting_times) / len(waiting_times)
	print ("Average Wait %6.2f secs %3d requests remaining."%(average_wait, server_queue.size()))

	
def main(argv):
	
	num_servers = 1
	
	if len(argv) == 1:
		filename = argv[0]
	elif len(argv) == 2:
		filename = argv[0]
		num_servers = int(argv[1])
	else:
		filename = 'requests.csv'
	
	if num_servers > 1:
		print "Number of servers: %d" %(num_servers)
		simulateManyServers(filename, num_servers)
	else:
		simulateOneServer(filename) 
	
	
if __name__ == "__main__":
	main(sys.argv[1:])
	











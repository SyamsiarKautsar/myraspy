# lets make the client code
import socket,cv2, pickle,struct

# create socket
client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host_ip = '172.24.155.130' # paste your server ip address here
port = 9999
client_socket.connect((host_ip,port)) # a tuple
data = b""
payload_size = struct.calcsize("Q")
while True:
	while len(data) < payload_size:
		packet = client_socket.recv(4*1024) # 4K
		if not packet: break
		data+=packet
	#try:
	packed_msg_size = data[:payload_size]
	data = data[payload_size:]
	msg_size = struct.unpack("Q",packed_msg_size)[0]
	#except:
	    #print("data camera eror")

	while len(data) < msg_size:
		data += client_socket.recv(4*1024)
	
	#try:
	frame_data = data[:msg_size]
	data  = data[msg_size:]
	frame = pickle.loads(frame_data)
	cv2.imshow("RECEIVING VIDEO",frame)
	#except:
		#print("data camera eror") 
	
	key = cv2.waitKey(1) & 0xFF
	if key  == ord('q'):
		break
client_socket.close()
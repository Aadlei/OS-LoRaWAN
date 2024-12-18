import paho.mqtt.client as mqttClient
import time
import xmlrpc
import xmlrpc.client
import zmq
import json
import base64
import binascii
import socket
import threading
import logging
from chirpstack_api.gw import gw_pb2

logging.basicConfig(level=logging.DEBUG,
                   format='[%(levelname)s] (%(threadName)-9s) %(message)s')

class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'

# Initialize counters for message timing
Count_1, Count_2, Count_3, Count_4, Count_5, Count_6 = 0, 0, 0, 0, 0, 0

server = xmlrpc.client.ServerProxy("http://localhost:8089/RPC2")

context = zmq.Context()

# TX sockets
tx_sock = context.socket(zmq.PUSH)
tx_sock.bind("tcp://127.0.0.1:5555")

tx_sock2 = context.socket(zmq.PUSH)
tx_sock2.bind("tcp://127.0.0.1:5554")

def send_message_lora(phyPayload, delay, frequency, spreadingfactor):
    Delay_offset_Sf12 = 2.5
    Delay_offset_Sf7 = 2.18
    counts = [Count_1, Count_2, Count_3, Count_4, Count_5, Count_6]
    max_index = counts.index(max(counts))
    
    formatted = base64.b64decode(phyPayload).hex() + ','
    print(formatted)
    end_time = time.perf_counter_ns()
    elapsed_time_ns = end_time - counts[max_index]
    elapsed_time_s = elapsed_time_ns / 1_000_000_000
    server.set_sink_freq(frequency)  # Convert MHz to Hz
    if spreadingfactor == 7:
        delay = int(delay) - Delay_offset_Sf7 - elapsed_time_s
        time.sleep(delay)
        tx_sock.send(formatted.encode())
    if spreadingfactor == 12:
        delay = int(delay) - Delay_offset_Sf12 - elapsed_time_s
        time.sleep(delay)
        tx_sock2.send(formatted.encode())
    
        
    logging.info(f"Sent LoRa message: SF{spreadingfactor}, {(frequency/1e6)}MHz, delay={delay:.4f}")

def send_packet_network(data, freq, sf):
    try:
        hex_data = data.hex()
        base64_data = base64.b64encode(bytes.fromhex(hex_data)).decode()
        
        packet = (
            bytes([2]) +  # Version
            b'\x02\xD0' +  # Random token
            bytes([0]) +  # PUSH_DATA identifier
            binascii.unhexlify("5680ea3344aeda16") +  # Gateway EUI
            json.dumps({
                "rxpk": [{
                    "time": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
                    "freq": freq,
                    "stat": 1,
                    "modu": "LORA",
                    "datr": f"SF{sf}BW125",
                    "codr": "4/5",
                    "size": len(data),
                    "data": base64_data
                }]
            }).encode()
        )
        
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.sendto(packet, ("10.225.150.112", 1700))
        
        logging.info(f"Sent packet to NS - Freq: {freq}MHz, SF{sf}")
    
    except Exception as e:
        logging.error(f"Error sending packet: {e}")

# Listener threads
def create_listener(freq, sf, port, count_var):
    def listener():
        rx_sock = context.socket(zmq.PULL)
        rx_sock.connect(f"tcp://127.0.0.1:{port}")
        while True:
            try:
                data = rx_sock.recv()
                globals()[count_var] = time.perf_counter_ns()
                thread = threading.Thread(target=send_packet_network, args=(data, freq, sf))
                thread.start()
            except Exception as e:
                logging.error(f"Listener error: {e}")
    return listener

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        logging.info("Connected to broker")
        client.subscribe("+/gateway/+/command/down")
    else:
        logging.error(f"Connection failed: {rc}")

def on_message(client, userdata, message):
    try:
        downlink = gw_pb2.DownlinkFrame()
        downlink.ParseFromString(message.payload)
        
        for item in downlink.items:
            phy_payload = base64.b64encode(item.phy_payload)
            frequency = item.tx_info.frequency
            delay = item.tx_info.timing.delay.delay.seconds
            sf = item.tx_info.modulation.lora.spreading_factor
            
            send_message_lora(phy_payload, delay, frequency, sf)
    
    except Exception as e:
        logging.error(f"Message handling error: {e}")

def main():
    # Set up listener threads
    listener_configs = [
        (868.1, 12, 5556, 'Count_1'),
        (868.3, 12, 5557, 'Count_2'),
        (868.5, 12, 5558, 'Count_3'),
        (868.1, 7, 5559, 'Count_4'),
        (868.3, 7, 5560, 'Count_5'),
        (868.5, 7, 5561, 'Count_6')
    ]

    threads = []
    for freq, sf, port, count_var in listener_configs:
        thread = threading.Thread(
            target=create_listener(freq, sf, port, count_var),
            daemon=True
        )
        thread.start()
        threads.append(thread)
        logging.info(f"Started listener: {freq}MHz SF{sf}")

    # MQTT setup
    client = mqttClient.Client(client_id="SDR", callback_api_version=mqttClient.CallbackAPIVersion.VERSION1)
    client.username_pw_set("", "")
    client.on_connect = on_connect
    client.on_message = on_message

    try:
        client.connect("10.225.150.112", 1883, 60)
        client.loop_forever()
    except Exception as e:
        logging.error(f"MQTT error: {e}")

if __name__ == "__main__":
    main()
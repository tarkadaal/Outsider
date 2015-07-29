#!/usr/bin/python
import usb1
import ctypes
import sys

canned_packet  = '\x81\x07\x14\x04\x03\x07\x00\x16\xd8\xa9\x0d\x7a\xd5\xa4\x5c\xb8\x1f\x27\xf2\x98\xe0\xf7\x1f\xb3\x69\x12\x06\xba\x60\x73\xe7\x2d\xaa\x6a\x54\xad\x24\xc9\x9e\x32\x63\xd5\x14\xaa\x26\x6d\x6b\x3e\x23\x3a\xd9\xca\x67\x5e\xe2\x02\x17\xd5\x8f\xd9\x9d\x6d\x69'
parameter_packet = '\x03\x01\x00\x2a\x04\x58\x19\x6e\x19\x32\x00\x04\x00\x00\x32\x3c\x40\x01\x00\x00\x00\x00\x0a\x40\x32\x32\x00\x0a\x00\x32\x00\x02\x00\x0a\x00\x32\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'

context = usb1.USBContext()
devices = context.getDeviceList()
for device in devices:
	print(device)

VENDOR_ID = 0x27d4
PRODUCT_ID = 0x0010

handle = context.openByVendorIDAndProductID(
	VENDOR_ID, PRODUCT_ID,
	skip_on_error=False,
)
if handle is None:
	print("ooh fuck")
	# Device not present, or user is not allowed to access device.#
handle.detachKernelDriver(0)
handle.claimInterface(0)

#handle.bulkWrite(1, canned_packet);
packet_count = 0
while True:
	print("pckt =" + str(packet_count))
	data = handle.bulkRead(0x81, 64)
	print(" ".join("{:02x}".format(ord(x)) for x in data))
	print("[7] == {:02x}".format(ord(data[7])) )
	print
	
	if packet_count >= 3:
		bass = sys.stdin.read(3) 
		print("bass ==" + bass)
		print("{:02x}.format(int(bass)) == " + "{:02x}".format(int(bass)))

		data = data[:7] + chr(int(bass)) + data[8:]
		print("new [7] == {:02x}".format(ord(data[7])))    
		print(" ".join("{:02x}".format(ord(x)) for x in data))    
		
		handle.bulkWrite(1, data);

	print("*" * 40)
	packet_count = packet_count + 1

	   

	#print(repr(data.raw))
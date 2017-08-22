#!/usr/bin/python
# -*-coding:utf-8-*-
__author__ = "ihciah"

import struct, zlib, logging
from bluetooth import BluetoothSocket, find_service, RFCOMM, discover_devices
from const import BtCommandByte


class BtManager:
    standardKey = 0x35769521
    padding_line = 300
    max_send_msg_length = 2016
    max_recv_msg_length = 1024
    uuid = "00001101-0000-1000-8000-00805F9B34FB"

    def __init__(self, address=None):
        self.address = address
        self.crckeyset = False
        self.connected = True if self.connect() else False

    def connect(self):
        if self.address is None and not self.scandevices():
            return False
        if not self.scanservices():
            return False
        logging.info("Service found. Connecting to \"%s\" on %s..." % (self.service["name"], self.service["host"]))
        self.sock = BluetoothSocket(RFCOMM)
        self.sock.connect((self.service["host"], self.service["port"]))
        self.sock.settimeout(60)
        logging.info("Connected.")
        self.registerCrcKeyToBt()
        return True

    def disconnect(self):
        try:
            self.sock.close()
        except:
            pass
        logging.info("Disconnected.")

    def scandevices(self):
        logging.warning("Searching for devices...\n"
                        "It may take time, you'd better specify mac address to avoid a scan.")
        valid_names = ['MiaoMiaoJi', 'Paperang']
        nearby_devices = discover_devices(lookup_names=True)
        valid_devices = filter(lambda d: len(d) == 2 and d[1] in valid_names, nearby_devices)
        if len(valid_devices) == 0:
            logging.error("Cannot find device with name %s." % " or ".join(valid_names))
            return False
        elif len(valid_devices) > 1:
            logging.warning("Found multiple valid machines, the first one will be used.\n")
            logging.warning("\n".join(valid_devices))
        else:
            logging.warning(
                "Found a valid machine with MAC %s and name %s" % (valid_devices[0][0], valid_devices[0][1])
            )
        self.address = valid_devices[0][0]
        return True

    def scanservices(self):
        logging.info("Searching for services...")
        service_matches = find_service(uuid=self.uuid, address=self.address)
        valid_service = filter(
            lambda s: 'protocol' in s and 'name' in s and s['protocol'] == 'RFCOMM' and s['name'] == 'SerialPort',
            service_matches
        )
        if len(valid_service) == 0:
            logging.error("Cannot find valid services on device with MAC %s." % self.address)
            return False
        logging.info("Found a valid service on target device.")
        self.service = valid_service[0]
        return True

    def sendMsgAllPackage(self, msg):
        # Write data directly to device
        sent_len = self.sock.send(msg)
        logging.info("Sending msg with length = %d..." % sent_len)

    def crc32(self, content):
        return zlib.crc32(content, self.crcKey if self.crckeyset else self.standardKey)

    def packPerBytes(self, bytes, control_command, i):
        result = struct.pack('<BBB', 2, control_command, i)
        result += struct.pack('<H', len(bytes))
        result += bytes
        result += struct.pack('<i', self.crc32(bytes))
        result += struct.pack('<B', 3)
        return result


    def addBytesToList(self, bytes):
        length = self.max_send_msg_length
        result = [bytes[i:i+length] for i in range(0, len(bytes), length)]
        return result

    def sendToBt(self, allbytes, control_command, need_reply=True):
        bytes_list = self.addBytesToList(allbytes)
        for i, bytes in enumerate(bytes_list):
            tmp = self.packPerBytes(bytes, control_command, i)
            self.sendMsgAllPackage(tmp)
        if need_reply:
            return self.recv()

    def recv(self):
        # Here we assume that there is only one received packet.
        raw_msg = self.sock.recv(self.max_recv_msg_length)
        parsed = self.resultParser(raw_msg)
        logging.info("Recv: " + raw_msg.encode('hex'))
        logging.info("Received %d packets: " % len(parsed) + "".join([str(p) for p in parsed]))
        return raw_msg, parsed

    def resultParser(self, data):
        base = 0
        res = []
        while base < len(data) and data[base] == '\x02':
            class Info(object):
                def __str__(self):
                    return "\nControl command: %s(%s)\nPayload length: %d\nPayload(hex): %s" % (
                        self.command, BtCommandByte.findCommand(self.command)
                        , self.payload_length, self.payload.encode('hex')
                    )
            info = Info()
            _, info.command, _, info.payload_length = struct.unpack('<BBBH', data[base:base+5])
            info.payload = data[base + 5: base + 5 + info.payload_length]
            info.crc32 = data[base + 5 + info.payload_length: base + 9 + info.payload_length]
            base += 10 + info.payload_length
            res.append(info)
        return res

    def registerCrcKeyToBt(self, key=0x6968634 ^ 0x2e696d):
        logging.info("Setting CRC32 key...")
        msg = struct.pack('<I', int(key ^ self.standardKey))
        self.sendToBt(msg, BtCommandByte.PRT_SET_CRC_KEY)
        self.crcKey = key
        self.crckeyset = True
        logging.info("CRC32 key set.")

    def sendPaperTypeToBt(self, paperType=0):
        # My guess:
        # paperType=0: normal paper
        # paperType=1: official paper
        msg = struct.pack('<B', paperType)
        self.sendToBt(msg, BtCommandByte.PRT_SET_PAPER_TYPE)

    def sendPowerOffTimeToBt(self, poweroff_time=0):
        msg = struct.pack('<H', poweroff_time)
        self.sendToBt(msg, BtCommandByte.PRT_SET_POWER_DOWN_TIME)

    def sendImageToBt(self, binary_img):
        self.sendPaperTypeToBt()
        msg = struct.pack("<%dc" % len(binary_img), *binary_img)
        self.sendToBt(msg, BtCommandByte.PRT_PRINT_DATA, need_reply=False)
        self.sendFeedLineToBt(self.padding_line)

    def sendSelfTestToBt(self):
        msg = struct.pack('<B', 0)
        self.sendToBt(msg, BtCommandByte.PRT_PRINT_TEST_PAGE)

    def sendDensityToBt(self, density):
        msg = struct.pack('<B', density)
        self.sendToBt(msg, BtCommandByte.PRT_SET_HEAT_DENSITY)

    def sendFeedLineToBt(self, length):
        msg = struct.pack('<H', length)
        self.sendToBt(msg, BtCommandByte.PRT_FEED_LINE)

    def queryBatteryStatus(self):
        msg = struct.pack('<B', 1)
        self.sendToBt(msg, BtCommandByte.PRT_GET_BAT_STATUS)

    def queryDensity(self):
        msg = struct.pack('<B', 1)
        self.sendToBt(msg, BtCommandByte.PRT_GET_HEAT_DENSITY)

    def sendFeedToHeadLineToBt(self, length):
        msg = struct.pack('<H', length)
        self.sendToBt(msg, BtCommandByte.PRT_FEED_TO_HEAD_LINE)

    def queryPowerOffTime(self):
        msg = struct.pack('<B', 1)
        self.sendToBt(msg, BtCommandByte.PRT_GET_POWER_DOWN_TIME)

    def querySNFromBt(self):
        msg = struct.pack('<B', 1)
        self.sendToBt(msg, BtCommandByte.PRT_GET_SN)

    def queryHardwareInfo(self):
        msg = struct.pack('<B', 1)
        self.sendToBt(msg, BtCommandByte.PRT_GET_HW_INFO)

if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)

    # If you know the MAC address of your device, use this parameter to avoid a scan, which is time-consuming
    # mmj = BtManager("69:68:63:69:61:68")

    # Start a scan to find valid devices
    mmj = BtManager()

    if mmj.connected:
        mmj.sendDensityToBt(95)

        # If you want it never powered-off
        # mmj.sendPowerOffTimeToBt(0)
        # mmj.queryPowerOffTime()

        # Print an existing image(need opencv):
        # from image_process import ImageConverter
        # img = ImageConverter.image2bmp(r"C:\Users\Lemon\Desktop\0.jpg")
        # mmj.sendImageToBt(img)

        # Print a pure black image with 300 lines
        # img = "\xff" * 48 * 300
        # mmj.sendImageToBt(img)

        # Print 2 line of text(need opencv)
        from image_process import TextConverter
        img = TextConverter.text2bmp("Coded By") + TextConverter.text2bmp(__author__)
        mmj.sendImageToBt(img)
        mmj.disconnect()
    else:
        logging.error("Oops! Cannot establish connection with Paperang devices.")

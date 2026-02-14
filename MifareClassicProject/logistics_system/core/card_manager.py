from smartcard.System import readers
from smartcard.util import toHexString, toBytes
from smartcard.Exceptions import NoCardException, CardConnectionException
import time
import json

class CardManager:
    def __init__(self):
        self.connection = None

    def connect(self):
        """
        Connects to the first available reader and card.
        Returns: list of ATR (Answer To Reset) bytes or None if failed.
        """
        r = readers()
        if len(r) == 0:
            raise Exception("No smart card readers found.")
        
        reader = r[1]
        try:
            self.connection = reader.createConnection()
            self.connection.connect()
            return toHexString(self.connection.getATR())
        except NoCardException:
            raise Exception("No card detected. Please place a card on the reader.")
        except Exception as e:
            raise Exception(f"Connection failed: {e}")

    def disconnect(self):
        if self.connection:
            try:
                self.connection.disconnect()
            except:
                pass

    def _send_apdu(self, apdu):
        data, sw1, sw2 = self.connection.transmit(apdu)
        if sw1 == 0x90 and sw2 == 0x00:
            return data
        else:
            raise Exception(f"APDU Failed: {toHexString(apdu)} -> SW: {hex(sw1)} {hex(sw2)}")

    def load_key(self, key=[0xFF]*6):
        """Loads the authentication key into the reader's volatile memory."""
        # APDU: FF 82 00 00 06 [KEY]
        apdu = [0xFF, 0x82, 0x20, 0x00, 0x06] + key
        self._send_apdu(apdu)

    def authenticate(self, block_num, key_type=0x60, key_slot=0x00):
        """
        Authenticates a specific block.
        key_type: 0x60 (Key A) or 0x61 (Key B)
        """
        # APDU: FF 86 00 00 05 01 00 [BLOCK] [KEY_TYPE] [KEY_SLOT]
        apdu = [0xFF, 0x86, 0x00, 0x00, 0x05, 0x01, 0x00, block_num, key_type, key_slot]
        self._send_apdu(apdu)

    def read_block(self, block_num):
        """Reads 16 bytes from a block."""
        # APDU: FF B0 00 [BLOCK] 10
        apdu = [0xFF, 0xB0, 0x00, block_num, 0x10]
        return self._send_apdu(apdu)

    def write_block(self, block_num, data):
        """Writes 16 bytes to a block. Data must be 16 bytes list/bytearray."""
        if len(data) != 16:
            raise ValueError("Data must be exactly 16 bytes.")
        
        # APDU: FF D6 00 [BLOCK] 10 [DATA]
        apdu = [0xFF, 0xD6, 0x00, block_num, 0x10] + list(data)
        self._send_apdu(apdu)

    def read_sector_string(self, block_num):
        """Helper to read a block and decode as trimmed utf-8 string."""
        data = self.read_block(block_num)
        # Remove trailing 0x00
        text = bytes(data).rstrip(b'\x00').decode('utf-8', errors='ignore')
        return text

    def write_sector_string(self, block_num, text):
        """Helper to write string to block (max 16 chars)."""
        data = text.encode('utf-8')[:16]
        padding = b'\x00' * (16 - len(data))
        self.write_block(block_num, list(data + padding))

    # --- High Level Logic ---

    def write_mission(self, driver_info, mission_data, articles):
        """
        Writes full mission data to card.
        driver_info: {name, license, id}
        mission_data: {origin, destination, status}
        articles: list of dicts
        """
        self.load_key() # Load default FF..FF key
        # Sector 2: Driver
        self.authenticate(8)
        self.write_sector_string(8, driver_info['name'])
        self.authenticate(9)
        self.write_sector_string(9, driver_info['license'])
        self.authenticate(10)
        self.write_sector_string(10, driver_info['id'])
        # Sector 3: Mission
        self.authenticate(12)
        self.write_sector_string(12, mission_data['origin'])
        self.authenticate(13)
        self.write_sector_string(13, mission_data['destination'])
        self.authenticate(14)
        self.write_sector_string(14, str(mission_data['status']))
        # Sector 4+: Articles (Simple JSON serialization across blocks)
        # For POC, let's just write summary or first few articles
        # Or split JSON into 16-byte chunks.
        
        # Simplified: Write first 3 articles to blocks 16, 17, 18
        # Each block: "Desc:Qty"
        self.authenticate(16)
        for i, article in enumerate(articles[:3]):
            self.authenticate(16+i)
            block = 16 + i
            # self.authenticate(block) # Required if crossing sectors? 
            # 4K card: Sector 4 starts at 16. Sector 5 starts at 20.
            # If we stay in Sector 4 (16,17,18), one auth is enough usually.
            
            content = f"{article['description']}:{article['quantity']}"
            self.write_sector_string(block, content)
        # Clear remaining blocks in sector 4 if fewer than 3 articles
        for i in range(len(articles), 3):
            self.authenticate(16+i)
            self.write_block(16+i, [0]*16)
    def read_mission(self):
        """Reads mission data from card."""
        self.load_key()
        
        data = {}
        
        # Driver
        self.authenticate(8)
        data['driver_name'] = self.read_sector_string(8)
        data['license_plate'] = self.read_sector_string(9)
        data['driver_id'] = self.read_sector_string(10)
        
        # Mission
        self.authenticate(12)
        data['origin'] = self.read_sector_string(12)
        data['destination'] = self.read_sector_string(13)
        data['status'] = self.read_sector_string(14) # Should be int string
        
        # Articles
        self.authenticate(16)
        articles = []
        for i in range(3):
            text = self.read_sector_string(16+i)
            if ":" in text:
                desc, qty = text.split(":")
                articles.append({'description': desc, 'quantity': qty})
        
        data['articles'] = articles
        return data

from smartcard.System import readers
from smartcard.util import toHexString
from .crypto import des_cbc_decrypt, des_cbc_encrypt, generate_reader_challenge, rotate_left


class DesfireCard:
    """
    Represents a connection to a MIFARE DESFire card.

    Provides low-level communication methods such as:
        - Version retrieval
        - Application selection
        - Authentication
        - Card formatting
    """

    def __init__(self, reader_index=None):
        """
        Initialize connection to a smart card reader and connect to the card.

        :param reader_index: Index of PC/SC reader to use
        """
        r = readers()

        self.reader = [re for re in r if "CL" in str(re)][0]
        self.connection = self.reader.createConnection()
        self.connection.connect()

        print(f"Connected to: {self.reader}")
        print(f"ATR: {toHexString(self.connection.getATR())}")


    def transmit(self, apdu):
        """
        Send APDU command to the card.

        :param apdu: List of integers representing APDU bytes
        :return: (data, sw1, sw2)
        """
        return self.connection.transmit(apdu)


    def get_version(self):
        """
        Retrieve DESFire card version information.

        This command may return multiple frames.
        If SW2 == 0xAF, additional frames must be requested using INS 0xAF.

        APDU:
            CLA  = 0x90
            INS  = 0x60 (GetVersion)
            P1   = 0x00
            P2   = 0x00
            Lc   = 0x00

        :return: List of data frames returned by the card
        """
        apdu = [0x90, 0x60, 0x00, 0x00, 0x00]
        data, sw1, sw2 = self.transmit(apdu)

        frames = [data]

        # Continue retrieving frames if more data is available
        while sw2 == 0xAF:
            apdu = [0x90, 0xAF, 0x00, 0x00, 0x00]
            data, sw1, sw2 = self.transmit(apdu)
            frames.append(data)

        return frames


    def select_application(self, aid):
        """
        Select an application by its 3-byte AID.

        APDU:
            CLA  = 0x90
            INS  = 0x5A (SelectApplication)
            P1   = 0x00
            P2   = 0x00
            Lc   = 0x03
            Data = AID (3 bytes)
            Le   = 0x00

        :param aid: 3-byte list
        :return: True if selection successful
        """
        apdu = [0x90, 0x5A, 0x00, 0x00, 0x03] + aid + [0x00]
        data, sw1, sw2 = self.transmit(apdu)

        return sw1 == 0x91 and sw2 == 0x00


    def authenticate(self, key_number, key_value):
        """
        Perform DES mutual authentication with the card.

        Authentication Steps:
            1. Request encrypted card challenge
            2. Decrypt card challenge
            3. Rotate card challenge
            4. Generate reader challenge
            5. Encrypt combined data
            6. Send response to card

        APDU 1:
            INS = 0x0A (Authenticate)

        APDU 2:
            INS = 0xAF (Additional Frame)

        :param key_number: 1-byte list identifying key index
        :param key_value: 8-byte DES key
        :return: True if authentication successful
        """

        # Step 1: Request card challenge
        apdu = [0x90, 0x0A, 0x00, 0x00, 0x01] + key_number + [0x00]
        encrypted_challenge, sw1, sw2 = self.transmit(apdu)

        # Step 2: Decrypt challenge
        card_challenge = des_cbc_decrypt(bytes(encrypted_challenge), key_value)

        # Step 3: Rotate card challenge
        rotated = rotate_left(card_challenge, 1)

        # Step 4: Generate reader challenge
        reader_challenge = generate_reader_challenge()
        response_data = reader_challenge + rotated

        # Step 5: Encrypt response
        encrypted_response = des_cbc_encrypt(response_data, key_value)

        # Step 6: Send encrypted response
        apdu = [0x90, 0xAF, 0x00, 0x00, 0x10] + list(encrypted_response) + [0x00]
        data, sw1, sw2 = self.transmit(apdu)

        return sw1 == 0x91 and sw2 == 0x00


    def format_card(self):
        """
        Format the entire card (deletes all applications and files).

        APDU:
            CLA  = 0x90
            INS  = 0xFC (FormatPICC)
            P1   = 0x00
            P2   = 0x00
            Lc   = 0x00

        :return: True if formatting successful
        """
        apdu = [0x90, 0xFC, 0x00, 0x00, 0x00]
        data, sw1, sw2 = self.transmit(apdu)

        return sw1 == 0x91 and sw2 == 0x00

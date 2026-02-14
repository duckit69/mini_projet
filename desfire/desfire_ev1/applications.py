from smartcard.util import toHexString

class ApplicationManager:
    """
    Manages DESFire applications (create, list, delete, modify key settings).

    This class expects a DesfireCard-like object that implements:
        transmit(apdu: list[int]) -> (data: list[int], sw1: int, sw2: int)
    """

    def __init__(self, card):
        """
        Initialize ApplicationManager with a DESFire card instance.

        :param card: Instance of a DesfireCard that supports APDU transmit()
        """
        self.card = card
    

    def list_applications(self):
        """
        Retrieve the list of Application IDs (AIDs) from the PICC.

        APDU Structure:
            CLA  = 0x90  (DESFire native command wrapper)
            INS  = 0x6A  (GetApplicationIDs)
            P1   = 0x00
            P2   = 0x00
            Lc   = 0x00  (No data)

        Expected Success Status:
            SW1 = 0x91
            SW2 = 0x00

        :return: List of AIDs (each AID is 3 bytes)
        """
        apdu = [0x90, 0x6A, 0x00, 0x00, 0x00]
        data, sw1, sw2 = self.card.transmit(apdu)

        if sw1 == 0x91 and sw2 == 0x00:
            # Each application ID is 3 bytes
            aids = [data[i:i+3] for i in range(0, len(data), 3)]
            for aid in aids:
                print(f"Application: {toHexString(aid)}")
            return aids
        
        # Return empty list if command failed
        return []
    

    def create_application(self, aid, key_settings=0x0F, num_keys=0x01):
        """
        Create a new application on the DESFire card.

        APDU Structure:
            CLA  = 0x90
            INS  = 0xCA  (CreateApplication)
            P1   = 0x00
            P2   = 0x00
            Lc   = 0x05
            Data = [AID (3 bytes), KeySettings (1 byte), NumKeys (1 byte)]
            Le   = 0x00

        :param aid: 3-byte list representing Application ID
        :param key_settings: Key configuration byte (default 0x0F)
        :param num_keys: Number of keys for the application (default 1)
        :return: True if creation succeeded, False otherwise
        """
        apdu = [0x90, 0xCA, 0x00, 0x00, 0x05] + aid + [key_settings, num_keys, 0x00]
        data, sw1, sw2 = self.card.transmit(apdu)

        print(f"Create app {toHexString(aid)} - Status: {sw1:02X} {sw2:02X}")

        return sw1 == 0x91 and sw2 == 0x00
    

    def delete_application(self, aid):
        """
        Delete an existing application from the DESFire card.

        APDU Structure:
            CLA  = 0x90
            INS  = 0xDA  (DeleteApplication)
            P1   = 0x00
            P2   = 0x00
            Lc   = 0x03
            Data = [AID (3 bytes)]
            Le   = 0x00

        :param aid: 3-byte list representing Application ID
        :return: True if deletion succeeded, False otherwise
        """
        apdu = [0x90, 0xDA, 0x00, 0x00, 0x03] + aid + [0x00]
        data, sw1, sw2 = self.card.transmit(apdu)

        print(f"Delete {toHexString(aid)} - Status: {sw1:02X} {sw2:02X}")

        return sw1 == 0x91 and sw2 == 0x00
    

    def change_key_settings(self, new_settings):
        """
        Change PICC-level key settings.

        APDU Structure:
            CLA  = 0x90
            INS  = 0x54  (ChangeKeySettings)
            P1   = 0x00
            P2   = 0x00
            Lc   = 0x01
            Data = [NewKeySettings]
            Le   = 0x00

        :param new_settings: 1-byte new key settings value
        :return: True if change succeeded, False otherwise
        """
        apdu = [0x90, 0x54, 0x00, 0x00, 0x01, new_settings, 0x00]
        data, sw1, sw2 = self.card.transmit(apdu)

        print(f"Change key settings - Status: {sw1:02X} {sw2:02X}")

        return sw1 == 0x91 and sw2 == 0x00

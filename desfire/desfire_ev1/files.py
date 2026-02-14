from smartcard.util import toHexString
from desfire_ev1.utils import to_3bytes, to_4bytes, from_4bytes


class FileManager:
    """
    Manages DESFire file operations inside a selected application.

    Supports:
        - File creation (Standard, Value, Record)
        - Read/Write operations
        - Value operations (credit/debit)
        - Transaction management
    """

    def __init__(self, card):
        """
        Initialize FileManager with a DesfireCard instance.

        :param card: Instance providing transmit(apdu)
        """
        self.card = card


    # ------------------------------------------------------------------
    # File Listing / Deletion
    # ------------------------------------------------------------------

    def list_files(self):
        """
        Retrieve all file IDs within the currently selected application.

        APDU:
            CLA = 0x90
            INS = 0x6F (GetFileIDs)

        :return: List of file IDs or empty list if failure
        """
        apdu = [0x90, 0x6F, 0x00, 0x00, 0x00]
        data, sw1, sw2 = self.card.transmit(apdu)

        if sw1 == 0x91 and sw2 == 0x00:
            file_ids = list(data)
            print(f"Files: {[f'0x{fid:02X}' for fid in file_ids]}")
            return file_ids

        return []


    def delete_file(self, file_id):
        """
        Delete a file from the current application.

        APDU:
            INS = 0xDF (DeleteFile)

        :param file_id: File identifier (1 byte)
        :return: True if successful
        """
        apdu = [0x90, 0xDF, 0x00, 0x00, 0x01, file_id, 0x00]
        data, sw1, sw2 = self.card.transmit(apdu)

        print(f"Delete file {file_id} - Status: {sw1:02X} {sw2:02X}")
        return sw1 == 0x91 and sw2 == 0x00


    def get_file_type(self, file_id):
        """
        Retrieve file type metadata.

        APDU:
            INS = 0xF5 (GetFileSettings)

        :param file_id: File identifier
        :return: File type byte or None if error
        """
        apdu = [0x90, 0xF5, 0x00, 0x00, 0x01, file_id, 0x00]
        data, sw1, sw2 = self.card.transmit(apdu)

        if sw1 != 0x91 or sw2 != 0x00 or not data:
            return None

        file_type = data[0]

        mapping = {
            0x00: "Standard data",
            0x01: "Backup data",
            0x02: "Value",
            0x03: "Linear record",
            0x04: "Cyclic record",
        }

        print(f"File {file_id} type: {mapping.get(file_type, 'Unknown')} (0x{file_type:02X})")
        return file_type


    # ------------------------------------------------------------------
    # Standard Data Files
    # ------------------------------------------------------------------

    def create_standard_file(self, file_id, file_size, comm_settings=0x00, access_rights=[0x00, 0x00]):
        """
        Create a Standard Data File.

        INS = 0xCD

        :param file_id: File ID (1 byte)
        :param file_size: File size in bytes
        :param comm_settings: Communication mode
        :param access_rights: [read/write access control]
        :return: True if successful
        """
        size_bytes = to_3bytes(file_size)

        apdu = (
            [0x90, 0xCD, 0x00, 0x00, 0x07, file_id, comm_settings]
            + access_rights
            + size_bytes
            + [0x00]
        )

        data, sw1, sw2 = self.card.transmit(apdu)

        print(f"Create standard file {file_id} - Status: {sw1:02X} {sw2:02X}")
        return sw1 == 0x91 and sw2 == 0x00


    def write_data(self, file_id, offset, data):
        """
        Write bytes into a Standard Data File.

        INS = 0x3D

        :param file_id: File ID
        :param offset: Byte offset
        :param data: List of bytes to write
        :return: True if successful
        """
        offset_bytes = to_3bytes(offset)
        length_bytes = to_3bytes(len(data))

        apdu = (
            [0x90, 0x3D, 0x00, 0x00, 7 + len(data), file_id]
            + offset_bytes
            + length_bytes
            + data
            + [0x00]
        )

        response, sw1, sw2 = self.card.transmit(apdu)

        print(f"Write to file {file_id} - Status: {sw1:02X} {sw2:02X}")
        return sw1 == 0x91 and sw2 == 0x00


    def read_data(self, file_id, offset, length):
        """
        Read data from a Standard Data File.

        INS = 0xBD

        :return: Raw data bytes
        """
        offset_bytes = to_3bytes(offset)
        length_bytes = to_3bytes(length)

        apdu = (
            [0x90, 0xBD, 0x00, 0x00, 0x07, file_id]
            + offset_bytes
            + length_bytes
            + [0x00]
        )

        data, sw1, sw2 = self.card.transmit(apdu)

        print(f"Read from file {file_id} - Status: {sw1:02X} {sw2:02X}")
        print(f"Data: {bytes(data).decode('utf-8', errors='ignore')}")

        return data


    # ------------------------------------------------------------------
    # Value Files
    # ------------------------------------------------------------------

    def create_value_file(self, file_id, lower_limit, upper_limit, initial_value,
                          limited_credit=False, comm_settings=0x00,
                          access_rights=[0x00, 0x00]):
        """
        Create a Value File.

        INS = 0xCC

        :return: True if successful
        """
        lower_bytes = to_4bytes(lower_limit)
        upper_bytes = to_4bytes(upper_limit)
        initial_bytes = to_4bytes(initial_value)

        limited = 0x01 if limited_credit else 0x00

        apdu = (
            [0x90, 0xCC, 0x00, 0x00, 0x11, file_id, comm_settings]
            + access_rights
            + lower_bytes
            + upper_bytes
            + initial_bytes
            + [limited, 0x00]
        )

        data, sw1, sw2 = self.card.transmit(apdu)

        print(f"Create value file {file_id} - Status: {sw1:02X} {sw2:02X}")
        return sw1 == 0x91 and sw2 == 0x00


    def credit_value(self, file_id, amount):
        """
        Increase value in Value File.

        INS = 0x0C
        """
        amount_bytes = to_4bytes(amount)

        apdu = [0x90, 0x0C, 0x00, 0x00, 0x05, file_id] + amount_bytes + [0x00]

        data, sw1, sw2 = self.card.transmit(apdu)

        print(f"Credit {amount} - Status: {sw1:02X} {sw2:02X}")
        return sw1 == 0x91 and sw2 == 0x00


    def debit_value(self, file_id, amount):
        """
        Decrease value in Value File.

        INS = 0xDC
        """
        amount_bytes = to_4bytes(amount)

        apdu = [0x90, 0xDC, 0x00, 0x00, 0x05, file_id] + amount_bytes + [0x00]

        data, sw1, sw2 = self.card.transmit(apdu)

        print(f"Debit {amount} - Status: {sw1:02X} {sw2:02X}")
        return sw1 == 0x91 and sw2 == 0x00


    def get_value(self, file_id):
        """
        Retrieve current stored value.

        INS = 0x6C

        :return: Integer value or None
        """
        apdu = [0x90, 0x6C, 0x00, 0x00, 0x01, file_id, 0x00]
        data, sw1, sw2 = self.card.transmit(apdu)

        if sw1 == 0x91 and sw2 == 0x00:
            value = from_4bytes(data)
            print(f"Value: {value}")
            return value

        return None


    # ------------------------------------------------------------------
    # Transaction Management
    # ------------------------------------------------------------------

    def commit_transaction(self):
        """
        Commit all pending changes.

        INS = 0xC7
        """
        apdu = [0x90, 0xC7, 0x00, 0x00, 0x00]
        data, sw1, sw2 = self.card.transmit(apdu)

        print(f"Commit transaction - Status: {sw1:02X} {sw2:02X}")
        return sw1 == 0x91 and sw2 == 0x00


    def abort_transaction(self):
        """
        Abort all pending changes.

        INS = 0xA7
        """
        apdu = [0x90, 0xA7, 0x00, 0x00, 0x00]
        data, sw1, sw2 = self.card.transmit(apdu)

        print(f"Abort transaction - Status: {sw1:02X} {sw2:02X}")
        return sw1 == 0x91 and sw2 == 0x00

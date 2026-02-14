import unittest

class MockCard:
    """Mock DESFire card for testing purposes"""

    def transmit(self, apdu):
        # Test behavior based on INS byte
        ins = apdu[1]

        # Simulate GetApplicationIDs success
        if ins == 0x6A:
            # Return two fake AIDs (6 bytes total)
            return ([0x01, 0x00, 0x01, 0x02, 0x00, 0x02], 0x91, 0x00)

        # Simulate successful create/delete/change
        return ([], 0x91, 0x00)


class TestApplicationManager(unittest.TestCase):

    def setUp(self):
        self.mock_card = MockCard()
        self.manager = ApplicationManager(self.mock_card)


    def test_list_applications(self):
        """Test retrieving application IDs"""
        aids = self.manager.list_applications()

        self.assertEqual(len(aids), 2)
        self.assertEqual(aids[0], [0x01, 0x00, 0x01])
        self.assertEqual(aids[1], [0x02, 0x00, 0x02])


    def test_create_application_success(self):
        """Test successful application creation"""
        result = self.manager.create_application([0x01, 0x02, 0x03])

        self.assertTrue(result)

from unittest.mock import MagicMock, patch


class TestDesfireCard(unittest.TestCase):

    @patch("smartcard.System.readers")
    def test_select_application_success(self, mock_readers):
        """Test successful application selection"""

        # Mock connection
        mock_connection = MagicMock()
        mock_connection.transmit.return_value = ([], 0x91, 0x00)
        mock_connection.getATR.return_value = [0x01, 0x02]

        mock_reader = MagicMock()
        mock_reader.createConnection.return_value = mock_connection
        mock_readers.return_value = [mock_reader]

        card = DesfireCard()

        result = card.select_application([0x01, 0x02, 0x03])

        self.assertTrue(result)


    @patch("smartcard.System.readers")
    def test_format_card_success(self, mock_readers):
        """Test successful card formatting"""

        mock_connection = MagicMock()
        mock_connection.transmit.return_value = ([], 0x91, 0x00)
        mock_connection.getATR.return_value = [0x01, 0x02]

        mock_reader = MagicMock()
        mock_reader.createConnection.return_value = mock_connection
        mock_readers.return_value = [mock_reader]

        card = DesfireCard()

        result = card.format_card()

        self.assertTrue(result)


class TestFileManager(unittest.TestCase):

    def setUp(self):
        self.mock_card = MagicMock()
        self.file_manager = FileManager(self.mock_card)


    def test_list_files_success(self):
        """Test retrieving file IDs"""

        self.mock_card.transmit.return_value = ([0x01, 0x02, 0x05], 0x91, 0x00)

        files = self.file_manager.list_files()

        self.assertEqual(files, [0x01, 0x02, 0x05])
        self.assertEqual(len(files), 3)


    def test_create_standard_file_success(self):
        """Test successful standard file creation"""

        self.mock_card.transmit.return_value = ([], 0x91, 0x00)

        result = self.file_manager.create_standard_file(
            file_id=0x01,
            file_size=32
        )

        self.assertTrue(result)

if __name__ == "__main__":
    unittest.main()

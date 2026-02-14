# Desktop Logistics Tracking Application

A Python-based desktop application for supply chain logistics using MIFARE Classic 4K smart cards.

## Features

- **Role-Based Access Control**:
  - **Validator A (Sender)**: Create missions, write to card.
  - **Validator B (Receiver)**: Scan card, verify location, approve/reject delivery.
  - **Admin**: User management, mission tracking, audit logs.
- **Smart Card Integration**: Full read/write support for MIFARE Classic 4K using PC/SC.
- **Local Database**: SQLite storage for users, missions, and logs.
- **Audit Trail**: Comprehensive logging of all actions.

## Installation

1. Install system dependencies (for PCSC):
   - **Linux**: `sudo apt install pcscd libpcsclite1 git python3-pyqt5`
   
2. Install Python dependencies:
   ```bash
   pip install -r logistics_system/requirements.txt
   ```

## Usage

Run the application:
```bash
python3 logistics_system/main.py
```

### Credentials

| Role | Username | Password |
|------|----------|----------|
| **Admin** | `admin` | `admin123` |
| **Sender** | `validator_a` | `pass123` |
| **Receiver** | `validator_b` | `pass123` |

## Card Mapping (MIFARE Classic 4K)
- **Sector 2**: Driver Info (Name, License, ID)
- **Sector 3**: Mission Data (Origin, Destination, Status)
- **Sector 4+**: Manifest/Articles

## Development Structure
- `core/`: Business logic and hardware managers.
- `ui/`: PyQt5 interface classes.
- `models/`: Data classes.
- `data/`: SQLite database.

# PyCoin Blockchain

A simple blockchain cryptocurrency implementation in Python with a web interface.

## Features

- Basic blockchain with proof-of-work mining
- Transaction system with digital signatures
- Wallet functionality
- Decentralized consensus algorithm
- Web interface for easy interaction
- RESTful API for programmatic access

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/pycoin.git
cd pycoin
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the blockchain node:
```bash
python main.py -p 5000
```

2. Open your web browser and navigate to:
http://localhost:5000

## Web Interface

The web interface provides easy access to:
- Blockchain explorer
- Wallet management
- Transaction creation
- Block mining

## API Endpoints

- `GET /mine` - Mine a new block
- `POST /transactions/new` - Create a new transaction
- `GET /chain` - Get the full blockchain
- `POST /nodes/register` - Register new nodes
- `GET /nodes/resolve` - Resolve conflicts

## Development

To run the development server with debug mode:
```bash
python main.py -p 5000 --debug
```

## Author
Jason Alvarez

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
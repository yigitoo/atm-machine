# ATM Machine Simulation

A Python-based ATM (Automated Teller Machine) simulation that mimics basic banking operations.

## Features

- Account balance inquiry
- Cash withdrawal
- Cash deposit
- PIN verification
- See Card Details

## Installation

```bash
$ git clone https://github.com/yourusername/atm-machine.git
$ cd atm-machine
$ pip3 install -r requirements.txt
$ pip3 install -e .
```

## Usage

1. Run the Server and after that run client

```bash

$ python3 -m atm_machine.server.run
# create another terminal and write that:
$ python3 -m atm_machine.client.ui
```


2. Enter your PIN (default: 1234)
3. Select from available operations
4. Follow the on-screen instructions

## Dependencies

- Python 3.13

## Contributing

Pull requests are welcome. For major changes, please open an issue first.

## License

Our [LICENSE](LICENSE.md) is MIT License.

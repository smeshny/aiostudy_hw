# Uniswap ERC20 Swap Permit Signer

This project shows how to sign a typed message for an ERC20 swap permit on Uniswap.

## Prerequisites

- Python 3.10+
- Install required packages

## Setup

1. **Clone the repository:**

   ```bash
   git clone <repository-url>
   cd aiostudy_hw/T7_4
   ```

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Configuration:**

   - Set `NETWORK_TO_WORK`, `PRIVATE_KEY`, and `PROXY` in `settings.py`.
   - Define `TOKENS_PER_CHAIN` and `CONTRACTS_PER_CHAIN` in `config.py`.

## Usage

Run the script:

```bash
python main.py
```

## Description

- Initializes a client and connects to Uniswap.
- Signs a swap permit for an ERC20 token and prints the signature.

## Notes

- Ensure private key and network settings are correct.
- Designed for non-native tokens.

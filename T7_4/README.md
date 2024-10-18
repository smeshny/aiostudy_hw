# Configuration

1. **Environment Variables:**

   - `PRIVATE_KEY`: Your private key for the EVM wallet.
   - `PROXY`: Proxy settings if required.

   Set these variables in a `.env` file or directly in your environment.

2. **CapMonster Configuration:**

   Ensure you have a CapMonster account and have configured it to solve reCaptchaV2 challenges.

## Usage

To run the script, execute the following command:

```bash
python aiostudy_hw/T7_3/main.py
```

## Project Structure

- `aiostudy_hw/T7_3/main.py`: Main script to run the project.
- `client.py`: Handles client connections.
- `modules/movement_faucet.py`: Contains logic for interacting with the Movement faucet.
- `modules/capmonster.py`: Contains logic for CapMonster.
- `settings.py`: Configuration settings for the project.

## Troubleshooting

- **Server Error:** If you encounter a server error, it may be an issue with the faucet. Try again later.
- **Captcha Issues:** Ensure your CapMonster account is active and correctly configured.

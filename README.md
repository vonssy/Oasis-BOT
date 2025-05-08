# Oasis - Distribute.ai BOT
Oasis - Distribute.ai BOT

- Register Here : [Oasis - Distribute.ai](https://r.distribute.ai/vonssy)
- Use Code : vonssy

## Features

  - Auto Get Account Information
  - Auto Run With [Monosans](https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/all.txt) Proxy - Choose 1
  - Auto Run With Private Proxy - Choose 2
  - Auto Run Without Proxy - Choose 3
  - Auto Take Exiting Providers
  - Auto Create New Providers If Don't Have
  - Auto Connect and Reconnect Websocket
  - Support Running Multi Providers Each Accounts
  - Multi Accounts With Threads

### Note: A little advice, when running setup.py it is better to do it locally, not on vps or rdp. there is a high possibility of being banned, because oasis saves your session.

## Requiremnets

- Make sure you have Python3.9 or higher installed and pip.

## Instalation

1. **Clone The Repositories:**
   ```bash
   git clone https://github.com/vonssy/Oasis-BOT.git
   ```
   ```bash
   cd Oasis-BOT
   ```

2. **Install Requirements:**
   ```bash
   pip install -r requirements.txt #or pip3 install -r requirements.txt
   ```

## Configuration

- **proxy.txt:** You will find the `proxy.txt` file in the project directory. Make sure `proxy.txt` contains data that matches the format expected by the script. Here are examples of file formats:
  ```bash
    ip:port # Default Protcol HTTP.
    protocol://ip:port
    protocol://user:pass@ip:port
  ```

## Script

1. Setup - to create new providers or take exiting providers, the data will be saved to accounts.json.
```bash
python setup.py #or python3 setup.py
```

2. Run
```bash
python bot.py #or python3 bot.py
```

## Note

Save your provider ids because it's important.

## Buy Me a Coffee

- **EVM:** 0xe3c9ef9a39e9eb0582e5b147026cae524338521a
- **TON:** UQBEFv58DC4FUrGqinBB5PAQS7TzXSm5c1Fn6nkiet8kmehB
- **SOL:** E1xkaJYmAFEj28NPHKhjbf7GcvfdjKdvXju8d8AeSunf
- **SUI:** 0xa03726ecbbe00b31df6a61d7a59d02a7eedc39fe269532ceab97852a04cf3347

Thank you for visiting this repository, don't forget to contribute in the form of follows and stars.
If you have questions, find an issue, or have suggestions for improvement, feel free to contact me or open an *issue* in this GitHub repository.

**vonssy**
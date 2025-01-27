from aiohttp import (
    ClientResponseError,
    ClientSession,
    ClientTimeout
)
from aiohttp_socks import ProxyConnector
from fake_useragent import FakeUserAgent
from datetime import datetime
from colorama import *
import asyncio, json, random, os, pytz

wib = pytz.timezone('Asia/Jakarta')

class OasisAI:
    def __init__(self) -> None:
        self.headers = {
            "Accept": "*/*",
            "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "Origin": "https://dashboard.distribute.ai",
            "Referer": "https://dashboard.distribute.ai/",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "cross-site",
            "User-Agent": FakeUserAgent().random
        }
        self.proxies = []
        self.proxy_index = 0
        self.account_proxies = {}

    def clear_terminal(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def log(self, message):
        print(
            f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}{message}",
            flush=True
        )

    def welcome(self):
        print(
            f"""
        {Fore.GREEN + Style.BRIGHT}Auto Create Providers {Fore.BLUE + Style.BRIGHT}Oasis AI - BOT
            """
            f"""
        {Fore.GREEN + Style.BRIGHT}Rey? {Fore.YELLOW + Style.BRIGHT}<INI WATERMARK>
            """
        )

    def format_seconds(self, seconds):
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"
    
    async def load_proxies(self, use_proxy_choice: int):
        filename = "proxy.txt"
        try:
            if use_proxy_choice == 1:
                async with ClientSession(timeout=ClientTimeout(total=30)) as session:
                    async with session.get("https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/all.txt") as response:
                        response.raise_for_status()
                        content = await response.text()
                        with open(filename, 'w') as f:
                            f.write(content)
                        self.proxies = content.splitlines()
            else:
                if not os.path.exists(filename):
                    self.log(f"{Fore.RED + Style.BRIGHT}File {filename} Not Found.{Style.RESET_ALL}")
                    return
                with open(filename, 'r') as f:
                    self.proxies = f.read().splitlines()
            
            if not self.proxies:
                self.log(f"{Fore.RED + Style.BRIGHT}No Proxies Found.{Style.RESET_ALL}")
                return

            self.log(
                f"{Fore.GREEN + Style.BRIGHT}Proxies Total  : {Style.RESET_ALL}"
                f"{Fore.WHITE + Style.BRIGHT}{len(self.proxies)}{Style.RESET_ALL}"
            )
        
        except Exception as e:
            self.log(f"{Fore.RED + Style.BRIGHT}Failed To Load Proxies: {e}{Style.RESET_ALL}")
            self.proxies = []

    def check_proxy_schemes(self, proxies):
        schemes = ["http://", "https://", "socks4://", "socks5://"]
        if any(proxies.startswith(scheme) for scheme in schemes):
            return proxies
        return f"http://{proxies}"

    def get_next_proxy_for_account(self, email):
        if email not in self.account_proxies:
            if not self.proxies:
                return None
            proxy = self.check_proxy_schemes(self.proxies[self.proxy_index])
            self.account_proxies[email] = proxy
            self.proxy_index = (self.proxy_index + 1) % len(self.proxies)
        return self.account_proxies[email]

    def rotate_proxy_for_account(self, email):
        if not self.proxies:
            return None
        proxy = self.check_proxy_schemes(self.proxies[self.proxy_index])
        self.account_proxies[email] = proxy
        self.proxy_index = (self.proxy_index + 1) % len(self.proxies)
        return proxy
            
    def load_accounts(self):
        try:
            with open('accounts.json', 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return []
        except json.JSONDecodeError:
            return []

    def save_accounts(self, accounts):
        with open('accounts.json', 'w') as file:
            json.dump(accounts, file, indent=4)
        
    def generate_random_id(self, length=26):
        characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        return ''.join(random.choice(characters) for _ in range(length))
    
    def mask_account(self, account):
        if "@" in account:
            local, domain = account.split('@', 1)
            mask_account = local[:3] + '*' * 3 + local[-3:]
            return f"{mask_account}@{domain}"
        
        mask_account = account[:3] + '*' * 3 + account[-3:]
        return mask_account
    
    def print_message(self, email, proxy, color, message):
        self.log(
            f"{Fore.CYAN + Style.BRIGHT}[ Account:{Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT} {self.mask_account(email)} {Style.RESET_ALL}"
            f"{Fore.MAGENTA + Style.BRIGHT}-{Style.RESET_ALL}"
            f"{Fore.CYAN + Style.BRIGHT} Proxy: {Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT}{proxy}{Style.RESET_ALL}"
            f"{Fore.MAGENTA + Style.BRIGHT} - {Style.RESET_ALL}"
            f"{Fore.CYAN + Style.BRIGHT}Status:{Style.RESET_ALL}"
            f"{color + Style.BRIGHT} {message} {Style.RESET_ALL}"
            f"{Fore.CYAN + Style.BRIGHT}]{Style.RESET_ALL}"
        )

    def print_question(self):
        while True:
            try:
                print(f"{Fore.WHITE+Style.BRIGHT}1. Run With Auto Proxy{Style.RESET_ALL}")
                print(f"{Fore.WHITE+Style.BRIGHT}2. Run With Manual Proxy{Style.RESET_ALL}")
                print(f"{Fore.WHITE+Style.BRIGHT}3. Run Without Proxy{Style.RESET_ALL}")
                use_proxy = int(input(f"{Fore.BLUE+Style.BRIGHT}Choose [1/2/3] -> {Style.RESET_ALL}").strip())

                if use_proxy in [1, 2, 3]:
                    proxy_type = (
                        "With Auto Proxy" if use_proxy == 1 else 
                        "With Manual Proxy" if use_proxy == 2 else 
                        "Without Proxy"
                    )
                    print(f"{Fore.GREEN+Style.BRIGHT}Run {proxy_type} Selected.{Style.RESET_ALL}")
                    break
                else:
                    print(f"{Fore.RED+Style.BRIGHT}Please enter either 1, 2 or 3.{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED+Style.BRIGHT}Invalid input. Enter a number (1, 2 or 3).{Style.RESET_ALL}")

        while True:
            try:
                print(f"{Fore.WHITE+Style.BRIGHT}1. Generate New Providers{Style.RESET_ALL}")
                print(f"{Fore.WHITE+Style.BRIGHT}2. Take Exiting Providers{Style.RESET_ALL}")
                run_type = int(input(f"{Fore.BLUE+Style.BRIGHT}Choose [1/2/3] -> {Style.RESET_ALL}").strip())

                if run_type in [1, 2]:
                    opsion = (
                        "Generate New" if use_proxy == 1 else 
                        "Take Exiting"
                    )
                    print(f"{Fore.GREEN+Style.BRIGHT}{opsion} Providers Selected.{Style.RESET_ALL}")
                    break
                else:
                    print(f"{Fore.RED+Style.BRIGHT}Please enter either 1 or 2.{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED+Style.BRIGHT}Invalid input. Enter a number (1 or 2).{Style.RESET_ALL}")

        provider_count = 0
        if run_type == 1:
            while True:
                try:
                    provider_count = int(input(f"{Fore.BLUE+Style.BRIGHT}How Many Provider Do You Want To Create? -> {Style.RESET_ALL}"))
                    if provider_count > 0:
                        break
                    else:
                        print(f"{Fore.RED+Style.BRIGHT}Please enter a positive number.{Style.RESET_ALL}")
                except ValueError:
                    print(f"{Fore.RED+Style.BRIGHT}Invalid input. Enter a number.{Style.RESET_ALL}")

        return provider_count, run_type, use_proxy
    
    async def user_login(self, email: str, password: str, proxy=None):
        url = "https://api.oasis.ai/internal/auth/login"
        data = json.dumps({"email":email, "password":password, "rememberSession":True})
        headers = {
            **self.headers,
            "Content-Length": str(len(data)),
            "Content-Type": "application/json"

        }
        connector = ProxyConnector.from_url(proxy) if proxy else None
        try:
            async with ClientSession(connector=connector, timeout=ClientTimeout(total=60)) as session:
                async with session.post(url=url, headers=headers, data=data) as response:
                    response.raise_for_status()
                    result = await response.json()
                    return result['token']
        except (Exception, ClientResponseError) as e:
            return self.print_message(email, proxy, Fore.RED, f"GET Access Token Failed: {Fore.YELLOW+Style.BRIGHT}{str(e)}")
        
    async def create_providers(self, email: str, token: str, use_proxy: bool, proxy=None, retries=5):
        url = "https://api.oasis.ai/internal/auth/connect"
        data = json.dumps({"name":self.generate_random_id(), "platform":"headless"})
        headers = {
            **self.headers,
            "Authorization": token,
            "Content-Length": str(len(data)),
            "Content-Type": "application/json"

        }
        for attempt in range(retries):
            connector = ProxyConnector.from_url(proxy) if proxy else None
            try:
                async with ClientSession(connector=connector, timeout=ClientTimeout(total=60)) as session:
                    async with session.post(url=url, headers=headers, data=data) as response:
                        response.raise_for_status()
                        result = await response.json()
                        return result['token']
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue

                proxy = self.rotate_proxy_for_account(email) if use_proxy else None
                return self.print_message(email, proxy, Fore.RED, f"Create Providers Failed: {Fore.YELLOW+Style.BRIGHT}{str(e)}")
            
    async def provider_lists(self, email: str, token: str, proxy=None, retries=5):
        url = "https://api.oasis.ai/internal/provider/providers?limit=100"
        headers = {
            **self.headers,
            "Authorization": token,
            "Content-Type": "application/json"
        }
        for attempt in range(retries):
            connector = ProxyConnector.from_url(proxy) if proxy else None
            try:
                async with ClientSession(connector=connector, timeout=ClientTimeout(total=60)) as session:
                    async with session.get(url=url, headers=headers) as response:
                        response.raise_for_status()
                        result = await response.json()
                        return result['results']
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue

                return self.print_message(email, proxy, Fore.RED, f"GET Provider Lists Failed: {Fore.YELLOW+Style.BRIGHT}{str(e)}")
    
    async def provider_token(self, email: str, token: str, id: str, proxy=None, retries=5):
        url = f"https://api.oasis.ai/internal/provider/token?id={id}"
        headers = {
            **self.headers,
            "Authorization": token,
            "Content-Type": "application/json"
        }
        for attempt in range(retries):
            connector = ProxyConnector.from_url(proxy) if proxy else None
            try:
                async with ClientSession(connector=connector, timeout=ClientTimeout(total=60)) as session:
                    async with session.get(url=url, headers=headers) as response:
                        response.raise_for_status()
                        result = await response.json()
                        return result['token']
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue

                return self.print_message(email, proxy, Fore.RED, f"GET Provider Token Failed: {Fore.YELLOW+Style.BRIGHT}{str(e)}")
            
    async def process_accounts(self, email: str, password: str, provider_count: int, run_type: int, use_proxy: bool):
        proxy = self.get_next_proxy_for_account(email) if use_proxy else None
        token = None
        while token is None:
            token = await self.user_login(email, password, proxy)
            if not token:
                proxy = self.rotate_proxy_for_account(email) if use_proxy else None
                continue

            self.print_message(email, proxy, Fore.GREEN, "GET Access Token Success")

            success_count = 0
            
            accounts = self.load_accounts()

            account = next((acc for acc in accounts if acc["Email"] == email), None)
            if not account:
                account = {"Email": email, "Providers": []}
                accounts.append(account)

            if run_type == 1:
                for _ in range(provider_count):
                    provider_id = await self.create_providers(email, token, use_proxy, proxy)
                    if provider_id:
                        if not any(provider["Provider_ID"] == provider_id for provider in account["Providers"]):
                            account["Providers"].append({"Provider_ID": provider_id})
                        else:
                            self.print_message(email, proxy, Fore.WHITE, 
                                f"Provider ID {self.mask_account(provider_id)} "
                                f"{Fore.YELLOW + Style.BRIGHT}Already Exists. Skipping...{Style.RESET_ALL}"
                            )
                            continue

                        self.print_message(email, proxy, Fore.WHITE, 
                            f"Provider ID {self.mask_account(provider_id)} "
                            f"{Fore.GREEN + Style.BRIGHT}Have Been Created Successfully{Style.RESET_ALL}"
                        )
                        success_count += 1
                        proxy = self.rotate_proxy_for_account(email) if use_proxy else None
                        
                    await asyncio.sleep(1)

                self.save_accounts(accounts)
                self.print_message(email, proxy, Fore.GREEN, 
                    f"{success_count} "
                    f"{Fore.WHITE + Style.BRIGHT}of{Style.RESET_ALL}"
                    f"{Fore.BLUE + Style.BRIGHT} {provider_count} {Style.RESET_ALL}"
                    f"{Fore.CYAN + Style.BRIGHT}Have Been Created Successfully{Style.RESET_ALL}"
                )
            
            else:
                providers = await self.provider_lists(email, token, proxy)
                if providers:
                    for provider in providers:
                        id = provider['id']

                        provider_id = await self.provider_token(email, token, id, proxy)
                        if provider_id:
                            account["Providers"].append({"Provider_ID": provider_id})
                            success_count += 1

                    self.save_accounts(accounts)
                    self.print_message(email, proxy, Fore.GREEN, 
                        f"{success_count} "
                        f"{Fore.CYAN + Style.BRIGHT}of{Style.RESET_ALL}"
                        f"{Fore.BLUE + Style.BRIGHT} {len(providers)} {Style.RESET_ALL}"
                        f"{Fore.CYAN + Style.BRIGHT}Providers Have Been Saved Successfully{Style.RESET_ALL}"
                    )
    
    async def main(self):
        try:
            email = input(f"{Fore.WHITE+Style.BRIGHT}Enter Email    -> {Style.RESET_ALL}")
            password = input(f"{Fore.WHITE+Style.BRIGHT}Enter Password -> {Style.RESET_ALL}")

            provider_count, run_type, use_proxy_choice = self.print_question()

            use_proxy = False
            if use_proxy_choice in [1, 2]:
                use_proxy = True

            self.clear_terminal()
            self.welcome()

            if use_proxy:
                await self.load_proxies(use_proxy_choice)

            self.log(f"{Fore.CYAN + Style.BRIGHT}-{Style.RESET_ALL}"*75)

            await self.process_accounts(email, password, provider_count, run_type, use_proxy)

        except Exception as e:
            self.log(f"{Fore.RED+Style.BRIGHT}Error: {e}{Style.RESET_ALL}")

if __name__ == "__main__":
    try:
        bot = OasisAI()
        asyncio.run(bot.main())
    except KeyboardInterrupt:
        print(
            f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
            f"{Fore.RED + Style.BRIGHT}[ EXIT ] Oasis AI - BOT{Style.RESET_ALL}                                       "                              
        )
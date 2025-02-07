from aiohttp import (
    ClientSession,
    ClientTimeout
)
from aiohttp_socks import ProxyConnector
from fake_useragent import FakeUserAgent
from datetime import datetime
from colorama import *
import asyncio, json, uuid, random, os, pytz

wib = pytz.timezone('Asia/Jakarta')

class OasisAI:
    def __init__(self) -> None:
        self.headers = {
            "Accept-encoding": "gzip, deflate, br, zstd",
            "Accept-language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "Cache-control": "no-cache",
            "Connection": "Upgrade",
            "Host": "ws.oasis.ai",
            "Origin": "chrome-extension://knhbjeinoabfecakfppapfgdhcpnekmm",
            "Pragma": "no-cache",
            "Sec-Websocket-Extensions": "permessage-deflate; client_max_window_bits",
            "Sec-Websocket-Key": "O6keZ3H4BfgCab6U/l3moA==",
            "Sec-Websocket-Version": "13",
            "Upgrade": "websocket",
            "User-Agent": FakeUserAgent().random
        }
        self.proxies = []
        self.proxy_index = 0
        self.account_proxies = {}
        self.providers_estabilished = 0
        self.total_providers = 0

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
        {Fore.GREEN + Style.BRIGHT}Auto Ping {Fore.BLUE + Style.BRIGHT}Oasis AI - BOT
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

    def get_next_proxy_for_account(self, account):
        if account not in self.account_proxies:
            if not self.proxies:
                return None
            proxy = self.check_proxy_schemes(self.proxies[self.proxy_index])
            self.account_proxies[account] = proxy
            self.proxy_index = (self.proxy_index + 1) % len(self.proxies)
        return self.account_proxies[account]

    def rotate_proxy_for_account(self, account):
        if not self.proxies:
            return None
        proxy = self.check_proxy_schemes(self.proxies[self.proxy_index])
        self.account_proxies[account] = proxy
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

    def generate_random_gpu_info(self):
        renderers = [
            "ANGLE (AMD, AMD Radeon(TM) Graphics (0x00001638) Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (NVIDIA, GeForce GTX 1080 Ti Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (Intel, Iris Xe Graphics (0x00008086) Direct3D11 vs_5_0 ps_5_0, D3D11)"
        ]
        vendors = ["Google Inc. (AMD)", "NVIDIA", "Intel"]
        return {
            "renderer":random.choice(renderers),
            "vendor":random.choice(vendors)
        }
        
    def generate_random_memory_info(self):
        return {
            "availableCapacity":random.randint(1000000000, 2000000000),
            "capacity":random.randint(2000000000, 3000000000)
        }
    
    def generate_random_operating_system(self):
        os_list = [ "windows","linux","macOS"]
        return random.choice(os_list)

    def generate_random_machine_id(self):
        machine_id = str(uuid.uuid4().hex)
        return machine_id
    
    def generate_random_cpu_info(self):
        features = ["mmx", "sse", "sse2", "sse3", "ssse3", "sse4_1", "sse4_2", "avx"]
        cpu_models = [
            "AMD Ryzen 5 5600G with Radeon Graphics",
            "Intel Core i7-9700K",
            "AMD Ryzen 7 5800X",
            "Intel Core i9-10900K",
            "Intel Core i5-11600K",
            "AMD Ryzen 9 5900X",
            "Intel Core i7-12700K",
            "AMD Ryzen 5 3600X",
            "Intel Core i9-11900K",
            "AMD Ryzen 3 3200G"
        ]
        num_of_processors = random.choice([4, 8, 16, 32])

        processors = []
        for _ in range(num_of_processors):
            processors.append({
                "usage": {
                    "idle": random.randint(0, 2000000000000),
                    "kernel": random.randint(0, 10000000000),
                    "total": random.randint(0, 2000000000000),
                    "user": random.randint(0, 50000000000)
                }
            })

        return {
            "archName": "x86_64",
            "features": features,
            "modelName": random.choice(cpu_models),
            "numOfProcessors": num_of_processors,
            "processors": processors,
            "temperatures": []
        }
    
    def generate_random_id(self):
        characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        return ''.join(random.choice(characters) for _ in range(26))
    
    def generate_random_system_data(self):
        return {
            "type":"system",
            "data":{
                "gpuInfo":self.generate_random_gpu_info(),
                "memoryInfo":self.generate_random_memory_info(),
                "operatingSystem":self.generate_random_operating_system(),
                "machineId":self.generate_random_machine_id(),
                "cpuInfo":self.generate_random_cpu_info(),
            },
            "id":self.generate_random_id()
        }
    
    def mask_account(self, account):
        if "@" in account:
            local, domain = account.split('@', 1)
            mask_account = local[:3] + '*' * 3 + local[-3:]
            return f"{mask_account}@{domain}"
        
        mask_account = account[:3] + '*' * 3 + account[-3:]
        return mask_account

    def print_message(self, account, proxy, color, message):
        self.log(
            f"{Fore.CYAN + Style.BRIGHT}[ Account:{Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT} {self.mask_account(account)} {Style.RESET_ALL}"
            f"{Fore.MAGENTA + Style.BRIGHT}-{Style.RESET_ALL}"
            f"{Fore.CYAN + Style.BRIGHT} Proxy: {Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT}{proxy}{Style.RESET_ALL}"
            f"{Fore.MAGENTA + Style.BRIGHT} - {Style.RESET_ALL}"
            f"{Fore.CYAN + Style.BRIGHT}Status:{Style.RESET_ALL}"
            f"{color + Style.BRIGHT} {message} {Style.RESET_ALL}"
            f"{Fore.CYAN + Style.BRIGHT}]{Style.RESET_ALL}"
        )

    async def print_providers_estabilished(self):
        while True:
            print(
                f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
                f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                f"{Fore.GREEN + Style.BRIGHT}{self.providers_estabilished}{Style.RESET_ALL}"
                f"{Fore.CYAN + Style.BRIGHT} of {Style.RESET_ALL}"
                f"{Fore.BLUE + Style.BRIGHT}{self.total_providers}{Style.RESET_ALL}"
                f"{Fore.CYAN + Style.BRIGHT} Providers Connection Estabilished... {Style.RESET_ALL}",
                end="\r",
                flush=True
            )
            await asyncio.sleep(10)

    def print_question(self):
        while True:
            try:
                print("1. Run With Monosans Proxy")
                print("2. Run With Private Proxy")
                print("3. Run Without Proxy")
                choose = int(input("Choose [1/2/3] -> ").strip())

                if choose in [1, 2, 3]:
                    proxy_type = (
                        "Run With Monosans Proxy" if choose == 1 else 
                        "Run With Private Proxy" if choose == 2 else 
                        "Run Without Proxy"
                    )
                    print(f"{Fore.GREEN + Style.BRIGHT}{proxy_type} Selected.{Style.RESET_ALL}")
                    return choose
                else:
                    print(f"{Fore.RED + Style.BRIGHT}Please enter either 1, 2 or 3.{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED + Style.BRIGHT}Invalid input. Enter a number (1, 2 or 3).{Style.RESET_ALL}")
            
    async def connect_websocket(self, email: str, provider_id: str, use_proxy: bool, proxy=None):
        wss_url = f"wss://ws.oasis.ai/?token={provider_id}&version=0.1.20&platform=extension"
        connected = False

        while True:
            connector = ProxyConnector.from_url(proxy) if proxy else None
            session = ClientSession(connector=connector, timeout=ClientTimeout(total=60))
            try:
                async with session.ws_connect(wss_url, headers=self.headers) as wss:
                    async def send_heartbeat():
                        while True:
                            heartbeat_data = {
                                "type": "heartbeat",
                                "data": {
                                    "version":"0.1.20",
                                    "mostRecentModel":"unknown",
                                    "status":"active",
                                    "inferenceState":True
                                },
                                "id":self.generate_random_id()
                            }
                            await wss.send_json(heartbeat_data)
                            self.print_message(email, proxy, Fore.WHITE, 
                                f"Provider {self.mask_account(provider_id)}"
                                f"{Fore.MAGENTA + Style.BRIGHT} - {Style.RESET_ALL}"
                                f"{Fore.GREEN + Style.BRIGHT}Sent Heartbeat Success{Style.RESET_ALL}"
                            )
                            await asyncio.sleep(60)
   
                    if not connected:
                        system_data = self.generate_random_system_data()
                        await wss.send_json(system_data)
                        self.print_message(email, proxy, Fore.WHITE, 
                            f"Provider {self.mask_account(provider_id)}"
                            f"{Fore.MAGENTA + Style.BRIGHT} - {Style.RESET_ALL}"
                            f"{Fore.GREEN + Style.BRIGHT}Websocket Is Connected{Style.RESET_ALL}"
                        )
                        connected = True
                        self.providers_estabilished += 1
                        send_ping = asyncio.create_task(send_heartbeat())

                    while connected:
                        try:
                            response = await wss.receive_json()
                            if response.get("type") == "updateSchedule":
                                self.print_message(email, proxy, Fore.WHITE, 
                                    f"Provider {self.mask_account(provider_id)}"
                                    f"{Fore.MAGENTA + Style.BRIGHT} - {Style.RESET_ALL}"
                                    f"{Fore.BLUE + Style.BRIGHT}Schedule Updated{Style.RESET_ALL}"
                                )

                            elif response.get("type") == "serverMetrics":
                                credits_earned = response["data"].get("creditsEarned")
                                total_uptime = response["data"].get("totalUptime")
                                self.print_message(email, proxy, Fore.WHITE, 
                                    f"Provider {self.mask_account(provider_id)}"
                                    f"{Fore.MAGENTA + Style.BRIGHT} - {Style.RESET_ALL}"
                                    f"{Fore.CYAN + Style.BRIGHT}Earning:{Style.RESET_ALL}"
                                    f"{Fore.WHITE + Style.BRIGHT} {credits_earned} PTS {Style.RESET_ALL}"
                                    f"{Fore.MAGENTA + Style.BRIGHT}-{Style.RESET_ALL}"
                                    f"{Fore.CYAN + Style.BRIGHT} Uptime: {Style.RESET_ALL}"
                                    f"{Fore.WHITE + Style.BRIGHT}{total_uptime}{Style.RESET_ALL}"
                                )

                            elif response.get("type") == "acknowledged":
                                self.print_message(email, proxy, Fore.WHITE, 
                                    f"Provider {self.mask_account(provider_id)}"
                                    f"{Fore.MAGENTA + Style.BRIGHT} - {Style.RESET_ALL}"
                                    f"{Fore.BLUE + Style.BRIGHT}System Updated{Style.RESET_ALL}"
                                )

                            elif response.get("type") == "error" and response["data"].get("code") == "Invalid body":
                                system_data = self.generate_random_system_data()
                                await wss.send_json(system_data)
                                self.print_message(email, proxy, Fore.WHITE, 
                                    f"Provider {self.mask_account(provider_id)}"
                                    f"{Fore.MAGENTA + Style.BRIGHT} - {Style.RESET_ALL}"
                                    f"{Fore.YELLOW + Style.BRIGHT}Invalid Body{Style.RESET_ALL}"
                                )

                        except Exception as e:
                            self.print_message(email, proxy, Fore.WHITE, 
                                f"Provider {self.mask_account(provider_id)} "
                                f"{Fore.MAGENTA + Style.BRIGHT}-{Style.RESET_ALL}"
                                f"{Fore.YELLOW + Style.BRIGHT} Websocket Connection Closed: {Style.RESET_ALL}"
                                f"{Fore.RED + Style.BRIGHT}{str(e)}{Style.RESET_ALL}"
                            )
                            if send_ping:
                                send_ping.cancel()
                                try:
                                    await send_ping
                                except asyncio.CancelledError:
                                    self.print_message(email, proxy, Fore.WHITE, 
                                        f"Provider {self.mask_account(provider_id)}"
                                        f"{Fore.MAGENTA + Style.BRIGHT} - {Style.RESET_ALL}"
                                        f"{Fore.YELLOW + Style.BRIGHT}Sent Heartbeat Cancelled{Style.RESET_ALL}"
                                    )

                            connected = False
                            self.providers_estabilished -= 1
                            await asyncio.sleep(5)
                            break

            except Exception as e:
                self.print_message(email, proxy, Fore.WHITE, 
                    f"Provider {self.mask_account(provider_id)} "
                    f"{Fore.MAGENTA + Style.BRIGHT}-{Style.RESET_ALL}"
                    f"{Fore.RED + Style.BRIGHT} Websocket Not Connected: {Style.RESET_ALL}"
                    f"{Fore.YELLOW + Style.BRIGHT}{str(e)}{Style.RESET_ALL}"
                )
                proxy = self.rotate_proxy_for_account(provider_id) if use_proxy else None
                await asyncio.sleep(5)

            except asyncio.CancelledError:
                self.print_message(email, proxy, Fore.WHITE, 
                    f"Provider {self.mask_account(provider_id)}"
                    f"{Fore.MAGENTA + Style.BRIGHT} - {Style.RESET_ALL}"
                    f"{Fore.YELLOW + Style.BRIGHT}Websocket Closed{Style.RESET_ALL}"
                )
                break
            finally:
                await session.close()
        
    async def process_accounts(self, email: str, providers: list, use_proxy: bool):
        tasks = []
        for provider in providers:
            if provider:
                provider_id = provider.get("Provider_ID")
                proxy = self.get_next_proxy_for_account(provider_id) if use_proxy else None
                tasks.append(self.connect_websocket(email, provider_id, use_proxy, proxy))
        
        await asyncio.gather(*tasks)
    
    async def main(self):
        try:
            accounts = self.load_accounts()
            if not accounts:
                self.log(f"{Fore.RED}No Accounts Loaded.{Style.RESET_ALL}")
                return

            use_proxy_choice = self.print_question()

            use_proxy = False
            if use_proxy_choice in [1, 2]:
                use_proxy = True

            self.clear_terminal()
            self.welcome()
            self.log(
                f"{Fore.GREEN + Style.BRIGHT}Account's Total: {Style.RESET_ALL}"
                f"{Fore.WHITE + Style.BRIGHT}{len(accounts)}{Style.RESET_ALL}"
            )

            if use_proxy:
                await self.load_proxies(use_proxy_choice)

            self.log(f"{Fore.CYAN + Style.BRIGHT}-{Style.RESET_ALL}"*75)

            while True:
                tasks = []
                for account in accounts:
                    email = account.get('Email')
                    providers = account.get('Providers', [])

                    if email and providers:
                        tasks.append(self.process_accounts(email, providers, use_proxy))
                        self.total_providers += len(providers)

                tasks.append(self.print_providers_estabilished())
                await asyncio.gather(*tasks)
                await asyncio.sleep(10)

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
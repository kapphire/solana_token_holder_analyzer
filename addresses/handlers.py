import requests
import json
from collections import defaultdict

class SolanaTokenAnalyzer:
    def __init__(self, token_mint_address):
        self.token_mint_address = token_mint_address
        self.rpc_url = "https://empty-billowing-wind.solana-mainnet.quiknode.pro/92932022ff7bf4dd95a0eeb9e66cd11157b20900/"
        self.headers = {"Content-Type": "application/json"}
        self.holder_data = defaultdict(lambda: {"quantities": [], "percentages": []})

    def get_token_largest_accounts(self):
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "getTokenLargestAccounts",
            "params": [self.token_mint_address]
        }
        try:
            response = requests.post(self.rpc_url, headers=self.headers, data=json.dumps(payload))
            response.raise_for_status()
            result = response.json()
            return result.get("result", {}).get("value", [])
        except requests.exceptions.RequestException as e:
            return []

    def get_token_total_supply(self):
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "getTokenSupply",
            "params": [self.token_mint_address]
        }
        try:
            response = requests.post(self.rpc_url, headers=self.headers, data=json.dumps(payload))
            response.raise_for_status()
            result = response.json()
            return int(result.get("result", {}).get("value", {}).get("amount", 0))
        except requests.exceptions.RequestException as e:
            return 0

    def update_holder_data(self):
        largest_accounts = self.get_token_largest_accounts()
        total_supply = self.get_token_total_supply()
        if not largest_accounts or not total_supply:
            return

        # max_length = max(len(data["quantities"]) for data in self.holder_data.values()) if self.holder_data else 0

        for account in largest_accounts:
            address = account.get("address")
            amount = int(account.get("amount"))
            percentage = round((amount / total_supply) * 100, 2)

            # if address not in self.holder_data:
            #     self.holder_data[address]["quantities"] = [0] * max_length
            #     self.holder_data[address]["percentages"] = [0] * max_length

            self.holder_data[address]["quantities"].append(amount)
            self.holder_data[address]["percentages"].append(percentage)

        # for data in self.holder_data.values():
        #     while len(data["quantities"]) < max_length + 1:
        #         data["quantities"].append(0)
        #         data["percentages"].append(0)

        return self.holder_data
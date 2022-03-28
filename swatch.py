import random
import requests
from bs4 import BeautifulSoup
import json
from discord_webhook import DiscordEmbed, DiscordWebhook
import os
from time import sleep

user_agents = ["Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.1331.54 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 UBrowser/6.1.2909.1022 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 UBrowser/6.1.2909.1022 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 UBrowser/6.0.1471.813 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 UBrowser/6.1.2015.1007 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 UBrowser/6.1.2107.204 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 UBrowser/6.1.2909.1213 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 UBrowser/6.0.1308.1016 Safari/420815",
                    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 UBrowser/6.1.2015.1007 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 UBrowser/6.1.2909.1022 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 UBrowser/6.1.2015.1007 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 UBrowser/6.0.1471.914 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 UBrowser/6.1.2015.1007 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 UBrowser/6.1.2909.1022 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.18 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.87 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.87 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.94 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.94 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.94 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.94 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.94 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.94 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.95 Safari/537.36 Core/1.50.1659.400 QQBrowser/9.5.9570.400",
                    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.95 Safari/537.36 Core/1.50.1659.400 QQBrowser/9.5.9769.400",
                    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2683.0 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2683.0 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2683.0 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36 OPR/38.0.2220.41",
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.47 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.63 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.63 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.63 Safari/537.36 OPR/38.0.2220.29",
                    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36"]

class SwatchBot:
    
    def __init__(self, task_options : dict, delay : int, webhook_link : str, task_number : int, proxies : list) -> None:
        self.task_options = task_options
        self.delay = delay
        self.webhook_link = webhook_link
        self.task_number = task_number
        self.proxies = proxies
        self.user_agent = {"user-agent": user_agents[random.randint(0, len(user_agents) - 1)]}
        pass

    def atc(self, session : requests.Session, pid : str) -> str:
        token = "" 
        try:
            fetch = session.get("https://www.swatch.com", headers=self.user_agent)
            if fetch.ok:
                soup = BeautifulSoup(fetch.text, features="html.parser")
                token_brut = soup.find("div", {"data-token-name": "csrf_token"})
                token = token_brut["data-token-value"]
                payload_atc = {"pid": pid, "quantity": 1, "options": [], "csrf_token": token}
                add_to_cart = session.post("https://www.swatch.com/on/demandware.store/Sites-swarp-EU-Site/fr_FR/Cart-AddProduct", headers=self.user_agent, data=payload_atc)
                if add_to_cart.ok:
                    print(f"[Task {self.task_number}] : Successfully added to cart !")
                    return True, token
                elif add_to_cart.status_code == 429:
                    print(f"[Task {self.task_number}] : Error adding to cart, rate limit. Rotating proxy")
                    return False, None
                else:
                    print(f"[Task {self.task_number}] : Error adding to cart.")
                    return False, None

        except Exception as e:
            print(f"[Task {self.task_number}] : Error adding to cart : ", e)
            return False, None

    def shipping(self, session : requests.Session, token : str, config : dict) -> bool:
        try:
            payload_shipping = {
                        "email": config["email"],
                        "title": config["title"],
                        "firstName": config["first_name"],
                        "lastName": config["last_name"],
                        "company": "",
                        "address1": config["addy1"],
                        "address2": config["addy2"],
                        "countryCode": config["country"],
                        "city": config["city"],
                        "postalCode": config["zip_code"],
                        "phone": config["phone"],
                        "mobilePhone": "",
                        "isBillingForm": "true",
                        "csrf_token": token
                    }
            update_shipping = session.post("https://www.swatch.com/on/demandware.store/Sites-swarp-EU-Site/fr_FR/CheckoutShippingServices-UpdateShippingMethodsList", headers=self.user_agent, data=payload_shipping)
            if update_shipping.ok:
                print(f"[Task {self.task_number}] : Shipping [1/3] : OK")
                payload_submit_shipping = {
                    "dwfrm_billing_email": config["email"],
                    "dwfrm_billing_title": config["title"],
                    "dwfrm_billing_firstName": config["first_name"],
                    "dwfrm_billing_lastName": config["last_name"],
                    "dwfrm_billing_company": "",
                    "dwfrm_billing_address1": config["addy1"],
                    "dwfrm_billing_address2": config["addy2"],
                    "dwfrm_billing_countryCode": config["country"],
                    "dwfrm_billing_city": config["city"],
                    "dwfrm_billing_postalCode": config["zip_code"],
                    "dwfrm_billing_phone": config["phone"],
                    "dwfrm_billing_mobilePhone": "",
                    "csrf_token": token
                }
                submit_shipping = session.post("https://www.swatch.com/on/demandware.store/Sites-swarp-EU-Site/fr_FR/CheckoutServices-SubmitBilling", headers=self.user_agent, data=payload_submit_shipping)
                if submit_shipping.ok:
                    print(f"[Task {self.task_number}] : Shipping [2/3] : OK")
                    payload_last_shipping = {
                        "dwfrm_shipping_shippingMethodID": "STANDARD-FR",
                        "differentShipmentAddress": "",
                        "dwfrm_shipping_title": config["title"],
                        "dwfrm_shipping_firstName": "",
                        "dwfrm_shipping_lastName": "",
                        "dwfrm_shipping_company": "",
                        "dwfrm_shipping_address1": "",
                        "dwfrm_shipping_address2": "",
                        "dwfrm_shipping_countryCode": config["country"],
                        "dwfrm_shipping_city": "",
                        "dwfrm_shipping_postalCode": "",
                        "dwfrm_shipping_isGift": "",
                        "dwfrm_shipping_giftMessage": "",
                        "dwfrm_giftWrapping_isGift": "",
                        "dwfrm_giftWrapping_from": "",
                        "dwfrm_giftWrapping_to": "",
                        "dwfrm_giftWrapping_message": "",
                        "csrf_token": token
                    }
                    submit_last_shipping = session.post("https://www.swatch.com/on/demandware.store/Sites-swarp-EU-Site/fr_FR/CheckoutShippingServices-SubmitShipping", headers=self.user_agent, data=payload_last_shipping)
                    if submit_last_shipping.ok:
                        print(f"[Task {self.task_number}] : Shipping [3/3] : OK")
                        return True
                    else:
                        self.shipping(session, token)
                else:
                    self.shipping(session, token)       
            else:
                self.shipping(session, token)
        except Exception as e:
            print(f"[Task {self.task_number}] : Error updating shipping : ", e)
            return False


    def payment(self, session : requests.Session, token : str):
        try:
            payload_payment = {
                    "paymentData" : json.dumps({"ID":"PAYPAL_DATATRANS","name":"PayPal","processor":"DATATRANS","description":None,"adyenData":None,"legalContentId":None,"image":"","disabled":False,"showAffirmPromo":False}, separators=(",", ":")),
                    "csrf_token": token
                }
            cookie_payment = {
                "accept": "application/json",
                "accept-encoding": "gzip, deflate, br",
                "accept-language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
                "content-length": "471",
                "content-type": "application/x-www-form-urlencoded",
                "dnt": "1",
                "origin": "https://www.swatch.com",
                "referer": "https://www.swatch.com/fr-fr/no-referrer",
                "sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"',
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": '"Windows"',
                "sec-fetch-dest": "empty",
                "sec-fetch-mode": "same-origin",
                "sec-fetch-site": "same-origin",
                "user-agent": self.user_agent["user-agent"]
            }
            update_payment = session.post("https://www.swatch.com/on/demandware.store/Sites-swarp-EU-Site/fr_FR/CheckoutServices-UpdatePaymentMethod", headers=cookie_payment, data=payload_payment)
            if update_payment.ok:
                print(f"[Task {self.task_number}] : Billing [1/3] : OK")
                payload_submit_payment = {
                    "dwfrm_payment_paymentMethod": "PAYPAL_DATATRANS",
                    "csrf_token": token
                }
                submit_payment = session.post("https://www.swatch.com/on/demandware.store/Sites-swarp-EU-Site/fr_FR/CheckoutServices-SubmitPayment", headers=self.user_agent, data=payload_submit_payment)
                if submit_payment.ok:
                    print(f"[Task {self.task_number}] : Billing [2/3] : OK")
                    payload_create_order = {
                    "paymentMethodID": "PAYPAL_DATATRANS",
                    "customerBirthday": "1899-12-31",
                    "csrf_token": token
                    }
                    create_order = session.post("https://www.swatch.com/on/demandware.store/Sites-swarp-EU-Site/fr_FR/Datatrans-CreateOrder", headers=self.user_agent, data=payload_create_order)
                    if create_order.ok:
                        json_resp = json.loads(create_order.text)
                        try:
                            config_payment = json_resp["datatransConfig"]
                            print(f"[Task {self.task_number}] : Billing [3/3] : OK")
                            req = requests.Request(method="GET", url="https://pay.datatrans.com/upp/jsp/upStart.jsp", params=config_payment)
                            prepared_request = req.prepare()
                            print(f"[Task {self.task_number}] : Successfully Checkout !")
                            return True, config_payment, prepared_request.url
                        except KeyError:
                            print(f"[Task {self.task_number}] : Error creating order, you must be rate limited. Sleeping 20 seconds")
                            sleep(20)
                            self.payment(session, token)
                    else:
                        self.payment(session, token)
                else:
                    self.payment(session, token)       
            else:
                self.payment(session, token)
        except Exception as e:
            print(f"[Task {self.task_number}] : Error updating billing : ", e)
            return False, None, None


    def send_webhook(self, config : dict, link : str, webhook_link : str):
        embed = DiscordEmbed(title=config["cdm_item_1_productName"] + " " + config["cdm_item_1_productSKU"], color="a0a0a0")
        embed.set_timestamp()
        embed.set_thumbnail(url=f'https://static.swatch.com/images/product/{self.task_options["pid"]}/sa000/{self.task_options["pid"]}_sa000_er003.png')
        embed.set_description("**Successfully Checked Out !**")
        embed.add_embed_field(name="Prix", value=f'{str(config["cdm_purchaseTotals_grandTotalAmount"])[:-2] + "€"}')
        embed.set_footer(text="Swatch Bot", icon_url="https://pbs.twimg.com/profile_images/1319740969059835907/6mOvjkfs_400x400.jpg")
        webhook = DiscordWebhook(url=webhook_link, username="Swatch Bot", avatar_url="https://pbs.twimg.com/profile_images/1319740969059835907/6mOvjkfs_400x400.jpg")
        webhook.add_embed(embed)
        with open("link.txt", "w+", encoding="utf-8") as link_file:
            link_file.write(link)
        with open("link.txt", "r", encoding="utf-8") as link_file:
            webhook.add_file(link_file.read(), filename="Checkout URL.txt")
        try:
            resp = webhook.execute(remove_embeds=True, remove_files=True)
            os.remove("link.txt")
            if resp.ok:
                return True, None 
            else:
                return False, f"[Task {self.task_number}] : {resp}"
        except Exception as e:
            print(f"[Task {self.task_number}] : Error sending webhook ! {e}")
            return False, None

    def start_task(self) -> None:
        try:
            with requests.Session() as s:
                if self.proxies != []:
                    s.proxies.update(self.proxies[random.randint(0, len(self.proxies) - 1)])
                isAdded, token = self.atc(s, self.task_options["pid"])
                if not isAdded:
                    self.start_task()
                else:
                    if token != "":
                        shipping = self.shipping(s, token, self.task_options)
                        if shipping:
                            isGood, informations, link = self.payment(s, token)
                            if isGood:
                                self.send_webhook(informations, link, self.webhook_link)
                            else:
                                self.start_task()
                        else:
                            self.start_task()
                    else:
                        self.start_task
        except Exception as e:
            print(f"[Task {self.task_number}] : Unexpected Error ({e})")
            self.start_task()
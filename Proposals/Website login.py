import requests
from time import sleep
import json
import re
from datetime import datetime
import pprint
from bs4 import BeautifulSoup

pp = pprint.PrettyPrinter(indent=4)

Account = {'Username':'c2946035@trbvn.com','Password':'Facebook!123'}

output = open("oauthtest_out.html", 'w')
msg = 'ok'
orderNumber = 'unknown'
headers = {'Host':'secure.m.newegg.com',
                        'User-Agent': 'Mozilla/5.0 (Linux; Android 4.4.2; GT-I9505 Build/KOT4H9) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.59 Mobile Safari/537.36', 
                        'Accept':'/',
                        'Accept-Language':'en-US,en;q=0.5',
                        'Accept-Encoding':'gzip, deflate, br',
                        'Connection':'keep-alive', 
                        'Pragma':'no-cache',
                        'Cache-Control':'no-cache'}

with requests.Session() as s:
        s.headers.update(headers)
        try:
                html = s.get("https://secure.newegg.com/NewMyAccount/AccountLogin.aspx", headers={'Referer':'http://www.newegg.com/'}, verify=True, timeout=300)
        except Exception as e:
                print("Failed to get login page")
                cleanHTMLOut(html.text, output)
                raise Exception("2) Failed to get the login page: " + str(e))
        if True:
                # token = valToken['value']
                credentials = {"UserName": Account['Username'], 
                                                "Password": Account['Password'],
                                                "Url":"http://m.newegg.com/",
                                                'ForCheckOut':'False',
                                                'Gvi':'',
                                                'RememberMe':'false',
                                                'historylength': '1',
                                                'walletStatus':'False',
                                                'IsShowCaptcha':'False' 
                                                }
                try:
                        # html = s.post("https://secure.m.newegg.com/Account/login", data = credentials, headers=headers, verify=False, timeout=300)
                        html = s.post("https://secure.newegg.com/NewMyAccount/AccountLogin.aspx", data = credentials, verify=False, timeout=300)
                        #print(html.request.headers)
                except Exception as e:
                        print("Failed to post login")
                        cleanHTMLOut(html.text, output)
                        raise Exception("3) Failed to Login: " + str(e))

                try:
                        html = s.get("https://secure.newegg.com/NewMyAccount/DashBoard.aspx", headers=headers, verify=False, timeout=300)
                except Exception as e:
                        print("Failed to get the AccountFull page")
                        cleanHTMLOut(html.text, output)
                        raise Exception("4) Failed to get the AccountFull page: " + str(e))
                soup = BeautifulSoup(html.text)
                logInSpan = soup.find('button',{'class':'logout'})
                if logInSpan:
                        if logInSpan.text != 'Sign Out':
                                print("Failed to find signout button.")

                        else:
                                print("Success!")
				
def cleanHTMLOut(htmlText, output):
	outText = ""
	for ht in htmlText:
		try:
			ht.encode("ascii")
		except:
			pass
		else:
			outText += ht
	output.write(outText)
	output.flush()




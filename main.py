from bs4 import BeautifulSoup
import requests
import lxml
import smtplib
import os

URL = "https://www.amazon.in/American-Tourister-AMT-SCH-02/dp/B07CJCGBVC?ref_=Oct_d_oup_d_2917436031&pd_rd_w=mo0af&content-id=amzn1.sym.cd95f89a-16eb-466e-94f2-c7a8ec8c5c6c&pf_rd_p=cd95f89a-16eb-466e-94f2-c7a8ec8c5c6c&pf_rd_r=EV273RQY2A1F6K4Y5DTJ&pd_rd_wg=3P3ll&pd_rd_r=3235f80e-6e80-4098-b0d8-38182755bc2f&pd_rd_i=B07CJCGBVC"

header = {
    "Accept-Language": os.environ["ACCEPT_LANG"],
    "User-Agent": os.environ["USER_AGENT"],
}

response = requests.get(URL, headers=header)
# print(response.text)

soup = BeautifulSoup(response.text, "lxml")
price = soup.find("span", class_="a-offscreen").text
# print(price)
price_number = float(price.split("₹")[1])
# print(price_number)
product_title = soup.select_one(".a-size-large").text.split("(")[0]

username = "aashishmalik3105@gmail.com"
pasw = os.environ["PASSWORD"]
message = f"Subject: Low Price Alert: {price_number} Rupees for {product_title} \n {product_title}'s price is dropped to {price_number} rupees.\nClick below to buy now:\n{URL} "

connection = smtplib.SMTP(host="smtp.gmail.com", port=587)
connection.starttls()
connection.login(user=username, password=pasw)
if price_number <= 700:
    try:
        # Sending email to myself.
        connection.sendmail(
            from_addr=username,
            to_addrs=username,
            msg=message
        )
        print("Successfully sent email")
    except smtplib.SMTPException:
        print("Error: unable to send email")
    finally:
        connection.quit()
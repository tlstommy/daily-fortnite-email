
import requests,json,smtplib, ssl
from emailAuth import email,emailPass
from emailData import emailList
from datetime import date
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
itemsJson = []
itemShop = []

print("running!")
def getShopJson():
    itemsJson.clear()
    itemShop.clear()
    apiEndpoint = "https://fortnite-api.com/v2/shop/br/"
    shop = requests.get(apiEndpoint).json()

    jData = json.dumps(shop, indent=4)
    with open("shopData.json", "w") as writeFile:
        writeFile.write(jData)
    writeFile.close()
   
   
    f = open("shopData.json")
    data = json.load(f)
    f.close()

    try:

        for i in range(len(data["data"]["daily"]["entries"])):
            for key in data["data"]["daily"]["entries"][i]["items"]:
                if key in itemsJson:
                    continue
                else:
                    itemsJson.append(key)
        for i in range(len(data["data"]["specialFeatured"]["entries"])):
            for key in data["data"]["specialFeatured"]["entries"][i]["items"]:
                if key in itemsJson:
                    continue
                else:
                    itemsJson.append(key)

        for i in range(len(data["data"]["featured"]["entries"])):
            for key in data["data"]["featured"]["entries"][i]["items"]:
                if key in itemsJson:
                    continue
                else:
                    itemsJson.append(key)
    except:
        itemsJson.append("Error (api server is down)")

def createEmailJson():
    htmlEmailParts = []
    itemShop = []
    for entry in itemsJson:
        print(entry)
        if(entry == "Error (api server is down)"):
            htmlEmailParts.append(entry)
            break
        name = entry["name"]
        description = entry["description"]
        entryType = entry["type"]["displayValue"]
        rarity = entry["rarity"]["displayValue"]
        imageUrl = entry["images"]["icon"]


        itemDict = {
            "name":name,
            "description":description,
            "type":entryType,
            "rarity":rarity,
            "image":imageUrl
        }
        itemShop.append(itemDict)

        htmlPart = """\
            <br>
            <img src="{imageUrl}" alt="{itemName}">
            <br>
            <p>Name: {itemName}<br>
            Type: {entryType}<br>
            Rarity: {rarity}<br>
            Description: {description}<br>
            <hr>
            </p>
            """.format(imageUrl=imageUrl,itemName=name,entryType=entryType,rarity=rarity,description=description)
        htmlEmailParts.append(htmlPart)

    port = 465 #SSL
    # Create a secure SSL context
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(email, emailPass)
        for recvEmail in emailList:

            message = MIMEMultipart("alternative")
            message["Subject"] = "Fortnite Item Shop - " + str(date.today().strftime("%m/%d/%Y"))
            message["From"] = email
            message["To"] = recvEmail  

            plainTextEmail= "succes plain text"
            htmlEmail = """\
            <html>
            <body>
            <br>
            <h1>Fortnite Item Shop {todaysDate}</h1>
            <br>
            <hr>
            """.format(todaysDate=date.today().strftime("%m/%d/%Y"))

            for item in htmlEmailParts:
               htmlEmail = htmlEmail + item


            #add more stuff here, such as random meme etc!
            htmlEmail = htmlEmail + """\
            <br>
            <hr>
            <p><small>This is an automated email sent out everyday at 12:10 AM UTC </small></p>
            </body>
            </html>""".format(currentdate = date.today().strftime("%m/%d/%Y"))

            # Turn these into plain/html objects
            part1 = MIMEText(plainTextEmail, "plain")
            part2 = MIMEText(htmlEmail, "html")
                       
            message.attach(part1)
            message.attach(part2)
           
            server.sendmail(email, recvEmail, message.as_string())

   
getShopJson()
createEmailJson() 
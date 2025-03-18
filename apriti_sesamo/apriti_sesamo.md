This one was pretty tricky. I looked at the hints, which said to look at the backup files and that the author was a "militant emacs user". I looked up "emacs backup files", and found that they were stored with a tilda `~` at the end.

I looked at /impossibleLogin.php~, and seems like the author left some comments.
```php
if(isset($_POST[base64_decode("\144\130\x4e\154\x63\155\x35\x68\142\127\125\x3d")])&& isset($_POST[base64_decode("\143\x48\x64\x6b")])){$yuf85e0677=$_POST[base64_decode("\144\x58\x4e\154\x63\x6d\65\150\x62\127\x55\75")];$rs35c246d5=$_POST[base64_decode("\143\x48\144\153")];if($yuf85e0677==$rs35c246d5){echo base64_decode("\x50\x47\112\x79\x4c\172\x35\x47\x59\127\154\163\132\127\x51\x68\111\x45\x35\166\x49\x47\132\163\131\127\x63\x67\x5a\155\71\171\111\x48\x6c\166\x64\x51\x3d\x3d");}else{if(sha1($yuf85e0677)===sha1($rs35c246d5)){echo file_get_contents(base64_decode("\x4c\151\64\166\x5a\x6d\x78\x68\x5a\x79\65\60\145\110\x51\75"));}else{echo base64_decode("\x50\107\112\171\x4c\x7a\65\107\x59\x57\154\x73\x5a\127\x51\x68\x49\105\x35\x76\111\x47\132\x73\131\127\x63\x67\x5a\155\71\x79\x49\110\154\x76\x64\x51\x3d\75");}}}
```
Decoding the base64 we get
```php
if (isset($_POST["user"]) && isset($_POST["pwd"])) {
    $yuf85e0677=$_POST["user"];
    $rs35c246d5=$_POST["pwd"];
    if($yuf85e0677==$rs35c246d5) {
        echo "<br>Failed! No file";
    } else {
        if(sha1($yuf85e0677)===sha1($rs35c246d5)) {
        echo file_get_contents("../flag.txt";
        } else {
            echo base64_decode("<br/>Failed! No file");
        }
    }
}
```

Looks like we need two values that have a SHA1 hash collision. Looking around, [I found someone's implementation of a PDF SHA1 collider](https://github.com/eopXD/SHA1collide). Conveniently, they gave us an x and y that collides.

```
[16:35:05] INFO: x and y that collides
[16:35:05] INFO: x = 255044462d312e330a25e2e3cfd30a0a0a312030206f626a0a3c3c2f57696474682032203020522f4865696768742033203020522f547970652034203020522f537562747970652035203020522f46696c7465722036203020522f436f6c6f7253706163652037203020522f4c656e6774682038203020522f42697473506572436f6d706f6e656e7420383e3e0a73747265616d0affd8fffe00245348412d3120697320646561642121212121852fec092339759c39b1a1c63c4c97e1fffe017346dc9166b67e118f029ab621b2560ff9ca67cca8c7f85ba84c79030c2b3de218f86db3a90901d5df45c14f26fedfb3dc38e96ac22fe7bd728f0e45bce046d23c570feb141398bb552ef5a0a82be331fea48037b8b5d71f0e332edf93ac3500eb4ddc0decc1a864790c782c76215660dd309791d06bd0af3f98cda4bc4629b13139333739333637
[16:35:05] INFO: y = 255044462d312e330a25e2e3cfd30a0a0a312030206f626a0a3c3c2f57696474682032203020522f4865696768742033203020522f547970652034203020522f537562747970652035203020522f46696c7465722036203020522f436f6c6f7253706163652037203020522f4c656e6774682038203020522f42697473506572436f6d706f6e656e7420383e3e0a73747265616d0affd8fffe00245348412d3120697320646561642121212121852fec092339759c39b1a1c63c4c97e1fffe017f46dc93a6b67e013b029aaa1db2560b45ca67d688c7f84b8c4c791fe02b3df614f86db1690901c56b45c1530afedfb76038e972722fe7ad728f0e4904e046c230570fe9d41398abe12ef5bc942be33542a4802d98b5d70f2a332ec37fac3514e74ddc0f2cc1a874cd0c78305a21566461309789606bd0bf3f98cda8044629a13139333739333637
[16:35:05] INFO: SHA1 of x and y
[16:35:05] INFO: SHA1(x) = 536de1918afce039dc2620935f86f3ca69123456
[16:35:05] INFO: SHA1(y) = 536de1918afce039dc2620935f86f3ca69123456
```

I had a bit of trouble thinking of how to send this to the server. I originally tried those exact strings as username and password, but I realized those were ASCII characters and not bytes, and would give different collisions. 

I tried many techniques, encoding it using latin1 and sending it, trying to generate my own PDF collisions, but nothing worked. I took a closer look at the network request. Sepcifically I saw that `Content-Type: application/x-www-form-urlencoded`. This gave me an idea. I could URL-encode the bytes, and send that over.

So I wrote a [python script](vuln.py), using urllib to encode my bytes.

```py
import requests
from hashlib import sha1
from binascii import hexlify
import urllib.parse

a = bytes.fromhex("255044462d312e330a25e2e3cfd30a0a0a312030206f626a0a3c3c2f57696474682032203020522f4865696768742033203020522f547970652034203020522f537562747970652035203020522f46696c7465722036203020522f436f6c6f7253706163652037203020522f4c656e6774682038203020522f42697473506572436f6d706f6e656e7420383e3e0a73747265616d0affd8fffe00245348412d3120697320646561642121212121852fec092339759c39b1a1c63c4c97e1fffe017346dc9166b67e118f029ab621b2560ff9ca67cca8c7f85ba84c79030c2b3de218f86db3a90901d5df45c14f26fedfb3dc38e96ac22fe7bd728f0e45bce046d23c570feb141398bb552ef5a0a82be331fea48037b8b5d71f0e332edf93ac3500eb4ddc0decc1a864790c782c76215660dd309791d06bd0af3f98cda4bc4629b13139333739333637")
b = bytes.fromhex("255044462d312e330a25e2e3cfd30a0a0a312030206f626a0a3c3c2f57696474682032203020522f4865696768742033203020522f547970652034203020522f537562747970652035203020522f46696c7465722036203020522f436f6c6f7253706163652037203020522f4c656e6774682038203020522f42697473506572436f6d706f6e656e7420383e3e0a73747265616d0affd8fffe00245348412d3120697320646561642121212121852fec092339759c39b1a1c63c4c97e1fffe017f46dc93a6b67e013b029aaa1db2560b45ca67d688c7f84b8c4c791fe02b3df614f86db1690901c56b45c1530afedfb76038e972722fe7ad728f0e4904e046c230570fe9d41398abe12ef5bc942be33542a4802d98b5d70f2a332ec37fac3514e74ddc0f2cc1a874cd0c78305a21566461309789606bd0bf3f98cda8044629a13139333739333637")

url = 'http://verbal-sleep.picoctf.net:56613/impossibleLogin.php'

data = f"username={urllib.parse.quote_plus(a)}&pwd={urllib.parse.quote_plus(b)}"

headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Content-Length': str(len(data))  
}

response = requests.post(url, headers=headers, data=data)

print("Status Code:", response.status_code)
print("Response Text:", response.text)
```

And it worked!

```
Status Code: 200
Response Text: <!DOCTYPE html>
<html>
<head>
    <title>Login Page</title>
</head>
<body style="text-align:center;">
    <pre>
 _               _         _  __
| |             (_)       (_)/ _|
| | ___   __ _   _ _ __    _| |_   _   _  ___  _   _    ___ __ _ _ __
| |/ _ \ / _` | | | '_ \  | |  _| | | | |/ _ \| | | |  / __/ _` | '_ \
| | (_) | (_| | | | | | | | | |   | |_| | (_) | |_| | | (_| (_| | | | |
|_|\___/ \__, | |_|_| |_| |_|_|    \__, |\___/ \__,_|  \___\__,_|_| |_|
          __/ |                     __/ |
         |___/                     |___/


    </pre>
    <br/>
    <form action="impossibleLogin.php" method="post">
        <label for="username">Username:</label><br>
        <input type="text" id="username" name="username"><br>
        <label for="pwd">Password:</label><br>
        <input type="password" id="pwd" name="pwd"><br><br>
        <input type="submit" value="Login">
    </form>
</body>
</html>

picoCTF{w3Ll_d3sErV3d_Ch4mp}
```
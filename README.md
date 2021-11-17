# wp_report_vulnerabilities
A Crawler that makes a request to a wordpress url by going to /feed (https://examplewp.com/feed) takes the wordpress version and consumes the wpscan api that returns the vulnerabilities found in the version the wp_report_vulnerabilities crawler found

# Usage
<p>pip install -r requirements.txt</p>
<p>python3 crawler_wp.py</p>

# Flask
This project uses the Flask tool to create a Rest API
<p>Para utilizar a api rest desenvolvida com o flask é necessário enviar um token no header da requisição com a key: **Authorization_Secret_Token**
https://flask.palletsprojects.com/en/2.0.x/

![image](https://user-images.githubusercontent.com/52108028/142212341-d21e6f6c-ec69-40ce-b8c0-0b90586b53f3.png)

# Deploy Flask
https://flask.palletsprojects.com/en/2.0.x/tutorial/deploy/




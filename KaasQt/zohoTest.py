import http.client

conn = http.client.HTTPSConnection("www.zohoapis.in")

headers = { 'Authorization': "Zoho-oauthtoken 1000.554cea0ad58509632bb0ae2f9e936fc1.6bb39626fed34274defd2d765c183c73" }

conn.request("GET", "/books/v3/chartofaccounts?organization_id=60029851485", headers=headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))

# 
# 1000.0SQKHCOMCQOBELBGMDTL9K1904GNIX
# 883e9bf021e43cb0b4147a2353319f4be8167138e5
# 1000.4ab7d912931ec1a0df1b2d0232efc109.a60a4ce5d0fb75315ab95c186e3e4fe9
# {"access_token":"1000.90be74d31c1b5313923b413dac9b009d.fea754b862ceb19d31e2617cc54676be","refresh_token":"1000.554cea0ad58509632bb0ae2f9e936fc1.6bb39626fed34274defd2d765c183c73","scope":"ZohoBooks.fullaccess.all","api_domain":"https://www.zohoapis.in","token_type":"Bearer","expires_in":3600}

#https://www.google.com/?state=testing&code=1000.4ab7d912931ec1a0df1b2d0232efc109.a60a4ce5d0fb75315ab95c186e3e4fe9&location=in&accounts-server=https%3A%2F%2Faccounts.zoho.in&
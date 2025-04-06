import requests

parm = {'cust_id':'2010078'}
resp = requests.request('GET','http://127.0.0.1:8000/getcustdata',params=parm)


# print('Response Code    : ', resp.status_code)
# print('Response Header  : ', resp.headers)
# print('Response Cookies : ', resp.cookies)
# print('Response Data (Content) : ', resp.content)
# print('Response Data (Text)    : ', resp.text)
print('Response Data (JSON)    : ', resp.json())


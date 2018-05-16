import requests

url = "http://10.40.8.134:9090/nwpudatacenterAPI"
headers = {'ContentType': 'application/x-www-form-urlencoded',"ClientId":"cn.edu.nwpu.zbcg","OperationCode":"cn.edu.nwpu.ggsjgl.teacher.getlist"}

data={"id":"","dateTime":"","pageSize":"100","pageIndex":"1","dataType":"teacher"}

#res = requests.post(url,headers=headers,data=data)


res = requests.get("http://222.24.192.8/interfaces/msg/?ucode=trh_15&api_key=34d8258a3f222853271c0e47dec4d414d50df0d7&mobiles=13282119520&content=test2")
print(res.text)
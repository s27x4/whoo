import requests, json
from uuid import uuid4

class Client():
  
  def __init__(self,token=None,support=True,email=None,password=None): #Tokenの検証
    self.base = 'https://www.wh00.ooo/'
    self.headers = {
      'Accept': 'application/json',
      'User-Agent': 'app.whoo/0.13.4 iOS/17.0',
      'Accept-Language': 'ja-JP',
      'Accept-Encoding': 'gzip, deflate, br'
      }
    if token is None and email and password:
      token=self.email_login(email,password)["access_token"]
    if token:
      self.headers["Authorization"]="Bearer "+token
      url=self.base+'api/my'
      response=requests.get(url,headers=self.headers)
      if response.status_code==200:
        self.token=True
        if support:
          print("Login successful!")
        return
      else:
        raise Exception(f'Request Error[{response.status_code}] (auth)')
    else:
      self.token=None
      
  
  

  ##############  アカウントの設定関連   ##############
  def email_login(self,email,password): #アカウントにログイン(メアド)
    url=self.base+'api/email/login'
    data={
      'email' : email,
      'password' : password
    }
    response=requests.post(url,headers=self.headers,data=data)
    if response.status_code==200:
      token=response.json()["access_token"]
      self.headers["Authorization"]="Bearer "+token
      return response.json()
    else:
      raise Exception(f'Request Error[{response.status_code}] (email login)')
      
  def create_account(self,email,password,name,profile_image,username,location=None): #アカウントを作成(メアド)
    url=self.base+'api/email/users'
    data={
      'user[email]': email,
      'user[password]': password,
      'user[display_name]': name,
      'user[profile_image]': profile_image,
      'user[username]': username
    }
    response=requests.post(url,headers=self.headers,data=data)
    if response.status_code==200:
      if location is None:
        return response.json()
      else:
        headers = {
          'Accept': 'application/json',
          'User-Agent': 'app.whoo/0.13.4 iOS/17.0',
          'Authorization': "Bearer "+response.json()['access_token'],
          'Accept-Language': 'ja-JP',
          'Accept-Encoding': 'gzip, deflate, br'
          }
        data={
          "user_location[latitude]" : str(location["latitude"]),
          "user_location[longitude]" : str(location["longitude"]),
          "user_location[speed]" : 0,
          "user_battery[level]" : 1,
          "user_battery[state]": 1
          }
        url=self.base+'api/user/location'
        response1=requests.patch(url,headers=headers,data=data)
        return response.json()
    else:
      raise Exception(f'Request Error[{response.status_code}] (account create)')
  def update_account(self,name=None,profile_image=None,username=None): #アカウントを更新(メアド)
    url=self.base+'api/user'
    data={
      'user[display_name]': name,
      'user[profile_image]': profile_image,
      'user[username]': username
    }
    response=requests.patch(url,headers=self.headers,data=data)
    if response.status_code==200:
      return response.json()
    else:
      raise Exception(f'Request Error[{response.status_code}] (account update)')
  def delete_account(self,alert=True): #アカウントの削除
    if self.token:
      if alert:
        res=input('Are you sure? (y/n): ')
        if res!='y':
          return 'Cansell'
      url=self.base+'api/user'
      response=requests.delete(url,headers=self.headers)
      if response.status_code==204:
        return 'Success'
      else:
        raise Exception(f'Request Error[{response.status_code}] (account delete)')
    else:
      raise Exception('Message: Token is required.')



  ##############  バックグラウンド処理   ##############              
  def account_info(self): #使用中のアカウントの情報
    if self.token:
      url=self.base+'api/my'
      response=requests.get(url,headers=self.headers)
      if response.status_code==200:
        return response.json()
      else:
        raise Exception(f'Request Error[{response.status_code}] (account info)')
    else:
      raise Exception('Message: Token is required.')
  def get_requested(self): #友達申請リストを取得
    if self.token:
      url=self.base+'api/friends/requested'
      response=requests.get(url,headers=self.headers)
      if response.status_code==200:
        return response.json()
      else:
        raise Exception(f'Request Error[{response.status_code}] (get requested)')
    else:
      raise Exception('Message: Token is required.')
  
  def get_my_friends(self): #友達リストを取得
    if self.token:
      url=self.base+'api/friends'
      response=requests.get(url,headers=self.headers)
      if response.status_code==200:
        return response.json()
      else:
        raise Exception(f'Request Error[{response.status_code}] (get my friends)')
    else:
      raise Exception('Message: Token is required.')
  def get_user(self,id,friends=False): #IDからそのアカウントの情報取得
    if self.token:
      url=self.base+'api/v2/users/'+str(id)
      response=requests.get(url,headers=self.headers)
      if response.status_code==200:
        js=response.json()
        if friends:
          if js["next_page"]:
            js["friends"]=[]
            for i in range(js["next_page"]):
              url=self.base+'api/v2/users/'+id+'/friends?page='+str(i+1)
              response=requests.get(url,headers=self.headers)
              if response.status_code==200:
                js["friends"]+=response.json()["friends"]
              else:
                raise Exception(f'Request Error[{response.status_code}] (get friends info)')
            else:
              js["next_page"] = None
              return js
        else:
          del js["friends"],js["next_page"]
          return js
      else:
        raise Exception(f'Request Error[{response.status_code}] (get about user info)')
    else:
      raise Exception('Message: Token is required.')
  def request_get_location(self,id): #位置情報再取得リクエストを任意のアカウントに送信します
    if self.token:
      url=self.base+f'api/users/{id}/location_request'
      response=requests.get(url,headers=self.headers)
      if response.status_code==200:
        return response.json()
      else:
        raise Exception(f'Request Error[{response.status_code}] (send location request)')
    else:
      raise Exception('Message: Token is required.')
  def post_location(self,latitude,longitude,level=100,state=0,speed=0.0,stayed_at=None,horizontal_accuracy=None): #位置情報の更新
    if self.token:
      url=self.base+'api/user/location'
      data={
        "user_location[latitude]" : str(latitude),
        "user_location[longitude]" : str(longitude),
        "user_location[speed]" : str(speed),
        "user_battery[level]" : str(level),
        "user_battery[state]": str(state)
      }
      if horizontal_accuracy:
        data["user_location[horizontal_accuracy]"]=str(horizontal_accuracy)
      if stayed_at:
        data["user_location[stayed_at]"]=str(stayed_at)
      response=requests.patch(url,headers=self.headers,data=data)
      if response.status_code==200:
        return response.json()
      else:
        raise Exception(f'Request Error[{response.status_code}] (post location)')
    else:
      raise Exception('Message: Token is required.')
  def get_locations(self,id=None):
    if self.token:
      url=self.base+'api/locations'
      response=requests.get(url,headers=self.headers)
      if response.status_code==200:
        js={}
        for loc in response.json()['locations']:
          if id:
            if id==loc['user']['id']:
              name=loc['user']['username']
              del loc['user']['username']
              loc["map"]="https://maps.google.com/maps?q="+loc['latitude']+','+loc['longitude']+"&t=k&z=24"
              loc['pano']='https://www.google.com/maps/@?api=1&map_action=pano&viewpoint='+loc['latitude']+','+loc['longitude']
              js[name]=loc
          else:
            name=loc['user']['username']
            del loc['user']['username']
            loc["map"]="https://maps.google.com/maps?q="+loc['latitude']+','+loc['longitude']+"&t=k&z=24"
            loc['pano']='https://www.google.com/maps/@?api=1&map_action=pano&viewpoint='+loc['latitude']+','+loc['longitude']
            js[name]=loc
        else:
          return js
      else:
        raise Exception(f'Request Error[{response.status_code}] (get locations)')
    else:
      raise Exception('Message: Token is required.')
  def online(self): #オンラインにします
    if self.token:
      url=self.base+f'api/user/online'
      response=requests.patch(url,headers=self.headers)
      if response.status_code==200:
        return response.json()
      else:
        raise Exception(f'Request Error[{response.status_code}] (online)')
    else:
      raise Exception('Message: Token is required.')
  def offline(self): #オフラインにします
    if self.token:
      url=self.base+f'api/user/offline'
      response=requests.patch(url,headers=self.headers)
      if response.status_code==204:
        return 'success'
      else:
        raise Exception(f'Request Error[{response.status_code}] (offline)')
    else:
      raise Exception('Message: Token is required.')
      
      
      
  ##############  基本操作   ##############        
  def send_stamp(self,user_id,stamp_id,quantity): #スタンプを送信します
    if self.token:
      url=self.base+f'api/stamp_messages'
      data={
        "message[user_id]" : user_id,
        "message[stamp_id]" : stamp_id,
        "message[stamp_count]" : quantity
      }
      response=requests.post(url,headers=self.headers,data=data)
      if response.status_code==204:
        return response
      else:
        raise Exception(f'Request Error[{response.status_code}] (stamp message)')
    else:
      raise Exception('Message: Token is required.')
  def send_message(self,room_id,content): #
    if self.token:
      url=self.base+f'api/rooms/{room_id}/messages'
      data={
        "message[uid]" : uuid4(),
        "message[body]" : content
      }
      response=requests.post(url,headers=self.headers,data=data)
      if response.status_code==200:
        return response.json()
      else:
        raise Exception(f'Request Error[{response.status_code}] (send message)')
    else:
      raise Exception('Message: Token is required.')
  def request_friend(self,id): #友達申請
    if self.token:
      url=self.base+f'api/friends'
      data={
        "user_id" : id
      }
      response=requests.post(url,headers=self.headers,data=data)
      if response.status_code==200:
        return response.json()
      else:
        raise Exception(f'Request Error[{response.status_code}] (request friend)')
    else:
      raise Exception('Message: Token is required.')
  def delete_requested(self,id): #友達申請を取り消す
    if self.token:
      url=self.base+f'api/friendships/{id}/retire'
      response=requests.delete(url,headers=self.headers)
      if response.status_code==200:
        return response.json()
      else:
        raise Exception(f'Request Error[{response.status_code}] (delete requested)')
    else:
      raise Exception('Message: Token is required.')

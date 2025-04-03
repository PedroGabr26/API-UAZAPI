# import requests
# import json
# from dataclasses import dataclass


# BASE_URL = "https://free.uazapi.com"
# API_KEY = "B7teYpdEf9I9LM9IxDE5CUqmxF68P2LrwtF6NZ5eZu2oqqXz3r"


# @dataclass

# #basicamente eu já tô criando um objeto instânciado dentro da classe já, só que apesar de eu estar criando ele, ainda preciso definir ele em uma variável
# class Channel:
#     name: str = 'free'
#     phone: str = '5561998548053'
#     token: str = 'teste1' # identificacao do canal
#     access_token: str = None # token para acesso ao whatsapp
#     #access_token: str = '286ce971-f6cc-4845-ad70-ee7330078b0f'
#     number: str = None
#     # colocar uma variavel chamado "ativo" como false aqui ou abaixo de created, quando for criado a instância coloca ela como True



# class UazapiApi:

#     @classmethod
#     def get_admin_headers(cls) -> dict:
#         return {
#             "Content-Type": "application/json",
#             "Admintoken": API_KEY
#         }


#     @classmethod
#     def create_instance(cls, channel: Channel):
#         url = f"{BASE_URL}/instance/init"
#         json = {
#         "name": channel.token,
#         "systemName": channel.name,
#         "adminField01": "primeiroteste",
#         "adminField02": "primeiroteste1"
#         }
#         headers = cls.get_admin_headers()
#         response = requests.post(url,json=json,headers=headers)
#         created = False
#         if response.status_code == 200: 
#             data = response.json()
#             channel.access_token = data.get("token")
#             created = True
#         else:
#             print(response.status_code())
#             print(response.text)
#         return channel, created
    


#     def get_headers(self, channel):
#         return {
#             "Content-Type": "application/json",
#             "token": channel.access_token
#         }


#     @classmethod
#     def connect_instance(cls, channel: Channel):
#         url = f"{BASE_URL}/instance/connect"
#         payload = {"phone":channel.phone}   # criar campo phone no model Channel
#         headers = cls.get_headers(channel)
#         print(url)
#         print(headers)
#         print(payload)
#         response = requests.post(url,headers=headers,json=payload)
#         print('---Resposta da conexão---')
#         if response.status_code == 200:
#             return response.json()
#         else:
#             return {'error':f"Erro {response.status_code}: {response.text}"}
#         # Erro descoberto, não está pegando o token


#     # @classmethod
#     # def send_message(cls, channel: Channel, number: str):
#     def send_message(
#         self,
#         log_msg: Chat or ChatGroup,
#         client: Client,
#         message: str,
#         quote_id: str = None,
#         from_me: bool = None,
#         **kwargs,
#     ):
#         group_jid = (
#             log_msg.whatsapp_group.jid if isinstance(log_msg, ChatGroup) else None
#         )
#         data = {
#             "number": group_jid or client.phone,
#             "text":log_msg,
#             "delay": 1200,
#             "linkPreview": False,
#             "replyid": "",
#             "mentions": "", # "all" = todos, ou separando vou virgula, assim: "1234, 321" 
#             "readchat": True, #// marcar chat como lido
#             "delay": 1200,
#             "convert":"true"
#         }
#         if quote_id:
#             data["quoted"] = {
#                 "key": {
#                     "id": quote_id,
#                     "fromMe": from_me,
#                     "participant": "",
#                     "remoteJid": group_jid or f"{client.phone}@s.whatsapp.net",
#                 }
#             }
#         if self.organization.is_beta:
#             data.update(**kwargs)
#         else:
#             data["chat_id"] = log_msg.id if log_msg else None

#         options = kwargs.get("options")
#         if (
#             kwargs.get("options")
#             and kwargs.get("send_menu_list")
#             and self.channel.can_send_list
#         ):
#             url, data = self.__prepare_list(data, message, options)
#             # dados de lista na raiz para v2 
#             # data.update(data["listMessage"])
#             # data["footerText"] = "Escolha uma opção"
#         else:
#             message = self.__prepare_message(message, options)
#             data["textMessage"] = {"text": message}
#             data["text"] = message
#             url = (
#                 f"{BASE_URL}/send/text"
#             )
#         try:
#             req = requests.post(
#                 url,
#                 timeout=10,
#                 verify=False,
#                 json=data,
#                 headers=self.get_headers(),
#             )
#             # print(req.json())
#             if req.status_code == 201:
#                 log_msg.uid = self.__get_uid(req.json())
#                 log_msg.status = Chat.STATUS_SENT
#                 if kwargs.get("campaign_id"):
#                     log_msg.campaign_id = kwargs.get("campaign_id")
#                 log_msg.save(update_fields=["uid", "status", "campaign_id"])
#         except:
#             return None
        
#         #channel.number = number
#         # url = f"{BASE_URL}/send/text"
#         # headers = self.get_headers(channel)
#         # json = {
#         #     "number": client.phone,
#         #     "text": message,
#         #     "linkPreview": False,
#         #     "replyid": "",
#         #     "mentions": "", # "all" = todos, ou separando vou virgula, assim: "1234, 321" 
#         #     "readchat": True, #// marcar chat como lido
#         #     "delay": 1200,
#         #     "convert":"true"
#         # }
#         # response = requests.post(url,headers=headers,json=json)
#         # if response.status_code == 200:
#         #     return response.json()
#         # else:
#         #     return {'error':f"Erro {response.status_code}: {response.text}"}



#     def __get_mimetype(self, mimetype):
#         if not mimetype: # tem uma condição pra cá
#             return "sticker"
#         if "video" in mimetype:
#             return "video"
#         elif "audio" in mimetype: # tem uma condição pra cá
#             return "audio"
#         elif "image" in mimetype:
#             return "image"
#         else:
#             return "document"



#     def send_media(
#         # url = f"{BASE_URL}/send/media"
#         # headers = self.get_headers(channel)
#         # json = {
#         #     "number": "{{chatID}}", # altero
#         #     "text": "texto da mensagem", # altero
#         #     "type": "image", # // document, video, image, audio, ptt, sticker
#         #     "file": "https://cdn.hasselblad.com/hasselblad-com/6cb604081ef3086569319ddb5adcae66298a28c5_x1d-ii-sample-01-web.jpg?auto=format&q=97",
#         #     "docName": "", #//opcional, serve apenas para document
#         #     "replyid": "",
#         #     "mentions": "",
#         #     "readchat": True, // marcar chat como lido
#         #     "delay": 0
#         # }
#         self,
#         log_msg: Chat, # mensagem trocada entre cliente e organization
#         client: Client,
#         message: str,
#         file: MessageFile,
#         quote_id: str = None,
#         from_me: bool = None,
#         **kwargs,
#     ):
#         group_jid = (
#             log_msg.whatsapp_group.jid if isinstance(log_msg, ChatGroup) else None
#         )
#         mimetype_ = guess_type(file.file.url)[0]
#         data = {
#             "number": group_jid or client.phone,
#             "file": file.file.url,
#             "docName": "",
#             "replyid": "",
#             "mentions": "",
#             "readchat": True,
#             "delay": 1200,
#         }
#         # POSSO MUDAR DE TYPE_ PARA type, senão type_ = type = "valor definido"
#         type = "" # mudo type_ para type e valor sendo message
#         url = f"{BASE_URL}/send/media" # mudo a url

#         # se for audio
#         if mimetype_ and "audio" in mimetype_:
#             type = "audio" # mudo pra "audio"
#             data.update(
#                 "type":type,
#             )

#         elif not mimetype_ and "sticker" in self.__get_mimetype(mimetype_):
#             #configurar pro json padrão do uazapi do tipo sticker
#             type = "sticker"
#             data.update(
#                 {
#                     "type":type,
#                 }
#             )
#         # elif mimetype_ and "message" in self.__get_mimetype(mimetype_):
#         #     type = "message"
#         #     data.update(
#         #         {
#         #             "text": message or "",
#         #             "type": type,
#         #         }
#         #     )
#         else:
#             data.update(
#                 {   
#                     #configurar pro json padrão do uazapi do tipo mensagem
#                     # type: {
#                     #     "caption": message or "",
#                     #     "mediatype": self.__get_mimetype(mimetype_),
#                     #     "fileName": file.file.name.split("/")[-1],
#                     #     "media": file.file.url,
#                     # },
#                     "text": log_msg or "", # ou log_message
#                     "type": self.__get_mimetype(mimetype_),
#                     #"fileName": file.file.name.split("/")[-1],
#                 }
#             )

#         if quote_id:
#             data["quotedMessage"] = {
#                 "messageId": quote_id,
#                 "fromMe": from_me,
#             }

#         try:
#             req = requests.post(
#                 url,
#                 # timeout=20,
#                 # verify=False,
#                 json=data,
#                 headers=self.get_headers(channel),
#             )
#             if req.status_code == 201:
#                 log_msg.uid = self.__get_uid(req.json())
#                 log_msg.status = Chat.STATUS_SENT
#                 if kwargs.get("campaign_id"):
#                     log_msg.campaign_id = kwargs.get("campaign_id")
#                 log_msg.save(update_fields=["uid", "status", "campaign_id"])

#             if mimetype_ and "audio" in mimetype_ and message:
#                 self.send_message(log_msg=log_msg, client=client, message=message)
#         except:
#             return None







# channel = Channel() # instância/cria a pessoa que vai usar a classe Uazapi
# uazapi = UazapiApi() # instância a classe uazapi

# print(uazapi.create_instance(channel))
# # print(uazapi.connect_instance(channel))
# print(uazapi.send_message(channel))













# def send_message(
#         self,
#         log_msg: Chat or ChatGroup, # o que é ? sei que log_msg é uma instância de Chat ou Chatgroup
#         client: Client, # o que é ? sei que é uma instância de Client
#         message: str, # o que é ?
#         #quote_id: str = None,
#         #from_me: bool = None,
#         **kwargs,
#     ):
#         group_jid = (
#             log_msg.whatsapp_group.jid if isinstance(log_msg, ChatGroup) else None
#         )
#         data = {
#             "number": group_jid or client.phone, # porque não passar log_msg.message ou só log_msg
#             "message":log_msg,
#             "linkPreview": False,
#             "replyid": "",
#             "mentions": "",  #// "all" = todos, ou separando vou virgula, assim: "1234, 321" 
#             "readchat": True, #// marcar chat como lido
#             "delay": 1200,
#             "convert":"true",
#             # "options": {"delay": 1200, "presence": "composing"},
#         }
#         # if quote_id:
#         #     data["quoted"] = {
#         #         "key": {
#         #             "id": quote_id,
#         #             "fromMe": from_me,
#         #             "participant": "",
#         #             "remoteJid": group_jid or f"{client.phone}@s.whatsapp.net",
#         #         }
#         #     }
#         if self.organization.is_beta:
#             data.update(**kwargs)
#         else:
#             data["chat_id"] = log_msg.id if log_msg else None

#         options = kwargs.get("options")
#         if (
#             kwargs.get("options")
#             and kwargs.get("send_menu_list")
#             and self.channel.can_send_list
#         ):
#             url, data = self.__prepare_list(data, message, options)
#             # dados de lista na raiz para v2
#             data.update(data["listMessage"])
#             data["footerText"] = "Escolha uma opção"
#         else:
#             message = self.__prepare_message(message, options)
#             data["textMessage"] = {"text": message}
#             data["text"] = message
#             url = (
#                 f"{self.channel.get_gateway_url}/message/sendText/{self.channel.token}"
#             )
#         try:
#             req = requests.post(
#                 url,
#                 # timeout=10,
#                 # verify=False,
#                 json=data,
#                 headers=self.get_headers(),
#             )
#             # print(req.json())
#             if req.status_code == 201:
#                 log_msg.uid = self.__get_uid(req.json())
#                 log_msg.status = Chat.STATUS_SENT
#                 if kwargs.get("campaign_id"):
#                     log_msg.campaign_id = kwargs.get("campaign_id")
#                 log_msg.save(update_fields=["uid", "status", "campaign_id"])
#         except:
#             return None

# def __prepare_list(self, data, message, options):
#         data["listMessage"] = {}
#         url = f"{self.channel.get_gateway_url}/message/sendList/{self.channel.token}"
#         data["listMessage"]["title"] = "Escolha uma opção"
#         data["listMessage"]["description"] = message
#         data["listMessage"]["buttonText"] = "VER OPÇÕES"
#         data["listMessage"]["sections"] = []
#         options_ = {"title": "Opções", "rows": []}
#         for option in options:
#             options_["rows"].append(
#                 {
#                     "title": option["option"],
#                     # "description": option["option"],
#                     "description": " ",
#                     "rowId": f'option-{option["id"]}',
#                 }
#             )
#         data["listMessage"]["sections"].append(options_)
#         return url, data

#     #verifica se a mensagem possui o menu interativo ou se é uma mensagem normal
# def __prepare_message(self, message, options):
#     if not options:
#         return message
#     for counter, option in enumerate(options, start=1):
#         if not option["option"] in message:
#             message += "{0} - {1}\n".format(counter, option["option"])
#     return message


# def send_message(
#         self,
#         log_msg: Chat or ChatGroup, # é passado como string ?
#         client: Client, # campo necessario pra saber qual cliente vai receber a mensagem
#         message: str, # mensagem é uma string aqui
#         quote_id: str = None,
#         from_me: bool = None,
#         **kwargs,
#     ):
#         group_jid = (
#             log_msg.whatsapp_group.jid if isinstance(log_msg, ChatGroup) else None
#         )
#         data = {
#             "number": group_jid or client.phone, # número que a mensagem vai ser enviada
#             #options começa daqui
#             # caso tenha options
#             "options": {"delay": 1200, "presence": "composing"},
#         }
#         if quote_id:
#             data["quoted"] = {
#                 "key": {
#                     "id": quote_id,
#                     "fromMe": from_me,
#                     "participant": "",
#                     "remoteJid": group_jid or f"{client.phone}@s.whatsapp.net",
#                 }
#             }
#         # eu preciso disso pra pegar options ?
#         if self.organization.is_beta:
#             data.update(**kwargs)
#         else:
#             data["chat_id"] = log_msg.id if log_msg else None

#         # options começa aqui

#         options = kwargs.get("options")
#         if (
#             kwargs.get("options")
#             and kwargs.get("send_menu_list")
#             and self.channel.can_send_list
#         ):
#             url, data = self.__prepare_list(data, message, options)
#             # dados de lista na raiz para v2
#             data.update(data["listMessage"])
#             data["footerText"] = "Escolha uma opção"
#         else:
#             message = self.__prepare_message(message, options)
#             data["textMessage"] = {"text": message}
#             data["text"] = message
#             url = (
#                 f"{self.channel.get_gateway_url}/message/sendText/{self.channel.token}"
#             )
#         try:
#             req = requests.post(
#                 url,
#                 timeout=10,
#                 verify=False,
#                 json=data,
#                 headers=self.get_headers(),
#             )
#             # print(req.json())
#             if req.status_code == 201:
#                 log_msg.uid = self.__get_uid(req.json())
#                 log_msg.status = Chat.STATUS_SENT
#                 if kwargs.get("campaign_id"):
#                     log_msg.campaign_id = kwargs.get("campaign_id")
#                 log_msg.save(update_fields=["uid", "status", "campaign_id"])
#         except:
#             return None






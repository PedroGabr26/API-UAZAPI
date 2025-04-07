import requests
from mimetypes import guess_type
from datetime import datetime,timedelta
# from uazapi import Channel

BASE_URL = "https://free.uazapi.com"
API_KEY = "B7teYpdEf9I9LM9IxDE5CUqmxF68P2LrwtF6NZ5eZu2oqqXz3r"
schedule_date = datetime(2025,4,2)
schedule_for = int((datetime.now() + timedelta(seconds=60)).timestamp() * 1000)
WEBHOOK_URL = None


class File:
    # url: str = None
    url: str = 'https://upload.wikimedia.org/wikipedia/commons/4/47/PNG_transparency_demonstration_1.png'


class Emoji:
    reaction: str = "\U0001F44D"

class Channel:
    name: str = 'free'
    systemname: str = 'tsuru'
    phone: str = '5586995774681'
    # access_token: str = None # token para acesso ao whatsapp
    # id: str = None
    chatid: str = None
    idmessage: str = None
    access_token: str = '5d734ded-5623-4cff-997f-bfda85754a27'
    id:str = 'rfd2a00ab2c3216'
    groupid: str = None
    invitelink: str = None

    def __repr__(self):
        return f"Channel(name='{self.name}', systemname='{self.systemname}',phone='{self.phone}',acess_token='{self.access_token}')"


class UazapiApi:
    @classmethod
    def get_admin_headers(cls) -> dict:
        return {
            "Content-Type": "application/json",
            "Admintoken": API_KEY
        }
    
    # usuario passa como parametro o json com name e systemname e atualizado payload com os parametros passados
    @classmethod
    def create_instance(cls, channel: Channel, json: dict ): # ou organization: Organization - pega "name": organization.name  e  "systemname": organization.token
        """
        Args: exemplo de parametro recebido como json
            json {
                "name": channel.name,
                "systemname":channel.systemname,
            }
        """
        url = f"{BASE_URL}/instance/init"
        headers = cls.get_admin_headers()
        payload = {
            "name":None,
            "systemname":None,
            "adminField01": "teste1",
            "adminField02": "teste2"
        }
        if 'name' and 'systemname' in json: # aqui é passado o valor referenciado no parametro da função
            payload['name'] = json['name']
            payload['systemname'] = json['systemname']
        else:
            return {"Error":"Passe as informaões corretamente"}
        response = requests.post(url, headers=headers, json=payload)
        created = False
        if response.status_code == 200:
            data = response.json()
            channel.access_token = data.get("token")
            channel.id = data.get('instance',{}).get('id','id não encontrado')
            created = True
        else:
            return {"error":f"{response.status_code}:{response.text}/n{data}"}
        return channel,created, data
    

    @classmethod
    def get_headers(self, channel: Channel):
        return {
            "Content-Type": "application/json",
            "token": channel.access_token # o token vem pra cá, esse token vai ser o headers em todas as outras funções, MAS PRECISA CONECTAR COM O WHATSAPP
        }



    @classmethod
    def connect_instance(cls, channel: Channel):
        url = f"{BASE_URL}/instance/connect"
        headers = cls.get_headers(channel)
        json = {"phone":channel.phone}
        # print(url)
        # print(headers)
        # print(json)
        response = requests.post(url,headers=headers, json=json)
        if response.status_code == 200:
            print('---Resposta da conexão---')
            data = response.json()
        else:
            return {'error':f"Erro {response.status_code}: {response.text}"}
        return data
    

    @classmethod    
    def instance_status(cls):
        url = f"{BASE_URL}/instance/status"
        headers = cls.get_headers(channel)
        json = {}
        response = requests.get(url,headers=headers,json=json)
        if response.status_code == 200:
            data = response.json()
        else:
            return {'error':f"Erro {response.status_code}: {response.text}"}
        return data



    @classmethod
    def disconnect_instance(cls):
        url = f"{BASE_URL}/instance/disconnect"
        headers = cls.get_headers(channel)
        json = {}
        response = requests.post(url,headers=headers,json=json)
        if response.status_code == 200:
            data = response.json()
        else:
            return {'error':f"Erro {response.status_code}: {response.text}"}
        return data


    
    @classmethod
    def delete_instance(cls):
        url = f"{BASE_URL}/instance"
        headers = cls.get_headers(channel)
        json = {}
        response = requests.delete(url,headers=headers,json=json)
        if response.status_code == 200:
            data = response.json()
        else:
            data = response.json()
            return {'error':f"Erro {response.status_code}: {response.text}\n{data}"}
        return data



    @classmethod
    def get_status(cls, channel):
        url = f"{BASE_URL}/instance/status"
        headers = cls.get_headers(channel)
        response = requests.get(url,headers=headers)
        if response.status_code == 200:
            data = response.json()
        else:
            data = response.json()
            return {'error':f"Erro {response.status_code}: {response.text}\n{data}"}
        return data



    @classmethod
    def send_message(cls, channel: Channel,number: str, text:str):
        """
        Args:
            number = DDD + number_default
        """
        url = f"{BASE_URL}/send/text"
        headers = cls.get_headers(channel)
        payload = {
            "number": number,
            "text": text,
            "linkPreview": False,
            "replyid": "",
            "mentions": "",     # "all" = todos, ou separando vou virgula, assim: "1234, 321" 
            "readchat": True,   # marcar chat como lido
            "delay": 1200,
            'convert': 'true'
        }
        response = requests.post(url, headers=headers,json=payload)
        if response.status_code == 200:
            data = response.json()
            channel.chatid = data.get('chatid')
            channel.idmessage = data.get('messageid')
        else:
            return {"error":f"{response.status_code}:{response.text}"}
        return data
    

    # preparar o data de uma requisição de envio de menu interativo
    @classmethod
    def prepare_menu(cls, message: str, type: str,number:str,options): # parametro message comentado
        data = {}
        # url = f"{self.channel.get_gateway_url}/message/sendList/{self.channel.token}"
        # OU POSSO COLOCR DATA = {...}
        data = {
            "number": number,
            "type": type, #// poll, list, button
            "text": message,
            "footerText": "Escolha uma opção",
            "buttonText": "Selecione",
            "selectableCount": 1,
            "choice":[],
            "replyid": "",
            "mentions": "",
            "readchat": True, #// marcar chat como lido
            "delay": 1200
        }
        for option in options:
            data["choice"].append(option)  # Adiciona diretamente strings
            if isinstance(option, dict) and "option" in option:
                data["choice"].append(option["option"])  # Adiciona o valor de "option"
        return data        

    #verifica se a mensagem possui o menu interativo ou se é uma mensagem normal
    # def prepare_message(self, message, options):
    #     # if not options: # retirava esse if
    #     #     return message
    #     for counter, option in enumerate(options, start=1):
    #         if not option["option"] in message: # retirava o if not 
    #             message += "{0} - {1}\n".format(counter, option["option"])
    #     return message



    # passo option como uma list[dict], porque ai no caso o usuario passaria tipo:
    """
        options = [
    {
        "title": "Opção 1",          # Título da opção (str)
        "description": "Detalhes",  # Descrição opcional (str)
        "rowId": "id_opcao_1"       # Identificador único da opção (str)
    },
    {
        "title": "Opção 2",
        "description": "Mais detalhes",
        "rowId": "id_opcao_2"
    }
]
    """
    @classmethod
    # o meu usuario vai passar só uma lista de dicionarios, então não tem porque eu montar um prepare_list ou prepare_Message, a mensagem já viria preparada agora imagine qual situação eu precisaria das duas funções anteriores
    def send_menu(cls,number: str,type: str,message: str, options):
        # passar uma messagem como parametro e options, passar um for por cada option em options
        #type: str, message: str, options: list[dict], **kwargs
        url = f"{BASE_URL}/send/menu"
        headers = cls.get_headers(channel)
        json = {
            "number": number,
            "type": type, #// poll, list, button
            "text": message,
            "footerText": "Escolha uma opção",
            "buttonText": "Selecione",
            "selectableCount": 1,
            "choices":[],
            "replyid": "",
            "mentions": "",
            "readchat": True, #// marcar chat como lido
            "delay": 1200
        }
        for option in options:
            json["choices"].append(option)  # Adiciona diretamente strings
            if isinstance(option, dict) and "option" in option:
                json["choices"].append(option["option"])  # Adiciona o valor de "option"
        # json = cls.prepare_menu(message, type,number,options)
        #     # dados de lista na raiz para v2
        response = requests.post(url,headers=headers,json=json)
        if response.status_code == 200:
            data = response.json()
        else:
            data = response.json()
            return {"error":f"{response.status_code}:{response.text}/n{data}"}
        return data

    
    # retorna o tipo de arquivo
    @classmethod
    def get_mimetype(cls, mimetype):
        if not mimetype:
            return "sticker"
        if "video" in mimetype:
            return "video"
        elif "audio" in mimetype:
            return "audio"
        elif "image" in mimetype:
            return "image"
        else:
            return "document"
    

    @classmethod
    def send_media(self, cls, channel: Channel,file: File, number:str, message:str):
        url = f"{BASE_URL}/send/media"
        headers = cls.get_headers(channel)
        mimetype = cls.get_mimetype(file.url) # aqui ele vai receber a url por meio de uma instância de File e di 
        # mimetype = mimetype.split[0] # retorna apenas o image, O VALOR QUE VAI AQUI, ELE APARECE NO TYPE EM DATA, CORRETO ?
        data = {
            "number": number,
            "text": message,
            "type": mimetype, #// document, video, image, audio, ptt, sticker
            "file": file.url,
            "docName": "", #//opcional, serve apenas para document
            "replyid": "",
            "mentions": "",
            "readchat": True, #// marcar chat como lido
            "delay": 1200
        }
        print(url)
        print(headers)
        print(data)
        response = requests.post(url, headers=headers,json=data)
        if response.status_code == 200:
            data = response.json()
        else:
            return {"error":f"{response.status_code}:{response.text}/n{data}"}
        return data
    


    @classmethod
    def send_location(cls,number: str, name: str,adress: str, latitude: str,longitude: str):
        url = f"{BASE_URL}/send/location"
        headers = cls.get_headers(channel)
        json = {
            "number": number,
            "name": name,
            "address": adress,
            "latitude": float(latitude),
            "longitude": float(longitude),
            "replyid": "",
            "mentions": "",
            "readchat": True, # marcar chat como lido
            "delay": 1200
        }
        print(json)
        response = requests.post(url,headers=headers,json=json)
        if response.status_code == 200:
            data = response.json()
        else:
            data = response.json()
            return {"error":f"{response.status_code}:{response.text}/n{data}"}
        return data




    @classmethod
    def send_contact(cls, channel: Channel, number: str, phonename: str, phonenumber: str):
        url = f"{BASE_URL}/send/contact"
        headers = cls.get_headers(channel)
        json = {
            "number": number, #numero da pessoa que vai receber a mensagem, no casa da api oficial, seria client.phone
            "fullName": phonename, # nome do contato que tô compartilhando
            "phoneNumber": phonenumber, # número do contato que tô comprtilhando
            "organization": "organization",# onde... 
            # client: Client
            # organization = client.organization 
            "email": "", # email = client.email
            "url": "",
            "replyid": "",
            "mentions": "",
            "readchat": True, #// marcar chat como lido
            "delay": 1200
        }
        response = requests.post(url,headers=headers,json=json)
        if response.status_code == 200:
            data = response.json()
        else:
            return {"error":f"{response.status_code}:{response.text}/n{data}"}
        return data

    
    @classmethod
    def download_message(cls,channel: Channel):
        url = f"{BASE_URL}/message/download"
        headers = cls.get_headers(channel)
        json = {
            "id": channel.idmessage,
            "transcribe": False,
            "openai_apikey": "",
        }
        print(json)
        response = requests.post(url,headers=headers,json=json)
        if response.status_code == 200:
            data = response.json()
        else:
            data = response.json()
            return {"error":f"{response.status_code}:{response.text}/n{data}"}
        return data

        
    @classmethod
    def find_message(cls,channel: Channel):
        url = f"{BASE_URL}/message/find"
        headers = cls.get_headers(channel)
        json = {
            "chatid": channel.chatid,
            "limit": 2
        }
        print(channel.chatid)
        response = requests.post(url,headers=headers,json=json)
        if response.status_code == 200:
            data = response.json()
        else:
            return {"error":f"{response.status_code}:{response.text}/n{data}"}
        return data



    @classmethod
    def delete_message(cls,channel: Channel):
        url = f"{BASE_URL}/message/delete"
        headers = cls.get_headers(channel)
        json = {
            "id":channel.idmessage,
        }
        response = requests.post(url,headers=headers,json=json)
        if response.status_code == 200:
            data = response.json()
        else:
            return {"error":f"{response.status_code}:{response.text}"}
        return data



    @classmethod
    def send_emoticon(cls,number: str,channel: Channel): # criar um model só pros emojis que se liga ao chat e rastreia pela instância do chat quem recebeu e quem enviou 
        url = f"{BASE_URL}/message/react"
        headers = cls.get_headers(channel)
        json = {
            "number":f'{number}@s.whatsapp.net',
            "text":"🤖",
            "id": channel.id,
        }
        print(url)
        print(headers)
        print(json)
        send = False
        response = requests.post(url,headers=headers,json=json)
        if response.status_code == 200:
            data = response.json()
            send = True
        else:
            data = response.json()
            return {f"{response.status_code}:{response.text}/n{data}"}
        return data,send
        
    @classmethod
    def find_Chat(cls,channel: Channel,name: str):
        url = f"{BASE_URL}/chat/find"
        headers = cls.get_headers(channel)
        json = {
            "lead_name": name,       #// Busca por nomes que contenham "John" (LIKE)
            "wa_isGroup": False,         #// Filtra apenas chats que são grupos
            "wa_unreadCount": ">0",     #// Chats com contagem de mensagens não lidas maior que 0
            "lead_status": "!~inactive", #// Exclui leads com status "inactive" (NOT LIKE)
            "sort": "-wa_lastMsgTimestamp", #// Ordena por 'wa_lastMsgTimestamp' em ordem decrescente
            "limit": 50,                #// Limita o resultado a 50 registros
            "offset": 0                 #// Começa a partir do primeiro registro
        }
        response = requests.post(url,headers=headers,json=json)
        if response.status_code == 200:
            data = response.json()
        else:
            data = response.json()
            return {f"{response.status_code}:{response.text}/n{data}"}
        return data


    @classmethod
    def get_contacts(cls):
        url = f"{BASE_URL}/contacts"
        headers = cls.get_headers(channel)
        json = {}
        response = requests.get(url,headers=headers,json=json)
        if response.status_code == 200:
            data = response.json()
        else:
            data = response.json()
            return {f"{response.status_code}:{response.text}/n{data}"}
        return data
        
    
    @classmethod
    def delete_chat(cls,number: str):
        url = f"{BASE_URL}/chat/delete"
        headers = cls.get_headers(channel)
        {
            "number": number,
            "deleteChatWhatsApp": True,
            "deleteChatDB": True,
            "deleteMessagesDB": True
        }
        response = requests.post(url,headers=headers,json=json)
        if response.status_code == 200:
            data = response.json()
        else:
            data = response.json()
            return {f"{response.status_code}:{response.text}/n{data}"}
        return data


    @classmethod
    def create_group(cls,namegroup,*numbers):
        url = f"{BASE_URL}/group/create"
        headers = cls.get_headers(channel)
        json = {
            "name":namegroup,
            "participants":[]
        }
        for number in numbers:
            json['participants'].append(number)
        response = requests.post(url,headers=headers,json=json)
        if response.status_code == 200:
            data = response.json()
            channel.groupid = data.get('group',{}).get('jid', 'id não encontrado')
        else:
            data = response.json()
            return {f"{response.status_code}:{response.text}/n{data}"}
        return data


    @classmethod
    def details_group(cls):
        url = f"{BASE_URL}/group/info"
        headers = cls.get_headers(channel)
        json = {
            "GroupJID": channel.groupid,
            "getInviteLink": True, # irá pegar o inviteLink atualizado se for admin
            "force": True  # Usamos cache para evitar ratelimit no servidor do whatsapp, se precisar resetar o cache , coloque como true.
        }
        response = requests.post(url,headers=headers,json=json)
        if response.status_code == 200:
            data = response.json()
        else:
            data = response.json()
            return {f"{response.status_code}:{response.text}/n{data}"}
        return data




    @classmethod
    def get_group(cls):
        url = f"{BASE_URL}/grouplist?force=false"
        headers = cls.get_headers(channel)
        json = {}
        response = requests.get(url,headers=headers,json=json)
        if response.status_code == 200:
            data = response.json()
        else:
            data = response.json()
            return {f"{response.status_code}:{response.text}/n{data}"}
        return data


    # cria o link do convite para entrar no grupo
    @classmethod
    def invite_link(cls):
        url = f"{BASE_URL}/group/invitelink/120363419258644935@g.us"
        headers = cls.get_headers(channel)
        json = {
            "number":"5586995774681"
        }
        response = requests.get(url,headers=headers,json=json)
        if response.status_code == 200:
            data = response.json()
            channel.invitelink = data.get('inviteLink')
        else:
            data = response.json()
            return {f"{response.status_code}:{response.text}/n{data}"}
        return data
    
    
    # mandar o link do grupo no send_message, aí o usuario pode entrar no grupo pelo convite 
    @classmethod
    def enter_group(cls,channel: Channel):
        url = f"{BASE_URL}/group/join"
        headers = cls.get_headers(channel)
        json = {
            "inviteCode": channel.invitelink
        }
        response = requests.post(url,headers=headers,json=json)
        if response.status_code == 200:
            data = response.json()
        else:
            data = response.json()
            return {f"{response.status_code}:{response.text}/n{data}"}
        return data

    @classmethod
    def exit_group(cls):
        url = f"{BASE_URL}/group/leave"
        headers = cls.get_headers(channel)
        json = {
            "groupjid": channel.groupid
        }
        response = requests.post(url,headers=headers,json=json)
        if response.status_code == 200:
            data = response.json()
        else:
            data = response.json()
            return {f"{response.status_code}:{response.text}/n{data}"}
        return data


    # sei que funciona
    @classmethod
    def create_comunity(cls,name):
        url = f"{BASE_URL}/community/create"
        headers = cls.get_headers(channel)
        json = {
            "name": name
        }
        response = requests.post(url,headers=headers,json=json)
        if response.status_code == 200:
            data = response.json()
        else:
            data = response.json()
            return {f"{response.status_code}:{response.text}/n{data}"}
        return data
        
    

    # funciona
    @classmethod
    # OBS: Seria importante ter um model só pra grupos, pra poder manipular melhor
    def edit_members(cls,action,*numbers):
        url = f"{BASE_URL}/group/updateParticipants"
        headers = cls.get_headers(channel)
        json = {
            "groupjid": channel.groupid,
            "action": action, # 'add' | 'remove' | 'promote' | 'demote' | 'reject' | 'approve';
            "participants": []
        }
        for number in numbers:
            json["participants"].append(number)
        response = requests.post(url,headers=headers,json=json)
        if response.status_code == 200:
            data = response.json()
        else:
            data = response.json()
            return {f"{response.status_code}:{response.text}/n{data}"}
        return data
        


    #funciona, mas tem que testar
    @classmethod
    def edit_groups(cls,*groupsid):
        url = f"{BASE_URL}/community/editgroups"
        headers = cls.get_headers(channel)
        json = {
            "community": "120363324255083289@g.us", # valor de exemplo, campo correspondente a comunidade que eu criei
            "action": "remove", # "add", "remove"
            "groupjids": []  # adicionar outros separado por virgula
        }
        for group in groupsid:
            json["groupjids"].append(group)
        response = requests.post(url,headers=headers,json=json)
        if response.status_code == 200:
            data = response.json()
        else:
            data = response.json()
            return {f"{response.status_code}:{response.text}/n{data}"}
        return data

    
    @classmethod
    def editlead(cls):
        url = f"{BASE_URL}/chat/editLead"
        headers = cls.get_headers(channel)
        json = {
            "id": "id",
            "lead_name": "lead_name",
            "lead_fullName": "lead_fullName",
            "lead_email": "lead_email",
            "lead_personalid": "lead_personalid", # // Espera um identificador pessoal único do lead, como CPF ou outro número de documento.
            "lead_status": "lead_status", # Espera o status atual do lead, como "ativo", "inativo", "em andamento" ou outro valor definido pela API. 
            "lead_tags": ["VIP", "teste2"], # Espera uma lista de etiquetas (tags) para categorizar o lead, como "VIP", "novo" ou "prioridade"
            "lead_notes": "lead_notes", # Espera uma string com anotações ou comentários sobre o lead, como "Cliente interessado em promoções".
            "lead_disableChatBotUntil": 123, # Espera um número (timestamp) indicando até quando o chatbot deve ficar desativado para esse lead.
            "lead_isTicketOpen": True, # Espera um valor booleano (true/false) indicando se há um ticket aberto para o lead.
            "lead_assignedAgent_id": "lead_assignedAgent_id", # Espera o ID do agente responsável pelo lead, como um código único de um usuário no sistema.
            "lead_kanbanOrder": 1, # Espera o ID do agente responsável pelo lead, como um código único de um usuário no sistema.
        }
        response = requests.post(url,headers=headers,json=json)
        if response.status_code == 200:
            data = response.json()
        else:
            data = response.json()
            return {f"{response.status_code}:{response.text}/n{data}"}
        return data





    @classmethod # função simples
    def massmessage(cls,folder,info,textmessage,*numbers):
        """ #   // Media message (image, video, audio, myaudio, document)
            #   "text": "Olá! Temos uma promoção especial para você.",
            #   "file": "https://example.com/arquivo.jpg",
            #   "docName": "documento.pdf",
            
            #   // Contact message
            #   "fullName": "João Silva",
            #   "phoneNumber": "+55 11 99999-9999",
            #   "organization": "Empresa XYZ",
            #   "email": "joao@email.com",
            #   "url": "https://exemplo.com",
            
            #   // Location message
            #   "name": "Shopping Center",
            #   "address": "Av. Paulista, 1000",
            #   "latitude": -23456789,
            #   "longitude": -46789012,
            
            
            #   // Menu message (poll, list, button)
            #   "text": "Olá! Temos uma promoção especial para você.",
            #   "footerText": "Escolha uma opção:",
            #   "buttonText": "Ver opções",
            #   "selectableCount": 1,
            #   "choices": ["Opção 1", "Opção 2", "Opção 3"]"""
        url = f"{BASE_URL}/sender/simple"
        headers = cls.get_headers(channel)
        json = {
            "numbers": [], # define quem vai receber a mensagem, daria pra pegar todos os contatos de um número pelo get_contacts, o problema seria como seria salvo e como pegar eles
            "type": "text",  #// options: text, image, video, audio, myaudio, document, sticker, contact, location, poll, list, button
            "folder": folder, # campanha de dezembro
            "delayMin": 20,
            "delayMax": 40,
            "info": info, #"campanha de natal"
            "scheduled_for": schedule_for, # // "1735689600000" = Agenda para 01/01/2025 (data unix em milisegundos) ou "30" = Agenda para daqui 30 minutos
            
            #// For all messages
            "delay": 1000,
            "mentions": "",

            #// Text message
            "text": f"{folder}\n{info}\n{textmessage}",
            "linkPreview": True
        } 
        for number in numbers:
            json['numbers'].append(number)
        response = requests.post(url,headers=headers,json=json)
        if response.status_code == 200:
            data = response.json()
        else:
            data = response.json()
            return {f"{response.status_code}:{response.text}/n{data}"}
        return data


    def massmessageadvanced(cls,):
        url = f"{BASE_URL}/sender/advanced"
        headers = cls.get_headers(channel)
        json = {
            "delayMin": 3,
            "delayMax": 6,
            "info": "teste avançado",
            "scheduled_for": 1,
            "messages": [
                {
                    "number": "número de telefone ou chat id",
                    "type": "text",
                    "text": "First message"
                },
                {
                    "number": "número de telefone ou chat id",
                    "type": "text",
                    "file": "https://example.com/image.jpg",
                    "text": "texto2"
                },
                {
                    "number": "número de telefone ou chat id",
                    "type": "list",
                    "text": "Choose an option",
                    "choices": [
                        "Option 1",
                        "Option 2"
                    ]
                }
            ]
        }
        response = requests.post(url,headers=headers, json=json)
        if response.status_code == 200:
            data = response.json()
        else:
            data = response.json()
            return {f"{response.status_code}:{response.text}/n{data}"}
        return data



    def definewebhook(cls):
        url = f"{BASE_URL}/webhook"
        wburl = "https://webhook.site/e532f4ef-77c8-4c16-9133-8262e8382794"
        headers = cls.get_headers(channel)
        json = {
            "enabled": True,
            "url": wburl,
            "events": [
                "connection",
                "history",
                "messages",
                "messages_update",
                "call",
                "contacts",
                "presence",
                "groups",
                "labels",
                "chats",
                "chat_labels",
                "blocks",
                "leads"
            ],
            "excludeMessages": [
                # "wasSentByApi",
                # "wasNotSentByApi",
                # "fromMeYes",
                # "fromMeNo",
                # "isGroupYes",
                # "IsGroupNo"
            ],
            "addUrlEvents": True,
            "addUrlTypesMessages": True,
            "action": "add"
        }
        response = requests.post(url,headers=headers,json=json)
        if response.status_code == 200:
            data = response.json()
            return f"WebHook configurado com sucesso"
        else:
            data = response.json()
            return {f"{response.status_code}:{response.text}/n{data}"}











channel = Channel() # instância/cria a pessoa que vai usar a classe Uazapi{

uazapi = UazapiApi() # instância a classe uazapi
file = File()
json = {
    "name":channel.name,
    "systemname":channel.systemname,
}
print(f'----- Rodando Teste de função -----')
# print(uazapi.create_instance(channel, json)) 
# print(uazapi.connect_instance(channel))
# print(uazapi.send_message(channel,'5586995774681',f'Acorda, criança!\n papai chegou\n{file.url}')) # "número de telefone ou chat id@s.whatsapp.net
options = ["escolha uma opção",'sim','não']
# print(uazapi.send_menu('5586998419749','list','Teste',options)) # funciona
# print(uazapi.send_media(UazapiApi,channel,file,'5586995774681','teste sendmedia')) # teste concluido com sucesso, mas só com a url especificada
# print(uazapi.find_message(channel)) # funciona, Vai pegar pela instância de Chat(chat.id_message), no projeto real
# print(uazapi.delete_message(channel))
emoji = Emoji()
# print(uazapi.get_status(channel)) # funciona
# print('-'*20)
# print(uazapi.send_emoticon("5586995774681",channel)) # o certo seria passar um emoji como paramêtro, mas como é teste...TÁ DANDO ERRO, JÁ TENTEI COM OS DOIS TIPOS DE PADRÃO
# print(uazapi.send_contact(channel,'5586995774681')) # funcionou
# print(uazapi.download_message(channel)) # PEGAR CHAVE DA OPENIA - FALTA TESTAR
# print(uazapi.find_Chat(channel,'Pedro Gabriel')) funciona 
# print(uazapi.get_contacts()) funciona
# print(uazapi.delete_chat(number)) # funciona
# print(uazapi.create_group("Teste","5586995774681","5586998419749"))
# print(uazapi.invite_link()) # funcionou
# print(uazapi.massmessage('Olá, teste de mensagem em massa','Teste de mensagem em massa pra ser enviado pra vários contatos referente ao mês do consumidor e bla bla bla', 'teste teste teste teste teste','5586995774681','558681698877','86998419749')) 
print(uazapi.definewebhook())
# print(uazapi.send_location('5586995774681','Ninho do urubu','Estr. dos Bandeirantes, 25997 - Vargem Grande, Rio de Janeiro - RJ, 22785-275','-22.9841','-43.5057'))
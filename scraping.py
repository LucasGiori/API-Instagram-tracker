import requests,json,re
from bs4 import BeautifulSoup
from datetime import datetime


#url do instagram
url="https://www.instagram.com/{}"

#Função de parser do json contido no script
def parser_sharedData(soup):
    try:
        #Neste for ele realiza um loop entre todos as tags script do site do instagram
        for i in soup.findAll("script"):   
            #Enquanto ele realiza o loop ele tenta verificar se encontra esse texto em alguma das tags script, é onde contem o json com os dados que precisamos coletar         
            if re.search('<script type="text/javascript">window._sharedData =', str(i)) is not None:
                jsoninfo= str(i)  
                #retirando os textos da script para pegar somente o conteudo e fazer o loads do json que contem.
                jsoninfo=jsoninfo.replace('<script type="text/javascript">window._sharedData =','').replace(';</script>','')
                jsoninfo=json.loads(jsoninfo)
                return jsoninfo
    except:          
        return None

def scrape_data(username):
    #requisição na página do instagram passando o parametro o nome do usuário
    r = requests.get(url.format(username))
    #biblioteca de parser do HTML
    soup = BeautifulSoup(r.text,"html.parser")     
    #chamando a função de parser dos dados   
    return parser_sharedData(soup) 


def getReturnScraping(listausuarios):
    request={}
    dataperfis=[]
    
    for nome in listausuarios:     
        try:   
            jsoninfo = scrape_data(nome)
            users={}
            users['nome_completo']   =jsoninfo["entry_data"]["ProfilePage"][0]["graphql"]["user"]["full_name"]
            users['usuario']         =jsoninfo["entry_data"]["ProfilePage"][0]["graphql"]["user"]["username"]
            users['conta_privada']   =jsoninfo["entry_data"]["ProfilePage"][0]["graphql"]["user"]["is_private"]
            users['seguindo']        =jsoninfo["entry_data"]["ProfilePage"][0]["graphql"]["user"]["edge_follow"]["count"]
            users['seguidores']      =jsoninfo["entry_data"]["ProfilePage"][0]["graphql"]["user"]["edge_followed_by"]["count"]
            users['qtdpublicacoes']  =jsoninfo["entry_data"]["ProfilePage"][0]["graphql"]["user"]["edge_owner_to_timeline_media"]["count"]
            users['biografia']       =jsoninfo["entry_data"]["ProfilePage"][0]["graphql"]["user"]["biography"]
            users['codigo_pais']     =jsoninfo["country_code"]
            users['conta_businsess'] =jsoninfo["entry_data"]["ProfilePage"][0]["graphql"]["user"]["is_business_account"]
            users['conta_recente']   =jsoninfo["entry_data"]["ProfilePage"][0]["graphql"]["user"]["is_joined_recently"]
            users['foto_perfil_url'] =jsoninfo["entry_data"]["ProfilePage"][0]["graphql"]["user"]["profile_pic_url"]

            timeline=[]
            #Verificando se a conta é privada
            if users['conta_privada'] == False:    
                for i in jsoninfo["entry_data"]["ProfilePage"][0]["graphql"]["user"]["edge_owner_to_timeline_media"]["edges"]:#percorrendo a timeline das contas publicas
                    datatimeline={}
                    raiz = i['node']
                    datatimeline['id']=raiz['id']
                    datatimeline['quantidade']=jsoninfo["entry_data"]["ProfilePage"][0]["graphql"]["user"]["edge_owner_to_timeline_media"]["count"]
                    datatimeline['url_visualizacao']=raiz['display_url']
                    datatimeline['video']=raiz['is_video']
                    try:
                        datatimeline['data_hora']= datetime.strftime(datetime.fromtimestamp(raiz['taken_at_timestamp']),'%d-%m-%Y %H:%M:%S')
                        datatimeline['data']=datetime.strftime(datetime.fromtimestamp(raiz['taken_at_timestamp']),'%d-%m-%Y')
                        datatimeline['hora']=datetime.strftime(datetime.fromtimestamp(raiz['taken_at_timestamp']),'%H:%M:%S')
                    except:                    
                        datatimeline['data_hora']=None
                        datatimeline['data']=None
                        datatimeline['hora']=None
                    try:
                        datatimeline['localizacao']=raiz['location']["name"]
                    except:
                        datatimeline['localizacao']=None 
                    datatimeline['qtdcomentarios']=raiz['edge_media_to_comment']["count"]
                    datatimeline['qtdcurtidas']=raiz['edge_media_preview_like']["count"]
                    datatimeline['mediacurtidas']=raiz['edge_liked_by']["count"]
                    try:
                        datatimeline['qtdvisualizacoes']=raiz['video_view_count']
                    except:
                        datatimeline['qtdvisualizacoes']=None
                    timeline.append(datatimeline)          
            users['estatisticatimeline'] = timeline  
            dataperfis.append(users)
        except:   
            #Caso não encontrar um usuário com o nome informado define este json!
            dataperfis.append({"usuario":nome,"status":"Não Encontrado!"})         

    request['info']=dataperfis        
    return request



    
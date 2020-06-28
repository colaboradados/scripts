from selenium import webdriver

driver = webdriver.Chrome()

pages = [
    "https://site-colaboradados.herokuapp.com/states/acre.html", "https://site-colaboradados.herokuapp.com/states/alagoas.html",
    "https://site-colaboradados.herokuapp.com/states/amapa.html", "https://site-colaboradados.herokuapp.com/states/amazonas.html",
    "https://site-colaboradados.herokuapp.com/states/bahia.html", "https://site-colaboradados.herokuapp.com/states/ceara.html",
    "https://site-colaboradados.herokuapp.com/states/espirito-santo.html", "https://site-colaboradados.herokuapp.com/states/goias.html",
    "https://site-colaboradados.herokuapp.com/states/maranhao.html", "https://site-colaboradados.herokuapp.com/states/mato-grosso-do-sul.html",
    "https://site-colaboradados.herokuapp.com/states/mato-grosso.html", "https://site-colaboradados.herokuapp.com/states/minas-gerais.html",
    "https://site-colaboradados.herokuapp.com/states/para.html", "https://site-colaboradados.herokuapp.com/states/paraiba.html",
    "https://site-colaboradados.herokuapp.com/states/parana.html", "https://site-colaboradados.herokuapp.com/states/pernambuco.html",
    "https://site-colaboradados.herokuapp.com/states/piaui.html", "https://site-colaboradados.herokuapp.com/states/rio-de-janeiro.html",
    "https://site-colaboradados.herokuapp.com/states/rio-grande-do-norte.html", "https://site-colaboradados.herokuapp.com/states/rio-grande-do-sul.html",
    "https://site-colaboradados.herokuapp.com/states/rondonia.html", "https://site-colaboradados.herokuapp.com/states/roraima.html",
    "https://site-colaboradados.herokuapp.com/states/santa-catarina.html", "https://site-colaboradados.herokuapp.com/states/sao-paulo.html",
    "https://site-colaboradados.herokuapp.com/states/sergipe.html", "https://site-colaboradados.herokuapp.com/states/tocantins.html",
    "https://site-colaboradados.herokuapp.com/jekyll/update/2019/01/21/esfera-federal.html",
    "https://site-colaboradados.herokuapp.com/jekyll/update/2019/01/20/esfera-estadual.html",
    "https://site-colaboradados.herokuapp.com/jekyll/update/2019/01/18/cinema.html",
    "https://site-colaboradados.herokuapp.com/jekyll/update/2019/01/17/musica.html",
    "https://site-colaboradados.herokuapp.com/jekyll/update/2019/01/16/saude.html",
    "https://site-colaboradados.herokuapp.com/jekyll/update/2019/01/15/educacao.html",
    "https://site-colaboradados.herokuapp.com/jekyll/update/2019/01/14/paises.html",
    "https://site-colaboradados.herokuapp.com/jekyll/update/2019/01/13/ibge.html",
    "https://site-colaboradados.herokuapp.com/jekyll/update/2019/01/12/colecoes.html",
    "https://site-colaboradados.herokuapp.com/jekyll/update/2019/01/11/seguranca-publica.html",
    "https://site-colaboradados.herokuapp.com/jekyll/update/2019/01/10/meio-ambiente.html",
    "https://site-colaboradados.herokuapp.com/jekyll/update/2020/03/19/coronavirus.html"
]

exclude = [
    "Colaboradados", "IMDB", "ORGANIZAÇÃO MUNDIAL DA SAÚDE (OMS)",
    "Dados mundiais sobre a saúde", "Base de dados do Internet Movie Database",
    "Base de dados de filmes estrangeiros exibidos no país entre o Omniógrafo (1896) e a passagem ao sonoro (1934)",
    "Base de dados de Filmes do Mercosul",
    "Portal de Acesso à Informação e Transparência dos Municípios do Estado do Amazonas",
    "https://site-colaboradados.herokuapp.com/jekyll/update/2019/01/17/musica.html",
    "https://site-colaboradados.herokuapp.com/jekyll/update/2019/01/14/paises.html",
    "https://site-colaboradados.herokuapp.com/jekyll/update/2019/01/12/colecoes.html",
    "ViriHealth – Canada’s Coronavirus COVID-19 Tracker",
    "Sundhedsstyrelsen (Ministério da saúde dinamarquês",
    "Governo britânico", "Global Change Data Lab",
    "CovidTrack", "Múltiplas fontes", "Universidade Federal de Viçosa",
    "The COVID Tracking Project", "Brasil.io", "Brasil.io: Coleção de CNPJs e CPFs brasileiros",
    "Johns Hopkins University", "Download de dados do coronavírus • coronabr",
    "GitHub - rodrilima/corona-analytic-api: API that generates information about coronavirus (COVID19) cases in the states of Brazil and other parts of the world",
    "Corona Virus (covid-19) Data for Brasil - Covid19br", "Observatório COVID-19 BR",
    "Coronavirus COVID19 API", "CrowdTangle", "Secretaria de Estado do Planejamento - Corona em Santa Catarina",
    "COVID-19 Canada", "Dados recolhidos de api pública que provê dados da Johns Hopkins University",
    "Reddit com informações moderadas a todo momento"
]

all_portals = open("all_portals.csv", "w")
bot_portals = open("bot_portals.csv", "w")

all_portals.write("url;orgao\n")
bot_portals.write("url;orgao\n")

total_amount_portals = open("total_amount_portals.txt","w")
total_amount_portals.write("----- CONTAGEM DE BASES - COLABORADADOS -----\n")
total_general = 0
total_city = 0
count_cities = True

for page in pages:
    driver.get(page)
    title = driver.find_element_by_class_name("title")
    strongs = driver.find_elements_by_xpath("//strong")
    total_portals = len(strongs)
    total_amount_portals.write("{}: {}\n".format(title.text, total_portals))
    total_general += total_portals
    if page == "https://site-colaboradados.herokuapp.com/jekyll/update/2019/01/21/esfera-federal.html":
        count_cities = False
        total_amount_portals.write("ESFERA MUNICIPAL: {}\n".format(total_city))
    if count_cities:
        total_city += total_portals

    for strong in strongs:
        orgao = strong.text
        links = strong.find_elements_by_tag_name('a')
        for link in links:
            url = link.get_attribute("href")
            all_portals.write(url + ";")
            if not (orgao in exclude or page in exclude):
                bot_portals.write(url + ";")
        if not (orgao in exclude or page in exclude):
            bot_portals.write(orgao.replace(":", "") + "\n")
        all_portals.write(orgao.replace(":", "") + "\n")

total_amount_portals.write("Total geral de bases: " + str(total_general))

all_portals.close()
bot_portals.close()
driver.close()

import requests
from bs4 import BeautifulSoup as bs

pages = [
    "http://colaboradados.com.br/states/acre.html", "http://colaboradados.com.br/states/alagoas.html",
    "http://colaboradados.com.br/states/amapa.html", "http://colaboradados.com.br/states/amazonas.html",
    "http://colaboradados.com.br/states/bahia.html", "http://colaboradados.com.br/states/ceara.html",
    "http://colaboradados.com.br/states/espirito-santo.html", "http://colaboradados.com.br/states/goias.html",
    "http://colaboradados.com.br/states/maranhao.html", "http://colaboradados.com.br/states/mato-grosso-do-sul.html",
    "http://colaboradados.com.br/states/mato-grosso.html", "http://colaboradados.com.br/states/minas-gerais.html",
    "http://colaboradados.com.br/states/para.html", "http://colaboradados.com.br/states/paraiba.html",
    "http://colaboradados.com.br/states/parana.html", "http://colaboradados.com.br/states/pernambuco.html",
    "http://colaboradados.com.br/states/piaui.html", "http://colaboradados.com.br/states/rio-de-janeiro.html",
    "http://colaboradados.com.br/states/rio-grande-do-norte.html", "http://colaboradados.com.br/states/rio-grande-do-sul.html",
    "http://colaboradados.com.br/states/rondonia.html", "http://colaboradados.com.br/states/roraima.html",
    "http://colaboradados.com.br/states/santa-catarina.html", "http://colaboradados.com.br/states/sao-paulo.html",
    "http://colaboradados.com.br/states/sergipe.html", "http://colaboradados.com.br/states/tocantins.html",
    "http://colaboradados.com.br/jekyll/update/2019/01/21/esfera-federal.html",
    "http://colaboradados.com.br/jekyll/update/2019/01/20/esfera-estadual.html",
    "http://colaboradados.com.br/jekyll/update/2019/01/18/cinema.html",
    "http://colaboradados.com.br/jekyll/update/2019/01/17/musica.html",
    "http://colaboradados.com.br/jekyll/update/2019/01/16/saude.html",
    "http://colaboradados.com.br/jekyll/update/2019/01/15/educacao.html",
    "http://colaboradados.com.br/jekyll/update/2019/01/14/paises.html",
    "http://colaboradados.com.br/jekyll/update/2019/01/13/ibge.html",
    "http://colaboradados.com.br/jekyll/update/2019/01/12/colecoes.html",
    "http://colaboradados.com.br/jekyll/update/2019/01/11/seguranca-publica.html",
    "http://colaboradados.com.br/jekyll/update/2019/01/10/meio-ambiente.html",
    "http://colaboradados.com.br/jekyll/update/2020/03/19/coronavirus.html"
]

exclude = [
    "Colaboradados", "IMDB", "ORGANIZAÇÃO MUNDIAL DA SAÚDE (OMS)",
    "Dados mundiais sobre a saúde", "Base de dados do Internet Movie Database",
    "Base de dados de filmes estrangeiros exibidos no país entre o Omniógrafo (1896) e a passagem ao sonoro (1934)",
    "Base de dados de Filmes do Mercosul",
    "Portal de Acesso à Informação e Transparência dos Municípios do Estado do Amazonas",
    "http://colaboradados.com.br/jekyll/update/2019/01/17/musica.html",
    "http://colaboradados.com.br/jekyll/update/2019/01/14/paises.html",
    "http://colaboradados.com.br/jekyll/update/2019/01/12/colecoes.html",
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

if __name__ == "__main__":
    all_portals = open("all_portals.csv", "w")
    bot_portals = open("bot_portals.csv", "w")

    all_portals.write("url;orgao\n")
    bot_portals.write("url;orgao\n")

    total_amount_portals = open("total_amount_portals.txt", "w")
    total_amount_portals.write(
        "----- CONTAGEM DE BASES - COLABORADADOS -----\n"
    )

    total_general = 0
    total_city = 0
    count_cities = True

    for page in pages:
        response = requests.get(page)
        soup = bs(response.text, "html.parser")
        main_div = soup.find("div", {"id": "main"})

        title = soup.find("title")
        strongs = main_div.find_all("strong")

        total_portals = len(strongs)
        total_amount_portals.write(f"{title.text}: {total_portals}\n")

        total_general += total_portals

        if page == "http://colaboradados.com.br/jekyll/update/2019/01/21/esfera-federal.html":
            count_cities = False
            total_amount_portals.write(f"ESFERA MUNICIPAL: {total_city}\n")

        if count_cities:
            total_city += total_portals

        for strong in strongs:
            orgao = strong.text
            links = strong.find_all('a')

            for link in links:
                url = link.get("href", None)
                all_portals.write(f"{url};")

                if not (orgao in exclude or page in exclude):
                    bot_portals.write(f"{url};")

            if not (orgao in exclude or page in exclude):
                bot_portals.write(orgao.replace(":", "") + "\n")

            all_portals.write(orgao.replace(":", "") + "\n")

    total_amount_portals.write(f"Total geral de bases: {total_general}")

    all_portals.close()
    bot_portals.close()

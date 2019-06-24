# Analise de séries temporáis de furto e roubos no estado do Espírito Santo

## Motivação

Segundo a legislação brasileira, (citar o artigo). Dessa forma a SESP-ES (Secretaria do Estado de Segurança Pública do Espírito Santo), disponibiliza um repositório com os boletins de ocorrencia registrados no estado. Com base nisso e a popularização de técnicas mais sofisticadas de predição, tais quais (Machine Learning e Deep Learning) surgiu o projeto. O objetivo é utilizar técnicas de predição já consolidadas e aplica-las neste dominio específico, que é a Analise de séries temporáis de roubos no estado do Espirito Santo, especificamente a [RMGV](https://pt.wikipedia.org/wiki/Região_Metropolitana_de_Vitória) (Região Metropolitana da Grande Vitória).

## Etapas do Projeto

Este projeto foi divido em 4 etapas principais: Data Collection, Data Cleaning & Transformation, Data Prediction e Data Visualization.

### Data Collection

A SESP-ES, disponibiliza em um [_Repositório_](https://boletins.sesp.es.gov.br) publico, divididos em lotes, todos os boletins registrado no estado do Espírito Santo em forato PDF. Com isso foi realizado a coleta desses lotes utilizando o [_Aria2_](https://aria2.github.io/manual/pt/html/index.html).
Para realização deste projeto foi feito a coleta de 244 lotes, totalizando 135 GB (aproximadamente 2.5 milhões de boletins). Contendo os boletins registrados no periodo de 01 de janeiro de 2013 até 31 de dezembro de 2018.


### Data Cleaning & Transformation

Após a coleta dos lotes, os mesmos foram extraidos em um diretório e foram segmentados segundo o lote pertencente. Em seguida fora utilizado a biblioteca [_Textract_](https://textract.readthedocs.io/en/stable/)  do Python para carregar os lotes de boletins em memória e a partir desse ponto realizar a remoção de boletins invalidados pela SESP-ES. terminado essa verificação os memos foram salvos em outro diretório em formato de texto (TXT), este diretório que possui a mesma estrutura do diretório de origem dos lotes.

O proximo passo foi realizar a extração das informações contidas nos boletins. Após analise da estrutura dos boletins foi utilizado a biblioteca [_RE_](https://docs.python.org/3/library/re.html) do Python, para através de expressões regulares, realizar a coleta das informações dos boletins. E em seguida os mesmos foram compilados em JSON e armazenados em outro diretório que possui a mesma estrutura dos anteriores.

Abaixo temos a estrutura dos boletins de ocorrencia em PDF e dos lotes em JSON.

![Boletim de ocorrência](https://github.com/andrebvitoria/Projeto-BO/blob/master/Images/BO/BO.png)

**Legenda:**
1. Data de Registro
2. Tipo de Local
3. Data de ocorrência
4. Categoria do BO e descrição da Categoria
5. Endereço aonde ocorreu o incidente
6. Objetos relacionados ao incidente


```JSONasPython
  [
    {
      "id": int,
      "registrado": [date, time],
      "data": [date, time],
      "codigo": string,
      "descricao": string,
      "tipo_de_local": string,
      "local": string,
      "complemento": string,
      "bairro": string,
      "municipio": string,
      "referencia": string,
      "item": { 
          string: [string, string, string],
          ...
          string: [string, string, string],
      }
    },
  ]
```
Exemplo.:
```json
[
  {
    "id": 29792131,
    "registrado": ["26/08/2016", "15:25"],
    "data": ["22/08/2016", "20:00"],
    "codigo": "B01A",
    "descricao": "CRIMES CONTRA PATRIM\u00d4NIO: FURTO: A PESSOA EM VIA P\u00daBLICA",
    "tipo_de_local": "VIA P\u00daBLICA",
    "local": "RUA ALEXANDRE CALMON",
    "complemento": "",
    "bairro": "CENTRO",
    "municipio": "COLATINA",
    "referencia": "PERTO DA MANTEL",
    "item": {
      "1": ["APARELHOS TELEFONICOS", "ROUBADO", "1"]
    }
  }
]
```

Em seguida foi realizado a segmentação dos boletins por categoria, e não mais por lote. A partir desse ponto foi definido qual seria o dominio do problema. As transformações e tratamentos foram realziados apenas nos boletins de Categoria B, nas subcategorias 01 e 02, que pertencem a categoria de Crimes Contra Patrimônio, e dividias em Furto e Roubo, respectivamente.

Realizado a segmentação foi iniciado o processo de Geocoding, que consiste em, a partir do endereço, identificar as coordenadas geográficas que pertencem a esse endereço. Para isso fora utilizado sistemas denominados GIS ([_Geographic Information System_](https://en.wikipedia.org/wiki/Geographic_information_system)), inicialmente fora utilizado o GIS disponibilizado pela Google, o [_Google Maps_](https://developers.google.com/maps/documentation/geocoding/start?hl=pt-br), porém devido a limitações no numero de mapeamentos permitidos, foi realizado a troca da plataforma para a [_ArcGis_](https://developers.arcgis.com). Terminado o processo de Geocoding os boletins foram armazenados em um outro diretório a parte, este segmentado por categoria.

A partir desse ponto os boletins, já mapeados, foram carregados utilizando a biblioteca [_Pandas_](https://pandas.pydata.org), em seguida foram aplicados filtros afim de remover dados que foram preenchidos de forma incorreta e foi iniciado o processo para construir o DataFrame que seria utilizado para alimentar o [_Microsoft Power BI_](https://powerbi.microsoft.com/pt-br/what-is-power-bi/) na Etapa de Visulização e os dados de Treino, Teste e Validação para a etapa de Data Prediction.

### Data Prediction

Terminado a etapa de Data Transformation, foi iniciado a etapa de construção de um modelo preditivo baseado no comportamento histórico dos dados. Nesta etapa foi utilizado as técnicas de Deep Learning propostas pela [M4 Forecasting Competition](https://github.com/M4Competition/M4-methods/) como parametros de benchmark.



### Data Visualization

Uma vez que os dados foram coletados, limpos e estruturados foi construido um relatório, afim de melhor visualizar e estudar os dados. Nesta etapa fora utilizado o [_Microsoft Power BI_](https://powerbi.microsoft.com/pt-br/what-is-power-bi/) pela sua flexibilidade e facilidade para criar um relatório interativo aonde é possivel filtar e melhor estudar os dados. 

O relatório foi dividido em 2 páginas, a primeria estudando o comportamento histórico de ocorrência de Roubos e Furtos na região da grande Vitória. A segunda apresentando os resultados obtidos pelo modelo preditivo.

#### Pagina 1. Análise Histórica

![Análise Histórica de Ocorrência de Roubos e Furtos](https://github.com/andrebvitoria/Projeto-BO/blob/master/Images/Report/Pagina_1.JPG)

**Legenda:**
1. Título do relatório
2. Seção de filtros. (Município, Bairro, Categoria e Data de ocorrência)
3. Mapa de Calor da Região Metropolitana da Grande Vitória
4. Gráfico de Barras interativo com o indicie de ocorrência de Roubos/Furtos por Município e Bairro.
5. Indicador total de ocorrências com base nos filtros aplicados.
6. Indicador de ocorrências diárias com base nos filtros aplicados.
7. Rank com as 10 categorias que mais ocorreram.
8. Gráfico de Barras interativo com a distribuição de ocorrência a cada 15 minutos ao decorrer do dia (24h).
9. Gráfico de Linhas interativo com o histórico de ocorrência de Roubos/Furtos dos municípios.

#### Página 2. Análise Preditiva

![Análise Preditiva de Ocorrência de Roubos e Furtos](https://github.com/andrebvitoria/Projeto-BO/blob/master/Images/Report/Pagina_2.JPG)
{{ Imagem da Segunda página do relatório}}

**Legenda:**
1. Título do relatório
2. Seção de filtros. (Município, Bairro, Categoria e Data de ocorrência)
3. Mapa de Calor da Região Metropolitana da Grande Vitória
4. Gráfico de Barras interativo com o indicie de ocorrência de Roubos/Furtos por Município e Bairro.
5. Indicador total de ocorrências com base nos filtros aplicados.
6. Indicador de ocorrências diárias com base nos filtros aplicados.
7. Rank com as 10 categorias que mais ocorreram.
8. Gráfico de Barras interativo com a distribuição de ocorrência a cada 15 minutos ao decorrer do dia (24h).
9. Gráfico de Linhas interativo com o histórico de ocorrência de Roubos/Furtos dos municípios.


# Analise de séries temporáis de roubos no estado do Espirito Santo

A documentação completa, junto com o diario de desenvolvimento pode ser encontrado na [Wiki](#) do repositório.

## Motivação

Segundo a legislação brasileira, (citar o artigo). Dessa forma a SESP-ES (Secretaria do Estado de Segurança Pública do Espírito Santo), disponibiliza um repositório com os boletins de ocorrencia registrados no estado. Com base nisso e a popularização de técnicas mais sofisticadas de predição, tais quais (Machine Learning e Deep Learning) surgiu o projeto. O objetivo é utilizar técnicas de predição já consolidadas e aplica-las neste dominio específico, que é a Analise de séries temporáis de roubos no estado do Espirito Santo, especificamente a [RMGV](https://pt.wikipedia.org/wiki/Região_Metropolitana_de_Vitória) (Região Metropolitana da Grande Vitória).

## Etapas do Projeto

Este projeto foi divido em 5 etapas principais: Data Collection, Data Cleaning, Data Transformation, Data Prediction e Data Visualization.

### Data Collection

A SESP-ES, disponibiliza em um [_Repositório_](https://boletins.sesp.es.gov.br) publico, divididos em lotes, todos os boletins registrado no estado do Espírito Santo em forato PDF. Com isso foi realizado a coleta desses lotes utilizando o [_Aria2_](https://aria2.github.io/manual/pt/html/index.html).
Para realização deste projeto foi feito a coleta de 244 lotes, totalizando 135 GB (aproximadamente 2.5 milhões de boletins). Contendo os boletins registrados no periodo de 01 de janeiro de 2013 até 31 de janeiro de 2019.


### Data Cleaning

Após a coleta dos lotes, os mesmos foram extraidos em um diretório e foram segmentados segundo o lote pertencente. Em seguida fora utilizado a biblioteca [_Textract_](https://textract.readthedocs.io/en/stable/)  do Python para carregar os lotes de boletins em memória e a partir desse ponto realizar a remoção de boletins invalidados pela SESP-ES. terminado essa verificação os memos foram salvos em outro diretório em formato de texto (TXT), este diretório que possui a mesma estrutura do diretório de origem dos lotes.

O proximo passo foi realizar a extração das informações contidas nos boletins. Após analise da estrutura dos boletins foi utilizado a biblioteca [_RE_](https://docs.python.org/3/library/re.html) do Python, para através de expressões regulares, realizar a coleta das informações dos boletins. E em seguida os mesmos foram compilados em JSON e armazenados em outro diretório que possui a mesma estrutura dos anteriores.

Abaixo temos a estrutura dos boletins de ocorrencia em PDF e dos lotes em JSON.

{{{Imagem do BO em PDF}}}

{{{ Estrutura dos lotes em JSON}}}

### Data Transformation

Nesta etapa foi realizado a segmentação dos boletins por categoria, e não mais por lote. A partir desse ponto foi definido qual seria o dominio do problema. As transformações e tratamentos foram realziados apenas nos boletins de Categoria B, nas subcategorias 01 e 02, que pertencem a categoria de Crimes Contra Patrimônio, e dividias em Furto e Roubo, respectivamente.

Realizado a segmentação foi iniciado o processo de Geocoding, que consiste em, a partir do endereço, identificar as coordenadas geográficas que pertencem a esse endereço. Para isso fora utilizado sistemas denominados GIS ([_Geographic Information System_](https://en.wikipedia.org/wiki/Geographic_information_system)), inicialmente fora utilizado o GIS disponibilizado pela Google, o [_Google Maps_](https://developers.google.com/maps/documentation/geocoding/start?hl=pt-br), porém devido a limitações no numero de mapeamentos permitidos, foi realizado a troca da plataforma para a [_ArcGis_](https://developers.arcgis.com). Terminado o processo de Geocoding os boletins foram armazenados em um outro diretório a parte, este segmentado por categoria.

### Data Prediction

Terminado a etapa de Data Transformation, foi iniciado a etapa de construção de um modelo preditivo baseado no comportamento histórico dos dados. Nesta etapa foi utilizado as técnicas de Deep Learning propostas pela [M4 Forecasting Competition](https://github.com/M4Competition/M4-methods/) como parametros de benchmark.

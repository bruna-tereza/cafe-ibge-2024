# Panorâma da Cafeicultura Brasileira em 2024

> **Análise exploratória e visual da produção de café no Brasil com base nos dados do IBGE (2024)**

---

## 1. RESUMO E PROPÓSITO

Este projeto tem como objetivo criar um **dashboard interativo** que apresenta insights sobre a produção de café no Brasil, utilizando dados públicos do **IBGE - Produção Agrícola Municipal (PAM)**.  
O trabalho busca oferecer uma visão analítica sobre as **principais regiões produtoras**, **diferenças entre os tipos de café Arábica e Canephora**, e **indicadores de desempenho da produção**.

A solução foi desenvolvida como parte de um estudo voltado à **modelagem e análise de dados agrícolas**, com foco em **qualidade, rastreabilidade e visualização inteligente**.

---

## 2. CONJUNTO DE DADOS

- **Fonte:** Instituto Brasileiro de Geografia e Estatística (IBGE)  
- **Base:** Produção Agrícola Municipal – ( Culturas permanentes - Café - 2024)
- **Formato:** Dados brutos no formato `xlsx.` e CSV processado em `data/processed/ibge_cafe_2024_processed.csv`

**Principais colunas do dataset:**
- Município  
- UF  
- Área destinada à colheita de Arábica / Canephora  
- Área colhida de Arábica / Canephora  
- Toneladas produzidas de Arábica / Canephora  
- Rendimento médio (kg/ha)  
- Valor da produção (mil R$)

---

## 3. PROCESSAMENTO E TRANSFORMAÇÃO DE DADOS

Os dados brutos foram tratados e consolidados para uso no dashboard:

1. Padronização de colunas e unidades de medida.  
2. Conversão de tipos numéricos e tratamento de valores ausentes.  
3. Cálculo de métricas agregadas por UF e tipo de café.  
4. Geração de um dataset consolidado para visualização interativa.  

O processamento foi realizado em Python com **pandas** e **numpy**, garantindo consistência e reprodutibilidade.

---

## 4. DASHBOARD ANALÍTICO

O dashboard foi desenvolvido com **Plotly Dash** e estruturado em painéis temáticos.

### Filtros Principais
- Tipo de café: Arábica, Canephora ou Total  
- Estado (UF)

### Indicadores-Chave (KPIs)
- Produção total (t)  
- Área colhida total (ha)  
- Rendimento médio (kg/ha)  
- Valor total da produção (mil R$)  

### Visualizações
- **Distribuição da produção por UF:** análise comparativa do volume total produzido.  
- **Top 10 municípios produtores:** identificação dos principais polos agrícolas.  
- **Rendimento médio por UF:** avaliação de produtividade e eficiência.  
- **Valor médio da produção:** análise econômica do setor.  
- **Correlação entre área colhida e produção:** relação direta entre extensão e volume produzido.

---

## 5. INSIGHTS PRINCIPAIS

A análise revelou padrões significativos na produção nacional:

- **Café Arábica** domina o volume total, concentrado em estados como **Minas Gerais**, **São Paulo** e **Bahia**.  
- **Canephora (Conilon)** se destaca na **Região Norte e Nordeste**, especialmente em **Espírito Santo** e **Rondônia**.  
- A **produtividade média por hectare** apresenta grande variação entre estados, indicando diferenças tecnológicas e climáticas.  
- O **valor econômico da produção** segue fortemente correlacionado à eficiência do rendimento, não apenas à extensão de área.  

Esses resultados ajudam a compreender **a dinâmica regional e econômica da cafeicultura brasileira**, fornecendo uma base sólida para análises de mercado, sustentabilidade e políticas agrícolas.

---

## 6. EXECUÇÃO LOCAL

### Requisitos
- Python 3.10+  
- Instalar dependências:
  ```bash
  pip install -r requirements.txt

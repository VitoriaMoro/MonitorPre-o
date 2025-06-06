import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from tqdm import tqdm
from datetime import datetime
import streamlit as st

def get_produtos(produto):
  session = requests.Session()
  url = "https://lista.mercadolivre.com.br/supermercado/market/"  + produto.replace(" ", "-")
  r = session.get(url, headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'})
  soup = BeautifulSoup(r.content, "lxml")
  boxes = soup.find_all("div", {"class": "ui-search-result__wrapper"})
  produtos = []
  for box in boxes:
    nome = box.find("h3", {"class": "poly-component__title-wrapper"}).get_text(strip=True)
    url = box.find("h3").find("a").get("href")
    preco = float(box.find("span", {"class": "andes-money-amount"}).get_text(strip=True).replace("R$", "").replace(".", "").replace(",", "."))
    produtos.append({"nome": nome,"url": url,"preco": preco})
  timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
  df = pd.DataFrame(produtos)
  df["timestamp"] = timestamp
  df["keyword"] = produto
  return df

def preco_medio_atual(df):
  preco_medio = df["preco"].mean()
  return preco_medio

def preco_mediano_atual(df):
  preco_mediano = df["preco"].median()
  return preco_mediano

def menor_preco(df):
  menor_preco = df["preco"].min()
  return menor_preco

def maior_preco(df):
  maior_preco = df["preco"].max()
  return maior_preco

st.title("Monitor de Preço")

produto = st.text_input("digite")
botao = st.button("ok")

if botao:
  df = get_produtos(produto=produto)
  st.write(df)
  st.write("Menor preço:", menor_preco(df))
  st.write("Maior preço:", maior_preco(df))
  st.write("Preço mediano atual:", preco_mediano_atual(df))
  st.write("Preço medio atual:", preco_medio_atual(df))
  

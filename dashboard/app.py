import pandas as pd
import streamlit as st
import plotly.express as px
import requests
import io

st.set_page_config(page_title="Panorama da Cafeicultura Brasileira (2024)", layout="wide")
df = pd.read_csv("data/processed/ibge_cafe_2024_processed.csv")

def fmt(num, dec=0):
    if pd.isna(num):
        return "-"
    s = f"{num:,.{dec}f}"
    s = s.replace(",", "X").replace(".", ",").replace("X", ".")
    return s

st.title("Panorama da Cafeicultura Brasileira (2024)")
st.sidebar.header("Filtros")
variedade = st.sidebar.selectbox("Variedade", ["Total", "Arábica", "Canephora"])
ufs = st.sidebar.multiselect("Filtrar por UF", options=sorted(df["UF"].unique()), default=sorted(df["UF"].unique()))
df = df[df["UF"].isin(ufs)].copy()

if variedade == "Arábica":
    df["Toneladas"] = df["Toneladas produzidas de Arábica"].fillna(0)
    df["Área colhida"] = df["Área colhida de Arábica"].fillna(0)
    df["Rendimento"] = df["Rendimento médio da produção (Quilogramas por Hectare) Arábica"]
    df["Valor"] = df["Valor da produção (Mil Reais) Arábica"].fillna(0)
elif variedade == "Canephora":
    df["Toneladas"] = df["Toneladas produzidas de Canephora"].fillna(0)
    df["Área colhida"] = df["Área colhida de Canephora"].fillna(0)
    df["Rendimento"] = df["Rendimento médio da produção (Quilogramas por Hectare) Canephora"]
    df["Valor"] = df["Valor da produção (Mil Reais) Canephora"].fillna(0)
else:
    df["Toneladas"] = df["Toneladas produzidas de Arábica"].fillna(0) + df["Toneladas produzidas de Canephora"].fillna(0)
    df["Área colhida"] = df["Área colhida de Arábica"].fillna(0) + df["Área colhida de Canephora"].fillna(0)
    a = df["Rendimento médio da produção (Quilogramas por Hectare) Arábica"].fillna(0)
    b = df["Rendimento médio da produção (Quilogramas por Hectare) Canephora"].fillna(0)
    df["Rendimento"] = ((a + b) / 2).replace(0, pd.NA)
    df["Valor"] = df["Valor da produção (Mil Reais) Arábica"].fillna(0) + df["Valor da produção (Mil Reais) Canephora"].fillna(0)

df["Rendimento"] = pd.to_numeric(df["Rendimento"], errors="coerce")

prod_total = df["Toneladas"].sum()
area_total = df["Área colhida"].sum()
rend_mean = df["Rendimento"].mean()
valor_total = df["Valor"].sum()
per_uf_std = df.groupby("UF")["Rendimento"].std().dropna()
std_media_uf = per_uf_std.mean() if not per_uf_std.empty else 0
uf_mais_instavel = per_uf_std.idxmax() if not per_uf_std.empty else None
uf_mais_instavel_val = per_uf_std.max() if not per_uf_std.empty else 0

k1, k2, k3, k4, k5 = st.columns([1,1,1,1,1])
k1.metric("Produção Total (t)", fmt(prod_total))
k2.metric("Área Colhida (ha)", fmt(area_total))
k3.metric("Rendimento Médio (kg/ha)", fmt(rend_mean))
k4.metric("Valor Total (Mil R$)", fmt(valor_total))
if uf_mais_instavel:
    k5.markdown(f"<div style='font-size:16px;'>Desvio Padrão médio por UF (kg/ha): <b>{fmt(std_media_uf)}</b><br><span style='color:#C62828;'>UF mais instável: {uf_mais_instavel} ({fmt(uf_mais_instavel_val)})</span></div>", unsafe_allow_html=True)
else:
    k5.metric("Desvio Padrão médio por UF (kg/ha)", fmt(std_media_uf))

tab1, tab2, tab3 = st.tabs(["Visão Geral", "Eficiência & Valor", "Dados & Export"])

with tab1:
    col_left, col_right = st.columns([1,2])
    prod_uf = df.groupby("UF", as_index=False)["Toneladas"].sum().sort_values("Toneladas", ascending=False)
    fig_bar = px.bar(prod_uf, x="UF", y="Toneladas", title="Produção Total por UF", color="Toneladas", color_continuous_scale=["#8EACBB","#304FFE"])
    fig_bar.update_layout(margin=dict(t=40,l=10,r=10,b=10), template="plotly_white")
    fig_bar.update_traces(texttemplate="%{y:,.0f}", textposition="outside")
    col_left.plotly_chart(fig_bar, use_container_width=True)

    geojson_url = "https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/brazil-states.geojson"
    geojson = requests.get(geojson_url, timeout=10).json()
    prod_map = prod_uf.copy()
    fig_map = px.choropleth(prod_map, geojson=geojson, locations="UF", featureidkey="properties.sigla",
                           color="Toneladas", color_continuous_scale=["#8EACBB","#304FFE"],
                           title="Mapa: Produção Total por UF", labels={"Toneladas":"Toneladas"})
    fig_map.update_geos(fitbounds="locations", visible=False)
    fig_map.update_layout(margin=dict(t=40,l=0,r=0,b=0), template="plotly_white")
    for d in fig_map.data:
        d.hovertemplate = "<b>%{location}</b><br>Toneladas: %{z:,.0f}<extra></extra>"
    col_right.plotly_chart(fig_map, use_container_width=True)

    top_mun = df.groupby("Município", as_index=False)["Toneladas"].sum().sort_values("Toneladas", ascending=False).head(10)
    fig_top = px.bar(top_mun.sort_values("Toneladas"), x="Toneladas", y="Município", orientation="h", title="Top 10 Municípios Produtores", color="Toneladas", color_continuous_scale=["#8EACBB","#304FFE"], text="Toneladas")
    fig_top.update_traces(texttemplate="%{text:,.0f}")
    fig_top.update_layout(margin=dict(t=40,l=10,r=10,b=10), template="plotly_white")
    st.plotly_chart(fig_top, use_container_width=True)

with tab2:
    col_a, col_b = st.columns([1,1])
    rend_uf = df.groupby("UF", as_index=False)["Rendimento"].mean().sort_values("Rendimento", ascending=False)
    fig_rend = px.bar(rend_uf, x="Rendimento", y="UF", orientation="h", title="Rendimento Médio por UF (kg/ha)", color="Rendimento", color_continuous_scale=["#90CAF9","#1565C0"])
    fig_rend.update_traces(texttemplate="%{x:,.0f}")
    fig_rend.update_layout(margin=dict(t=40,l=10,r=10,b=10), template="plotly_white")
    col_a.plotly_chart(fig_rend, use_container_width=True)

    val_uf = df.groupby("UF", as_index=False)["Valor"].mean().sort_values("Valor", ascending=False)
    fig_val = px.bar(val_uf, x="Valor", y="UF", orientation="h", title="Valor Médio da Produção por UF (Mil R$)", color="Valor", color_continuous_scale=["#FBC02D","#E65100"])
    fig_val.update_traces(texttemplate="%{x:,.0f}")
    fig_val.update_layout(margin=dict(t=40,l=10,r=10,b=10), template="plotly_white")
    col_b.plotly_chart(fig_val, use_container_width=True)

    col_c, col_d = st.columns(2)
    fig_scatter1 = px.scatter(df, x="Área colhida", y="Toneladas", color="UF", size="Toneladas", hover_data=["Município"], title="Área Colhida x Produção (t)", trendline="ols")
    fig_scatter1.update_layout(template="plotly_white")
    col_c.plotly_chart(fig_scatter1, use_container_width=True)

    fig_scatter2 = px.scatter(df, x="Rendimento", y="Valor", color="UF", size="Toneladas", hover_data=["Município"], title="Rendimento x Valor da Produção", trendline="ols")
    fig_scatter2.update_layout(template="plotly_white")
    col_d.plotly_chart(fig_scatter2, use_container_width=True)

    per_uf_std = df.groupby("UF", as_index=False)["Rendimento"].std().dropna().sort_values("Rendimento", ascending=False)
    fig_std = px.bar(per_uf_std, x="Rendimento", y="UF", orientation="h", title="Desvio Padrão do Rendimento por UF (kg/ha)", color="Rendimento", color_continuous_scale=["#FFE082","#F57C00"])
    fig_std.update_traces(texttemplate="%{x:,.1f}")
    fig_std.update_layout(margin=dict(t=40,l=10,r=10,b=10), template="plotly_white")
    st.plotly_chart(fig_std, use_container_width=True)

with tab3:
    st.subheader("Dados filtrados")
    st.dataframe(df.reset_index(drop=True))
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False, sep=";")
    st.download_button("Exportar CSV", data=csv_buffer.getvalue(), file_name="ibge_cafe_2024_filtrado.csv", mime="text/csv")
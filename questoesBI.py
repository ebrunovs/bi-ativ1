import pandas as pd

fornecedores = pd.read_csv("csv/Fornecedores.csv")

transportadoras = pd.read_csv("csv/Transportadoras.csv")

vendedores = pd.read_csv("csv/Vendedores.csv")

vendasGlobais = pd.read_csv("csv/VendasGlobais.csv")

# 1. Quem são os meus 10 maiores clientes, em termos de vendas ($)?
print("1. Quem são os meus 10 maiores clientes, em termos de vendas ($)?")
maiores_clientes = vendasGlobais.groupby(
    [
        "ClienteID",
        "ClienteNome"
        ]
        )[
            "Vendas"
            ].sum().nlargest(10).to_frame()
print(maiores_clientes)

# 2. Quais os três maiores países, em termos de vendas ($)?
print("\n2 . Quais os três maiores países, em termos de vendas ($)?")
maiores_paises = vendasGlobais.groupby(
    "ClientePaís"
    )[
        "Vendas"
        ].sum().nlargest(3).to_frame()
print(maiores_paises)

# 3. Quais as categorias de produtos que geram maior faturamento (vendas $) 
# no Brasil?
print("\n3. Quais as categorias de produtos que geram maior faturamento" 
      + "(vendas $) no Brasil?")
maiores_categorias = vendasGlobais[
    vendasGlobais[
        "ClientePaís"] == "Brazil"
        ].groupby(
            "CategoriaNome"
            )[
                "Vendas"
                ].sum().nlargest(3)
print(maiores_categorias)

# 4. Qual a despesa com frete envolvendo cada transportadora?
print("\n4. Qual a despesa com frete envolvendo cada transportadora?")
despesa_frete = vendasGlobais.groupby(
    "TransportadoraID"
    )[
        "Frete"
        ].sum().reset_index().merge(
            transportadoras,
            on="TransportadoraID"
            ).set_index("TransportadoraNome")["Frete"].sort_values(ascending=False)
print(despesa_frete)

#5. Quais são os principais clientes (vendas $) do segmento 
# "Calçados Masculinos" (Men ́s Footwear) na Alemanha?
print("\n5. Quais são os principais clientes (vendas $) do segmento" 
      + "\"Calçados Masculinos\" (Men´s Footwear) na Alemanha?")
principais_clientes = vendasGlobais[
    (
        vendasGlobais["CategoriaNome"] == "Men´s Footwear"
        ) & (
            vendasGlobais["ClientePaís"] == "Germany"
            )
            ]
principais_clientes = principais_clientes.groupby(
    ["ClienteID", "ClienteNome"]
    )[
        "Vendas"
      ].sum().nlargest(10).to_frame()
print(principais_clientes)

# 6. Quais os vendedores que mais dão descontos nos Estados Unidos?
print("\n6. Quais os vendedores que mais dão descontos nos Estados Unidos?")
vendedores_descontos = vendasGlobais[
    vendasGlobais["ClientePaís"] == "USA"
    ].groupby(
        "VendedorID"
        )[
        "Desconto"
        ].sum().reset_index().merge(
            vendedores,
            on="VendedorID"
            ).nlargest(
                10,
                "Desconto"
                ).set_index(
                    "VendedorNome"
                    )[
                        "Desconto"
                        ].to_frame().sort_values(
                            "Desconto",
                            ascending=False
                            )
print(vendedores_descontos)

# 7. Quais os fornecedores que dão a maior margem de lucro ($) no segmento de 
# “Vestuário Feminino” (Womens wear)?
print("\n7. Quais os fornecedores que dão a maior margem de lucro ($) no" +
       " segmento de “Vestuário Feminino” (Womens wear)?")
fornecedores_margem = vendasGlobais[
    vendasGlobais["CategoriaNome"] == "Womens wear"].groupby(
        "FornecedorID"
        )[
            "Margem Bruta"
            ].sum().reset_index().merge(
                fornecedores,
                on="FornecedorID").nlargest(
                    10, "Margem Bruta"
                    ).set_index(
                        "FornecedorNome"
                        )[
                            "Margem Bruta"
                            ].to_frame()
print(fornecedores_margem)

# 8. Quanto que foi vendido ($) no ano de 2009? Analisando as vendas anuais 
# entre 2009 e 2012, podemos concluir que o faturamento vem crescendo, se 
# mantendo estável ou decaindo?
print("\n8. Quanto que foi vendido ($) no ano de 2009? Analisando as vendas"+
       "anuais entre 2009 e 2012, podemos concluir que o faturamento vem"+
       "crescendo, se mantendo estável ou decaindo?")

# Converter a coluna Data para datetime e extrair o ano
vendasGlobais['Data'] = pd.to_datetime(
    vendasGlobais['Data'], format='%d/%m/%Y'
    )
vendasGlobais['Ano'] = vendasGlobais['Data'].dt.year

# Vendas anuais de 2009 a 2012
vendas_anuais = vendasGlobais[
    vendasGlobais['Ano'].between(2009, 2012)
    ].groupby("Ano")["Vendas"].sum().to_frame()
print("\nVendas anuais (2009-2012):")
print(vendas_anuais)

# Vendas específicas de 2009
vendas_2009 = vendasGlobais[vendasGlobais['Ano'] == 2009]['Vendas'].sum()
print(f"\nVendas em 2009: ${vendas_2009:,.2f}")

# Análise de tendência
crescimento_2009_2010 = (
    (
        vendas_anuais.loc[2010, 'Vendas'] - vendas_anuais.loc[2009, 'Vendas']
        ) / vendas_anuais.loc[2009, 'Vendas']
        ) * 100
crescimento_2010_2011 = (
    (
        vendas_anuais.loc[2011, 'Vendas'] - vendas_anuais.loc[2010, 'Vendas']
        ) / vendas_anuais.loc[2010, 'Vendas']
        ) * 100
crescimento_2011_2012 = (
    (
        vendas_anuais.loc[2012, 'Vendas'] - vendas_anuais.loc[2011, 'Vendas']
        ) / vendas_anuais.loc[2011, 'Vendas']
        ) * 100

print(f"\nAnálise de crescimento:")
print(f"2009 → 2010: {crescimento_2009_2010:.2f}%")
print(f"2010 → 2011: {crescimento_2010_2011:.2f}%")
print(f"2011 → 2012: {crescimento_2011_2012:.2f}%")

# Conclusão automática
if all(
    [
        crescimento_2009_2010 > 0,
        crescimento_2010_2011 > 0,
        crescimento_2011_2012 > 0
        ]
        ):
    conclusao = "O faturamento vem CRESCENDO consistentemente."
elif all(
    [
        abs(crescimento_2009_2010) < 5,
        abs(crescimento_2010_2011) < 5,
        abs(crescimento_2011_2012) < 5
        ]
        ):
    conclusao = "O faturamento se mantém ESTÁVEL."
elif all(
    [
        crescimento_2009_2010 < 0,
        crescimento_2010_2011 < 0,
        crescimento_2011_2012 < 0
        ]
        ):
    conclusao = "O faturamento vem DECAINDO."

print(f"\nConclusão: {conclusao}\n\n\n")

# 9. Quais são os principais clientes (vendas $) do segmento “Calçados 
# Masculinos” (Men ́s Footwear) no ano de 2013. Para quais cidades houve venda e
#  quanto?# 9. Quais são os principais clientes (vendas $) do segmento 
# "Calçados Masculinos" (Men ́s Footwear) no ano de 2013. Para quais cidades 
# houve venda e quanto?
print("\n9. Quais são os principais clientes (vendas $) do segmento"+
      "\"Calçados Masculinos\" (Men´s Footwear) no ano de 2013. Para quais "
      +"cidades houve venda e quanto?")
principais_clientes_2013 = vendasGlobais[
	(pd.to_datetime(vendasGlobais["Data"], format="%d/%m/%Y").dt.year == 2013) 
    & (vendasGlobais["CategoriaNome"] == "Men´s Footwear")
].groupby(
    [
        "ClienteID", "ClienteNome", "ClienteCidade"
        ]
        )[
            "Vendas"
            ].sum().reset_index().sort_values(
                "Vendas",
                ascending=False
                ).head(10)
print(principais_clientes_2013)

# 10. Na Europa, quanto que se vende ($) para cada país?

paises_da_europa = [ "Austria", "Belgium", "Denmark", "Finland", "France",
    "Germany", "Ireland", "Italy", "Netherlands", "Norway", "Portugal", "Spain",
    "Sweden", "Switzerland", "UK"]

print("\n10. Na Europa, quanto que se vende ($) para cada país?")
vendas_por_pais = (
    vendasGlobais[vendasGlobais["ClientePaís"].isin(paises_da_europa)]
    .groupby("ClientePaís")["Vendas"]   
    .sum()
    .reset_index()
    .sort_values("Vendas", ascending=False)
)
print(vendas_por_pais)


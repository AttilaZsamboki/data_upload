import pandas as pd
from sqlalchemy import create_engine
from unas_api import UnasAPIBase, Product

DB_HOST = "defaultdb.c0rzdkeutp8f.eu-central-1.rds.amazonaws.com"
DB_NAME = "defaultdb"
DB_USER = "doadmin"
DB_PASS = "AVNS_FovmirLSFDui0KIAOnu"
DB_PORT = "25060"

engine = create_engine(
    "postgresql://"
    + DB_USER
    + ":"
    + DB_PASS
    + "@"
    + DB_HOST
    + ":"
    + DB_PORT
    + "/"
    + DB_NAME
)

unas_client = UnasAPIBase("cfcdf8a7109a30971415ff7f026becdc50dbebbd")


def add_category():
    df = pd.read_sql(
        con=engine,
        sql="""select distinct sr.sku,
                on_stock
from fol_min_pcs mp
         LEFT JOIN fol_unas_extended u ON u."1_alkategoria" = mp.category
         left join fol_stock_report_last sr on sr.sku = u.cikkszam
         left join fol_stock_aging on fol_stock_aging.sku = u.cikkszam
where sr.on_stock <= mp."limit"
  and concat("Alternativ_Kategoria_1", "Alternativ_Kategoria_2", "Alternativ_Kategoria_3",
                    "Alternativ_Kategoria_4", "Alternativ_Kategoria_5", "Alternativ_Kategoria_6",
                    "Alternativ_Kategoria_7") not like '%%UTOLSÓ DARABOK%%' 
  and sr.on_stock
    > 0
  and fol_stock_aging.age > 90;
""",
    )

    for item in df.iloc:
        product = Product(
            sku=item["sku"],
            categories=[
                Product.Category("alt", "684112", "UTOLSÓ DARABOK"),
            ],
            action="modify",
            minimum_qty=item["on_stock"],
            maximum_qty=item["on_stock"],
        )
        unas_client.set_product(product)


def remove_category():
    df = pd.read_sql(
        con=engine,
        sql="""select distinct cikkszam
from fol_unas u
         left join fol_stock_report_last sr on sr.sku = u.cikkszam
         left join fol_min_pcs mp on mp.category = u."Category"
where concat("Alternativ_Kategoria_1", "Alternativ_Kategoria_2", "Alternativ_Kategoria_3",
             "Alternativ_Kategoria_4", "Alternativ_Kategoria_5", "Alternativ_Kategoria_6",
             "Alternativ_Kategoria_7") like '%%UTOLSÓ DARABOK%%'
  and sr.on_stock > mp."limit";""",
    )

    for sku in df["cikkszam"]:
        init_product = unas_client.get_product(sku, "full")
        product = Product(sku=sku, categories=init_product.categories)
        product.action = "modify"
        product.minimum_qty = 1
        product.maximum_qty = None
        product.remove_category(684112)
        product.add_category(Product.Category("alt", "", ""))
        unas_client.set_product(product)


def main():
    add_category()
    remove_category()


if __name__ == "__main__":
    main()

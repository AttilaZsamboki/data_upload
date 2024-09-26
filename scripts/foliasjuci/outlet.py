import pandas as pd
from sqlalchemy import create_engine, text
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


def reset_outlet():
    df = pd.read_sql(
        con=engine,
        sql="""SELECT op.sku, srl.on_stock
FROM fol_outlet_products op
         LEFT JOIN (SELECT sku, max(age) age from fol_stock_aging group by 1) sa ON sa.sku = op.sku
         LEFT JOIN fol_stock_report_last srl on srl.sku = op.sku
WHERE age < 90;""",
    )
    successful = []
    for i in df.iloc:
        init_product = unas_client.get_product(i["sku"], "full")
        product = Product(
            sku=i["sku"],
            params=[
                Product.Param(
                    id=5421535,
                    type="text",
                    value="",
                    name="Outlet%",
                    group="Outlet",
                    before=None,
                    after=None,
                )
            ],
            action="modify",
            prices=Product.Prices(
                appearance=None,
                vat=None,
                price=Product.Price(type="sale", net=0, gross=0),
            ),
            categories=[i for i in init_product.categories if i.id != 392880]
            + [Product.Category("alt", "", "")],
        )
        unas_client.set_product(product)
        with engine.connect() as connection:
            connection.execute(
                text(
                    f"insert into fol_outlet_log (timestamp, action, sku, on_stock) values (current_timestamp, 'REMOVE', '{i.sku}', {i.on_stock})"
                )
            )
            connection.commit()
        successful.append(i["sku"])
        break
    with engine.connect() as connection:
        connection.execute(
            text(
                "delete from fol_outlet_products where sku in ('"
                + "','".join(successful)
                + "')"
            )
        )
        connection.commit()


def set_outlet():
    df = pd.read_sql(con=engine, sql="select * from fol_outlet;")
    successful = []
    for i in df.iloc:
        product_category = unas_client.get_product(i["sku"], "full").categories
        unas_client.set_product(
            Product(
                sku=i["sku"],
                params=[
                    Product.Param(
                        id=5421535,
                        type="text",
                        value=str(int(i["discount"])) + "%",
                        name="Outlet%",
                        group="Outlet",
                        before=None,
                        after=None,
                    )
                ],
                categories=[
                    Product.Category("alt", "392880", None),
                    *product_category,
                ],
                action="modify",
                prices=Product.Prices(
                    appearance=None,
                    vat=None,
                    price=Product.Price(
                        type="sale",
                        net=round(i["netto_ar"] * (1 - i["discount"] / 100) * 1.27 / 5)
                        * 5
                        / 1.27,
                        gross=round(
                            i["netto_ar"] * (1 - i["discount"] / 100) * 1.27 / 5
                        )
                        * 5,
                    ),
                ),
            )
        )
        with engine.connect() as connection:
            connection.execute(
                text(
                    f"insert into fol_outlet_log (timestamp, action, sku, on_stock) values (current_timestamp, 'ADD', '{i.sku}', {i.on_stock})"
                )
            )
            connection.commit()
        if not i["start_date"]:
            successful.append(i["sku"])

    if len(successful) > 0:
        with engine.connect() as connection:
            connection.execute(
                text(
                    "insert into fol_outlet_products (sku, start_date) values "
                    + ",".join([f"('{i}', current_date)" for i in successful])
                )
            )
            connection.commit()


def main():
    set_outlet()
    reset_outlet()


if __name__ == "__main__":
    main()

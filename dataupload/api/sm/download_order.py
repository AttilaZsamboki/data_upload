import os
from datetime import datetime
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
load_dotenv()

DB_HOST = os.environ.get("DB_HOST")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")
DB_PORT = os.environ.get("DB_PORT")

engine = create_engine('postgresql://'+DB_USER+':' +
                       DB_PASS + '@'+DB_HOST+':'+DB_PORT+'/'+DB_NAME)


def download_order(vendor):
    directory = '/home/atti/googleds/files/sm_pos/{}'.format(
        vendor)
    if not os.path.exists(directory):
        os.makedirs(directory)
    path = directory + "/{}.xlsx".format(
        datetime.now().strftime('%Y-%m-%d'))

    if os.path.exists(path):
        print("Order for {} already exists".format(vendor))
        return {"data": pd.read_excel(path), "path": path}
    print("Downloading order for {}".format(vendor))
    data = pd.read_sql(f"""

                    select sku, sum(to_order) as quantity
                    from (select sku, to_order
                        from sm_product_data
                        where vendor = '{vendor}'
                            and replenish_date::date <= current_date
                            and sku not like '%%5M%%'
                        union
                        select sm_order_queue.sku, quantity
                        from sm_order_queue
                        where sm_order_queue.vendor = '{vendor}' and sm_order_queue.status in ('ADDED', 'NEW')) as combined
                    group by 1
                    order by 1;

                """, con=engine)
    data.to_excel(
        path, index=False)
    return {"data": data, "path": path}

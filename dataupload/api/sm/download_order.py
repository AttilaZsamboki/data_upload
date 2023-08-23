import os
from datetime import datetime
import pandas as pd
from dotenv import load_dotenv

from ..utils.base_path import base_path
from ..utils.utils import connect_to_db

load_dotenv()

engine = connect_to_db()

def download_order(vendor):
    directory = f'{base_path}/files/sm_pos/{vendor}'
    if not os.path.exists(directory):
        os.makedirs(directory)
    path = directory + "/{}.xlsx".format(
        datetime.now().strftime('%Y-%m-%d'))

    if os.path.exists(path):
        return {"data": pd.read_excel(path), "path": path}
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

download_order('konrad hornschuch ag')
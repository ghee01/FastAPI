import os
import pandas as pd
from database import engine, get_session
from models import Menu, Orders
from sqlalchemy.dialects.postgresql import insert as pg_insert

BASE_DIR = os.getcwd()
MENU_PATH = os.path.join(BASE_DIR, 'input', 'menu.csv')
ORDERS_PATH = os.path.join(BASE_DIR, 'input', 'orders.csv')

def load_menu(path: str=MENU_PATH) -> dict:
    df = pd.read_csv(path, encoding='utf-8-sig')

    db = get_session()
    success = 0
    failed = 0

    for _, row in df.iterrows():
        try:
            m = Menu(
                메뉴코드 = str(row['메뉴코드']),
                메뉴명 = str(row['메뉴명']),
                가격 = int(row['가격'])
            )
            db.merge(m)
            db.commit()
            success += 1

        except Exception as e:
            db.rollback()
            failed += 1
            print(f'[적재실패] - {row["메뉴코드"]} / {e}')
    
    db.close()
    print(f'[menu 적재완료] - 성공 {success}건 / 실패 {failed}건')
    return {'success':success, 'failed':failed}

def load_orders(path: str=ORDERS_PATH) -> dict:
    df = pd.read_csv(path, encoding='utf-8-sig')
    df['주문일시'] = pd.to_datetime(df['주문일시'], errors='coerce')
    df = df.dropna(subset=['주문일시', '테이블번호', '메뉴코드', '수량'])

    records = df[['주문일시', '테이블번호', '메뉴코드', '수량']].to_dict(orient='records')

    if not records:
        return {'success':0, 'skipped_duplicate':0, 'failed':0}
    
    try:
        with engine.begin() as conn:
            stmt = pg_insert(Orders).values(records)
            stmt = stmt.on_conflict_do_nothing(constraint='uq_orders_key')
            result = conn.execute(stmt)

        inserted = result.rowcount if result.rowcount is not None else 0
        skipped = len(records) - inserted

        print(f'[orders 적재완료] - 신규 {inserted}건 / 중복스킵 {skipped}건')
        return {'success':inserted, 'skipped_duplicate':skipped, 'failed':0}

    except Exception as e:
        print(f'[적재실패] - {e}')
        return {'success':0, 'skipped_duplicate':0, 'failed':len(records)}
    
if __name__ == '__main__':
    load_menu()
    load_orders()
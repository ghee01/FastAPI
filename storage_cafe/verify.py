from sqlalchemy import text
from database import engine

def verify():
    with engine.connect() as conn:
        # 메뉴 검증
        menu_total = conn.execute(text("SELECT COUNT(*) FROM menu")).scalar()
        menu_negative_price = conn.execute(text("SELECT COUNT(*) FROM menu WHERE 가격 <= 0")).scalar()
        menu_null_name = conn.execute(text("SELECT COUNT(*) FROM menu WHERE 메뉴명 IS NULL")).scalar()        
        
        # 주문 검증
        orders_total = conn.execute(text("SELECT COUNT(*) FROM orders")).scalar()
        orders_negative_cnt = conn.execute(text("SELECT COUNT(*) FROM orders WHERE 수량 <= 0")).scalar()
        orders_not_menu = conn.execute(text("""
            SELECT COUNT(*) FROM orders
            WHERE 메뉴코드 NOT IN (SELECT 메뉴코드 FROM menu)
        """)).scalar()
        orders_duplicate = conn.execute(text("""
            SELECT COUNT(*) FROM (
                SELECT 주문일시, 테이블번호, 메뉴코드, COUNT(*) AS cnt
                FROM orders
                GROUP BY 주문일시, 테이블번호, 메뉴코드
                HAVING COUNT(*) > 1
            ) t
        """)).scalar()

    print('==== menu 검증 ====')
    print(f'전체 건수 : {menu_total}')
    print(f'가격 이상값 : {menu_negative_price}')
    print(f'메뉴명 NULL : {menu_null_name}')

    print('==== orders 검증 ====')
    print(f'전체 건수 : {orders_total}')
    print(f'수량 이상값 : {orders_negative_cnt}')
    print(f'존재하지 않는 메뉴코드 참조 : {orders_not_menu}')
    print(f'중복 키 건수 : {orders_duplicate}')

    ok = (
        menu_total > 0 and menu_negative_price == 0 and menu_null_name == 0
        and orders_total > 0 and orders_negative_cnt == 0 and orders_not_menu == 0 and orders_duplicate == 0
    )
    print(f'검증결과 : {"PASS" if ok else "FAIL"}')
    return ok

if __name__ == '__main__':
    verify()
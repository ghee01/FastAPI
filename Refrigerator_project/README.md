# 수정 및 추가 사항

## 1. 모듈 분리
```
├── database.py
├── models.py
├── schemas/
│   ├── requests.py
│   └── requests.py
├── routers/
│   └── ingredient.py
└── main.py
```

## 2. 오타 수정
- stroage → storage

## 3. ingredient.py 수정 내용
| 함수 | 변경 내용 |
| --- | --- |
| `upload_ingredients_csv` | 날짜 타입으로 형변환 하는 코드 추가 |
| `upload_ingredients_csv` | 필수값 누락/형식 오류 시 해당 행 건너뛰는 코드 추가 |
| `list_ingredients` | 카테고리 뿐만 아니라 보관 방법, 키워드로도 검색할 수 있게 수정 |
| `list_ingredients` | 페이지네이션 추가(skip, limit 파라미터) |

## 4. ingredient.py 추가 내용
| 함수 | 역할 |
| --- | --- |
| `create_ingredient` | 식재료 단건 추가 / POST |
| `get_ingredient` | 식재료 단건 조회 / GET |
| `update_ingredient` | 식재료 부분 수정 / PATCH |
| `delete_ingredient` | 식재료 삭제 / DELETE |
| `parse_date` | 'M/D' 문자열 → 'YYYY-MM-DD' 문자열 (공통 유틸 함수) |
| `get_ingredient_or_404` | id로 식재료 조회 후 반환 (공통 유틸 함수) |

## 5. requests.py
- 식재료 수정 요청 모델 `IngredientUpdate` 추가

## 6. main.py
- 기본 루트 경로(/)에 서버 상태 확인용 엔드포인트(`root`) 추가
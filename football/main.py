# ==================
# football/main.py
# ==================

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from datetime import date

import crud, schemas
from database import SessionLocal

app = FastAPI()

# 종속성
def get_db():
    """
    요청 하나하나마다 PostgreSQL 세션을 열고, 응답 후 닫아주는 의존성 함수
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get('/')
async def root():
    """API 서버가 살아있는지 확인하는 헬스 체크 엔드포인트"""
    return {"message":"API 상태 확인 성공"}

@app.get('/v0/players/', response_model=list[schemas.Player])
def read_players(skip: int=0, limit: int=100,
                 minimum_last_changed_date: date=None,
                 first_name: str=None, last_name: str=None, db: Session=Depends(get_db)):
    """
    선수 목록 조회
    
    skip/limit : 페이지네이션
    날짜/이름 : 선택 필터
    response_model : SQLAlchemy ORM 객체를 Pydantic 응답 모델로 변환
    """
    players = crud.get_players(db, skip=skip, limit=limit, min_last_changed_date=minimum_last_changed_date,
                               first_name=first_name, last_name=last_name)
    return players

@app.get('/v0/players/{player_id}', response_model=schemas.Player)
def read_player(player_id: int, db: Session=Depends(get_db)):
    """player_id 하나로 특정 선수 상세 정보 조회"""
    player = crud.get_player(db, player_id)
    if player is None:
        raise HTTPException(status_code=404, detail='선수를 찾을 수 없습니다')
    return player

@app.get('/v0/performances/', response_model=list[schemas.Performance])
def read_performances(db: Session=Depends(get_db),skip: int=0, limit:int=100,
                      minimun_last_changed_date: date=None):
    """선수 성적 목록 조회"""
    performances = crud.get_performances(db, skip=skip, limit=limit,
                                         min_last_changed_date=minimun_last_changed_date)
    return performances

@app.get('/v0/league/{league_id}', response_model=schemas.League)
def read_league(league_id: int, db: Session=Depends(get_db)):
    """특정 리그 조회"""
    league = crud.get_league(db, league_id=league_id)
    if league is None:
        raise HTTPException(status_code=404, detail='리그를 찾을 수 없습니다')
    
    return league

@app.get('/v0/leagues/', response_model=list[schemas.League])
def read_leagues(skip: int=0, limit: int=100,
                 minimum_last_changed_date: date=None,
                 league_name: str=None, db: Session=Depends(get_db)):
    """리그 목록 조회 - 이름(league_name)과 변경일 필터를 선택적으로 적용"""
    leagues = crud.get_leagues(db, skip=skip, limit=limit,
                               min_last_changed_date=minimum_last_changed_date,
                               league_name=league_name)
    return leagues

@app.get('/v0/teams/', response_model=list[schemas.Team])
def read_teams(skip: int=0, limit: int=100,
               minimum_last_changed_date: date=None,
               team_name: str=None, league_id: int=None,
               db: Session=Depends(get_db)):
    """
    팀 목록 조회
    
    league_id 조건으로 특정 리그의 팀만 가져올 수 있다
    예) GET /v0/teams/?league_id=5001 → 5001번 리그 소속 팀만 응답
    """
    teams = crud.get_teams(db, skip=skip, limit=limit,
                           min_last_changed_date=minimum_last_changed_date,
                           team_name=team_name, league_id=league_id)
    return teams

@app.get('/v0/counts/', response_model=schemas.Counts)
def read_count(db: Session=Depends(get_db)):
    """
    대시보드나 상태 화면에서 쓰기 좋은 요약 통계 API
    
    엔드포인트 하나 안에서 crud.py의 서로 다른 함수 3개를 호출해도 된다
    """
    counts = schemas.Counts(
        league_count=crud.get_league_count(db),
        team_count=crud.get_team_count(db),
        player_count=crud.get_player_count(db)
    )
    return counts
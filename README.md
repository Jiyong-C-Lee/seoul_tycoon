# 🏙️ 서울 부동산 타이쿤

서울의 부동산 시장을 배경으로 한 경영 시뮬레이션 게임입니다. 플레이어는 제한된 자금으로 시작하여 부동산을 매입하고 관리하며 자산을 늘려나갑니다.

## 🎮 게임 특징

- **실시간 시뮬레이션**: 월 단위로 진행되는 부동산 시장 시뮬레이션
- **다양한 건물 유형**: 주거용, 상업용, 오피스 등 다양한 부동산 투자
- **동적 시장**: 지역별로 변동하는 부동산 가격과 임대료
- **이벤트 시스템**: 정책 변화, 경제 상황 등 다양한 이벤트
- **전략적 의사결정**: 매수/매도 타이밍, 포트폴리오 관리

## 🚀 시작하기

### 필요 사항

- Python 3.8 이상
- pygame

### 설치 방법

```bash
# 저장소 클론
git clone https://github.com/Jiyong-C-Lee/seoul_tycoon.git
cd seoul_tycoon

# 가상환경 생성 (권장)
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux

# 의존성 설치
pip install -r requirements.txt
```

### 실행 방법

```bash
python main.py
```

## 🎯 게임 목표

36개월(3년) 동안 최대한 많은 자산을 축적하세요!
- 초기 자금: 100,000,000원
- 게임 기간: 36개월
- 파산 조건: 현금이 마이너스가 되면 게임 오버

## 🎮 조작법

- **마우스 클릭**: 건물 선택, 버튼 클릭
- **Space**: 일시정지/재개
- **1, 2, 4**: 게임 속도 조절 (1배속, 2배속, 4배속)
- **ESC**: 선택 해제

## 📁 프로젝트 구조

```
seoul_tycoon/
├── game/
│   ├── core/           # 게임 핵심 로직
│   │   ├── game.py     # 메인 게임 클래스
│   │   └── constants.py # 게임 상수
│   ├── data/           # 데이터 모델
│   │   └── models.py   # 게임 상태, 플레이어, 건물 등
│   ├── systems/        # 게임 시스템
│   │   ├── economy.py  # 경제 시스템
│   │   └── event_system.py # 이벤트 시스템
│   ├── ui/             # UI 렌더링
│   │   └── renderer.py # 화면 렌더링
│   └── utils/          # 유틸리티
│       └── helpers.py  # 맵 생성, 건물 배치 등
├── game_design/        # 게임 기획 문서
├── main.py            # 엔트리포인트
└── requirements.txt   # 의존성 목록
```

## 🛠️ 개발

### 개발 환경 설정

```bash
# 개발 모드로 실행
python main.py
```

### 코드 스타일

- Python 3.8+ 타입 힌트 사용
- PEP 8 스타일 가이드 준수
- 모듈별 명확한 책임 분리

## 📝 변경 이력

### v0.1.0 (Initial Release)
- 기본 게임 루프 구현
- 부동산 매매 시스템
- 경제 시뮬레이션
- 이벤트 시스템
- UI 렌더링

## 🤝 기여하기

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 라이선스

이 프로젝트는 개인 프로젝트입니다.

## 👤 개발자

**Jiyong-C-Lee**
- GitHub: [@Jiyong-C-Lee](https://github.com/Jiyong-C-Lee)

## 🙏 감사의 말

이 게임은 서울의 부동산 시장을 재미있게 시뮬레이션하기 위해 만들어졌습니다.

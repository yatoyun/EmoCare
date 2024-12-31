# EmoCare: プロジェクト設計と仕様書

## 概要

EmoCareはメンタルヘルスケアに特化したLINE BotとWebアプリケーションです。LINE Botはリアルタイムの感情分析とアドバイス提供を、Webアプリは感情ジャーナルとユーザー認証機能を提供します。

---

## 技術スタック

- Backend: Django REST Framework
- Frontend: React.js
- Database: SQLite
- Additional Services: Google Cloud Language API, GPT-3 API, LINE Messaging API

---

## 機能

### LINE Bot

1. **感情分析:** 
    - Google Cloud Language APIを使用。
    - ユーザーが送ったテキストメッセージから感情を分析。

2. **アドバイス提供:**
    - GPT-3 APIを使用。
    - 感情分析の結果に基づいてアドバイスを生成。

### Webアプリ

1. **ユーザー認証:**
    - RegisterとLogin機能。
    - Djangoの認証システムを使用。

2. **感情ジャーナル:**
    - ユーザーが過去に送ったメッセージと感情分析結果を表示。

---

## アーキテクチャ

### Backend (Django REST Framework)

- `emo_core/`
  - `models.py`: データモデル
  - `serializers.py`: シリアライザ
  - `views.py`: APIエンドポイント
  - `urls.py`: URLルーティング
  - `line_bot_api.py`: LINE Botロジック
  - `auth/views_auth.py`: 認証ビュー
  - `auth/serializers_auth.py`: 認証シリアライザ

### Frontend (React.js)

- `src/`
  - `index.js`: エントリーポイント
  - `App.js`: メインアプリコンポーネント
  - `components/`
    - `Login.js`: ログインコンポーネント
    - `Register.js`: 登録コンポーネント
    - `EmoJournal.js`: 感情ジャーナルコンポーネント
  - `api/api.js`: API呼び出し

---

## タイムライン

### LINE Bot

- 週1: 設計と準備
- 週2: 感情分析機能
- 週3: アドバイス提供機能
- 週4: 統合とテスト

### Webアプリ

- 週1: プロジェクト設定とReactの基礎構築
- 週2: ユーザー認証機能
- 週3: 感情ジャーナル機能
- 週4: テストとデバッグ

---

注意: この設計と仕様書は初版であり、プロジェクト進行中に調整が必要な場合があります。

バックエンドのディレクトリ
```
backend/
├── apps
│   ├── chat
│   │   ├── __init__.py
│   │   ├── apps.py
│   │   ├── migrations
│   │   ├── models.py
│   │   ├── serializers
│   │   │   ├── __init__.py
│   │   │   └── chat_serializers.py
│   │   ├── services
│   │   │   ├── __init__.py
│   │   │   └── chat_services.py
│   │   ├── tests
│   │   │   ├── __init__.py
│   │   │   └── test_chat.py
│   │   ├── urls.py
│   │   └── views
│   │       ├── __init__.py
│   │       └── chat_views.py
│   ├── user_statistics
│   │   ├── __init__.py
│   │   ├── apps.py
│   │   ├── migrations
│   │   ├── models.py
│   │   ├── serializers
│   │   │   ├── __init__.py
│   │   │   └── user_statistics_serializers.py
│   │   ├── services
│   │   │   ├── __init__.py
│   │   │   └── user_statistics_services.py
│   │   ├── tests
│   │   │   ├── __init__.py
│   │   │   └── test_user_statistics.py
│   │   ├── urls.py
│   │   └── views
│   │       ├── __init__.py
│   │       └── user_statistics_views.py
│   └── users
│       ├── __init__.py
│       ├── admin.py
│       ├── apps.py
│       ├── managers.py
│       ├── migrations
│       ├── models.py
│       ├── serializers
│       │   ├── __init__.py
│       │   └── users_serializers.py
│       ├── services
│       │   ├── __init__.py
│       │   └── users_services.py
│       ├── tests
│       │   ├── __init__.py
│       │   └── test_users.py
│       ├── urls.py
│       └── views
│           ├── __init__.py
│           └── users_views.py
├── config
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── config.json
├── db
│   └── db.sqlite3
├── google_cresidentials.json
├── manage.py
├── nginx.conf
├── poetry.lock
├── pyproject.toml
├── pytest.ini
├── requirements-dev.txt
├── requirements.txt
├── supervisord.conf
├── supervisord.log
├── supervisord.pid
└── validations // 以前のモジュール、今後はusersに統合
    └── password_strength_validator.py
```
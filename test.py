import requests
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

import config

USERS_FILE = "users.txt"  # 사용자 목록 파일 경로

# Google API 권한 설정
GOOGLE_SCOPES = ['https://www.googleapis.com/auth/admin.directory.group.member']
google_credentials = Credentials.from_service_account_file(
    config.GOOGLE_SERVICE_ACCOUNT_FILE, scopes=GOOGLE_SCOPES
)
google_service = build('admin', 'directory_v1', credentials=google_credentials)

# GitHub 사용자 삭제 함수
def delete_github_user(username):
    url = f"https://api.github.com/orgs/{config.GITHUB_ORG}/members/{username}"
    headers = {
        "Authorization": f"Bearer {config.GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }
    response = requests.delete(url, headers=headers)
    if response.status_code == 204:
        print(f"✅ GitHub 사용자 {username} 성공적으로 제거됨.")
    elif response.status_code == 404:
        print(f"⚠️ GitHub 사용자 {username}를 찾을 수 없음.")
    else:
        print(f"❌ GitHub 사용자 {username} 제거 실패: {response.status_code}, {response.text}")

# Google Groups 사용자 삭제 함수
def delete_google_group_user(email):
    try:
        google_service.members().delete(
            groupKey=config.GOOGLE_GROUP_EMAIL, memberKey=email
        ).execute()
        print(f"✅ Google Groups 사용자 {email} 성공적으로 제거됨.")
    except Exception as e:
        print(f"❌ Google Groups 사용자 {email} 제거 실패: {e}")

# 사용자 파일 처리 및 삭제 실행
def process_users(file_path):
    with open(file_path, "r") as file:
        for line in file:
            if line.strip():  # 빈 줄 무시
                try:
                    user_id, user_email = line.strip().split()
                    # GitHub 사용자 삭제
                    delete_github_user(user_id)
                    # Google Groups 사용자 삭제
                    delete_google_group_user(user_email)
                except ValueError:
                    print(f"⚠️ 잘못된 형식의 데이터: {line.strip()}")

# 스크립트 실행
if __name__ == "__main__":
    process_users(USERS_FILE)

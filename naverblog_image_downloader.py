import os
import sys
import time

def wait_enter(msg="계속하려면 Enter를 누르세요..."):
    input(msg)

def ask_next(msg="다음 단계로 넘어가겠습니까? (Y/n): "):
    ans = input(msg).strip().lower()
    return ans in ["y", "yes", ""]

def banner(text):
    print("\n" + "="*70)
    print(text)
    print("="*70 + "\n")

def safe_remove(path):
    if os.path.exists(path):
        try:
            os.remove(path)
            print(f"  - {path} 삭제 완료")
        except Exception as e:
            print(f"  - {path} 삭제 실패: {e}")

def main():
    banner("STEP 1) 개발자도구 열기 및 이미지 URL 추출 안내")

    print("""
1. 브라우저에서 네이버 블로그 글을 엽니다.
2. 개발자도구를 엽니다:
   - Windows: F12 또는 Ctrl + Shift + I
   - Mac: Cmd + Opt + I
3. 개발자도구 상단 탭에서 'Console'을 클릭합니다.
4. Console 창에 아래 코드를 붙여넣고 Enter를 누르세요:

Array.from(document.querySelectorAll('img.se-image-resource.egjs-visible'))
     .map(img => img.src)
     .join('\\n')

""")

    wait_enter("url들이 출력되어야 정상 작동입니다. 정상 작동했으면 Enter를 누르세요.")

    # STEP 2: 붙여넣기 파일 생성
    banner("STEP 2) paste_urls.txt 파일에 붙여넣기")

    paste_file = "paste_urls.txt"
    if not os.path.exists(paste_file):
        with open(paste_file, "w", encoding="utf-8") as f:
            f.write("// 여기에 콘솔에서 복사한 내용을 붙여넣고 저장하세요.\n")

    print(f"""
📄 이제 '{paste_file}' 파일이 생성되었습니다.

1. paste_urls.txt 파일을 열고 (다운로드 창을 확인 하세요 or 현재 파이썬 파일 실행 위치)
2. 콘솔에서 출력된 URL 전체를 그대로 복붙하고
3. 저장 (Ctrl+S / Cmd+S) 하세요.

저장을 완료했다면 Enter를 누르세요.
""")

    input()

    # STEP 3: 파일 읽기
    with open(paste_file, "r", encoding="utf-8") as f:
        raw = f.read()

    with open("urls_raw.txt", "w", encoding="utf-8") as f:
        f.write(raw)

    print("📄 urls_raw.txt 생성 완료!")

    if not ask_next():
        return

    # STEP 4: \n 문자열을 실제 줄바꿈으로 치환
    banner("STEP 3) 줄바꿈 정상화 → urls_clean.txt 생성")

    cleaned = (
        raw.replace("\\n", "\n")   
           .replace("'", "")      
    )

    with open("urls_clean.txt", "w", encoding="utf-8") as f:
        f.write(cleaned)

    print("📄 urls_clean.txt 생성 완료!")

    if not ask_next():
        return

    # STEP 5: 블로그 referer 받기
    banner("STEP 4) 블로그 주소 입력")

    page_url = input("이제 마지막 단계입니다. 블로그 글 주소를 입력하세요: (https://...)\n").strip()

    if page_url == "":
        print("잘못된 URL — 종료.")
        return


    # STEP 6: 다운로드
    banner("STEP 5) 이미지 다운로드 시작")

    import requests

    if not os.path.exists("downloaded"):
        os.makedirs("downloaded")

    lines = cleaned.split("\n")

    for i, url in enumerate(lines, start=1):
        if not url.strip() or url.startswith("//"):
            continue

        print(f"[{i}/{len(lines)}] 다운로드 시도: {url}")

        try:
            r = requests.get(
                url,
                headers={
                    "User-Agent": "Mozilla/5.0",
                    "Referer": page_url
                },
                timeout=10
            )

            if r.status_code == 200:
                ext = ".jpg"
                if ".png" in url.lower():
                    ext = ".png"

                fname = f"downloaded/img_{i}{ext}"
                with open(fname, "wb") as f:
                    f.write(r.content)

                print(f"  ✔ 저장됨: {fname}")

            else:
                print(f"  ❗ 실패 (HTTP {r.status_code})")

        except Exception as e:
            print("  ❗ 오류:", e)

    banner("완료!")
    print("downloaded 폴더를 확인하세요.")
    print("\n")
    wait_enter("파일을 정리해 드리겠습니다 (paste_urls.txt, urls_raw.txt, urls_clean.txt) \nEnter를 누르세요.")
    safe_remove("paste_urls.txt")
    safe_remove("urls_raw.txt")
    safe_remove("urls_clean.txt")

    print("정리 끝!")
    banner("☆.。.:*・°☆ ｡행복한 하루 되세요+.｡☆ﾟ:;｡+ﾟ†_(′▽`*)β))")

if __name__ == "__main__":
    main()

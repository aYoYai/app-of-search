import streamlit as st
import google.generativeai as genai
from duckduckgo_search import DDGS
import requests
from bs4 import BeautifulSoup
import json
import time

# --- Functions ---

def search_web(query: str, max_results: int = 4):
    """DuckDuckGoを使用してWeb検索を実行し、結果を返す"""
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=max_results))
        return results
    except Exception as e:
        st.error(f"検索中にエラーが発生しました: {e}")
        return []

def scrape_content(url: str, timeout: int = 10) -> str:
    """指定されたURLからWebページの主要なテキストコンテンツを抽出する"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()  # HTTPエラーがあれば例外を発生させる
        soup = BeautifulSoup(response.content, 'html.parser', from_encoding=response.encoding)
        
        # 主要なコンテンツのタグを優先的に探す
        main_content = soup.find('main') or soup.find('article') or soup.body
        
        paragraphs = main_content.find_all('p', recursive=True)
        content = "\n".join([p.get_text(strip=True) for p in paragraphs if len(p.get_text(strip=True)) > 50])
        
        # パラグラフから十分なコンテンツが取れない場合は、メイン領域のテキスト全体を取得
        if len(content) < 200:
            content = main_content.get_text(separator='\n', strip=True)
            
        return content[:4000]  # APIのトークン制限のため、コンテンツを短縮
    except requests.RequestException:
        return f"コンテンツの取得に失敗しました: {url}"
    except Exception:
        return f"予期せぬエラーでコンテンツ取得に失敗しました: {url}"

def get_summary(api_key: str, query: str, search_results: list):
    """Gemini APIを使用して、検索結果から要約を生成する"""
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')

    scraped_contents = []
    progress_bar = st.progress(0, text="各Webページから情報を収集中...")

    for i, result in enumerate(search_results):
        content = scrape_content(result['href'])
        if not content.startswith("コンテンツの取得に失敗") and not content.startswith("予期せぬエラー"):
            scraped_contents.append(f"--- ソース {i+1} ({result['title']}) ---\n{content}\n\n")
        time.sleep(0.5)  # サーバーへの負荷軽減
        progress_bar.progress((i + 1) / len(search_results), text=f"情報収集中: {result['title']}")
    
    progress_bar.empty()
    
    if not scraped_contents:
        return "すべてのソースからコンテンツを取得できませんでした。別のキーワードで試すか、時間をおいて再度実行してください。"

    prompt = f"""
    ユーザーの検索クエリと、Webから収集した以下の情報を基に、包括的で分かりやすい要約を作成してください。

    # 検索クエリ:
    {query}

    # Webからの収集情報:
    {''.join(scraped_contents)}

    # 生成する要約のルール:
    - マークダウン形式を使用して、重要なポイントを箇条書きで整理してください。
    - 専門用語には簡単な説明を加えてください。
    - 全体として、中立的かつ客観的な視点で記述してください。

    # 要約:
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"要約の生成中にエラーが発生しました: {e}"

def generate_quiz(api_key: str, history_item: dict):
    """Gemini APIを使用して、検索履歴から4択クイズを生成する"""
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')

    prompt = f"""
    以下の検索履歴（検索クエリとAIによる要約）を基にして、その内容の理解度を測るための高品質な4択クイズを1問作成してください。
    必ず以下のJSON形式で、日本語で出力してください。

    {{
      "question": "（ここに問題文）",
      "options": ["（選択肢1）", "（選択肢2）", "（選択肢3）", "（選択肢4）"],
      "answer": "（ここに正解の選択肢の文字列）",
      "explanation": "（ここに、なぜそれが正解なのかを説明する丁寧な解説文）"
    }}

    # 検索履歴:
    ## クエリ:
    {history_item['query']}

    ## 要約:
    {history_item['summary']}
    """
    try:
        response = model.generate_content(prompt)
        cleaned_response = response.text.strip().lstrip("```json").rstrip("```").strip()
        quiz_data = json.loads(cleaned_response)
        if all(k in quiz_data for k in ["question", "options", "answer", "explanation"]) and len(quiz_data["options"]) == 4:
            return quiz_data
        else:
            return None
    except Exception:
        return None

# --- Streamlit App ---

st.set_page_config(page_title="AI Search & Quiz App", layout="wide", initial_sidebar_state="expanded")

# セッション状態の初期化
if 'search_history' not in st.session_state:
    st.session_state.search_history = []
if 'quizzes' not in st.session_state:
    st.session_state.quizzes = {}
if 'api_key' not in st.session_state:
    st.session_state.api_key = ""

# --- サイドバー ---
with st.sidebar:
    st.header("🛠️ 設定")
    st.session_state.api_key = st.text_input("Google AI (Gemini) APIキー", value=st.session_state.api_key, type="password", key="api_key_input")
    st.markdown("[APIキーはこちらで取得](https://aistudio.google.com/app/apikey)")
    st.info("⚠️ 入力されたAPIキーはページの再読み込み後も保持されますが、ブラウザを閉じると消えます。サーバーには一切保存されません。")
    page = st.radio("メニュー", ["検索エンジン", "検索履歴とクイズ"])
    st.markdown("---")
    st.write("Created by a helpful AI assistant.")

# --- メインコンテンツ ---

api_key_configured = bool(st.session_state.api_key)

if page == "検索エンジン":
    st.title("🧠 AI搭載 検索エンジン")
    st.markdown("入力したキーワードでWeb検索し、AIが結果を要約します。")
    if not api_key_configured:
        st.warning("サイドバーでGoogle AI APIキーを設定してください。検索機能が有効になります。")

    query = st.text_input("検索したいキーワードを入力してください", "", key="search_query")

    if st.button("検索実行", type="primary", disabled=not api_key_configured):
        if not query:
            st.warning("検索キーワードを入力してください。")
        else:
            with st.spinner("Webから情報を検索し、AIが要約を作成しています..."):
                search_results = search_web(query)
                if not search_results:
                    st.error("検索結果が見つかりませんでした。別のキーワードでお試しください。")
                else:
                    summary = get_summary(st.session_state.api_key, query, search_results)
                    st.success("要約が完了しました！")
                    st.markdown(summary)
                    with st.expander("参照した情報源"):
                        for result in search_results:
                            st.write(f"- [{result['title']}]({result['href']})")
                    history_item = {
                        "query": query, "summary": summary,
                        "sources": [{"title": r['title'], "href": r['href']} for r in search_results]
                    }
                    st.session_state.search_history.insert(0, history_item)

elif page == "検索履歴とクイズ":
    st.title("📚 検索履歴とクイズチャレンジ")
    st.markdown("過去の検索履歴を確認し、その内容に関するクイズに挑戦できます。")
    if not api_key_configured:
        st.warning("サイドバーでGoogle AI APIキーを設定してください。クイズの生成機能が利用可能になります。")

    if not st.session_state.search_history:
        st.info("まだ検索履歴がありません。「検索エンジン」ページで検索を行ってください。")
    else:
        for i, item in enumerate(st.session_state.search_history):
            st.markdown("---")
            with st.container():
                st.subheader(f"履歴{i+1}: {item['query']}")
                with st.expander("この検索の要約と参照元を見る"):
                    st.markdown(item['summary'])
                    st.markdown("**参照した情報源**")
                    for source in item['sources']:
                        st.write(f"- [{source['title']}]({source['href']})")
                
                if i in st.session_state.quizzes:
                    quiz_data = st.session_state.quizzes[i]
                    with st.form(key=f"quiz_form_{i}"):
                        st.write(f"**問題:** {quiz_data['question']}")
                        user_answer = st.radio("選択肢:", quiz_data['options'], key=f"ans_{i}", label_visibility="collapsed")
                        submitted = st.form_submit_button("解答する")
                        if submitted:
                            if user_answer == quiz_data['answer']:
                                st.success(f"正解！ 🎉 正しい答えは「{quiz_data['answer']}」です。")
                            else:
                                st.error(f"不正解... 正解は「{quiz_data['answer']}」でした。")
                            st.info(f"**解説:**\n{quiz_data['explanation']}")
                else:
                    if st.button(f"この履歴でクイズを生成", key=f"gen_quiz_{i}", disabled=not api_key_configured):
                        with st.spinner("AIがクイズを作成中..."):
                            quiz = generate_quiz(st.session_state.api_key, item)
                            if quiz:
                                st.session_state.quizzes[i] = quiz
                                st.success("クイズができました！ページを自動で更新します。")
                                time.sleep(1)
                                st.rerun()
                            else:
                                st.error("クイズの生成に失敗しました。AIの応答が不正か、コンテンツが不十分な可能性があります。")

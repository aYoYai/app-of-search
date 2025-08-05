website↓
https://ayoyai.github.io/app-of-search/
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>検索履歴クイズアプリ</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: #333;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }

        .header {
            text-align: center;
            margin-bottom: 30px;
            color: white;
        }

        .header h1 {
            font-size: 2.5rem;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }

        .tab-container {
            display: flex;
            justify-content: center;
            margin-bottom: 30px;
        }

        .tab-button {
            background: rgba(255,255,255,0.2);
            color: white;
            border: none;
            padding: 12px 24px;
            margin: 0 5px;
            border-radius: 25px;
            cursor: pointer;
            transition: all 0.3s ease;
            backdrop-filter: blur(10px);
        }

        .tab-button.active {
            background: rgba(255,255,255,0.9);
            color: #333;
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }

        .tab-content {
            background: rgba(255,255,255,0.95);
            border-radius: 20px;
            padding: 30px;
            backdrop-filter: blur(10px);
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            min-height: 500px;
        }

        .search-section {
            margin-bottom: 30px;
        }

        .api-key-input {
            width: 100%;
            padding: 12px;
            border: 2px solid #ddd;
            border-radius: 10px;
            margin-bottom: 15px;
            font-size: 16px;
            transition: border-color 0.3s ease;
        }

        .api-key-input:focus {
            outline: none;
            border-color: #667eea;
        }

        .search-container {
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
        }

        .search-input {
            flex: 1;
            padding: 15px;
            border: 2px solid #ddd;
            border-radius: 10px;
            font-size: 16px;
            transition: border-color 0.3s ease;
        }

        .search-input:focus {
            outline: none;
            border-color: #667eea;
        }

        .search-button {
            background: linear-gradient(45deg, #667eea, #764ba2);
            color: white;
            border: none;
            padding: 15px 30px;
            border-radius: 10px;
            cursor: pointer;
            font-size: 16px;
            transition: transform 0.2s ease;
        }

        .search-button:hover {
            transform: translateY(-2px);
        }

        .search-button:disabled {
            opacity: 0.6;
            cursor: not-allowed;
            transform: none;
        }

        .search-result {
            background: #f8f9fa;
            border-left: 4px solid #667eea;
            padding: 20px;
            margin: 20px 0;
            border-radius: 10px;
            animation: fadeIn 0.5s ease;
        }

        .search-result h3 {
            color: #333;
            margin-bottom: 10px;
        }

        .search-result p {
            line-height: 1.6;
            color: #666;
        }

        .history-item {
            background: #f8f9fa;
            border-radius: 10px;
            padding: 15px;
            margin-bottom: 15px;
            border-left: 4px solid #667eea;
            cursor: pointer;
            transition: all 0.3s ease;
        }

        .history-item:hover {
            background: #e9ecef;
            transform: translateX(5px);
        }

        .quiz-container {
            background: #f8f9fa;
            border-radius: 15px;
            padding: 25px;
            margin-bottom: 20px;
            border: 2px solid #667eea;
        }

        .quiz-question {
            font-size: 18px;
            font-weight: bold;
            margin-bottom: 20px;
            color: #333;
        }

        .quiz-option {
            display: block;
            background: white;
            border: 2px solid #ddd;
            border-radius: 10px;
            padding: 15px;
            margin-bottom: 10px;
            cursor: pointer;
            transition: all 0.3s ease;
        }

        .quiz-option:hover {
            border-color: #667eea;
            background: #f0f0f0;
        }

        .quiz-option.selected {
            border-color: #667eea;
            background: #e3f2fd;
        }

        .quiz-option.correct {
            border-color: #4caf50;
            background: #e8f5e8;
        }

        .quiz-option.incorrect {
            border-color: #f44336;
            background: #ffebee;
        }

        .quiz-submit {
            background: linear-gradient(45deg, #667eea, #764ba2);
            color: white;
            border: none;
            padding: 12px 30px;
            border-radius: 10px;
            cursor: pointer;
            margin-top: 15px;
            font-size: 16px;
        }

        .quiz-explanation {
            background: #e8f5e8;
            border-left: 4px solid #4caf50;
            padding: 15px;
            margin-top: 15px;
            border-radius: 10px;
            display: none;
        }

        .loading {
            display: inline-block;
            width: 20px;
            height: 20px;
            border: 3px solid rgba(255,255,255,.3);
            border-radius: 50%;
            border-top-color: #fff;
            animation: spin 1s ease-in-out infinite;
        }

        .error {
            background: #ffebee;
            color: #c62828;
            padding: 15px;
            border-radius: 10px;
            margin: 10px 0;
            border-left: 4px solid #f44336;
        }

        .hidden {
            display: none;
        }

        @keyframes spin {
            to { transform: rotate(360deg); }
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }

        @media (max-width: 768px) {
            .container {
                padding: 10px;
            }
            
            .search-container {
                flex-direction: column;
            }
            
            .tab-button {
                padding: 10px 16px;
                font-size: 14px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔍 検索履歴クイズアプリ</h1>
            <p>Gemini AIを使用した高機能検索エンジン</p>
        </div>

        <div class="tab-container">
            <button class="tab-button active" onclick="showTab('search')">検索</button>
            <button class="tab-button" onclick="showTab('history')">履歴</button>
            <button class="tab-button" onclick="showTab('quiz')">クイズ</button>
        </div>

        <div id="search-tab" class="tab-content">
            <div class="search-section">
                <input type="password" id="api-key" class="api-key-input" placeholder="Gemini APIキーを入力してください">
                <div class="search-container">
                    <input type="text" id="search-input" class="search-input" placeholder="検索したいキーワードを入力してください...">
                    <button id="search-button" class="search-button" onclick="performSearch()">検索</button>
                </div>
            </div>
            <div id="search-results"></div>
        </div>

        <div id="history-tab" class="tab-content hidden">
            <h2>検索履歴</h2>
            <div id="history-list"></div>
        </div>

        <div id="quiz-tab" class="tab-content hidden">
            <h2>検索履歴クイズ</h2>
            <div id="quiz-content">
                <p>検索履歴がまだありません。まず検索を行ってください。</p>
            </div>
        </div>
    </div>

    <script>
        let searchHistory = [];
        let currentQuiz = null;

        // タブ切り替え機能
        function showTab(tabName) {
            // すべてのタブを非表示にする
            document.querySelectorAll('.tab-content').forEach(tab => {
                tab.classList.add('hidden');
            });
            
            // すべてのタブボタンからactiveクラスを削除
            document.querySelectorAll('.tab-button').forEach(button => {
                button.classList.remove('active');
            });
            
            // 選択されたタブを表示
            document.getElementById(tabName + '-tab').classList.remove('hidden');
            event.target.classList.add('active');
            
            // クイズタブが選択された場合、クイズを更新
            if (tabName === 'quiz') {
                updateQuizContent();
            } else if (tabName === 'history') {
                updateHistoryContent();
            }
        }

        // 検索機能
        async function performSearch() {
            const apiKey = document.getElementById('api-key').value.trim();
            const query = document.getElementById('search-input').value.trim();
            const searchButton = document.getElementById('search-button');
            const resultsDiv = document.getElementById('search-results');

            if (!apiKey) {
                showError('APIキーを入力してください。');
                return;
            }

            if (!query) {
                showError('検索キーワードを入力してください。');
                return;
            }

            searchButton.disabled = true;
            searchButton.innerHTML = '<span class="loading"></span> 検索中...';
            resultsDiv.innerHTML = '';

            try {
                // Google AI Studioを使用して検索と要約を実行
                const summary = await searchAndSummarize(apiKey, query);
                
                // 検索結果を表示
                displaySearchResult(query, summary);
                
                // 検索履歴に追加
                addToHistory(query, summary);
                
            } catch (error) {
                showError('検索中にエラーが発生しました: ' + error.message);
            } finally {
                searchButton.disabled = false;
                searchButton.innerHTML = '検索';
            }
        }

        // Gemini APIを使用した検索と要約
        async function searchAndSummarize(apiKey, query) {
            const prompt = `以下の検索クエリについて、ウェブ検索を行ったと仮定して情報を提供してください。

検索クエリ: "${query}"

以下の条件を満たしてください：
- 回答は日本語で正確に300文字以内で簡潔にまとめる
- わかりやすく教育的価値がある内容にする
- 重要なポイントを含める
- 文字数制限を必ず守る`;

            try {
                const response = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=${apiKey}`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        contents: [{
                            parts: [{
                                text: prompt
                            }]
                        }]
                    })
                });

                if (!response.ok) {
                    const errorData = await response.json().catch(() => null);
                    
                    if (response.status === 400) {
                        if (errorData?.error?.message?.includes('API_KEY_INVALID')) {
                            throw new Error('APIキーが無効です。正しいGemini APIキーを入力してください。');
                        } else {
                            throw new Error(`リクエストエラー: ${errorData?.error?.message || '不正なリクエストです。'}`);
                        }
                    } else if (response.status === 403) {
                        throw new Error('APIキーのアクセス権限がありません。Gemini APIが有効になっているか確認してください。');
                    } else if (response.status === 429) {
                        throw new Error('API使用制限に達しました。しばらく待ってから再試行してください。');
                    } else if (response.status === 500) {
                        throw new Error('サーバーエラーが発生しました。しばらく待ってから再試行してください。');
                    } else {
                        throw new Error(`API呼び出しエラー (${response.status}): ${errorData?.error?.message || 'APIキーを確認してください。'}`);
                    }
                }

                const data = await response.json();
                
                if (!data.candidates || data.candidates.length === 0) {
                    throw new Error('APIからの応答が空です。リクエストを確認してください。');
                }
                
                if (!data.candidates[0].content || !data.candidates[0].content.parts || data.candidates[0].content.parts.length === 0) {
                    throw new Error('APIからの応答形式が不正です。');
                }

                return data.candidates[0].content.parts[0].text;
                
            } catch (error) {
                if (error.name === 'TypeError' && error.message.includes('fetch')) {
                    throw new Error('ネットワークエラー: インターネット接続を確認してください。');
                }
                throw error;
            }
        }

        // 検索結果を表示
        function displaySearchResult(query, summary) {
            const resultsDiv = document.getElementById('search-results');
            const charCount = summary.length;
            resultsDiv.innerHTML = `
                <div class="search-result">
                    <h3>「${query}」の検索結果</h3>
                    <div style="background: white; padding: 15px; border-radius: 8px; margin: 10px 0;">
                        <p style="line-height: 1.8; white-space: pre-wrap;">${summary}</p>
                    </div>
                    <div style="text-align: right; color: #666; font-size: 12px; margin-top: 5px;">
                        文字数: ${charCount}/300文字
                    </div>
                </div>
            `;
        }

        // 検索履歴に追加
        function addToHistory(query, summary) {
            const historyItem = {
                id: Date.now(),
                query: query,
                summary: summary,
                timestamp: new Date().toLocaleString('ja-JP')
            };
            
            searchHistory.unshift(historyItem);
            
            // 最大20件まで保持
            if (searchHistory.length > 20) {
                searchHistory = searchHistory.slice(0, 20);
            }
        }

        // 履歴コンテンツを更新
        function updateHistoryContent() {
            const historyList = document.getElementById('history-list');
            
            if (searchHistory.length === 0) {
                historyList.innerHTML = '<p>検索履歴がありません。</p>';
                return;
            }

            historyList.innerHTML = searchHistory.map(item => `
                <div class="history-item" onclick="showHistoryDetail(${item.id})">
                    <h4>${item.query}</h4>
                    <p style="color: #666; font-size: 14px;">${item.timestamp}</p>
                    <p style="margin-top: 10px;">${item.summary.substring(0, 100)}...</p>
                </div>
            `).join('');
        }

        // 履歴詳細を表示
        function showHistoryDetail(id) {
            const item = searchHistory.find(h => h.id === id);
            if (item) {
                // モーダル風のポップアップを作成
                const modal = document.createElement('div');
                modal.style.cssText = `
                    position: fixed; top: 0; left: 0; width: 100%; height: 100%;
                    background: rgba(0,0,0,0.8); z-index: 1000;
                    display: flex; align-items: center; justify-content: center;
                `;
                
                const content = document.createElement('div');
                content.style.cssText = `
                    background: white; border-radius: 15px; padding: 30px;
                    max-width: 80%; max-height: 80%; overflow-y: auto;
                    position: relative;
                `;
                
                content.innerHTML = `
                    <button onclick="this.closest('div[style*=\"fixed\"]').remove()" 
                            style="position: absolute; top: 10px; right: 15px; background: none; border: none; font-size: 24px; cursor: pointer;">×</button>
                    <h3 style="margin-bottom: 15px; color: #333;">検索クエリ: ${item.query}</h3>
                    <p style="color: #666; margin-bottom: 20px; font-size: 14px;">検索日時: ${item.timestamp}</p>
                    <div style="background: #f8f9fa; padding: 20px; border-radius: 10px; border-left: 4px solid #667eea;">
                        <h4 style="margin-bottom: 10px;">検索結果（全文表示）</h4>
                        <p style="line-height: 1.8; white-space: pre-wrap;">${item.summary}</p>
                        <div style="text-align: right; color: #666; font-size: 12px; margin-top: 10px;">
                            文字数: ${item.summary.length}文字
                        </div>
                    </div>
                `;
                
                modal.appendChild(content);
                document.body.appendChild(modal);
                
                // 背景クリックで閉じる
                modal.addEventListener('click', function(e) {
                    if (e.target === modal) {
                        modal.remove();
                    }
                });
            }
        }

        // クイズコンテンツを更新
        function updateQuizContent() {
            const quizContent = document.getElementById('quiz-content');
            
            if (searchHistory.length < 2) {
                quizContent.innerHTML = '<p>クイズを生成するには、少なくとも2回の検索が必要です。</p>';
                return;
            }

            generateQuiz();
        }

        // クイズ生成
        async function generateQuiz() {
            const quizContent = document.getElementById('quiz-content');
            const apiKey = document.getElementById('api-key').value.trim();
            
            if (!apiKey) {
                quizContent.innerHTML = '<div class="error">クイズ生成にはAPIキーが必要です。検索タブでAPIキーを入力してください。</div>';
                return;
            }
            
            quizContent.innerHTML = '<p>クイズを生成中...</p>';

            try {
                // ランダムに検索履歴からアイテムを選択
                const randomItem = searchHistory[Math.floor(Math.random() * searchHistory.length)];
                
                // APIを使用してクイズを生成
                const quiz = await createQuizWithAPI(apiKey, randomItem);
                currentQuiz = quiz;
                
                displayQuiz(quiz);
            } catch (error) {
                quizContent.innerHTML = `<div class="error">クイズの生成に失敗しました: ${error.message}</div>`;
            }
        }

        // APIを使用してクイズを作成
        async function createQuizWithAPI(apiKey, historyItem) {
            const prompt = `以下の検索クエリと要約を元に、4択クイズを作成してください。

検索クエリ: "${historyItem.query}"
検索結果要約: "${historyItem.summary}"

以下の条件を満たしてください：
1. 問題文は検索クエリを60文字程度で説明する文章にする（検索クエリ自体は絶対に問題文に含めない）
2. 正解は検索クエリそのもの
3. 間違いの選択肢3つは関連性のあるフェイクを作成（実在する可能性のある自然な選択肢）
4. 解説は検索結果の要約を含めて教育的にする

以下のJSON形式で回答してください：
{
  "question": "検索クエリを説明する60文字程度の問題文",
  "options": ["正解の検索クエリ", "フェイク1", "フェイク2", "フェイク3"],
  "correctAnswer": "正解の検索クエリ",
  "explanation": "解説文（検索結果要約を含む）"
}`;

            try {
                const response = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=${apiKey}`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        contents: [{
                            parts: [{
                                text: prompt
                            }]
                        }]
                    })
                });

                if (!response.ok) {
                    throw new Error('クイズ生成APIの呼び出しに失敗しました');
                }

                const data = await response.json();
                const responseText = data.candidates[0].content.parts[0].text;
                
                // JSONを抽出
                const jsonMatch = responseText.match(/\{[\s\S]*\}/);
                if (!jsonMatch) {
                    throw new Error('APIからの応答形式が不正です');
                }
                
                const quizData = JSON.parse(jsonMatch[0]);
                
                // 選択肢をシャッフル
                const shuffledOptions = [...quizData.options].sort(() => Math.random() - 0.5);
                
                return {
                    question: quizData.question,
                    options: shuffledOptions,
                    correctAnswer: quizData.correctAnswer,
                    explanation: quizData.explanation
                };
                
            } catch (error) {
                console.error('API Error:', error);
                throw new Error('クイズ生成中にエラーが発生しました');
            }
        }

        // クイズを表示
        function displayQuiz(quiz) {
            const quizContent = document.getElementById('quiz-content');
            
            quizContent.innerHTML = `
                <div class="quiz-container">
                    <div class="quiz-question">${quiz.question}</div>
                    ${quiz.options.map((option, index) => `
                        <label class="quiz-option" onclick="selectOption(${index})">
                            <input type="radio" name="quiz-answer" value="${option}" style="display: none;">
                            ${option}
                        </label>
                    `).join('')}
                    <button class="quiz-submit" onclick="submitQuiz()">回答</button>
                    <div class="quiz-explanation" id="quiz-explanation">
                        ${quiz.explanation.replace(/\n/g, '<br>')}
                    </div>
                </div>
                <button class="quiz-submit" onclick="generateQuiz()" style="margin-top: 10px;">新しいクイズ</button>
            `;
        }

        // 選択肢を選択
        function selectOption(index) {
            document.querySelectorAll('.quiz-option').forEach(option => {
                option.classList.remove('selected');
            });
            document.querySelectorAll('.quiz-option')[index].classList.add('selected');
        }

        // クイズを提出
        function submitQuiz() {
            const selectedOption = document.querySelector('.quiz-option.selected');
            if (!selectedOption) {
                alert('選択肢を選んでください。');
                return;
            }

            const selectedAnswer = selectedOption.textContent.trim();
            const isCorrect = selectedAnswer === currentQuiz.correctAnswer;

            // すべての選択肢にスタイルを適用
            document.querySelectorAll('.quiz-option').forEach(option => {
                const optionText = option.textContent.trim();
                if (optionText === currentQuiz.correctAnswer) {
                    option.classList.add('correct');
                } else if (option.classList.contains('selected') && !isCorrect) {
                    option.classList.add('incorrect');
                }
            });

            // 解説を表示
            document.getElementById('quiz-explanation').style.display = 'block';
            
            // 提出ボタンを無効化
            document.querySelector('.quiz-submit').disabled = true;
        }

        // エラー表示
        function showError(message) {
            const resultsDiv = document.getElementById('search-results');
            resultsDiv.innerHTML = `<div class="error">${message}</div>`;
        }

        // Enterキーで検索
        document.getElementById('search-input').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                performSearch();
            }
        });

        // APIキー入力欄でもEnterキーで検索
        document.getElementById('api-key').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                document.getElementById('search-input').focus();
            }
        });
    </script>
</body>
</html>



# 🔍 検索履歴クイズアプリ

Gemini AIを使用した高機能な検索エンジンと、検索履歴から自動生成されるクイズ機能を備えたWebアプリケーションです。

## ✨ 特徴

- 🤖 **AI検索機能**: Gemini APIを使用した高精度な検索と要約（300文字以内）
- 📚 **検索履歴管理**: 過去の検索結果を自動保存・管理（最大20件）
- 🎯 **AIクイズ生成**: 検索履歴から自動生成される4択問題
- 🎨 **モダンデザイン**: レスポンシブ対応のモダンUI
- 🔒 **セキュア**: APIキーはクライアントサイドでのみ使用

## 🚀 デモ

[ライブデモを見る](https://yourusername.github.io/search-quiz-app/)

## 🛠️ 技術仕様

- **フロントエンド**: HTML5, CSS3, JavaScript (ES6+)
- **AI API**: Google Gemini API
- **ホスティング**: GitHub Pages対応
- **デザイン**: モダンCSS（グラデーション、ガラスモーフィズム）
- **レスポンシブ**: モバイル・タブレット対応

## 📋 機能一覧

### 🔍 検索機能
- Gemini APIを使用したAI検索
- 300文字以内の要約自動生成
- 文字数カウント表示
- 検索結果の全文表示

### 📖 履歴管理
- 検索履歴の自動保存
- 日時付きで最大20件まで保存
- モーダルウィンドウでの詳細表示
- 履歴からの再検索

### 🎯 クイズ機能
- AIによる高品質な4択問題生成
- 検索キーワードを60文字で説明する問題文
- 関連性のあるフェイク選択肢
- 詳細な解説付き

## 🚀 セットアップ

### 1. リポジトリのクローン
```bash
git clone https://github.com/yourusername/search-quiz-app.git
cd search-quiz-app
```

### 2. Gemini APIキーの取得
1. [Google AI Studio](https://aistudio.google.com/app/apikey)にアクセス
2. Googleアカウントでログイン
3. 「Create API Key」をクリック
4. 生成されたAPIキーをコピー

### 3. GitHub Pagesの設定
1. GitHubリポジトリの「Settings」タブに移動
2. 左サイドバーの「Pages」をクリック
3. Source で「Deploy from a branch」を選択
4. Branch で「main」を選択
5. 「Save」をクリック

### 4. アプリの使用
1. デプロイされたURLにアクセス
2. APIキーを入力
3. 検索を開始！

## 💡 使用方法

### 基本的な使い方

1. **APIキーの設定**
   - 検索タブでGemini APIキーを入力
   - APIキーはブラウザセッション中のみ保存

2. **検索の実行**
   - 検索バーにキーワードを入力
   - AIが300文字以内で要約を生成
   - 検索履歴に自動保存

3. **履歴の確認**
   - 履歴タブで過去の検索を一覧表示
   - 項目をクリックで詳細をモーダル表示

4. **クイズに挑戦**
   - クイズタブで自動生成された問題に挑戦
   - 検索キーワードを当てる4択問題
   - 正解後に詳しい解説を表示

### 高度な機能

- **全文表示**: 履歴から検索結果の全文を確認可能
- **文字数管理**: 300文字制限で読みやすい要約
- **問題生成**: 検索キーワードを自然な文章で説明
- **教育的価値**: 学習に適した解説付きクイズ

## 🔒 セキュリティ

### APIキーの保護
- ✅ クライアントサイドでのみ使用
- ✅ GitHub上にAPIキーは保存されない
- ✅ セッション終了時に自動削除
- ✅ パスワード形式での入力

### 安全な使用のために
- 個人のAPIキーのみ使用
- 公共の端末では使用後にブラウザを閉じる
- APIキーの共有は避ける

## 📊 API使用制限

Gemini API（無料プラン）の制限:
- **リクエスト数**: 60回/分
- **文字数**: 32,000文字/リクエスト
- **レスポンス**: 8,192文字まで

詳細は[Gemini API料金](https://ai.google.dev/pricing)を参照してください。


## 🙏 謝辞

- [Google Gemini AI](https://ai.google.dev/) - AI検索機能を提供
- [GitHub Pages](https://pages.github.com/) - 無料ホスティング

## 📈 更新履歴

### v1.0.0 (2024-07-27)
- 初回リリース
- Gemini API検索機能
- 検索履歴管理
- AIクイズ生成機能
- レスポンシブデザイン

---

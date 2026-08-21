import boto3
import botocore
import streamlit as st

# --- ページ設定 ---
st.set_page_config(
    page_title="Bedrockサンプルアプリ",
    page_icon=":smile:",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# --- バージョン確認 ---
st.write("boto3:", boto3.__version__)
st.write("botocore:", botocore.__version__)

# --- UI ---
st.title("Bedrockサンプルアプリ :smile:")
st.write("ナレッジベースに質問して、AIからの回答を受け取りましょう。")

question = st.text_input("質問を入力してください", placeholder="例: AWSとは何ですか？")

# --- ボタン押下時 ---
if st.button("質問する") and question:
    kb = boto3.client("bedrock-agent-runtime", region_name="us-east-1")

    with st.spinner("回答を生成中..."):
        try:
            response = kb.retrieve_and_generate(
                input={"text": question},
                retrieveAndGenerateConfiguration={
                    "type": "KNOWLEDGE_BASE",
                    "knowledgeBaseConfiguration": {
                        "knowledgeBaseId": "NJJWKHHDTQ",
                        "modelArn": "arn:aws:bedrock:us-east-1:959431448750:inference-profile/us.anthropic.claude-sonnet-4-6"
                    }
                }
            )

            st.success("回答が見つかりました！")
            st.write(response["output"]["text"])

            citations = response.get("citations", [])
            if citations:
                with st.expander("参照元を見る"):
                    for citation in citations:
                        for ref in citation.get("retrievedReferences", []):
                            content = ref.get("content", {}).get("text", "")
                            location = ref.get("location", {})
                            st.markdown(f"- {content[:200]}...")
                            st.caption(f"出典: {location}")

        except botocore.exceptions.ClientError as e:
            error_code = e.response.get("Error", {}).get("Code", "Unknown")
            error_message = e.response.get("Error", {}).get("Message", str(e))
            st.error(f"エラーが発生しました [{error_code}]: {error_message}")

        except Exception as e:
            st.error(f"予期しないエラーが発生しました: {e}")

# --- フッター ---
st.markdown(
    """
    <hr>
    <footer style="text-align: center;">
        <p>© 2024 CloudTech</p>
    </footer>
    """,
    unsafe_allow_html=True,
)

import os
import requests
import json
import base64
from flask import Flask, request, jsonify, render_template, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__, template_folder='templates', static_folder='static')


# DeepSeek API配置
DEEPSEEK_API_KEY = "sk-4ebf195cf11a4c17a407c6346fd4e2c8"  # 替换为你的DeepSeek API密钥
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"  # DeepSeek API的URL

# 简短提示词(可按需修改)
SYSTEM_PROMPT = "你是临床辅助撰写助手。只基于提供的病历文本给出结构化输出，语气专业、简洁，加入病人身份信息。同时，加上报告生成日期"
USER_PROMPT = ("请提取:"
    "1. 第一部分:患者姓名、性别、年龄、与核心病史：主宿、现病历、重要既往史(以医学报告风格写出患者基本资料与病史摘要。) "
    "2. 第二部分:诊断、分期与病理学特征"
    "按表格显示分子病理(Gene / Variant / Abundance / Clinical Significance)，"
    "对分期、诊断重点进行专业总结，对病理解读保持中立客观。"
    "3. 第三部分:治疗经过与疗效评估，使用表格呈现影像学动态，"
    "必须给出整体疗效总结(总体趋势、反应类型、关键转折点)。"
    "4. 第四部分:预后评估与未来规划，包括:复发风险分层、"
    "核心治疗建议(依据 NCCN/CSCO/ESMO 等指南，不需引用文献但需保持专业合理)、"
    "随访计划(影像+实验室)。"
    "并返回一个拥有报告可读性的markdown格式文本。"
    " 病历/问题:{text}  ---END---"
)


@app.route('/')
def index():
    """渲染主页"""
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    """处理聊天请求并调用DeepSeek API"""
    try:
        data = request.json
        user_message = data.get('message', '')
        
        if not user_message:
            return jsonify({"error": "消息不能为空"}), 400
        
        # 调用DeepSeek API
        response = call_deepseek_api(user_message)
        
        return jsonify({"response": response})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def call_deepseek_api(message):
    """调用DeepSeek API并返回响应"""
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}"
    }
    user_content = USER_PROMPT.format(text=message)
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_content}
    ]
    payload = {
        "model": "deepseek-chat",  # 使用的模型，根据DeepSeek API文档调整
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 1000
    }
    
    try:
        response = requests.post(DEEPSEEK_API_URL, headers=headers, json=payload)
        response.raise_for_status()  # 如果请求失败，抛出异常
        
        result = response.json()
        # 根据DeepSeek API的响应格式提取回复内容
        assistant_message = result.get('choices', [{}])[0].get('message', {}).get('content', '')
        
        return assistant_message
    
    except requests.exceptions.RequestException as e:
        print(f"API请求错误: {e}")
        return f"API请求错误: {e}"

if __name__ == '__main__':
    # 确保templates目录存在
    os.makedirs('templates', exist_ok=True)
    # 确保static目录存在
    os.makedirs('static', exist_ok=True)
    
    # 启动Flask应用
    app.run(host='0.0.0.0', port=5000, debug=True)
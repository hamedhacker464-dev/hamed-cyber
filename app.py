import socket
import hashlib
import random
import base64
import uuid
import requests
import re
import urllib.parse
import string
import json
from flask import Flask, render_template_string, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)
limiter = Limiter(get_remote_address, app=app, default_limits=["60 per minute"], storage_uri="memory://")

# --- هوش مصنوعی پیشرفته (منطق پاسخگویی) ---
def ai_respond(text):
    text = text.lower()
    
    if any(word in text for word in ["پایتون", "python"]): 
        return "پایتون (Python) یه زبان فوق‌العاده برای هک و امنیته. برای شروع، کتابخونه‌های `requests` و `socket` رو یاد بگیر. من خودم با همینا نوشته شدم! 🐍"
    if any(word in text for word in ["هک", "hack", "نفوذ"]): 
        return "هک فقط کد زدن نیست، هنر فکر کردنه! همیشه از سیستم‌های خودت برای تست (مثل TryHackMe) استفاده کن و قوانین رو رعایت کن. 🤫"
    if any(word in text for word in ["ddos", "دیزاس", "د دیداس"]): 
        return "حمله DDoS از کار انداختن سرویسه. برای یادگیری می‌تونی تو محیط‌های شبیه‌سازی شده تمرین کنی، ولی استفاده ازش روی سایت دیگران غیرقانونیه! ⚠️"
    if any(word in text for word in ["سلام", "درود", "hi", "hello"]): 
        return "سلام رفیق! من دستیار هوشمند تیم حامد هستم. چه خبر؟ چطور می‌تونم کمکت کنم؟ 🦅"
    if any(word in text for word in ["شوخی", "بخند", "جوک"]): 
        return random.choice([
            "یه بار یه هکر به دوستش گفت: من عاشق زندگیم. دوستش گفت چرا؟ گفت چون پسورد همه چیز رو دارم! 😂",
            "می‌دونی چرا برنامه‌نویس‌ها عینک می‌زنن؟ چون نمی‌خوان C# (سی‌شارپ) رو با C (سی) اشتباه بگیرن! 😎",
            "فرق بین هکر و برنامه‌نویس چیه؟ هکر کد می‌زنه که خرابکاری کنه، برنامه‌نویس کد می‌زنه که خرابکاری نکنه (ولی می‌کنه)! 💻"
        ])
    if any(word in text for word in ["خوبی", "چطوری", "حالت"]): 
        return "من که همیشه تو دنیای مجازی سرحالم! تو چطوری Kovak؟ چه خبر از پروژه‌های هکریت؟ ⚡"
    
    return "من یه هوش مصنوعی سایبری‌ام و هنوز دارم یاد می‌گیرم. می‌تونی درباره هک، برنامه‌نویسی، امنیت یا شوخی ازم بپرسی! 🦾"

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hamed Cyber Ops | Ultimate Arsenal</title>
    <link href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300;400;700;900&family=Share+Tech+Mono&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-dark: #02050a;
            --neon-cyan: #00f3ff;
            --neon-purple: #b026ff;
            --neon-red: #ff003c;
            --glass-bg: rgba(5, 12, 20, 0.85);
            --glass-border: rgba(0, 243, 255, 0.2);
            --text-main: #e0e0e0;
            --text-muted: #8892b0;
        }
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            background-color: var(--bg-dark);
            background-image: linear-gradient(rgba(255, 0, 60, 0.03) 1px, transparent 1px), linear-gradient(90deg, rgba(255, 0, 60, 0.03) 1px, transparent 1px);
            background-size: 30px 30px;
            color: var(--text-main);
            font-family: 'Vazirmatn', sans-serif;
            min-height: 100vh;
        }
        header { display: flex; justify-content: space-between; align-items: center; padding: 15px 25px; background: rgba(2, 5, 10, 0.95); border-bottom: 1px solid var(--glass-border); backdrop-filter: blur(10px); position: sticky; top: 0; z-index: 100; }
        .logo-container { display: flex; align-items: center; gap: 12px; }
        .logo-icon { width: 35px; height: 35px; border: 2px solid var(--neon-red); border-radius: 50%; display: flex; justify-content: center; align-items: center; box-shadow: 0 0 15px var(--neon-red); }
        .logo-icon::after { content: '☠'; font-size: 1.2rem; color: var(--neon-red); }
        header h1 { font-size: 1.1rem; color: var(--neon-red); font-family: 'Share Tech Mono', monospace; letter-spacing: 2px; text-shadow: 0 0 10px var(--neon-red);}
        
        .main-container { max-width: 1100px; margin: 0 auto; padding: 20px; }
        .glass-card { background: var(--glass-bg); border: 1px solid var(--glass-border); border-radius: 12px; padding: 25px; margin-bottom: 25px; backdrop-filter: blur(10px); box-shadow: 0 10px 30px rgba(0,0,0,0.6); }
        
        .hero-section { text-align: center; padding: 30px 20px; }
        .hero-section h2 { font-size: 2.2rem; background: linear-gradient(90deg, var(--neon-red), var(--neon-purple)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 10px; font-weight: 900; }
        .hero-section p { color: var(--text-muted); line-height: 1.8; font-size: 0.95rem; }
        
        .section-title { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; color: var(--neon-cyan); font-size: 1.3rem; border-bottom: 1px solid rgba(0,243,255,0.2); padding-bottom: 10px; }

        /* کارهایی که انجام دادم */
        .work-list { display: flex; flex-direction: column; gap: 12px; }
        .work-item { background: rgba(0,0,0,0.5); border-radius: 8px; padding: 15px; border-right: 3px solid var(--neon-purple); transition: 0.3s; }
        .work-item:hover { background: rgba(176, 38, 255, 0.05); transform: translateX(-5px); }
        .work-item h5 { color: #fff; margin-bottom: 5px; font-size: 1.1rem; }
        .work-item p { color: var(--text-muted); font-size: 0.9rem; line-height: 1.6; }

        /* ابزارهای کاربردی */
        .tools-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 15px; }
        .tool-box { background: rgba(0,0,0,0.6); border: 1px solid rgba(255,0,60,0.2); border-radius: 8px; padding: 15px; transition: 0.3s; }
        .tool-box:hover { border-color: var(--neon-cyan); box-shadow: 0 0 15px rgba(0, 243, 255, 0.2); }
        .tool-box h4 { color: var(--neon-red); margin-bottom: 15px; font-family: 'Share Tech Mono', monospace; font-size: 0.95rem;}
        .input-group { display: flex; gap: 10px; margin-bottom: 15px; flex-wrap: wrap; }
        .input-group input { flex: 1; padding: 10px; background: #000; border: 1px solid var(--glass-border); color: #fff; border-radius: 5px; font-family: inherit; outline: none; font-size: 0.85rem;}
        .input-group button { padding: 10px 15px; background: var(--neon-red); color: #fff; border: none; border-radius: 5px; cursor: pointer; font-weight: bold; font-family: inherit; font-size: 0.85rem; transition: 0.3s;}
        .input-group button:hover { background: #fff; color: #000; box-shadow: 0 0 15px var(--neon-red); }
        .result-box { background: #000; padding: 10px; border-radius: 5px; font-family: inherit; color: var(--neon-cyan); min-height: 40px; font-size: 0.9rem; display: none; white-space: pre-wrap; direction: rtl; text-align: right; border-right: 2px solid var(--neon-red); }
        
        /* چت هوش مصنوعی (طراحی جدید و خفن) */
        .ai-container {
            background: rgba(0, 0, 0, 0.8);
            border: 1px solid rgba(0, 243, 255, 0.3);
            border-radius: 15px;
            overflow: hidden;
            box-shadow: 0 0 30px rgba(0, 243, 255, 0.15);
            display: flex;
            flex-direction: column;
            height: 450px;
            position: relative;
        }
        .ai-header {
            background: linear-gradient(90deg, rgba(0, 243, 255, 0.1), rgba(176, 38, 255, 0.1));
            padding: 15px 20px;
            border-bottom: 1px solid rgba(0, 243, 255, 0.2);
            display: flex;
            align-items: center;
            gap: 15px;
        }
        .ai-avatar {
            width: 40px; height: 40px;
            background: radial-gradient(circle, var(--neon-cyan), var(--neon-purple));
            border-radius: 50%;
            display: flex; justify-content: center; align-items: center;
            font-size: 1.2rem;
            box-shadow: 0 0 15px var(--neon-cyan);
            animation: pulse 2s infinite;
        }
        @keyframes pulse {
            0% { box-shadow: 0 0 15px var(--neon-cyan); }
            50% { box-shadow: 0 0 30px var(--neon-purple); }
            100% { box-shadow: 0 0 15px var(--neon-cyan); }
        }
        .ai-header h4 { color: #fff; font-size: 1.1rem; font-family: 'Share Tech Mono', monospace; }
        .ai-header p { color: var(--neon-cyan); font-size: 0.75rem; margin-top: 3px; }
        
        .ai-chat-box {
            flex: 1;
            padding: 20px;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 15px;
            scroll-behavior: smooth;
        }
        
        .chat-msg {
            padding: 12px 18px;
            border-radius: 15px;
            max-width: 85%;
            font-size: 0.95rem;
            line-height: 1.6;
            position: relative;
            animation: fadeIn 0.3s ease;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .chat-msg.user {
            background: linear-gradient(135deg, var(--neon-purple), #7a00cc);
            color: #fff;
            align-self: flex-end;
            border-bottom-right-radius: 2px;
            box-shadow: 0 5px 15px rgba(176, 38, 255, 0.3);
        }
        
        .chat-msg.bot {
            background: rgba(0, 243, 255, 0.05);
            color: var(--text-main);
            border: 1px solid rgba(0, 243, 255, 0.2);
            align-self: flex-start;
            border-bottom-left-radius: 2px;
            box-shadow: 0 5px 15px rgba(0, 243, 255, 0.1);
        }
        
        .chat-input-area {
            display: flex;
            padding: 15px;
            background: rgba(0, 0, 0, 0.5);
            border-top: 1px solid rgba(0, 243, 255, 0.1);
            gap: 10px;
        }
        .chat-input-area input {
            flex: 1;
            padding: 12px 20px;
            background: #000;
            border: 1px solid var(--glass-border);
            color: #fff;
            border-radius: 25px;
            outline: none;
            font-family: inherit;
            font-size: 0.95rem;
            transition: 0.3s;
        }
        .chat-input-area input:focus {
            border-color: var(--neon-cyan);
            box-shadow: 0 0 10px rgba(0, 243, 255, 0.3);
        }
        .chat-input-area button {
            padding: 12px 25px;
            background: var(--neon-cyan);
            color: #000;
            border: none;
            border-radius: 25px;
            cursor: pointer;
            font-weight: bold;
            font-family: inherit;
            transition: 0.3s;
        }
        .chat-input-area button:hover {
            box-shadow: 0 0 20px var(--neon-cyan);
            transform: scale(1.05);
        }
        
        /* تایپینگ افکت */
        .typing-indicator {
            display: inline-block;
            width: 5px; height: 15px;
            background: var(--neon-cyan);
            animation: blink 1s infinite;
            vertical-align: middle;
            margin-right: 5px;
        }
        @keyframes blink { 50% { opacity: 0; } }

        .tg-box { text-align: center; }
        .btn-tg { display: inline-block; background: var(--neon-cyan); color: #000; padding: 12px 30px; border-radius: 8px; text-decoration: none; font-weight: bold; box-shadow: 0 0 15px rgba(0, 243, 255, 0.4); margin-top: 15px; }
        .team-footer { text-align: center; font-family: 'Share Tech Mono', monospace; color: var(--text-muted); font-size: 0.8rem; padding: 30px 0; line-height: 2; border-top: 1px solid rgba(255,255,255,0.05); }
    </style>
</head>
<body>
    <header><div class="logo-container"><div class="logo-icon"></div><h1>HAMED_OPS // BLACK_HAT</h1></div></header>
    <div class="main-container">
        <div class="glass-card hero-section">
            <h2>حامد (Hamed)</h2>
            <p style="color: var(--neon-red); font-weight: bold; margin-bottom: 15px; text-shadow: 0 0 10px var(--neon-red);">هکر کلاه سیاه (Black Hat) ۱۷ ساله</p>
            <p>بنیان‌گذار HamedCyberTeam — بدون محدودیت، بدون قانون.</p>
        </div>

        <!-- هوش مصنوعی پیشرفته -->
        <div class="glass-card" style="padding: 0; overflow: hidden; border: none; background: transparent; box-shadow: none;">
            <div class="ai-container">
                <div class="ai-header">
                    <div class="ai-avatar">🤖</div>
                    <div>
                        <h4>Hamed AI Assistant</h4>
                        <p>● آنلاین | نسخه سایبری</p>
                    </div>
                </div>
                <div class="ai-chat-box" id="chat-box">
                    <div class="chat-msg bot">سیستم راه‌اندازی شد. سلام حامد! من دستیار هوشمند تو هستم. می‌تونم درباره هک، امنیت و برنامه‌نویسی باهات حرف بزنم. چی می‌خوای بدونی؟</div>
                </div>
                <div class="chat-input-area">
                    <input type="text" id="chat-input" placeholder="پیام خود را وارد کنید..." onkeypress="if(event.key==='Enter') sendChat()">
                    <button onclick="sendChat()">ارسال ➤</button>
                </div>
            </div>
        </div>

        <!-- کارهایی که انجام دادم -->
        <div class="glass-card">
            <h3 class="section-title"><span>🏆 کارهایی که انجام دادم</span></h3>
            <div class="work-list">
                <div class="work-item">
                    <h5>نفوذ به سیستم‌های ابری (Cloud Breach)</h5>
                    <p>بایپس فایروال‌های سطح بالا و استخراج دیتابیس ۱۵ میلیون کاربر بدون بر جای گذاشتن هیچ ردپایی. (عملیات مخفی)</p>
                </div>
                <div class="work-item">
                    <h5>حمله DDoS ویرانگر (Multi-Vector)</h5>
                    <p>ارسال ۱.۵ میلیون پکت در ثانیه به سرورهای هدف و از کار انداختن کامل CDN آن‌ها.</p>
                </div>
                <div class="work-item">
                    <h5>کشف باگ Zero-Day در هسته لینوکس</h5>
                    <p>پیدا کردن آسیب‌پذیری روز صفر (RCE) و اخذ دسترسی کامل Root به سرورهای مرکزی.</p>
                </div>
                <div class="work-item">
                    <h5>کرک هش‌های NTLM با خوشه GPU</h5>
                    <p>بازگردانی ۲ میلیون پسورد پیچیده با استفاده از Rainbow Table و قدرت پردازش گرافیکی.</p>
                </div>
            </div>
        </div>

        <!-- ابزارهای کاربردی -->
        <div class="glass-card">
            <h3 class="section-title"><span>🧰 ابزارهای کاربردی</span></h3>
            <div class="tools-grid">
                <div class="tool-box"><h4>> اسکنر پورت</h4><div class="input-group"><input type="text" id="scan-ip" placeholder="IP/Domain" value="scanme.nmap.org"><button onclick="runTool('scan')">اسکن</button></div><div class="result-box" id="res-scan"></div></div>
                <div class="tool-box"><h4>> اطلاعات آی‌پی</h4><div class="input-group"><input type="text" id="ip-info" placeholder="IP" value="8.8.8.8"><button onclick="runTool('ipinfo')">بگیر</button></div><div class="result-box" id="res-ipinfo"></div></div>
                <div class="tool-box"><h4>> ساخت هش</h4><div class="input-group"><input type="text" id="hash-text" placeholder="متن" value="Hamed123"><button onclick="runTool('hash')">هش کن</button></div><div class="result-box" id="res-hash"></div></div>
                <div class="tool-box"><h4>> اسکن زیردامنه</h4><div class="input-group"><input type="text" id="sub-domain" placeholder="Domain" value="google.com"><button onclick="runTool('subdomain')">اسکن</button></div><div class="result-box" id="res-subdomain"></div></div>
                <div class="tool-box"><h4>> مولد رمز عبور</h4><div class="input-group"><input type="number" id="pass-len" placeholder="طول" value="16"><button onclick="runTool('genpass')">تولید</button></div><div class="result-box" id="res-genpass"></div></div>
                <div class="tool-box"><h4>> بررسی وضعیت سایت</h4><div class="input-group"><input type="text" id="url-check" placeholder="https://example.com" value="https://google.com"><button onclick="runTool('urlcheck')">بررسی</button></div><div class="result-box" id="res-urlcheck"></div></div>
            </div>
        </div>

        <div class="glass-card tg-box">
            <h3>عضویت در کانال تلگرام</h3>
            <p style="color: var(--neon-cyan); font-family: monospace; margin: 10px 0;">T.me/HamedHacksDB</p>
            <a href="https://t.me/+TSrDJ-VSRs43YjY0" target="_blank" class="btn-tg">عضویت در کانال امن</a>
        </div>

        <div class="team-footer">
            <p>☠ تیم سایبری هکری حامد | HamedCyberTeam ☠</p>
            <p>╔═══════════✦═══════════╗</p>
            <p>💎 خانواده رسمی حامد 💎</p>
            <p>╚═══════════✦═══════════╝</p>
        </div>
    </div>

    <script>
        async function sendChat() {
            let input = document.getElementById('chat-input');
            let text = input.value.trim();
            if(!text) return;
            
            let chatBox = document.getElementById('chat-box');
            // پیام کاربر
            chatBox.innerHTML += `<div class="chat-msg user">${text}</div>`;
            input.value = '';
            chatBox.scrollTop = chatBox.scrollHeight;

            // افکت تایپ
            let typingId = 'typing-' + Date.now();
            chatBox.innerHTML += `<div class="chat-msg bot" id="${typingId}"><span class="typing-indicator"></span> در حال پردازش...</div>`;
            chatBox.scrollTop = chatBox.scrollHeight;

            try {
                let response = await fetch('/api/ai', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({text: text})
                });
                let data = await response.json();
                
                // حذف افکت تایپ و نمایش جواب
                document.getElementById(typingId).remove();
                chatBox.innerHTML += `<div class="chat-msg bot">${data.reply}</div>`;
                chatBox.scrollTop = chatBox.scrollHeight;
            } catch(e) {
                document.getElementById(typingId).innerText = "خطا در برقراری ارتباط با سرور.";
            }
        }

        async function runTool(type) {
            let url = '/api/' + type;
            let body = {};
            if(type === 'scan') { body = {target: document.getElementById('scan-ip').value}; document.getElementById('res-scan').style.display='block'; document.getElementById('res-scan').innerText="در حال اسکن..."; }
            else if(type === 'ipinfo') { body = {ip: document.getElementById('ip-info').value}; document.getElementById('res-ipinfo').style.display='block'; document.getElementById('res-ipinfo').innerText="در حال دریافت..."; }
            else if(type === 'hash') { body = {text: document.getElementById('hash-text').value}; document.getElementById('res-hash').style.display='block'; }
            else if(type === 'subdomain') { body = {domain: document.getElementById('sub-domain').value}; document.getElementById('res-subdomain').style.display='block'; document.getElementById('res-subdomain').innerText="در حال اسکن..."; }
            else if(type === 'genpass') { body = {len: document.getElementById('pass-len').value}; document.getElementById('res-genpass').style.display='block'; }
            else if(type === 'urlcheck') { body = {url: document.getElementById('url-check').value}; document.getElementById('res-urlcheck').style.display='block'; document.getElementById('res-urlcheck').innerText="در حال بررسی..."; }

            try {
                let response = await fetch(url, { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(body) });
                let data = await response.json();
                let resId = 'res-' + type;
                if(type === 'subdomain') resId = 'res-subdomain';
                if(type === 'genpass') resId = 'res-genpass';
                if(type === 'urlcheck') resId = 'res-urlcheck';
                document.getElementById(resId).innerText = data.result;
            } catch(e) { alert("خطا در اجرای ابزار"); }
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home(): return render_template_string(HTML_TEMPLATE)

# --- API های هوش مصنوعی و ابزارها ---
@app.route('/api/ai', methods=['POST'])
def api_ai():
    text = request.json.get('text', '')
    return jsonify({"reply": ai_respond(text)})

@app.route('/api/scan', methods=['POST'])
def api_scan():
    target = request.json.get('target')
    result = f"هدف: {target}\\n"
    try:
        ip = socket.gethostbyname(target)
        result += f"آی‌پی: {ip}\\n\\n"
        for port in [21, 22, 23, 25, 53, 80, 110, 443, 445, 3306, 8080]:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.5)
            if s.connect_ex((ip, port)) == 0: result += f"پورت {port}: باز است\\n"
            s.close()
    except Exception as e: result += f"خطا: {str(e)}"
    return jsonify({"result": result})

@app.route('/api/ipinfo', methods=['POST'])
def api_ipinfo():
    ip = request.json.get('ip')
    try:
        data = requests.get(f"http://ip-api.com/json/{ip}?fields=status,country,city,isp,org,query", timeout=5).json()
        if data.get('status') == 'success':
            return jsonify({"result": f"آی‌پی: {data['query']}\\nکشور: {data['country']}\\nشهر: {data['city']}\\nسازمان: {data.get('org', data.get('isp'))}"})
        return jsonify({"result": "آی‌پی نامعتبر."})
    except Exception as e: return jsonify({"result": f"خطا: {str(e)}"})

@app.route('/api/hash', methods=['POST'])
def api_hash():
    text = request.json.get('text').encode('utf-8')
    return jsonify({"result": f"MD5:\\n{hashlib.md5(text).hexdigest()}\\n\\nSHA256:\\n{hashlib.sha256(text).hexdigest()}"})

@app.route('/api/subdomain', methods=['POST'])
def api_subdomain():
    domain = request.json.get('domain')
    found = []
    for sub in ['www', 'mail', 'ftp', 'admin', 'blog', 'api', 'dev', 'test']:
        try:
            socket.gethostbyname(f"{sub}.{domain}")
            found.append(f"{sub}.{domain}")
        except: pass
    if found: return jsonify({"result": "زیردامنه‌های پیدا شده:\\n" + "\\n".join(found)})
    return jsonify({"result": "هیچ زیردامنه‌ای پیدا نشد."})

@app.route('/api/genpass', methods=['POST'])
def api_genpass():
    length = int(request.json.get('len', 16))
    if length > 50: length = 50
    chars = string.ascii_letters + string.digits + "!@#$%^&*"
    return jsonify({"result": f"رمز عبور:\\n{''.join(random.choice(chars) for _ in range(length))}"})

@app.route('/api/urlcheck', methods=['POST'])
def api_urlcheck():
    url = request.json.get('url')
    try:
        r = requests.head(url, timeout=5, allow_redirects=True)
        return jsonify({"result": f"کد وضعیت: {r.status_code}\\nسرور: {r.headers.get('Server', 'ناشناخته')}"})
    except Exception as e: return jsonify({"result": f"خطا: {str(e)}"})

@app.errorhandler(429)
def ratelimit_handler(e):
    return "429 Too Many Requests", 429

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)

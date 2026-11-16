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
import ssl
import time
import datetime
import ipaddress
import logging
from flask import Flask, render_template_string, request, jsonify, abort
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - SECURITY_LOG - %(message)s')
BLACKLISTED_IPS = {}
BAN_TIME = 3600 

limiter = Limiter(get_remote_address, app=app, default_limits=["60 per minute", "1000 per day"], storage_uri="memory://")

@app.after_request
def add_security_headers(response):
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['Content-Security-Policy'] = "default-src 'self' 'unsafe-inline' https://fonts.googleapis.com https://fonts.gstatic.com; frame-ancestors 'none'; object-src 'none'; base-uri 'self';"
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains; preload'
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    response.headers['Permissions-Policy'] = "camera=(), microphone=(), geolocation=(), payment=()"
    response.headers['Server'] = 'Secure-Web-Gateway-2.0'
    return response

@app.before_request
def advanced_waf():
    client_ip = get_remote_address()
    now = time.time()

    if client_ip in BLACKLISTED_IPS:
        if now < BLACKLISTED_IPS[client_ip]:
            abort(403) 
        else:
            del BLACKLISTED_IPS[client_ip]

    bad_paths = ['/wp-admin', '/.env', '/config', '/phpmyadmin', '/.git', '/etc/passwd', '/../../']
    if any(path in request.path.lower() for path in bad_paths):
        logging.warning(f"Attack Blocked: Bad Path from {client_ip}")
        abort(403)

    try:
        payload = request.get_data(as_text=True).lower()
        attack_patterns = [
            r"union\s+select", r"or\s+1\s*=\s*1", r"drop\s+table", r"information_schema",
            r"<script", r"javascript:", r"onerror=", r"onload=", r"alert\(",
            r";\s*cat\s+", r"\|\s*bash", r"&\s*whoami", r"\.\./", r"/etc/passwd",
            r"sleep\(", r"benchmark\(", r"pg_sleep", r"waitfor\s+delay"
        ]
        for pattern in attack_patterns:
            if re.search(pattern, payload):
                logging.warning(f"WAF BLOCKED: Payload '{pattern}' from {client_ip}")
                BLACKLISTED_IPS[client_ip] = now + BAN_TIME
                abort(403)
    except Exception:
        pass

def is_internal_ip(hostname):
    try:
        ip_str = socket.gethostbyname(hostname)
        ip = ipaddress.ip_address(ip_str)
        if ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_reserved or ip.is_multicast:
            return True
        return False
    except Exception:
        return True

def validate_input(data, key, max_len=500):
    if not isinstance(data, dict) or key not in data: return None
    val = data[key]
    if not isinstance(val, str) or len(val) > max_len: return None
    clean_val = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', val)
    return clean_val.strip()

def ai_respond(text):
    text = text.lower()
    if any(word in text for word in ["پایتون", "python"]): return "پایتون عالیه برای هک. `requests` و `socket` یاد بگیر."
    if any(word in text for word in ["هک", "hack"]): return "هک هنر فکر کردنه! همیشه از سیستم‌های خودت تست بگیر."
    if any(word in text for word in ["سلام", "درود"]): return "سلام رفیق! چطور می‌تونم کمکت کنم؟"
    if any(word in text for word in ["شوخی", "بخند"]): return random.choice(["هکر به دوستش گفت: پسورد همه چیز رو دارم! 😂", "برنامه‌نویس‌ها عینک می‌زنن تا C# رو با C اشتباه نگیرن! 😎"])
    return "من دستیار هوشمند سایبری‌ام. درباره هک، برنامه‌نویسی یا شوخی بپرس!"

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
            --bg-dark: #02050a; --neon-cyan: #00f3ff; --neon-purple: #b026ff; --neon-red: #ff003c;
            --glass-bg: rgba(5, 12, 20, 0.85); --glass-border: rgba(0, 243, 255, 0.2);
            --text-main: #e0e0e0; --text-muted: #8892b0;
        }
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { background-color: var(--bg-dark); background-image: linear-gradient(rgba(255, 0, 60, 0.03) 1px, transparent 1px), linear-gradient(90deg, rgba(255, 0, 60, 0.03) 1px, transparent 1px); background-size: 30px 30px; color: var(--text-main); font-family: 'Vazirmatn', sans-serif; min-height: 100vh; }
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
        
        .work-list { display: flex; flex-direction: column; gap: 12px; }
        .work-item { background: rgba(0,0,0,0.5); border-radius: 8px; padding: 15px; border-right: 3px solid var(--neon-purple); transition: 0.3s; }
        .work-item:hover { background: rgba(176, 38, 255, 0.05); transform: translateX(-5px); }
        .work-item h5 { color: #fff; margin-bottom: 5px; font-size: 1.1rem; }
        .work-item p { color: var(--text-muted); font-size: 0.9rem; line-height: 1.6; }

        .ai-container { background: rgba(0, 0, 0, 0.8); border: 1px solid rgba(0, 243, 255, 0.3); border-radius: 15px; overflow: hidden; box-shadow: 0 0 30px rgba(0, 243, 255, 0.15); display: flex; flex-direction: column; height: 400px; }
        .ai-header { background: linear-gradient(90deg, rgba(0, 243, 255, 0.1), rgba(176, 38, 255, 0.1)); padding: 15px 20px; border-bottom: 1px solid rgba(0, 243, 255, 0.2); display: flex; align-items: center; gap: 15px; }
        .ai-avatar { width: 40px; height: 40px; background: radial-gradient(circle, var(--neon-cyan), var(--neon-purple)); border-radius: 50%; display: flex; justify-content: center; align-items: center; font-size: 1.2rem; box-shadow: 0 0 15px var(--neon-cyan); animation: pulse 2s infinite; }
        @keyframes pulse { 0% { box-shadow: 0 0 15px var(--neon-cyan); } 50% { box-shadow: 0 0 30px var(--neon-purple); } 100% { box-shadow: 0 0 15px var(--neon-cyan); } }
        .ai-header h4 { color: #fff; font-size: 1.1rem; font-family: 'Share Tech Mono', monospace; }
        .ai-header p { color: var(--neon-cyan); font-size: 0.75rem; margin-top: 3px; }
        .ai-chat-box { flex: 1; padding: 20px; overflow-y: auto; display: flex; flex-direction: column; gap: 15px; scroll-behavior: smooth; }
        .chat-msg { padding: 12px 18px; border-radius: 15px; max-width: 85%; font-size: 0.95rem; line-height: 1.6; animation: fadeIn 0.3s ease; }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
        .chat-msg.user { background: linear-gradient(135deg, var(--neon-purple), #7a00cc); color: #fff; align-self: flex-end; border-bottom-right-radius: 2px; }
        .chat-msg.bot { background: rgba(0, 243, 255, 0.05); color: var(--text-main); border: 1px solid rgba(0, 243, 255, 0.2); align-self: flex-start; border-bottom-left-radius: 2px; }
        .chat-input-area { display: flex; padding: 15px; background: rgba(0, 0, 0, 0.5); border-top: 1px solid rgba(0, 243, 255, 0.1); gap: 10px; }
        .chat-input-area input { flex: 1; padding: 12px 20px; background: #000; border: 1px solid var(--glass-border); color: #fff; border-radius: 25px; outline: none; font-family: inherit; }
        .chat-input-area button { padding: 12px 25px; background: var(--neon-cyan); color: #000; border: none; border-radius: 25px; cursor: pointer; font-weight: bold; font-family: inherit; transition: 0.3s; }
        .chat-input-area button:hover { box-shadow: 0 0 20px var(--neon-cyan); transform: scale(1.05); }
        
        .tools-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 15px; }
        .tool-box { background: rgba(0,0,0,0.6); border: 1px solid rgba(255,0,60,0.2); border-radius: 8px; padding: 15px; transition: 0.3s; }
        .tool-box:hover { border-color: var(--neon-cyan); box-shadow: 0 0 15px rgba(0, 243, 255, 0.2); }
        .tool-box h4 { color: var(--neon-red); margin-bottom: 15px; font-family: 'Share Tech Mono', monospace; font-size: 0.95rem;}
        .input-group { display: flex; gap: 10px; margin-bottom: 15px; flex-wrap: wrap; }
        .input-group input { flex: 1; padding: 10px; background: #000; border: 1px solid var(--glass-border); color: #fff; border-radius: 5px; font-family: inherit; outline: none; font-size: 0.85rem;}
        .input-group button { padding: 10px 15px; background: var(--neon-red); color: #fff; border: none; border-radius: 5px; cursor: pointer; font-weight: bold; font-family: inherit; font-size: 0.85rem; transition: 0.3s;}
        .input-group button:hover { background: #fff; color: #000; box-shadow: 0 0 15px var(--neon-red); }
        .result-box { background: #000; padding: 10px; border-radius: 5px; font-family: inherit; color: var(--neon-cyan); min-height: 40px; font-size: 0.85rem; display: none; white-space: pre-wrap; direction: ltr; text-align: left; border-left: 2px solid var(--neon-red); }

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

        <div class="glass-card" style="padding: 0; overflow: hidden; border: none; background: transparent; box-shadow: none;">
            <div class="ai-container">
                <div class="ai-header">
                    <div class="ai-avatar">🤖</div>
                    <div><h4>Hamed AI Assistant</h4><p>● آنلاین | نسخه سایبری</p></div>
                </div>
                <div class="ai-chat-box" id="chat-box">
                    <div class="chat-msg bot">سیستم راه‌اندازی شد. سلام حامد! من دستیار هوشمند تو هستم. درباره هک، امنیت یا برنامه‌نویسی بپرس!</div>
                </div>
                <div class="chat-input-area">
                    <input type="text" id="chat-input" placeholder="پیام خود را وارد کنید..." onkeypress="if(event.key==='Enter') sendChat()">
                    <button onclick="sendChat()">ارسال ➤</button>
                </div>
            </div>
        </div>

        <div class="glass-card">
            <h3 class="section-title"><span>🏆 کارهایی که انجام دادم (۱۰ عملیات برتر)</span></h3>
            <div class="work-list">
                <div class="work-item"><h5>۱. نفوذ به سیستم‌های ابری (AWS/Azure)</h5><p>بایپس فایروال‌های سطح بالا و استخراج دیتابیس ۱۵ میلیون کاربر بدون ردپا.</p></div>
                <div class="work-item"><h5>۲. حمله DDoS ویرانگر (Multi-Vector)</h5><p>ارسال ۱.۵ میلیون پکت در ثانیه و از کار انداختن کامل CDN سرورهای هدف.</p></div>
                <div class="work-item"><h5>۳. کشف باگ Zero-Day در هسته لینوکس</h5><p>پیدا کردن آسیب‌پذیری روز صفر (RCE) و اخذ دسترسی کامل Root.</p></div>
                <div class="work-item"><h5>۴. کرک هش‌های NTLM با خوشه GPU</h5><p>بازگردانی ۲ میلیون پسورد پیچیده با Rainbow Table.</p></div>
                <div class="work-item"><h5>۵. نفوذ به سیستم‌های SCADA (کنترل صنعتی)</h5><p>دسترسی به پنل‌های PLC نیروگاه‌ها و زیرساخت‌های حساس.</p></div>
            </div>
        </div>

        <div class="glass-card">
            <h3 class="section-title"><span>🧰 ۳۰ ابزار کاربردی و زنده</span></h3>
            <div class="tools-grid">
                <div class="tool-box"><h4>> اسکنر پورت</h4><div class="input-group"><input type="text" id="scan-ip" placeholder="IP" value="scanme.nmap.org"><button onclick="runTool('scan')">اسکن</button></div><div class="result-box" id="res-scan"></div></div>
                <div class="tool-box"><h4>> اطلاعات آی‌پی</h4><div class="input-group"><input type="text" id="ip-info" placeholder="IP" value="8.8.8.8"><button onclick="runTool('ipinfo')">بگیر</button></div><div class="result-box" id="res-ipinfo"></div></div>
                <div class="tool-box"><h4>> ساخت هش</h4><div class="input-group"><input type="text" id="hash-text" placeholder="متن" value="Hamed123"><button onclick="runTool('hash')">هش کن</button></div><div class="result-box" id="res-hash"></div></div>
                <div class="tool-box"><h4>> اسکن زیردامنه</h4><div class="input-group"><input type="text" id="sub-domain" placeholder="Domain" value="google.com"><button onclick="runTool('subdomain')">اسکن</button></div><div class="result-box" id="res-subdomain"></div></div>
                <div class="tool-box"><h4>> مولد رمز عبور</h4><div class="input-group"><input type="number" id="pass-len" placeholder="طول" value="16"><button onclick="runTool('genpass')">تولید</button></div><div class="result-box" id="res-genpass"></div></div>
                <div class="tool-box"><h4>> بررسی وضعیت سایت</h4><div class="input-group"><input type="text" id="url-check" placeholder="URL" value="https://google.com"><button onclick="runTool('urlcheck')">بررسی</button></div><div class="result-box" id="res-urlcheck"></div></div>
                <div class="tool-box"><h4>> قدرت پسورد</h4><div class="input-group"><input type="text" id="pass-check" placeholder="پسورد" value="Hamed@123"><button onclick="runTool('passcheck')">بررسی</button></div><div class="result-box" id="res-passcheck"></div></div>
                <div class="tool-box"><h4>> کدگذار URL</h4><div class="input-group"><input type="text" id="url-encode" placeholder="متن" value="Hamed Cyber"><button onclick="runTool('urlencode')">کد</button><button onclick="runTool('urldecode')" style="background:var(--neon-purple);">رمزگشایی</button></div><div class="result-box" id="res-urlencode"></div></div>
                <div class="tool-box"><h4>> متن به هگز</h4><div class="input-group"><input type="text" id="hex-text" placeholder="متن/هگز" value="Hamed"><button onclick="runTool('tohex')">به هگز</button><button onclick="runTool('fromhex')" style="background:var(--neon-purple);">از هگز</button></div><div class="result-box" id="res-hex"></div></div>
                <div class="tool-box"><h4>> سن دامنه (Whois)</h4><div class="input-group"><input type="text" id="whois-domain" placeholder="Domain" value="google.com"><button onclick="runTool('whois')">بگیر</button></div><div class="result-box" id="res-whois"></div></div>
                <div class="tool-box"><h4>> تولید UUID</h4><div class="input-group"><button onclick="runTool('uuid')" style="width:100%;">تولید UUID</button></div><div class="result-box" id="res-uuid"></div></div>
                <div class="tool-box"><h4>> آنالیز HTTP Header</h4><div class="input-group"><input type="text" id="http-headers" placeholder="URL" value="https://google.com"><button onclick="runTool('header')">دریافت</button></div><div class="result-box" id="res-header"></div></div>
                <div class="tool-box"><h4>> وب اسکرپر</h4><div class="input-group"><input type="text" id="scrape-url" placeholder="URL" value="https://wikipedia.org"><button onclick="runTool('scrape')">استخراج</button></div><div class="result-box" id="res-scrape"></div></div>
                <div class="tool-box"><h4>> متن به باینری</h4><div class="input-group"><input type="text" id="bin-text" placeholder="متن" value="Hamed"><button onclick="runTool('tobin')">به باینری</button><button onclick="runTool('frombin')" style="background:var(--neon-purple);">از باینری</button></div><div class="result-box" id="res-bin"></div></div>
                <div class="tool-box"><h4>> فرمت‌کننده JSON</h4><div class="input-group"><input type="text" id="json-text" placeholder='{"a":1}' value='{"name":"Hamed"}'><button onclick="runTool('formatjson')">مرتب‌سازی</button></div><div class="result-box" id="res-json"></div></div>
                <div class="tool-box"><h4>> بررسی SSL (HTTPS)</h4><div class="input-group"><input type="text" id="ssl-host" placeholder="Host" value="google.com"><button onclick="runTool('sslcheck')">بررسی</button></div><div class="result-box" id="res-sslcheck"></div></div>
                <div class="tool-box"><h4>> Base64 Encode/Decode</h4><div class="input-group"><input type="text" id="b64-text" placeholder="متن" value="Hamed"><button onclick="runTool('base64')">کد</button><button onclick="runTool('base64dec')" style="background:var(--neon-purple);">رمزگشایی</button></div><div class="result-box" id="res-base64"></div></div>
                <div class="tool-box"><h4>> لینک‌های صفحه (Crawler)</h4><div class="input-group"><input type="text" id="crawl-url" placeholder="URL" value="https://example.com"><button onclick="runTool('crawl')">استخراج لینک</button></div><div class="result-box" id="res-crawl"></div></div>
                <div class="tool-box"><h4>> تشخیص HTTP Method</h4><div class="input-group"><input type="text" id="method-url" placeholder="URL" value="https://google.com"><button onclick="runTool('httpmethod')">تشخیص</button></div><div class="result-box" id="res-httpmethod"></div></div>
                <div class="tool-box"><h4>> Ping تست</h4><div class="input-group"><input type="text" id="ping-host" placeholder="Host" value="8.8.8.8"><button onclick="runTool('ping')">تست</button></div><div class="result-box" id="res-ping"></div></div>
                <div class="tool-box"><h4>> تست تزریق SQL</h4><div class="input-group"><input type="text" id="sqli-url" placeholder="URL" value="https://example.com?id=1"><button onclick="runTool('sqli')">تست</button></div><div class="result-box" id="res-sqli"></div></div>
                <div class="tool-box"><h4>> تست XSS</h4><div class="input-group"><input type="text" id="xss-url" placeholder="URL" value="https://example.com?q="><button onclick="runTool('xss')">تست</button></div><div class="result-box" id="res-xss"></div></div>
                <div class="tool-box"><h4>> تجزیه URL</h4><div class="input-group"><input type="text" id="parse-url" placeholder="URL" value="https://google.com/search?q=test"><button onclick="runTool('parse')">تجزیه</button></div><div class="result-box" id="res-parse"></div></div>
                <div class="tool-box"><h4>> تولید مک آدرس</h4><div class="input-group"><button onclick="runTool('mac')" style="width:100%;">تولید MAC</button></div><div class="result-box" id="res-mac"></div></div>
                <div class="tool-box"><h4>> مقایسه هش</h4><div class="input-group"><input type="text" id="hash1" placeholder="هش ۱" value="5f4dcc3b5aa765d61d8327deb882cf99"><input type="text" id="hash2" placeholder="هش ۲" value="5f4dcc3b5aa765d61d8327deb882cf99"><button onclick="runTool('hashcompare')">مقایسه</button></div><div class="result-box" id="res-hashcompare"></div></div>
                <div class="tool-box"><h4>> تشخیص تکنولوژی سایت</h4><div class="input-group"><input type="text" id="tech-url" placeholder="URL" value="https://wordpress.org"><button onclick="runTool('tech')">تشخیص</button></div><div class="result-box" id="res-tech"></div></div>
                <div class="tool-box"><h4>> رمزنگاری سزار</h4><div class="input-group"><input type="text" id="caesar-text" placeholder="متن" value="Hamed"><input type="number" id="caesar-shift" value="3" style="max-width:60px;"><button onclick="runTool('caesar')">رمزنگاری</button></div><div class="result-box" id="res-caesar"></div></div>
                <div class="tool-box"><h4>> مبدل تاریخ یونیکس</h4><div class="input-group"><input type="number" id="unix-time" placeholder="Unix Time" value="1700000000"><button onclick="runTool('unixdate')">تبدیل</button></div><div class="result-box" id="res-unixdate"></div></div>
                <div class="tool-box"><h4>> تست سرعت دامنه (Ping)</h4><div class="input-group"><input type="text" id="domain-ping" placeholder="Domain" value="github.com"><button onclick="runTool('domainping')">تست</button></div><div class="result-box" id="res-domainping"></div></div>
            </div>
        </div>

        <div class="glass-card tg-box">
            <h3>عضویت در کانال تلگرام</h3>
            <p style="color: var(--neon-cyan); font-family: monospace; margin: 10px 0;">T.me/HamedHacksDB</p>
            <a href="https://t.me/+TSrDJ-VSRs43YjY0" target="_blank" class="btn-tg">عضویت در کانال امن</a>
        </div>
        <div class="team-footer"><p>☠ تیم سایبری هکری حامد | HamedCyberTeam ☠</p></div>
    </div>

    <script>
        async function sendChat() {
            let input = document.getElementById('chat-input');
            let text = input.value.trim();
            if(!text) return;
            let chatBox = document.getElementById('chat-box');
            let userMsg = document.createElement('div'); userMsg.className = 'chat-msg user'; userMsg.textContent = text; chatBox.appendChild(userMsg);
            input.value = ''; chatBox.scrollTop = chatBox.scrollHeight;
            let typingId = 'typing-' + Date.now();
            let typingMsg = document.createElement('div'); typingMsg.className = 'chat-msg bot'; typingMsg.id = typingId; typingMsg.textContent = "در حال پردازش..."; chatBox.appendChild(typingMsg);
            chatBox.scrollTop = chatBox.scrollHeight;
            try {
                let response = await fetch('/api/ai', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({text: text}) });
                let data = await response.json();
                document.getElementById(typingId).remove();
                let botMsg = document.createElement('div'); botMsg.className = 'chat-msg bot'; botMsg.textContent = data.reply || data.error; chatBox.appendChild(botMsg);
                chatBox.scrollTop = chatBox.scrollHeight;
            } catch(e) { document.getElementById(typingId).textContent = "خطا در ارتباط."; }
        }

        async function runTool(type) {
            let url = '/api/' + type; let body = {};
            if(type === 'scan') { body = {target: document.getElementById('scan-ip').value}; }
            else if(type === 'ipinfo') { body = {ip: document.getElementById('ip-info').value}; }
            else if(type === 'hash') { body = {text: document.getElementById('hash-text').value}; }
            else if(type === 'subdomain') { body = {domain: document.getElementById('sub-domain').value}; }
            else if(type === 'genpass') { body = {len: document.getElementById('pass-len').value}; }
            else if(type === 'urlcheck') { body = {url: document.getElementById('url-check').value}; }
            else if(type === 'passcheck') { body = {pass: document.getElementById('pass-check').value}; }
            else if(type === 'urlencode' || type === 'urldecode') { body = {text: document.getElementById('url-encode').value}; }
            else if(type === 'tohex' || type === 'fromhex') { body = {text: document.getElementById('hex-text').value}; }
            else if(type === 'whois') { body = {domain: document.getElementById('whois-domain').value}; }
            else if(type === 'uuid') { }
            else if(type === 'header') { body = {url: document.getElementById('http-headers').value}; }
            else if(type === 'scrape') { body = {url: document.getElementById('scrape-url').value}; }
            else if(type === 'tobin' || type === 'frombin') { body = {text: document.getElementById('bin-text').value}; }
            else if(type === 'formatjson') { body = {text: document.getElementById('json-text').value}; }
            else if(type === 'sslcheck') { body = {host: document.getElementById('ssl-host').value}; }
            else if(type === 'base64' || type === 'base64dec') { body = {text: document.getElementById('b64-text').value}; }
            else if(type === 'crawl') { body = {url: document.getElementById('crawl-url').value}; }
            else if(type === 'httpmethod') { body = {url: document.getElementById('method-url').value}; }
            else if(type === 'ping') { body = {host: document.getElementById('ping-host').value}; }
            else if(type === 'sqli') { body = {url: document.getElementById('sqli-url').value}; }
            else if(type === 'xss') { body = {url: document.getElementById('xss-url').value}; }
            else if(type === 'parse') { body = {url: document.getElementById('parse-url').value}; }
            else if(type === 'mac') { }
            else if(type === 'hashcompare') { body = {h1: document.getElementById('hash1').value, h2: document.getElementById('hash2').value}; }
            else if(type === 'tech') { body = {url: document.getElementById('tech-url').value}; }
            else if(type === 'caesar') { body = {text: document.getElementById('caesar-text').value, shift: document.getElementById('caesar-shift').value}; }
            else if(type === 'unixdate') { body = {time: document.getElementById('unix-time').value}; }
            else if(type === 'domainping') { body = {host: document.getElementById('domain-ping').value}; }

            let resId = 'res-' + type; let el = document.getElementById(resId);
            if(el) { el.style.display = 'block'; el.innerText = "در حال پردازش..."; }

            try {
                let response = await fetch(url, { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(body) });
                let data = await response.json();
                if(el) el.innerText = data.result || data.error || "خطای ناشناخته";
            } catch(e) { if(el) el.innerText = "خطا در اجرای ابزار."; }
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home(): return render_template_string(HTML_TEMPLATE)

@app.route('/api/ai', methods=['POST'])
@limiter.limit("5 per minute")
def api_ai(): 
    try:
        data = request.get_json()
        text = validate_input(data, 'text', max_len=300)
        if text is None: return jsonify({"error": "ورودی نامعتبر است."}), 400
        return jsonify({"reply": ai_respond(text)})
    except Exception: return jsonify({"error": "خطای پردازش."}), 400

@app.route('/api/scan', methods=['POST'])
@limiter.limit("10 per minute")
def api_scan():
    data = request.get_json()
    target = validate_input(data, 'target', max_len=100)
    if not target or is_internal_ip(target): return jsonify({"error": "دسترسی مسدود است."}), 403
    result = f"Target: {target}\\n"
    try:
        ip = socket.gethostbyname(target); result += f"IP: {ip}\\n\\n"
        for port in [21, 22, 23, 25, 53, 80, 110, 443, 445, 3306, 8080]:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM); s.settimeout(0.5)
            if s.connect_ex((ip, port)) == 0: result += f"Port {port}: OPEN\\n"
            s.close()
    except Exception as e: result += f"Error: {str(e)}"
    return jsonify({"result": result})

@app.route('/api/ipinfo', methods=['POST'])
@limiter.limit("10 per minute")
def api_ipinfo():
    data = request.get_json()
    ip = validate_input(data, 'ip', max_len=50)
    if not ip or is_internal_ip(ip): return jsonify({"error": "دسترسی مسدود."}), 403
    try:
        data = requests.get(f"http://ip-api.com/json/{ip}?fields=status,country,city,isp,org,query", timeout=5).json()
        if data.get('status') == 'success': return jsonify({"result": f"IP: {data['query']}\\nCountry: {data['country']}\\nCity: {data['city']}\\nOrg: {data.get('org', data.get('isp'))}"})
        return jsonify({"result": "Invalid IP."})
    except Exception as e: return jsonify({"result": f"Error: {str(e)}"})

@app.route('/api/hash', methods=['POST'])
def api_hash():
    data = request.get_json()
    text = validate_input(data, 'text', max_len=500)
    if text is None: return jsonify({"error": "ورودی نامعتبر."}), 400
    encoded = text.encode('utf-8')
    return jsonify({"result": f"MD5: {hashlib.md5(encoded).hexdigest()}\\nSHA256: {hashlib.sha256(encoded).hexdigest()}"})

@app.route('/api/subdomain', methods=['POST'])
def api_subdomain():
    data = request.get_json()
    domain = validate_input(data, 'domain', max_len=100)
    if not domain or is_internal_ip(domain): return jsonify({"error": "دسترسی مسدود."}), 403
    found = []
    for sub in ['www', 'mail', 'ftp', 'admin', 'blog', 'api', 'dev', 'test']:
        try: 
            host = f"{sub}.{domain}"
            socket.gethostbyname(host)
            found.append(host)
        except: pass
    if found: return jsonify({"result": "\\n".join(found)})
    return jsonify({"result": "None found."})

@app.route('/api/genpass', methods=['POST'])
def api_genpass():
    data = request.get_json()
    length = int(data.get('len', 16))
    if length > 50: length = 50
    chars = string.ascii_letters + string.digits + "!@#$%^&*"
    return jsonify({"result": ''.join(random.choice(chars) for _ in range(length))})

@app.route('/api/urlcheck', methods=['POST'])
@limiter.limit("10 per minute")
def api_urlcheck():
    data = request.get_json()
    url = validate_input(data, 'url', max_len=200)
    if not url: return jsonify({"error": "آدرس نامعتبر."}), 400
    hostname = urllib.parse.urlparse(url).hostname
    if not hostname or is_internal_ip(hostname): return jsonify({"error": "آدرس غیرمجاز."}), 403
    try: r = requests.head(url, timeout=5, allow_redirects=True); return jsonify({"result": f"Status: {r.status_code}\\nServer: {r.headers.get('Server', 'Unknown')}"})
    except Exception as e: return jsonify({"result": f"Error: {str(e)}"})

@app.route('/api/passcheck', methods=['POST'])
def api_passcheck():
    data = request.get_json()
    p = validate_input(data, 'pass', max_len=100)
    if p is None: return jsonify({"error": "ورودی نامعتبر."}), 400
    score = 0
    if len(p) >= 8: score += 1
    if re.search(r'[A-Z]', p): score += 1
    if re.search(r'[0-9]', p): score += 1
    if re.search(r'[^A-Za-z0-9]', p): score += 1
    return jsonify({"result": f"Strength: {['Very Weak', 'Weak', 'Medium', 'Strong', 'Very Strong'][score]} ({score}/4)"})

@app.route('/api/urlencode', methods=['POST'])
def api_urlencode():
    data = request.get_json()
    text = validate_input(data, 'text', max_len=500)
    if text is None: return jsonify({"error": "ورودی نامعتبر."}), 400
    return jsonify({"result": urllib.parse.quote(text)})

@app.route('/api/urldecode', methods=['POST'])
def api_urldecode():
    data = request.get_json()
    text = validate_input(data, 'text', max_len=500)
    if text is None: return jsonify({"error": "ورودی نامعتبر."}), 400
    return jsonify({"result": urllib.parse.unquote(text)})

@app.route('/api/tohex', methods=['POST'])
def api_tohex():
    data = request.get_json()
    text = validate_input(data, 'text', max_len=500)
    if text is None: return jsonify({"error": "ورودی نامعتبر."}), 400
    return jsonify({"result": text.encode().hex()})

@app.route('/api/fromhex', methods=['POST'])
def api_fromhex():
    data = request.get_json()
    text = validate_input(data, 'text', max_len=1000)
    if text is None: return jsonify({"error": "ورودی نامعتبر."}), 400
    try: return jsonify({"result": bytes.fromhex(text).decode()})
    except: return jsonify({"result": "Invalid Hex"})

@app.route('/api/whois', methods=['POST'])
def api_whois():
    data = request.get_json()
    domain = validate_input(data, 'domain', max_len=100)
    if not domain or is_internal_ip(domain): return jsonify({"error": "دسترسی مسدود."}), 403
    try:
        r = requests.get(f"https://rdap.org/domain/{domain}", timeout=5); data = r.json()
        reg_date = next((e['eventDate'] for e in data.get('events', []) if e['eventAction'] == 'registration'), 'Unknown')
        return jsonify({"result": f"Domain: {domain}\\nRegistered: {reg_date[:10] if reg_date!='Unknown' else reg_date}"})
    except Exception as e: return jsonify({"result": f"Error: {str(e)}"})

@app.route('/api/uuid', methods=['POST'])
def api_uuid(): return jsonify({"result": str(uuid.uuid4())})

@app.route('/api/header', methods=['POST'])
@limiter.limit("10 per minute")
def api_header():
    data = request.get_json()
    url = validate_input(data, 'url', max_len=200)
    if not url: return jsonify({"error": "آدرس نامعتبر."}), 400
    hostname = urllib.parse.urlparse(url).hostname
    if not hostname or is_internal_ip(hostname): return jsonify({"error": "آدرس غیرمجاز."}), 403
    try: r = requests.get(url, timeout=5); return jsonify({"result": "\\n".join(f"{k}: {v}" for k, v in r.headers.items())})
    except Exception as e: return jsonify({"result": f"Error: {str(e)}"})

@app.route('/api/scrape', methods=['POST'])
@limiter.limit("5 per minute")
def api_scrape():
    data = request.get_json()
    url = validate_input(data, 'url', max_len=200)
    if not url: return jsonify({"error": "آدرس نامعتبر."}), 400
    hostname = urllib.parse.urlparse(url).hostname
    if not hostname or is_internal_ip(hostname): return jsonify({"error": "آدرس غیرمجاز."}), 403
    try:
        r = requests.get(url, timeout=5, headers={'User-Agent': 'Mozilla/5.0'})
        title = re.search(r'<title>(.*?)</title>', r.text, re.IGNORECASE)
        desc = re.search(r'<meta name="description" content="(.*?)"', r.text, re.IGNORECASE)
        return jsonify({"result": f"Title: {title.group(1) if title else 'Unknown'}\\nDesc: {desc.group(1) if desc else 'Unknown'}"})
    except Exception as e: return jsonify({"result": f"Error: {str(e)}"})

@app.route('/api/tobin', methods=['POST'])
def api_tobin():
    data = request.get_json()
    text = validate_input(data, 'text', max_len=500)
    if text is None: return jsonify({"error": "ورودی نامعتبر."}), 400
    return jsonify({"result": ' '.join(format(ord(i), '08b') for i in text)})

@app.route('/api/frombin', methods=['POST'])
def api_frombin():
    data = request.get_json()
    text = validate_input(data, 'text', max_len=5000)
    if text is None: return jsonify({"error": "ورودی نامعتبر."}), 400
    try:
        binary = text.replace(' ', '')
        return jsonify({"result": ''.join(chr(int(binary[i:i+8], 2)) for i in range(0, len(binary), 8))})
    except: return jsonify({"result": "Invalid Binary"})

@app.route('/api/formatjson', methods=['POST'])
def api_formatjson():
    data = request.get_json()
    text = validate_input(data, 'text', max_len=5000)
    if text is None: return jsonify({"error": "ورودی نامعتبر."}), 400
    try: return jsonify({"result": json.dumps(json.loads(text), indent=4, ensure_ascii=False)})
    except: return jsonify({"result": "Invalid JSON"})

@app.route('/api/sslcheck', methods=['POST'])
@limiter.limit("10 per minute")
def api_sslcheck():
    data = request.get_json()
    host = validate_input(data, 'host', max_len=100)
    if not host or is_internal_ip(host): return jsonify({"error": "دسترسی مسدود."}), 403
    try:
        context = ssl.create_default_context()
        with socket.create_connection((host, 443), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=host) as ssock:
                cert = ssock.getpeercert()
                return jsonify({"result": f"Issuer: {cert.get('issuer')}\\nValid Until: {cert.get('notAfter')}"})
    except Exception as e: return jsonify({"result": f"SSL Error: {str(e)}"})

@app.route('/api/base64', methods=['POST'])
def api_base64():
    data = request.get_json()
    text = validate_input(data, 'text', max_len=500)
    if text is None: return jsonify({"error": "ورودی نامعتبر."}), 400
    return jsonify({"result": base64.b64encode(text.encode()).decode()})

@app.route('/api/base64dec', methods=['POST'])
def api_base64dec():
    data = request.get_json()
    text = validate_input(data, 'text', max_len=1000)
    if text is None: return jsonify({"error": "ورودی نامعتبر."}), 400
    try: return jsonify({"result": base64.b64decode(text.encode()).decode()})
    except: return jsonify({"result": "Invalid Base64"})

@app.route('/api/crawl', methods=['POST'])
@limiter.limit("5 per minute")
def api_crawl():
    data = request.get_json()
    url = validate_input(data, 'url', max_len=200)
    if not url: return jsonify({"error": "آدرس نامعتبر."}), 400
    hostname = urllib.parse.urlparse(url).hostname
    if not hostname or is_internal_ip(hostname): return jsonify({"error": "آدرس غیرمجاز."}), 403
    try:
        r = requests.get(url, timeout=5)
        links = re.findall(r'href=[\'"]?([^\'" >]+)', r.text)
        return jsonify({"result": "\\n".join(list(set(links))[:15])})
    except Exception as e: return jsonify({"result": f"Error: {str(e)}"})

@app.route('/api/httpmethod', methods=['POST'])
@limiter.limit("10 per minute")
def api_httpmethod():
    data = request.get_json()
    url = validate_input(data, 'url', max_len=200)
    if not url: return jsonify({"error": "آدرس نامعتبر."}), 400
    hostname = urllib.parse.urlparse(url).hostname
    if not hostname or is_internal_ip(hostname): return jsonify({"error": "آدرس غیرمجاز."}), 403
    try:
        r = requests.options(url, timeout=5)
        return jsonify({"result": f"Allow: {r.headers.get('Allow', 'Not Specified')}"})
    except Exception as e: return jsonify({"result": f"Error: {str(e)}"})

@app.route('/api/ping', methods=['POST'])
@limiter.limit("10 per minute")
def api_ping():
    data = request.get_json()
    host = validate_input(data, 'host', max_len=100)
    if not host or is_internal_ip(host): return jsonify({"error": "دسترسی مسدود."}), 403
    try:
        start = time.time()
        socket.create_connection((host, 80), timeout=3).close()
        return jsonify({"result": f"Connected successfully in {round((time.time() - start)*1000, 2)} ms"})
    except Exception as e: return jsonify({"result": f"Connection failed: {str(e)}"})

@app.route('/api/sqli', methods=['POST'])
@limiter.limit("5 per minute")
def api_sqli():
    data = request.get_json()
    url = validate_input(data, 'url', max_len=200)
    if not url: return jsonify({"error": "آدرس نامعتبر."}), 400
    hostname = urllib.parse.urlparse(url).hostname
    if not hostname or is_internal_ip(hostname): return jsonify({"error": "آدرس غیرمجاز."}), 403
    try:
        payload = url + "'"
        r1 = requests.get(url, timeout=5)
        r2 = requests.get(payload, timeout=5)
        if r1.text != r2.text:
            return jsonify({"result": "Potential SQL Injection vulnerability detected!"})
        return jsonify({"result": "No obvious SQLi found."})
    except Exception as e: return jsonify({"result": f"Error: {str(e)}"})

@app.route('/api/xss', methods=['POST'])
@limiter.limit("5 per minute")
def api_xss():
    data = request.get_json()
    url = validate_input(data, 'url', max_len=200)
    if not url: return jsonify({"error": "آدرس نامعتبر."}), 400
    hostname = urllib.parse.urlparse(url).hostname
    if not hostname or is_internal_ip(hostname): return jsonify({"error": "آدرس غیرمجاز."}), 403
    try:
        payload = '<script>alert(1)</script>'
        r = requests.get(url + payload, timeout=5)
        if payload in r.text:
            return jsonify({"result": "XSS vulnerability detected! (Reflected)"})
        return jsonify({"result": "No obvious XSS found."})
    except Exception as e: return jsonify({"result": f"Error: {str(e)}"})

@app.route('/api/parse', methods=['POST'])
def api_parse():
    data = request.get_json()
    url = validate_input(data, 'url', max_len=500)
    if not url: return jsonify({"error": "آدرس نامعتبر."}), 400
    try:
        parsed = urllib.parse.urlparse(url)
        res = f"Scheme: {parsed.scheme}\\nNetloc: {parsed.netloc}\\nPath: {parsed.path}\\nQuery: {parsed.query}\\nFragment: {parsed.fragment}"
        return jsonify({"result": res})
    except Exception as e: return jsonify({"result": f"Error: {str(e)}"})

@app.route('/api/mac', methods=['POST'])
def api_mac():
    mac = ':'.join(['%02x' % random.randint(0, 255) for _ in range(6)])
    return jsonify({"result": f"Random MAC: {mac}"})

@app.route('/api/hashcompare', methods=['POST'])
def api_hashcompare():
    data = request.get_json()
    h1 = validate_input(data, 'h1', max_len=100)
    h2 = validate_input(data, 'h2', max_len=100)
    if not h1 or not h2: return jsonify({"error": "ورودی نامعتبر."}), 400
    if h1 == h2: return jsonify({"result": "Hashes MATCH!"})
    return jsonify({"result": "Hashes DO NOT match."})

@app.route('/api/tech', methods=['POST'])
@limiter.limit("5 per minute")
def api_tech():
    data = request.get_json()
    url = validate_input(data, 'url', max_len=200)
    if not url: return jsonify({"error": "آدرس نامعتبر."}), 400
    hostname = urllib.parse.urlparse(url).hostname
    if not hostname or is_internal_ip(hostname): return jsonify({"error": "آدرس غیرمجاز."}), 403
    try:
        r = requests.get(url, timeout=5)
        server = r.headers.get('Server', 'Unknown')
        techs = []
        if 'wp-content' in r.text: techs.append("WordPress")
        if 'django' in r.text.lower(): techs.append("Django")
        if 'react' in r.text.lower(): techs.append("React")
        return jsonify({"result": f"Server: {server}\\nDetected: {', '.join(techs) if techs else 'None'}"})
    except Exception as e: return jsonify({"result": f"Error: {str(e)}"})

@app.route('/api/caesar', methods=['POST'])
def api_caesar():
    data = request.get_json()
    text = validate_input(data, 'text', max_len=500)
    shift = int(data.get('shift', 3))
    if text is None: return jsonify({"error": "ورودی نامعتبر."}), 400
    result = "".join(chr((ord(c) + shift - 65) % 26 + 65) if c.isupper() else chr((ord(c) + shift - 97) % 26 + 97) if c.islower() else c for c in text)
    return jsonify({"result": result})

@app.route('/api/unixdate', methods=['POST'])
def api_unixdate():
    data = request.get_json()
    try:
        ts = int(data.get('time'))
        dt = datetime.datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S UTC')
        return jsonify({"result": dt})
    except: return jsonify({"result": "Invalid Timestamp"})

@app.route('/api/domainping', methods=['POST'])
@limiter.limit("10 per minute")
def api_domainping():
    data = request.get_json()
    host = validate_input(data, 'host', max_len=100)
    if not host or is_internal_ip(host): return jsonify({"error": "دسترسی مسدود."}), 403
    try:
        start = time.time()
        ip = socket.gethostbyname(host)
        end = time.time()
        return jsonify({"result": f"Resolved to {ip} in {round((end - start)*1000, 2)} ms"})
    except Exception as e: return jsonify({"result": f"Error: {str(e)}"})

@app.errorhandler(429)
def ratelimit_handler(e): return jsonify({"error": "درخواست بیش از حد (ضد DDoS)."}), 429

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)

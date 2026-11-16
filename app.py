import socket
import hashlib
import random
import base64
import uuid
import requests
import re
import urllib.parse
from flask import Flask, render_template_string, request, jsonify, abort
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)
limiter = Limiter(get_remote_address, app=app, default_limits=["60 per minute"], storage_uri="memory://")

@app.after_request
def add_security_headers(response):
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['Server'] = 'Hamed-Secure-Core'
    return response

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
        .hack-list { display: flex; flex-direction: column; gap: 12px; }
        .hack-item { background: rgba(0,0,0,0.5); border-radius: 8px; padding: 15px; border-right: 3px solid var(--neon-red); display: flex; justify-content: space-between; align-items: center;}
        .hack-item h5 { color: #fff; margin-bottom: 5px; font-size: 1rem; }
        .hack-item p { color: var(--text-muted); font-size: 0.85rem; }
        .hack-status { font-family: 'Share Tech Mono', monospace; font-size: 0.8rem; padding: 3px 8px; border-radius: 4px; border: 1px solid var(--neon-red); color: var(--neon-red); white-space: nowrap;}
        .tools-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 15px; }
        .tool-box { background: rgba(0,0,0,0.6); border: 1px solid rgba(255,0,60,0.2); border-radius: 8px; padding: 15px; }
        .tool-box h4 { color: var(--neon-red); margin-bottom: 15px; font-family: 'Share Tech Mono', monospace; font-size: 0.95rem;}
        .input-group { display: flex; gap: 10px; margin-bottom: 15px; }
        .input-group input { flex: 1; padding: 10px; background: #000; border: 1px solid var(--glass-border); color: #fff; border-radius: 5px; font-family: monospace; outline: none; font-size: 0.85rem;}
        .input-group button { padding: 10px 15px; background: var(--neon-red); color: #fff; border: none; border-radius: 5px; cursor: pointer; font-weight: bold; font-family: inherit; font-size: 0.85rem; transition: 0.3s;}
        .input-group button:hover { background: #fff; color: #000; box-shadow: 0 0 15px var(--neon-red); }
        .result-box { background: #000; padding: 10px; border-radius: 5px; font-family: monospace; color: var(--neon-cyan); min-height: 40px; font-size: 0.85rem; display: none; white-space: pre-wrap; direction: rtl; text-align: right; border-right: 2px solid var(--neon-red); }
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
        
        <div class="glass-card">
            <h3 class="section-title"><span>📂 آرشیو عملیات‌های حامد</span></h3>
            <div class="hack-list">
                <div class="hack-item"><div><h5>نفوذ به زیرساخت‌های ابری (AWS/Azure)</h5><p>بایپس WAF و استخراج دیتابیس ۱۵ میلیون کاربر بدون ردپا</p></div><span class="hack-status">موفق</span></div>
                <div class="hack-item"><div><h5>حمله DDoS ترکیبی (Layer 4 & 7)</h5><p>ارسال ۱.۵ میلیون پکت در ثانیه به CDN هدف</p></div><span class="hack-status">بحرانی</span></div>
                <div class="hack-item"><div><h5>اکسپلویت Zero-Day (RCE)</h5><p>کشف باگ روز صفر در هسته لینوکس و اخذ دسترسی Root</p></div><span class="hack-status">سری</span></div>
                <div class="hack-item"><div><h5>کرک هش‌های NTLM</h5><p>بازگردانی ۲ میلیون پسورد با خوشه GPU</p></div><span class="hack-status">موفق</span></div>
            </div>
        </div>

        <div class="glass-card">
            <h3 class="section-title"><span>⚙️ زرادخانه هکر (ابزارهای زنده)</span></h3>
            <div class="tools-grid">
                <div class="tool-box"><h4>> اسکنر پورت</h4><div class="input-group"><input type="text" id="scan-ip" placeholder="آی‌پی یا دامنه" value="scanme.nmap.org"><button onclick="runTool('scan')">اسکن</button></div><div class="result-box" id="res-scan"></div></div>
                <div class="tool-box"><h4>> اطلاعات آی‌پی</h4><div class="input-group"><input type="text" id="ip-info" placeholder="آی‌پی" value="8.8.8.8"><button onclick="runTool('ipinfo')">بگیر</button></div><div class="result-box" id="res-ipinfo"></div></div>
                <div class="tool-box"><h4>> ساخت هش</h4><div class="input-group"><input type="text" id="hash-text" placeholder="متن" value="Hamed123"><button onclick="runTool('hash')">هش کن</button></div><div class="result-box" id="res-hash"></div></div>
                <div class="tool-box"><h4>> بررسی وضعیت سایت</h4><div class="input-group"><input type="text" id="url-check" placeholder="https://example.com" value="https://google.com"><button onclick="runTool('urlcheck')">بررسی</button></div><div class="result-box" id="res-urlcheck"></div></div>
                <div class="tool-box"><h4>> قدرت پسورد</h4><div class="input-group"><input type="text" id="pass-check" placeholder="پسورد" value="Hamed@123"><button onclick="runTool('passcheck')">بررسی</button></div><div class="result-box" id="res-passcheck"></div></div>
                <div class="tool-box"><h4>> کدگذار URL</h4><div class="input-group"><input type="text" id="url-encode" placeholder="متن" value="Hamed Cyber"><button onclick="runTool('urlencode')">کد</button><button onclick="runTool('urldecode')" style="background:var(--neon-purple);">رمزگشایی</button></div><div class="result-box" id="res-urlencode"></div></div>
                <div class="tool-box"><h4>> متن به هگز</h4><div class="input-group"><input type="text" id="hex-text" placeholder="متن/هگز" value="Hamed"><button onclick="runTool('tohex')">به هگز</button><button onclick="runTool('fromhex')" style="background:var(--neon-purple);">از هگز</button></div><div class="result-box" id="res-hex"></div></div>
                <div class="tool-box"><h4>> سن دامنه (Whois)</h4><div class="input-group"><input type="text" id="whois-domain" placeholder="google.com" value="google.com"><button onclick="runTool('whois')">بگیر</button></div><div class="result-box" id="res-whois"></div></div>
                <div class="tool-box"><h4>> تولید UUID</h4><div class="input-group"><button onclick="runTool('uuid')" style="width:100%;">تولید UUID</button></div><div class="result-box" id="res-uuid"></div></div>
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
        async function runTool(type) {
            let url = '/api/' + type;
            let body = {};
            
            if(type === 'scan') { body = {target: document.getElementById('scan-ip').value}; document.getElementById('res-scan').style.display='block'; document.getElementById('res-scan').innerText="در حال اسکن..."; }
            else if(type === 'ipinfo') { body = {ip: document.getElementById('ip-info').value}; document.getElementById('res-ipinfo').style.display='block'; document.getElementById('res-ipinfo').innerText="در حال دریافت..."; }
            else if(type === 'hash') { body = {text: document.getElementById('hash-text').value}; document.getElementById('res-hash').style.display='block'; }
            else if(type === 'urlcheck') { body = {url: document.getElementById('url-check').value}; document.getElementById('res-urlcheck').style.display='block'; document.getElementById('res-urlcheck').innerText="در حال بررسی..."; }
            else if(type === 'passcheck') { body = {pass: document.getElementById('pass-check').value}; document.getElementById('res-passcheck').style.display='block'; }
            else if(type === 'urlencode' || type === 'urldecode') { body = {text: document.getElementById('url-encode').value}; document.getElementById('res-urlencode').style.display='block'; }
            else if(type === 'tohex' || type === 'fromhex') { body = {text: document.getElementById('hex-text').value}; document.getElementById('res-hex').style.display='block'; }
            else if(type === 'whois') { body = {domain: document.getElementById('whois-domain').value}; document.getElementById('res-whois').style.display='block'; document.getElementById('res-whois').innerText="در حال دریافت..."; }
            else if(type === 'uuid') { document.getElementById('res-uuid').style.display='block'; }

            try {
                let response = await fetch(url, { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(body) });
                let data = await response.json();
                if(type === 'scan') document.getElementById('res-scan').innerText = data.result;
                if(type === 'ipinfo') document.getElementById('res-ipinfo').innerText = data.result;
                if(type === 'hash') document.getElementById('res-hash').innerText = data.result;
                if(type === 'urlcheck') document.getElementById('res-urlcheck').innerText = data.result;
                if(type === 'passcheck') document.getElementById('res-passcheck').innerText = data.result;
                if(type === 'urlencode' || type === 'urldecode') document.getElementById('res-urlencode').innerText = data.result;
                if(type === 'tohex' || type === 'fromhex') document.getElementById('res-hex').innerText = data.result;
                if(type === 'whois') document.getElementById('res-whois').innerText = data.result;
                if(type === 'uuid') document.getElementById('res-uuid').innerText = data.result;
            } catch(e) { alert("خطا در اجرای ابزار"); }
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home(): return render_template_string(HTML_TEMPLATE)

@app.route('/api/scan', methods=['POST'])
def api_scan():
    target = request.json.get('target')
    result = f"هدف: {target}\\n"
    try:
        ip = socket.gethostbyname(target)
        result += f"آی‌پی سرور: {ip}\\n\\n"
        ports_info = {
            21: "FTP (انتقال فایل)", 22: "SSH (مدیریت از راه دور)", 23: "Telnet (امنیت پایین)", 
            25: "SMTP (ایمیل)", 53: "DNS (سیستم نام دامنه)", 80: "HTTP (وب‌سایت)", 
            110: "POP3 (ایمیل)", 443: "HTTPS (وب‌سایت امن)", 445: "SMB (اشتراک فایل ویندوز)", 
            3306: "MySQL (دیتابیس)", 8080: "HTTP-Alt (پورت جایگزین وب)"
        }
        found_any = False
        for port, desc in ports_info.items():
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.5)
            if s.connect_ex((ip, port)) == 0: 
                result += f"پورت {port} ({desc}): باز است\\n"
                found_any = True
            s.close()
        if not found_any:
            result += "هیچ پورت بازی از لیست رایج پیدا نشد."
    except Exception as e: 
        result += f"خطا در اسکن: {str(e)}"
    return jsonify({"result": result})

@app.route('/api/ipinfo', methods=['POST'])
def api_ipinfo():
    ip = request.json.get('ip')
    try:
        data = requests.get(f"http://ip-api.com/json/{ip}?fields=status,country,city,isp,org,query", timeout=5).json()
        if data.get('status') == 'success':
            return jsonify({"result": f"آی‌پی: {data['query']}\\nکشور: {data['country']}\\nشهر: {data['city']}\\nسازمان (ISP): {data.get('org', data.get('isp'))}"})
        return jsonify({"result": "آی‌پی نامعتبر است یا پیدا نشد."})
    except Exception as e: return jsonify({"result": f"خطا: {str(e)}"})

@app.route('/api/hash', methods=['POST'])
def api_hash():
    text = request.json.get('text').encode('utf-8')
    return jsonify({"result": f"هش MD5:\\n{hashlib.md5(text).hexdigest()}\\n\\nهش SHA256:\\n{hashlib.sha256(text).hexdigest()}"})

@app.route('/api/urlcheck', methods=['POST'])
def api_urlcheck():
    url = request.json.get('url')
    try:
        r = requests.head(url, timeout=5, allow_redirects=True)
        return jsonify({"result": f"کد وضعیت (Status Code): {r.status_code}\\nسرور میزبان: {r.headers.get('Server', 'ناشناخته')}"})
    except Exception as e: return jsonify({"result": f"خطا در اتصال به سایت: {str(e)}"})

@app.route('/api/passcheck', methods=['POST'])
def api_passcheck():
    p = request.json.get('pass')
    score = 0
    if len(p) >= 8: score += 1
    if re.search(r'[A-Z]', p): score += 1
    if re.search(r'[0-9]', p): score += 1
    if re.search(r'[^A-Za-z0-9]', p): score += 1
    levels = ["خیلی ضعیف (به راحتی هک می‌شود)", "ضعیف", "متوسط", "قوی", "بسیار قوی (غیرقابل نفوذ)"]
    return jsonify({"result": f"میزان امنیت: {levels[score]}\\nامتیاز: {score} از 4"})

@app.route('/api/urlencode', methods=['POST'])
def api_urlencode():
    return jsonify({"result": f"متن کد شده:\\n{urllib.parse.quote(request.json.get('text'))}"})

@app.route('/api/urldecode', methods=['POST'])
def api_urldecode():
    return jsonify({"result": f"متن رمزگشایی شده:\\n{urllib.parse.unquote(request.json.get('text'))}"})

@app.route('/api/tohex', methods=['POST'])
def api_tohex():
    return jsonify({"result": f"کد هگزادسیمال:\\n{request.json.get('text').encode().hex()}"})

@app.route('/api/fromhex', methods=['POST'])
def api_fromhex():
    try: return jsonify({"result": f"متن اصلی:\\n{bytes.fromhex(request.json.get('text')).decode()}"})
    except: return jsonify({"result": "خطا: کد هگز وارد شده نامعتبر است."})

@app.route('/api/whois', methods=['POST'])
def api_whois():
    domain = request.json.get('domain')
    try:
        r = requests.get(f"https://rdap.org/domain/{domain}", timeout=5)
        data = r.json()
        events = data.get('events', [])
        reg_date = next((e['eventDate'] for e in events if e['eventAction'] == 'registration'), 'ناشناخته')
        return jsonify({"result": f"نام دامنه: {domain}\\nتاریخ ثبت دامنه: {reg_date[:10] if reg_date!='ناشناخته' else reg_date}"})
    except Exception as e: return jsonify({"result": f"خطا در دریافت اطلاعات دامنه: {str(e)}"})

@app.route('/api/uuid', methods=['POST'])
def api_uuid():
    return jsonify({"result": f"شناسه یکتای تولید شده (UUID):\\n{str(uuid.uuid4())}"})

@app.errorhandler(429)
def ratelimit_handler(e):
    return "429 درخواست بیش از حد - محافظت ضد DDoS فعال است", 429

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)

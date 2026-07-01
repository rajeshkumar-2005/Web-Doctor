// ===============================
// GOVSCAN SECURITY CENTER
// ===============================

let currentUrl = "";
let chartInstance = null;
let lang = "en";

// ===============================
// LANGUAGE
// ===============================

const t = {

    en:{

        title:"WebDoctor",
        scan:"Scan Website",
        report:"Download Report",
        trend:"Security Trend",

        low:"LOW",
        medium:"MEDIUM",
        high:"HIGH"

    },

    ta:{

        title:"அரசு பாதுகாப்பு",
        scan:"சோதிக்கவும்",
        report:"அறிக்கை",
        trend:"பாதுகாப்பு நிலை",

        low:"குறைவு",
        medium:"நடுத்தரம்",
        high:"அதிகம்"

    }

};

// ===============================

function toggleLang(){

    lang=(lang==="en")?"ta":"en";

    applyLang();

}

// ===============================

function applyLang(){

    document.getElementById("title").innerText=t[lang].title;

    document.getElementById("scanBtn").innerText=t[lang].scan;

    document.getElementById("reportBtn").innerText=t[lang].report;

}

// ===============================

function setUrl(url){

    document.getElementById("url").value=url;

}

// ===============================
// LOADING
// ===============================

function loading(){

    let score=document.getElementById("score");

    score.innerHTML=`
        <div class="loader"></div>
    `;

}

// ===============================
// SCAN
// ===============================

async function scan(){

    currentUrl=document.getElementById("url").value.trim();

    if(currentUrl===""){

        alert("Enter Website URL");

        return;

    }

    loading();

    let response=await fetch(`/scan?url=${currentUrl}`);

    let data=await response.json();

    displayResult(data);

    loadTrend(data);

}

// ===============================
// DISPLAY
// ===============================

function displayResult(data){

    let score=data.risk.score;

    let risk=data.risk.risk;

    document.getElementById("score").innerHTML=score;

    let riskText=risk;

    if(lang==="ta"){

        if(risk==="LOW") riskText=t.ta.low;

        if(risk==="MEDIUM") riskText=t.ta.medium;

        if(risk==="HIGH") riskText=t.ta.high;

    }

    let riskDiv=document.getElementById("risk");

    riskDiv.innerHTML=riskText;

    riskDiv.className="risk-text "+risk.toLowerCase();

    document.getElementById("ssl").innerHTML=

        data.data.ssl.valid ?

        "🟢 Secure"

        :

        "🔴 Invalid";

    document.getElementById("headers").innerHTML=

        data.data.headers.missing.length===0 ?

        "🟢 Complete"

        :

        data.data.headers.missing.join("<br>");

    document.getElementById("ports").innerHTML=

        data.data.ports.open_ports.length===0 ?

        "🟢 None"

        :

        data.data.ports.open_ports.join(", ");

    document.getElementById("vulns").innerHTML=

        data.data.vulns.sqli ?

        "🔴 Detected"

        :

        "🟢 Safe";

    showAlert(score);

    buildPriority(data);

    buildMeasures(data);

}
// ========================================
// ALERT
// ========================================

function showAlert(score){

    let box=document.getElementById("alertBox");
    let text=document.getElementById("alertText");

    box.style.display="none";

    if(score<40){

        box.style.display="block";
        box.style.background="rgba(255,77,109,.12)";
        box.style.borderLeft="6px solid #ff4d6d";

        text.innerHTML="🚨 Critical Risk Detected. Immediate action is required.";

    }

    else if(score<70){

        box.style.display="block";
        box.style.background="rgba(247,183,49,.12)";
        box.style.borderLeft="6px solid #f7b731";

        text.innerHTML="⚠ Medium Risk. Improve the highlighted security issues.";

    }

}

// ========================================
// PRIORITY
// ========================================

function buildPriority(data){

    let priority=[];

    if(!data.data.ssl.valid)
        priority.push({
            level:"CRITICAL",
            text:"Enable HTTPS with a valid SSL certificate."
        });

    if(data.data.vulns.sqli)
        priority.push({
            level:"CRITICAL",
            text:"Resolve possible SQL Injection vulnerability."
        });

    if(data.data.ports.open_ports.length>0)
        priority.push({
            level:"HIGH",
            text:"Close unused exposed ports."
        });

    if(data.data.headers.missing.length>0)
        priority.push({
            level:"MEDIUM",
            text:"Configure all recommended HTTP Security Headers."
        });

    if(priority.length===0){

        priority.push({
            level:"LOW",
            text:"No major security issues detected."
        });

    }

    let html="";

    priority.forEach((p,index)=>{

        let color="#21d07a";

        if(p.level==="CRITICAL") color="#ff4d6d";
        else if(p.level==="HIGH") color="#ff9f43";
        else if(p.level==="MEDIUM") color="#f7b731";

        html+=`

        <div style="
            border-left:5px solid ${color};
            padding:18px;
            margin-bottom:14px;
            border-radius:12px;
            background:#16243d;
        ">

            <strong>${index+1}. ${p.level}</strong>

            <br><br>

            ${p.text}

        </div>

        `;

    });

    document.getElementById("priority").innerHTML=html;

}

// ========================================
// RECOMMENDATIONS
// ========================================

function buildMeasures(data){

    let list=[];

    if(!data.data.ssl.valid)
        list.push("Install a trusted SSL certificate.");

    if(data.data.headers.missing.length>0)
        list.push("Enable CSP, HSTS and X-Frame-Options headers.");

    if(data.data.ports.open_ports.length>0)
        list.push("Restrict unused network ports using firewall.");

    if(data.data.vulns.sqli)
        list.push("Use parameterized SQL queries to prevent SQL Injection.");

    if(list.length===0)
        list.push("Excellent! No major recommendations.");

    let html="";

    list.forEach(item=>{

        html+=`

        <div>

            ✔ ${item}

        </div>

        `;

    });

    document.getElementById("measures").innerHTML=html;

}

// ========================================
// DOWNLOAD REPORT
// ========================================

function downloadReport(){

    if(currentUrl===""){

        alert("Scan a website first.");

        return;

    }

    window.location.href=`/report?url=${currentUrl}`;

}

// ========================================
// LOAD TREND GRAPH
// ========================================

async function loadTrend(data){

    let response=await fetch("/trend");

    let trend=await response.json();

    if(trend.length===0)
        return;

    let labels=trend.map(item=>item.time.split(" ")[1]);

    let scores=trend.map(item=>Number(item.score));

    let ctx=document
    .getElementById("trendChart")
    .getContext("2d");

    if(chartInstance)
        chartInstance.destroy();

    let color="#21d07a";

    if(data.risk.score<70)
        color="#f7b731";

    if(data.risk.score<40)
        color="#ff4d6d";

    let gradient=ctx.createLinearGradient(0,0,0,350);

    gradient.addColorStop(0,color);
    gradient.addColorStop(1,"rgba(0,0,0,0)");

    chartInstance=new Chart(ctx,{

        type:"line",

        data:{

            labels:labels,

            datasets:[{

                label:"Security Score",

                data:scores,

                borderColor:color,

                backgroundColor:gradient,

                fill:true,

                borderWidth:3,

                tension:.45,

                pointRadius:5,

                pointHoverRadius:8,

                pointBackgroundColor:color

            }]

        },

        options:{

            responsive:true,

            maintainAspectRatio:false,

            plugins:{

                legend:{

                    labels:{
                        color:"#ffffff"
                    }

                }

            },

            scales:{

                x:{

                    ticks:{
                        color:"#9aa7bd"
                    },

                    grid:{
                        color:"rgba(255,255,255,.05)"
                    }

                },

                y:{

                    min:0,
                    max:100,

                    ticks:{
                        color:"#9aa7bd"
                    },

                    grid:{
                        color:"rgba(255,255,255,.05)"
                    }

                }

            }

        }

    });

}

// ========================================
// PAGE LOAD
// ========================================

window.onload=function(){

    loadTrend({
        risk:{
            score:80
        }
    });

}
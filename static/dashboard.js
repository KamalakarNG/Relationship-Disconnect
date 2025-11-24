const ctx = document.getElementById('pciChart').getContext('2d');
const pciData = {labels: [], datasets: [{label:'PCI', data:[], fill:false}, {label:'Disconnect', data:[], fill:false}] };
const chart = new Chart(ctx, { type:'line', data:pciData });

async function sendSample() {
  const payload = {
    hrv_change: parseFloat(document.getElementById('hrv').value),
    tone_shift: parseFloat(document.getElementById('tone').value),
    breath_sync: parseFloat(document.getElementById('breath').value),
    micro_neg: parseFloat(document.getElementById('micro').value),
    micro_pos: 0.05
  };
  const res = await fetch('/api/pci', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify(payload)});
  const j = await res.json();
  pushPoint(j);
}

document.getElementById('send').addEventListener('click', sendSample);

function pushPoint(entry){
  const ts = new Date(entry.ts);
  pciData.labels.push(ts.toLocaleTimeString());
  pciData.datasets[0].data.push(entry.pci);
  pciData.datasets[1].data.push(entry.disconnect_score);
  if(pciData.labels.length>60){ pciData.labels.shift(); pciData.datasets.forEach(d=>d.data.shift()); }
  chart.update();
}

async function pollInit(){
  const res = await fetch('/api/timeline');
  const arr = await res.json();
  arr.forEach(pushPoint);
}
window.onload = pollInit;

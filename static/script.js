const formatRadios = document.querySelectorAll('input[name="format"]');
const qualitySelect = document.getElementById('quality');

const audioOptions = ["190k", "256k", "320k"];
const videoOptions = ["360p", "480p", "720p", "1080p"];

function updateOptions() {
  const selected = document.querySelector('input[name="format"]:checked').value;
  qualitySelect.innerHTML = "";

  const options = selected === "audio" ? audioOptions : videoOptions;
  options.forEach(opt => {
    const o = document.createElement("option");
    o.value = opt;
    o.innerText = opt;
    qualitySelect.appendChild(o);
  });
}

formatRadios.forEach(r => r.addEventListener("change", updateOptions));
window.onload = updateOptions;

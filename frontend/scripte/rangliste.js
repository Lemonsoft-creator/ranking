document.addEventListener("DOMContentLoaded", () => {
    fetchAndDisplayRankingData();
  });
  
  async function fetchAndDisplayRankingData() {
    try {
      const data = await fetchRankingData("/rangliste_daten");
      const sortedKeys = sortGroupKeys(data);
      renderRankingGroups(data, sortedKeys);
    } catch (error) {
      console.error("Fehler beim Laden der Ranglistendaten:", error);
    }
  }
  
  async function fetchRankingData(endpoint) {
    const response = await fetch(endpoint);
    if (!response.ok) {
      throw new Error(`HTTP-Fehler: ${response.status}`);
    }
    return await response.json();
  }
  
  function sortGroupKeys(data) {
    return Object.keys(data).sort((a, b) => {
      const [genderA, classA] = a.split(" - ");
      const [genderB, classB] = b.split(" - ");
  
      const weightValue = klass => {
        const num = parseFloat(klass.replace("+", "").replace("-", "").replace("kg", ""));
        return klass.includes("+") ? num + 1000 : num;
      };
  
      if (genderA !== genderB) {
        return genderA === "Maennlich" ? -1 : 1;
      }
  
      return weightValue(classB) - weightValue(classA);
    });
  }
  
  function renderRankingGroups(data, sortedKeys) {
    sortedKeys.forEach(key => {
      const [gender, weightClass] = key.split(" - ");
      const participants = data[key];
      const sectionId = gender.toLowerCase();
      const groupElement = createRankingGroupElement(weightClass, participants);
      document.getElementById(sectionId)?.appendChild(groupElement);
    });
  }
  
  function createRankingGroupElement(weightClass, participants) {
    const container = document.createElement("div");
    container.className = "gruppe";
  
    const tableRows = participants.map((participant, index) => {
      const place = getPlaceSymbol(index);
      return `
        <tr>
          <td class="medaille ${place}">${place}</td>
          <td>${participant.pseudonym}</td>
          <td>${participant.max_schlagkraft.toFixed(1)}</td>
        </tr>`;
    }).join("");
  
    container.innerHTML = `
      <h3>${weightClass}</h3>
      <table>
        <thead>
          <tr><th>Platz</th><th>Pseudonym</th><th>💪 Schlagkraft (kg)</th></tr>
        </thead>
        <tbody>${tableRows}</tbody>
      </table>`;
  
    return container;
  }
  
  function getPlaceSymbol(index) {
    switch (index) {
      case 0: return "🥇";
      case 1: return "🥈";
      case 2: return "🥉";
      default: return (index + 1).toString();
    }
  }
  
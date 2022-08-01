const peticion = new XMLHttpRequest();

function obtenerMovimientos() {
  console.log("Obteniendo movimientos");
  peticion.open('GET', 'http://127.0.0.1:5000/api/v1/movimientos', true);
  peticion.send();
  console.log("FIN de obtener movimientos");
}

function mostrarMovimientos() {
  console.log('entramos en mostrar movimientos');
  const tabla = document.querySelector('#cuerpo-tabla');

  if (this.readyState === 4 && this.status === 200) {
    console.log('--- TODO OK ----');
    const respuesta = JSON.parse(peticion.responseText);
    const movimientos = respuesta.data;
    

    let html = '';
    for (let i = 0; i < movimientos.length; i = i + 1) {
      const mov = movimientos[i];
      html = html + `
        <tr>
        <td>${mov.date}</td>
        <td>${mov.time}</td>
        <td>${mov.moneda_from}</td>
        <td>${mov.cantidad_from}</td>
        <td>${mov.moneda_to}</td>
        <td>${mov.cantidad_to}</td>
        </tr>
      `;
    }

    tabla.innerHTML = html;
  } else {
    console.error('---- Algo ha ido mal en la petición ----');
    alert('Error al cargar los movimientos');
  }
  console.log('FIN de mostrar movimientos');
}

window.onload = function () {
  console.log('Inicio de window.onload');
  obtenerMovimientos();
  peticion.onload = mostrarMovimientos;

  const boton = document.querySelector('#boton-recarga');
  boton.addEventListener('click', obtenerMovimientos);
};

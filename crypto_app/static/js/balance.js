const peticion_movimientos = new XMLHttpRequest();
const peticion_rate = new XMLHttpRequest();
const peticion_compra = new XMLHttpRequest();
const peticion_status = new XMLHttpRequest();
const peticion_monedas = new XMLHttpRequest();
let tema_dark = true;
function obtenerMovimientos() {
  peticion_movimientos.open('GET', 'http://127.0.0.1:5000/api/v1/movimientos', true);
  peticion_movimientos.send();
}
function obtenerEstadoCuenta() {
  peticion_status.open('GET', 'http://127.0.0.1:5000/api/v1/status', true);
  peticion_status.send();
}
function obtenerMonedasDisponibles(){
  peticion_monedas.open('GET', 'http://127.0.0.1:5000/api/v1/monedas_disponibles_usuario', true);
  peticion_monedas.send();
}
function mostrarMonedasDisponibles(){
  const select_from = document.querySelector('#moneda_from');
  const select_to = document.querySelector('#moneda_to');
  if (this.readyState === 4 && this.status === 200) {
    const respuesta = JSON.parse(this.responseText);
    const monedas = respuesta;
    console.log(monedas)
    let html = '';
    for (let i = 0; i < monedas.length; i = i + 1) {
      html += `<option value="${monedas[i]}">${monedas[i]}</option>`;
    }
    select_from.innerHTML = html;
    select_to.innerHTML = html;
  }
}
function mostrarEstadoCuenta(){
  const tabla_estado = document.querySelector('#cuerpo-tabla-estado');
  let html = '';
  
  if (this.readyState === 4 && this.status === 200) {
    const respuesta = JSON.parse(this.responseText);
    console.log(respuesta)
    let estado_cuenta = respuesta.data;
    const monedas = Object.keys(estado_cuenta);
    const valores = Object.values(estado_cuenta);
    if (monedas.length === 0) {
      html = '<tr><td>No hay movimientos para mostrar</td></tr>';
    }
    else{
    for (let i = 0; i < monedas.length; i = i + 1) {
      html += `
        <tr>
          <td>${monedas[i]}</td>
          <td>${valores[i]}</td>
        </tr>
      `;
    }
  }
    tabla_estado.innerHTML = html;
  }

}
function mostrarMovimientos() {
  const tabla = document.querySelector('#cuerpo-tabla');
  const mensajes = document.querySelector("#mensajes-control")
  let html = '';
  if (this.readyState === 4 && this.status === 200) {
    const respuesta = JSON.parse(peticion_movimientos.responseText);
    const movimientos = respuesta.data;
    if (movimientos.length === 0) {
      mensajes.innerHTML = 'No hay movimientos para mostrar';
    }
    
    if(movimientos.length >= 1){
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
    
  }
  tabla.innerHTML = html; 
  } 
  else {
    alert('Error al cargar los movimientos');
  }
}

function obtenerConversion() {
  //Probar a crear la peticion aqui dentro
  const moneda_from = document.querySelector('#moneda_from').value;
  const moneda_to = document.querySelector('#moneda_to').value;
  let cantidad = document.querySelector('#cantidad_from').value;
  cantidad = parseFloat(cantidad);
  cantidad = cantidad.toFixed(2);

  peticion_rate.open('GET', `http://127.0.0.1:5000/api/v1/rate/${moneda_from}/${moneda_to}/${cantidad}`, false);
  peticion_rate.send();
  if(peticion_rate.status === 404){
    alert("No se pudo realizar la conversion, revisa los datos o intentalo mas tarde")
  }
  if (peticion_rate.readyState === 4 && peticion_rate.status === 200) {
    const respuesta = JSON.parse(peticion_rate.responseText);
    const datos = respuesta.data;
    document.getElementById("conversion").value = datos.tipo_cambio.toFixed(2);
  }
}

function compraMonedas() {
  const moneda_from = document.querySelector('#moneda_from').value;
  const moneda_to = document.querySelector('#moneda_to').value;
  let cantidad_from = parseFloat(document.querySelector('#cantidad_from').value);
  
  cantidad_from = parseFloat(cantidad_from);
  cantidad_from = cantidad_from.toFixed(2);
  
  peticion_rate.open('GET', `http://127.0.0.1:5000/api/v1/rate/${moneda_from}/${moneda_to}/${cantidad_from}`, false);
  peticion_rate.send();
  if (peticion_rate.readyState === 4 && peticion_rate.status === 200) {
    const respuesta = JSON.parse(peticion_rate.responseText);
    const datos = respuesta.data;
    const cantidad_to = datos.tipo_cambio.toFixed(2);
    output_aux = {"moneda_from": moneda_from, "cantidad_from": cantidad_from, "moneda_to": moneda_to, "cantidad_to": cantidad_to};
    output = {"data": output_aux};
    peticion_compra.open('POST', 'http://127.0.0.1:5000/api/v1/movimiento', true);
    peticion_compra.setRequestHeader('Content-Type', 'application/json;charset=utf-8');
    peticion_compra.send(JSON.stringify(output_aux));
    peticion_compra.onload = location.reload()
  }
}


window.onload = function() {
  obtenerMovimientos();
  peticion_movimientos.onload = mostrarMovimientos; //request de html
  
  obtenerEstadoCuenta();
  peticion_status.onload = mostrarEstadoCuenta;
  
  obtenerMonedasDisponibles();
  peticion_monedas.onload = mostrarMonedasDisponibles;
  
  const boton_conversion = document.querySelector('#boton-convertir'); //funciona mediante el #id de html
  boton_conversion.addEventListener('click', obtenerConversion);

  const boton_compra = document.querySelector('#boton-comprar');
  boton_compra.addEventListener('click', compraMonedas)

};

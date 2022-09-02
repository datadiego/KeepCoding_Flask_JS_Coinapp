const peticion_movimientos = new XMLHttpRequest();
const peticion_rate = new XMLHttpRequest();
const peticion_compra = new XMLHttpRequest();

function obtenerMovimientos() {
  console.log("####################")
  console.log("Obteniendo movimientos");
  peticion_movimientos.open('GET', 'http://127.0.0.1:5000/api/v1/movimientos', true);
  peticion_movimientos.send();
  console.log("FIN de obtener movimientos");
}

function mostrarMovimientos() {
  console.log('entramos en mostrar movimientos');
  const tabla = document.querySelector('#cuerpo-tabla');

  if (this.readyState === 4 && this.status === 200) {
    console.log('--- TODO OK ----');
    const respuesta = JSON.parse(peticion_movimientos.responseText);
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

function obtenerConversion() {
  //Probar a crear la peticion aqui dentro
  console.log("######################")
  console.log('entramos en obtener conversion');
  const moneda_from = document.querySelector('#moneda_from').value;
  const moneda_to = document.querySelector('#moneda_to').value;
  let cantidad = document.querySelector('#cantidad_from').value;
  cantidad = parseFloat(cantidad);
  cantidad = cantidad.toFixed(2);
  console.log("moneda_from: " + moneda_from);
  console.log("moneda_to: " + moneda_to);
  console.log("cantidad: " + cantidad);

  peticion_rate.open('GET', `http://127.0.0.1:5000/api/v1/rate/${moneda_from}/${moneda_to}/${cantidad}`, false);
  peticion_rate.send();
  if(peticion_rate.status === 404){
    alert("No se pudo realizar la conversion, revisa los datos o intentalo mas tarde")

  }
  if (peticion_rate.readyState === 4 && peticion_rate.status === 200) {
    console.log('--- TODO OK ----');
    const respuesta = JSON.parse(peticion_rate.responseText);
    const datos = respuesta.data;
    console.log(datos);
    document.getElementById("conversion").value = datos.tipo_cambio.toFixed(2);
  }
  
}

function compraMonedas() {
  console.log("######################")
  console.log('entramos en obtener conversion');
  const moneda_from = document.querySelector('#moneda_from').value;
  const moneda_to = document.querySelector('#moneda_to').value;
  let cantidad_from = parseFloat(document.querySelector('#cantidad_from').value);
  
  cantidad_from = parseFloat(cantidad_from);
  cantidad_from = cantidad_from.toFixed(2);
  

  peticion_rate.open('GET', `http://127.0.0.1:5000/api/v1/rate/${moneda_from}/${moneda_to}/${cantidad_from}`, false);
  peticion_rate.send();
  if (peticion_rate.readyState === 4 && peticion_rate.status === 200) {
    console.log('--- TODO OK ----');
    const respuesta = JSON.parse(peticion_rate.responseText);
    const datos = respuesta.data;
    const cantidad_to = datos.tipo_cambio.toFixed(2);
    output_aux = {"moneda_from": moneda_from, "cantidad_from": cantidad_from, "moneda_to": moneda_to, "cantidad_to": cantidad_to};
    output = {"data": output_aux};
    peticion_compra.open('POST', 'http://127.0.0.1:5000/api/v1/movimiento', true);
    peticion_compra.setRequestHeader('Content-Type', 'application/json;charset=utf-8');
    //console.log(data);
    peticion_compra.send(JSON.stringify(output_aux));
  }
}

window.onload = function() {
  console.log('Inicio de window.onload');
  obtenerMovimientos();
  peticion_movimientos.onload = mostrarMovimientos; //request de html

  const boton_conversion = document.querySelector('#boton-convertir'); //funciona mediante el #id de html
  boton_conversion.addEventListener('click', obtenerConversion);

  const boton_compra = document.querySelector('#boton-comprar');
  boton_compra.addEventListener('click', compraMonedas) 
};

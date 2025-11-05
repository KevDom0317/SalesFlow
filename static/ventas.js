// Cargar clientes y productos al iniciar
document.addEventListener('DOMContentLoaded', function() {
    cargarClientes();
    cargarProductos();
    cargarVentas();
    
    // Event listeners
    document.getElementById('ventaForm').addEventListener('submit', crearVenta);
    document.getElementById('btnCancelar').addEventListener('click', resetForm);
    document.getElementById('btnRefresh').addEventListener('click', cargarVentas);
    document.getElementById('searchInput').addEventListener('input', buscarVentas);
    
    // Calcular total cuando cambia cantidad o producto
    document.getElementById('id_producto').addEventListener('change', calcularTotal);
    document.getElementById('cantidad').addEventListener('input', calcularTotal);
});

// Cargar lista de clientes
async function cargarClientes() {
    try {
        const response = await fetch('/api/clientes');
        const data = await response.json();
        
        const select = document.getElementById('id_cliente');
        select.innerHTML = '<option value="">Seleccionar cliente...</option>';
        
        if (data.success && data.data) {
            data.data.forEach(cliente => {
                const option = document.createElement('option');
                option.value = cliente.id_cliente;
                option.textContent = `${cliente.nombre} (${cliente.correo})`;
                select.appendChild(option);
            });
        }
    } catch (error) {
        console.error('Error al cargar clientes:', error);
    }
}

// Cargar lista de productos
async function cargarProductos() {
    try {
        const response = await fetch('/api/productos');
        const data = await response.json();
        
        const select = document.getElementById('id_producto');
        select.innerHTML = '<option value="">Seleccionar producto...</option>';
        
        if (data.success && data.data) {
            data.data.forEach(producto => {
                const option = document.createElement('option');
                option.value = producto.id_producto;
                option.textContent = `${producto.nombre} - $${producto.precio}`;
                option.dataset.precio = producto.precio;
                select.appendChild(option);
            });
        }
    } catch (error) {
        console.error('Error al cargar productos:', error);
    }
}

// Calcular total
function calcularTotal() {
    const productoSelect = document.getElementById('id_producto');
    const cantidadInput = document.getElementById('cantidad');
    const precioUnitarioInput = document.getElementById('precio_unitario');
    const totalInput = document.getElementById('total');
    
    const selectedOption = productoSelect.options[productoSelect.selectedIndex];
    const precio = parseFloat(selectedOption.dataset.precio || 0);
    const cantidad = parseInt(cantidadInput.value) || 0;
    
    precioUnitarioInput.value = precio.toFixed(2);
    totalInput.value = (precio * cantidad).toFixed(2);
}

// Crear nueva venta
async function crearVenta(e) {
    e.preventDefault();
    
    const formData = {
        id_cliente: parseInt(document.getElementById('id_cliente').value),
        id_producto: parseInt(document.getElementById('id_producto').value),
        cantidad: parseInt(document.getElementById('cantidad').value)
    };
    
    try {
        const response = await fetch('/api/ventas', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });
        
        const data = await response.json();
        
        if (data.success) {
            alert('Venta creada exitosamente');
            resetForm();
            cargarVentas();
        } else {
            alert('Error: ' + data.error);
        }
    } catch (error) {
        console.error('Error al crear venta:', error);
        alert('Error al crear la venta');
    }
}

// Cargar todas las ventas
async function cargarVentas() {
    try {
        const response = await fetch('/api/ventas');
        const data = await response.json();
        
        const tbody = document.getElementById('ventasTableBody');
        
        if (data.success && data.data) {
            if (data.data.length === 0) {
                tbody.innerHTML = '<tr><td colspan="7" class="loading">No hay ventas registradas</td></tr>';
                return;
            }
            
            tbody.innerHTML = data.data.map(venta => `
                <tr>
                    <td>${venta.id_venta}</td>
                    <td>${venta.cliente_nombre}</td>
                    <td>${venta.producto_nombre}</td>
                    <td>${venta.cantidad}</td>
                    <td>$${parseFloat(venta.total).toFixed(2)}</td>
                    <td>${new Date(venta.fecha).toLocaleString('es-ES')}</td>
                    <td>
                        <button class="btn btn-success" onclick="verFactura(${venta.id_venta})">Factura</button>
                        <button class="btn btn-danger" onclick="eliminarVenta(${venta.id_venta})">Eliminar</button>
                    </td>
                </tr>
            `).join('');
        } else {
            tbody.innerHTML = '<tr><td colspan="7" class="loading">Error al cargar ventas</td></tr>';
        }
    } catch (error) {
        console.error('Error al cargar ventas:', error);
        document.getElementById('ventasTableBody').innerHTML = 
            '<tr><td colspan="7" class="loading">Error al cargar ventas</td></tr>';
    }
}

// Buscar ventas
async function buscarVentas() {
    const searchTerm = document.getElementById('searchInput').value.toLowerCase();
    const rows = document.querySelectorAll('#ventasTableBody tr');
    
    rows.forEach(row => {
        const text = row.textContent.toLowerCase();
        row.style.display = text.includes(searchTerm) ? '' : 'none';
    });
}

// Ver factura
async function verFactura(idVenta) {
    try {
        const response = await fetch(`/api/facturas/${idVenta}`);
        const data = await response.json();
        
        if (data.success) {
            mostrarFactura(data.factura);
        } else {
            alert('Error: ' + data.error);
        }
    } catch (error) {
        console.error('Error al obtener factura:', error);
        alert('Error al obtener la factura');
    }
}

// Mostrar factura en modal o ventana
function mostrarFactura(factura) {
    const facturaHTML = `
        <div class="factura-container">
            <div class="factura-header">
                <h2>FACTURA #${factura.numero_factura}</h2>
                <p>Fecha: ${new Date(factura.fecha).toLocaleDateString('es-ES')}</p>
            </div>
            <div class="factura-cliente">
                <h3>Cliente:</h3>
                <p><strong>${factura.cliente.nombre}</strong></p>
                <p>${factura.cliente.correo}</p>
                <p>${factura.cliente.telefono || ''}</p>
                <p>${factura.cliente.direccion || ''}</p>
            </div>
            <div class="factura-items">
                <h3>Items:</h3>
                <div class="factura-item" style="font-weight: bold; background: #f5f5f5;">
                    <div>Producto</div>
                    <div>Cantidad</div>
                    <div>Precio Unit.</div>
                    <div>Subtotal</div>
                </div>
                ${factura.items.map(item => `
                    <div class="factura-item">
                        <div>${item.producto}</div>
                        <div>${item.cantidad}</div>
                        <div>$${item.precio_unitario.toFixed(2)}</div>
                        <div>$${item.subtotal.toFixed(2)}</div>
                    </div>
                `).join('')}
            </div>
            <div class="factura-totals">
                <p><strong>Total: $${factura.total.toFixed(2)}</strong></p>
            </div>
        </div>
    `;
    
    // Mostrar en ventana nueva o alerta
    const nuevaVentana = window.open('', '_blank', 'width=800,height=600');
    nuevaVentana.document.write(`
        <html>
            <head>
                <title>Factura #${factura.numero_factura}</title>
                <style>
                    body { font-family: Arial, sans-serif; padding: 20px; }
                    .factura-container { max-width: 700px; margin: 0 auto; }
                    .factura-header { text-align: center; border-bottom: 2px solid #667eea; padding-bottom: 20px; margin-bottom: 20px; }
                    .factura-item { display: grid; grid-template-columns: 2fr 1fr 1fr 1fr; gap: 10px; padding: 10px; border-bottom: 1px solid #ddd; }
                    .factura-totals { margin-top: 20px; text-align: right; padding-top: 20px; border-top: 2px solid #667eea; }
                </style>
            </head>
            <body>
                ${facturaHTML}
            </body>
        </html>
    `);
    nuevaVentana.document.close();
}

// Eliminar venta
async function eliminarVenta(idVenta) {
    if (!confirm('¿Está seguro de eliminar esta venta?')) {
        return;
    }
    
    try {
        const response = await fetch(`/api/ventas/${idVenta}`, {
            method: 'DELETE'
        });
        
        const data = await response.json();
        
        if (data.success) {
            alert('Venta eliminada exitosamente');
            cargarVentas();
        } else {
            alert('Error: ' + data.error);
        }
    } catch (error) {
        console.error('Error al eliminar venta:', error);
        alert('Error al eliminar la venta');
    }
}

// Resetear formulario
function resetForm() {
    document.getElementById('ventaForm').reset();
    document.getElementById('precio_unitario').value = '';
    document.getElementById('total').value = '';
}


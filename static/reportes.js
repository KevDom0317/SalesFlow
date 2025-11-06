// Cargar clientes y productos al iniciar
document.addEventListener('DOMContentLoaded', function() {
    cargarClientes();
    cargarProductos();
    
    // Event listeners
    document.getElementById('reporteForm').addEventListener('submit', generarReporte);
    document.getElementById('facturaForm').addEventListener('submit', generarFactura);
});

// Cargar lista de clientes
async function cargarClientes() {
    try {
        const response = await fetch('/api/clientes');
        const data = await response.json();
        
        const selectReporte = document.getElementById('reporte_cliente');
        
        if (data.success && data.data) {
            data.data.forEach(cliente => {
                const option = document.createElement('option');
                option.value = cliente.id_cliente;
                option.textContent = `${cliente.nombre} (${cliente.correo})`;
                selectReporte.appendChild(option);
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
        
        const select = document.getElementById('reporte_producto');
        
        if (data.success && data.data) {
            data.data.forEach(producto => {
                const option = document.createElement('option');
                option.value = producto.id_producto;
                option.textContent = `${producto.nombre}`;
                select.appendChild(option);
            });
        }
    } catch (error) {
        console.error('Error al cargar productos:', error);
    }
}

// Generar reporte de ventas
async function generarReporte(e) {
    e.preventDefault();
    
    const formData = new FormData(e.target);
    const params = new URLSearchParams();
    
    // Agregar parámetros solo si tienen valor
    if (formData.get('id_cliente')) {
        params.append('id_cliente', formData.get('id_cliente'));
    }
    if (formData.get('id_producto')) {
        params.append('id_producto', formData.get('id_producto'));
    }
    if (formData.get('fecha_inicio')) {
        params.append('fecha_inicio', formData.get('fecha_inicio'));
    }
    if (formData.get('fecha_fin')) {
        params.append('fecha_fin', formData.get('fecha_fin'));
    }
    
    try {
        const url = `/api/reportes/ventas${params.toString() ? '?' + params.toString() : ''}`;
        const response = await fetch(url);
        const data = await response.json();
        
        if (data.success) {
            mostrarReporte(data.reporte);
        } else {
            mostrarError(data.error);
        }
    } catch (error) {
        console.error('Error al generar reporte:', error);
        mostrarError('Error al generar el reporte');
    }
}

// Mostrar reporte
function mostrarReporte(reporte) {
    const container = document.getElementById('resultsContainer');
    
    const reporteHTML = `
        <div class="reporte-container">
            <div class="reporte-header">
                <h3>${reporte.titulo}</h3>
                <p><strong>Tipo:</strong> ${reporte.tipo}</p>
                <p><strong>Fecha de Generación:</strong> ${new Date(reporte.fecha_generacion).toLocaleString('es-ES')}</p>
                <p><strong>Filtros Aplicados:</strong></p>
                <ul>
                    ${Object.keys(reporte.filtros_aplicados).length > 0 
                        ? Object.entries(reporte.filtros_aplicados).map(([key, value]) => 
                            `<li><strong>${key}:</strong> ${value}</li>`
                          ).join('')
                        : '<li>Ningún filtro aplicado (mostrando todas las ventas)</li>'
                    }
                </ul>
            </div>
            
            <div class="reporte-metricas">
                <div class="metrica-card">
                    <h3>Total de Ventas</h3>
                    <div class="valor">${reporte.metricas.total_ventas}</div>
                </div>
                <div class="metrica-card">
                    <h3>Total en Monto</h3>
                    <div class="valor">$${reporte.metricas.total_monto.toFixed(2)}</div>
                </div>
                <div class="metrica-card">
                    <h3>Promedio por Venta</h3>
                    <div class="valor">$${reporte.metricas.promedio_venta.toFixed(2)}</div>
                </div>
                <div class="metrica-card">
                    <h3>Items Vendidos</h3>
                    <div class="valor">${reporte.metricas.cantidad_items}</div>
                </div>
            </div>
            
            <h4 style="margin-top: 30px; color: #667eea;">Datos del Reporte:</h4>
            <div class="table-container">
                <table class="data-table">
                    <thead>
                        <tr>
                            <th>ID Venta</th>
                            <th>Cliente</th>
                            <th>Producto</th>
                            <th>Cantidad</th>
                            <th>Total</th>
                            <th>Fecha</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${reporte.datos.length > 0 
                            ? reporte.datos.map(venta => `
                                <tr>
                                    <td>${venta.id_venta}</td>
                                    <td>${venta.cliente_nombre}</td>
                                    <td>${venta.producto_nombre}</td>
                                    <td>${venta.cantidad}</td>
                                    <td>$${parseFloat(venta.total).toFixed(2)}</td>
                                    <td>${new Date(venta.fecha).toLocaleString('es-ES')}</td>
                                </tr>
                            `).join('')
                            : '<tr><td colspan="6" class="loading">No hay datos para mostrar</td></tr>'
                        }
                    </tbody>
                </table>
            </div>
            
            <div style="margin-top: 20px;">
                <h4 style="color: #667eea;">JSON del Reporte:</h4>
                <div class="json-output">${JSON.stringify(reporte, null, 2)}</div>
            </div>
        </div>
    `;
    
    container.innerHTML = reporteHTML;
}

// Generar factura
async function generarFactura(e) {
    e.preventDefault();
    
    const idVenta = document.getElementById('factura_venta').value;
    
    if (!idVenta) {
        mostrarError('Por favor ingrese un ID de venta');
        return;
    }
    
    try {
        const response = await fetch(`/api/facturas/${idVenta}`);
        const data = await response.json();
        
        if (data.success) {
            mostrarFactura(data.factura);
        } else {
            mostrarError(data.error);
        }
    } catch (error) {
        console.error('Error al generar factura:', error);
        mostrarError('Error al generar la factura');
    }
}

// Mostrar factura
function mostrarFactura(factura) {
    const container = document.getElementById('resultsContainer');
    
    const facturaHTML = `
        <div class="factura-container">
            <div class="factura-header">
                <h2>FACTURA #${factura.numero_factura}</h2>
                <p><strong>Fecha:</strong> ${new Date(factura.fecha).toLocaleDateString('es-ES')}</p>
                <p><strong>Estado:</strong> ${factura.estado}</p>
            </div>
            
            <div class="factura-cliente">
                <h3>Datos del Cliente:</h3>
                <p><strong>Nombre:</strong> ${factura.cliente.nombre}</p>
                <p><strong>Correo:</strong> ${factura.cliente.correo}</p>
                ${factura.cliente.telefono ? `<p><strong>Teléfono:</strong> ${factura.cliente.telefono}</p>` : ''}
                ${factura.cliente.direccion ? `<p><strong>Dirección:</strong> ${factura.cliente.direccion}</p>` : ''}
            </div>
            
            <div class="factura-items">
                <h3>Items de la Factura:</h3>
                <div class="factura-item" style="font-weight: bold; background: #f5f5f5;">
                    <div>Producto</div>
                    <div>Cantidad</div>
                    <div>Precio Unitario</div>
                    <div>Subtotal</div>
                </div>
                ${factura.items.map(item => `
                    <div class="factura-item">
                        <div>
                            <strong>${item.producto}</strong>
                            ${item.descripcion ? `<br><small>${item.descripcion}</small>` : ''}
                        </div>
                        <div>${item.cantidad}</div>
                        <div>$${item.precio_unitario.toFixed(2)}</div>
                        <div>$${item.subtotal.toFixed(2)}</div>
                    </div>
                `).join('')}
            </div>
            
            <div class="factura-totals">
                <p><strong>Subtotal: $${factura.subtotal.toFixed(2)}</strong></p>
                <p><strong style="font-size: 1.3em;">Total: $${factura.total.toFixed(2)}</strong></p>
            </div>
            
            <div style="margin-top: 20px;">
                <h4 style="color: #667eea;">JSON de la Factura:</h4>
                <div class="json-output">${JSON.stringify(factura, null, 2)}</div>
            </div>
        </div>
    `;
    
    container.innerHTML = facturaHTML;
}

// Mostrar error
function mostrarError(mensaje) {
    const container = document.getElementById('resultsContainer');
    container.innerHTML = `
        <div class="message error">
            <strong>Error:</strong> ${mensaje}
        </div>
    `;
}


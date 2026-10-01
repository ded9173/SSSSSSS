{% extends "base-dashboard.html" %}

{% block title %}Спецификации{% endblock %}
{% block content %}
<script>
    let productsList = [];
    let materialsList = [];
    let operationsList = [];

    async function loadProducts() {
        try {
            const res = await fetch('/api/products/', { credentials: 'include' });
            const data = await res.json();
            productsList = data.products || [];
        } catch (e) {
            productsList = [];
        }
    }

    async function loadMaterials() {
        try {
            const res = await fetch('/api/materials/', { credentials: 'include' });
            const data = await res.json();
            materialsList = data.materials || [];
        } catch (e) {
            materialsList = [];
        }
    }

    async function loadOperations() {
        try {
            const res = await fetch('/api/operations/', { credentials: 'include' });
            const data = await res.json();
            operationsList = data.operations || [];
        } catch (e) {
            operationsList = [];
        }
    }

    async function loadSpecMaterials() {
        try {
            const response = await fetch('/api/specifications/materials/', { credentials: 'include' });
            const data = await response.json();
            const tbody = document.getElementById('specMaterialsTableBody');
            
            if (!data.specifications || data.specifications.length === 0) {
                tbody.innerHTML = '<tr><td colspan="6" class="empty-state">Спецификаций материалов пока нет</td></tr>';
                return;
            }

            tbody.innerHTML = '';
            data.specifications.forEach(spec => {
                const tr = document.createElement('tr');
                tr.innerHTML = `
                    <td>${spec.product_name || '—'}</td>
                    <td>${spec.material_name || '—'}</td>
                    <td>${spec.quantity_per_unit}</td>
                    <td>${spec.material_price} ₽</td>
                    <td>${spec.total_price.toFixed(2)} ₽</td>
                `;
                tbody.appendChild(tr);
            });
        } catch (error) {
            showNotification('error', 'Ошибка', 'Не удалось загрузить данные');
        }
    }

    async function loadSpecOperations() {
        try {
            const response = await fetch('/api/specifications/operations/', { credentials: 'include' });
            const data = await response.json();
            const tbody = document.getElementById('specOperationsTableBody');
            
            if (!data.specifications || data.specifications.length === 0) {
                tbody.innerHTML = '<tr><td colspan="6" class="empty-state">Спецификаций операций пока нет</td></tr>';
                return;
            }

            tbody.innerHTML = '';
            data.specifications.forEach(spec => {
                const tr = document.createElement('tr');
                tr.innerHTML = `
                    <td>${spec.product_name || '—'}</td>
                    <td>${spec.operation_name || '—'}</td>
                    <td>${spec.time_norm} ч</td>
                    <td>${spec.op_quantity}</td>
                    <td>${spec.operation_price} ₽/ч</td>
                    <td>${spec.total_price.toFixed(2)} ₽</td>
                `;
                tbody.appendChild(tr);
            });
        } catch (error) {
            showNotification('error', 'Ошибка', 'Не удалось загрузить данные');
        }
    }

    function openAddSpecMaterialModal() {
        document.getElementById('specMaterialForm').reset();
        populateProductSelect('specMatProductId', '');
        populateMaterialSelect('specMatMaterialId', '');
        openModal('specMaterialModal');
    }

    function openAddSpecOperationModal() {
        document.getElementById('specOperationForm').reset();
        populateProductSelect('specOpProductId', '');
        populateOperationSelect('specOpOperationId', '');
        openModal('specOperationModal');
    }

    function populateProductSelect(selectId, currentValue) {
        const select = document.getElementById(selectId);
        select.innerHTML = '<option value="">Выберите продукцию...</option>' + 
            productsList.map(p => `<option value="${p.product_id}" ${p.product_id === currentValue ? 'selected' : ''}>${p.name} (${p.code})</option>`).join('');
    }

    function populateMaterialSelect(selectId, currentValue) {
        const select = document.getElementById(selectId);
        select.innerHTML = '<option value="">Выберите материал...</option>' + 
            materialsList.map(m => `<option value="${m.material_id}" ${m.material_id === currentValue ? 'selected' : ''}>${m.name} (${m.code})</option>`).join('');
    }

    function populateOperationSelect(selectId, currentValue) {
        const select = document.getElementById(selectId);
        select.innerHTML = '<option value="">Выберите операцию...</option>' + 
            operationsList.map(o => `<option value="${o.operation_id}" ${o.operation_id === currentValue ? 'selected' : ''}>${o.name} (${o.code})</option>`).join('');
    }

    async function saveSpecMaterial(event) {
        event.preventDefault();
        const data = {
            product_id: document.getElementById('specMatProductId').value,
            material_id: document.getElementById('specMatMaterialId').value,
            quantity_per_unit: parseFloat(document.getElementById('specMatQuantity').value)
        };

        if (!data.product_id || !data.material_id) {
            showNotification('error', 'Ошибка', 'Выберите продукцию и материал');
            return;
        }

        try {
            const response = await fetch('/api/specifications/materials/', {
                method: 'POST',
                credentials: 'include',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });
            const result = await response.json();
            if (!response.ok) throw new Error(result.message || 'Error');
            showNotification('success', 'Успех', result.message || 'Спецификация создана');
            closeModal('specMaterialModal');
            loadSpecMaterials();
        } catch (error) {
            showNotification('error', 'Ошибка', error.message);
        }
    }

    async function saveSpecOperation(event) {
        event.preventDefault();
        const data = {
            product_id: document.getElementById('specOpProductId').value,
            operation_id: document.getElementById('specOpOperationId').value,
            time_norm: parseFloat(document.getElementById('specOpTimeNorm').value) || 1.0,
            op_quantity: parseFloat(document.getElementById('specOpQuantity').value) || 1.0
        };

        if (!data.product_id || !data.operation_id) {
            showNotification('error', 'Ошибка', 'Выберите продукцию и операцию');
            return;
        }

        try {
            const response = await fetch('/api/specifications/operations/', {
                method: 'POST',
                credentials: 'include',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });
            const result = await response.json();
            if (!response.ok) throw new Error(result.message || 'Error');
            showNotification('success', 'Успех', result.message || 'Спецификация создана');
            closeModal('specOperationModal');
            loadSpecOperations();
        } catch (error) {
            showNotification('error', 'Ошибка', error.message);
        }
    }

    document.addEventListener('DOMContentLoaded', () => {
        loadSpecMaterials();
        loadSpecOperations();
        loadProducts();
        loadMaterials();
        loadOperations();
    });
</script>

<div style="margin-bottom: 24px;">
    <button class="btn btn-primary" onclick="openAddSpecMaterialModal()" style="margin-right: 10px;">+ Добавить спецификацию материалов</button>
    <button class="btn btn-success" onclick="openAddSpecOperationModal()">+ Добавить спецификацию операций</button>
</div>

<div class="data-table" style="margin-bottom: 32px;">
    <div class="table-header">
        <div class="table-title">Спецификации материалов</div>
    </div>
    <table>
        <thead>
            <tr>
                <th>Продукция</th>
                <th>Материал</th>
                <th>Кол-во на 1 ед.</th>
                <th>Цена материала</th>
                <th>Сумма</th>
            </tr>
        </thead>
        <tbody id="specMaterialsTableBody">
            <tr><td colspan="5" class="loading-spinner">Загрузка...</td></tr>
        </tbody>
    </table>
</div>

<div class="data-table">
    <div class="table-header">
        <div class="table-title">Спецификации операций</div>
    </div>
    <table>
        <thead>
            <tr>
                <th>Продукция</th>
                <th>Операция</th>
                <th>Норма времени</th>
                <th>Кол-во операций</th>
                <th>Ставка</th>
                <th>Сумма</th>
            </tr>
        </thead>
        <tbody id="specOperationsTableBody">
            <tr><td colspan="6" class="loading-spinner">Загрузка...</td></tr>
        </tbody>
    </table>
</div>

<div id="specMaterialModal" class="modal-overlay" style="display:none;">
    <div class="modal">
        <div class="modal-header">
            <h3 class="modal-title">Добавить спецификацию материалов</h3>
            <button class="modal-close" onclick="closeModal('specMaterialModal')">&times;</button>
        </div>
        <form id="specMaterialForm" onsubmit="saveSpecMaterial(event)">
            <div class="modal-body">
                <div class="form-group">
                    <label class="form-label">Продукция <span class="required">*</span></label>
                    <select id="specMatProductId" class="form-input" required>
                        <option value="">Выберите продукцию...</option>
                    </select>
                </div>
                <div class="form-group">
                    <label class="form-label">Материал <span class="required">*</span></label>
                    <select id="specMatMaterialId" class="form-input" required>
                        <option value="">Выберите материал...</option>
                    </select>
                </div>
                <div class="form-group">
                    <label class="form-label">Количество на 1 ед. <span class="required">*</span></label>
                    <input type="number" id="specMatQuantity" class="form-input" step="0.0001" required>
                </div>
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-outline" onclick="closeModal('specMaterialModal')">Отмена</button>
                <button type="submit" class="btn btn-primary">Сохранить</button>
            </div>
        </form>
    </div>
</div>

<div id="specOperationModal" class="modal-overlay" style="display:none;">
    <div class="modal">
        <div class="modal-header">
            <h3 class="modal-title">Добавить спецификацию операций</h3>
            <button class="modal-close" onclick="closeModal('specOperationModal')">&times;</button>
        </div>
        <form id="specOperationForm" onsubmit="saveSpecOperation(event)">
            <div class="modal-body">
                <div class="form-group">
                    <label class="form-label">Продукция <span class="required">*</span></label>
                    <select id="specOpProductId" class="form-input" required>
                        <option value="">Выберите продукцию...</option>
                    </select>
                </div>
                <div class="form-group">
                    <label class="form-label">Операция <span class="required">*</span></label>
                    <select id="specOpOperationId" class="form-input" required>
                        <option value="">Выберите операцию...</option>
                    </select>
                </div>
                <div class="form-group">
                    <label class="form-label">Норма времени (ч)</label>
                    <input type="number" id="specOpTimeNorm" class="form-input" step="0.01" value="1.0">
                </div>
                <div class="form-group">
                    <label class="form-label">Количество операций</label>
                    <input type="number" id="specOpQuantity" class="form-input" step="0.01" value="1.0">
                </div>
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-outline" onclick="closeModal('specOperationModal')">Отмена</button>
                <button type="submit" class="btn btn-primary">Сохранить</button>
            </div>
        </form>
    </div>
</div>
{% endblock %}
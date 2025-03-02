# Equipo 2

Módulo: hr_department_management
Este módulo permite gestionar los departamentos de la empresa, facilitando la administración de la plantilla, la asignación de centros de costo y áreas de nómina, y el mantenimiento de un historial de departamentos inactivos.

Funcionalidades Principales
1. Creación de Nuevos Departamentos
Se añadieron campos nuevos a los departamentos:

Código único del departamento.

Centro de costo.

Área de nómina.

Los departamentos se registran como "Activos".

2. Asignación de Empleados a Departamentos
Al asignar un empleado a un departamento, el sistema asigna automáticamente el centro de costo y el área de nómina asociados al departamento.

Los empleados no pueden ser asignados a departamentos inactivos.

3. Desactivación de Departamentos
Los departamentos pueden ser desactivados, cambiando su estado a "Inactivo".

Se registra la fecha de desactivación y se impide la asignación de nuevos empleados a departamentos inactivos.

4. Consulta de Departamentos Activos e Inactivos
Filtrado de departamentos por estado ("Activo" o "Inactivo").

Visualización de la fecha de desactivación para departamentos inactivos.

5. Generación de Informes de Plantilla
Generación de informes detallados de la plantilla actual de un departamento, incluyendo:

Nombre del departamento.

Centro de costo.

Área de nómina.

Lista de empleados asignados con sus datos básicos (código, nombre, apellidos, cargo).

Exportación de informes en formato PDF.

6. Edición de Departamentos
Modificación de los datos de un departamento existente.

Actualización automática del centro de costo y área de nómina en todos los empleados asignados al departamento.

Validaciones y Restricciones
Campos Obligatorios: Al crear o editar un departamento, los campos obligatorios deben completarse (nombre, código, centro de costo, área de nómina).

Desactivación de Departamentos: Requiere confirmación antes de proceder.

Asignación de Empleados: No se permite asignar empleados a departamentos inactivos.

Desactivación de Departamento:

El sistema debe cambiar el estado del departamento a "Inactivo" y registrar la fecha de desactivación.

No se permiten nuevas asignaciones de empleados a departamentos inactivos.

Edición de Departamentos:

El sistema debe actualizar automáticamente el centro de costo y área de nómina en todos los empleados asignados al departamento.

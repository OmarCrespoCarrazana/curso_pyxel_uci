# Nursing Request Inventory User's Guide

## Settings

### User Settings>Users>Create User

1. Define user's role(Nurse, Storekeeper)
2. Grant access to base inventory module
    Admin: (Storekeeper,Manager)
    User: Nurse
3. Assing a group to the user for RBAC(Nurse,Storekeeper,Manager)
4. Preferences>Notification>Handle by Odoo
5. Assign an email and password to the user

### General Settings>Inventory

1. Enable packages inside the Operations section
2. Enable product packagings in Products section
3. Enable Lots & Serial Numbers, Expiration Dates and Display options in Traceability section
4. Enable Landed Costs and Display Lots and Serial Numbers in Valuation section
5. Enable Storage Locations and Storage Categories in Warehouse section
6. Enable Security Lead time for purchase in Advanced Scheduling section

### Inventory Settings>Warehouse Management

1. Create a new WH (Childcare WH)
2. Create new internal locations (CC-WH/BaseStock)
    Child Medications: CC-WH/MedicationStock
    Medical Supplies:  CC-WH/SupplieStock
3. Create new operation types (Receipts,Deliveries,Internals)
4. Create Storage Categories(Child Meds, Dry and Cool, Medical Supplies)
5. Create Putaway rules so when Product arrives to A when can relocate it to B

### Inventory Settings>Products

1. Create Products categories (Child Meds and Medical Supplies under Nursing)
2. Create Reordering Rules for Child Meds and Med Supplies with min and max qty per product(Automatically Handled by Odoo)
3. Assign a vendor to each order

### Inventory Settings>Deliveries

1. Create package types

### Base Rules

1. All users must be internal users
2. All users must have its own related partner
3. All users must have an email assigned
4. All users must been able to receive Odoo notificactions.
5. All users must be active in the system

### Access and actions Rules

1. Storekeepers and Managers must have full access to Inventory module
2. Nurses can only access and request medical supplies inside the Inventory module
3. Nurses can only see their own NR
4. Nurses can edit its own NR while these are in Draft or Pending state only
5. Nurses can cancel its own NR while these are in Draft or Pending states only
6. Nurses cant change the state of a NR once these is canceled or approved
7. Storekeepers and managers can see all NR and change its states from draft or pending to approved only
8. Storekeepers can't approve an already approved or canceled NR
9. If the Storekeeper try to approve and NR with a product qty that exceed its stock, the NR automatically pass to Pending
10. When the stock is updated, storekeepers can again try to approve the NR
11. Storekeepers can see all NRL, filter and print them as they want
12. Storekeepers can print the delivery orders related with the approved NRs

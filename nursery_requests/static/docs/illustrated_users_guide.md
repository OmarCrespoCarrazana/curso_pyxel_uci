# Nursing Request Illustrated User Guide

## Settings

### User Settings > Users > Create User

General Settings Applied over user groups

- Define user's role(Nurse, Storekeeper)

![Section 1 Defined Users](settings/defined_users.png)

![Section 1 Defined Nurse User](settings/nurse_user.png)

- Grant access to base inventory module
    Admin: (Storekeeper,Manager)
    User: Nurse

![Section 1 Defined access groups](settings/inventory_groups.png)

- Assign an email and password to the user

![Section 1 Asign email and password](settings/change_password_user_settings_LI.jpg)

![Section 1 Asign email and password](settings/change_password_wizard_LI.jpg)

### Preferences > Notification > Handle by Odoo

![Section 1 Notifications settings](settings/notifications_settings.jpg)

![Section 1 System notifications](settings/notifications_system.png)

![Section 1 Receive Odoo notifications](settings/odoo_notifications.jpg)

### General Settings > Inventory

Settings applied over Inventory module

- Enable packages inside the Operations section

- Enable product packagings in Products section

![Section 2 Packages enabled ](settings/product_packagin.png)

- Enable Storage Locations and Storage Categories in Warehouse section

![Section 2 Locations and Storage enabled ](settings/storage_location.png)

![Section 2 Storage Categories enabled ](settings/storage_categories.png)

### Inventory Settings > Warehouse Management

Settings applied over Inventory Warehouse section

- Create a new WH (Childcare WH)

![Section 3 new WH](settings/new_Wh.png)

- Create new internal locations (CC-WH/BaseStock)
    Child Medications: CC-WH/MedicationStock
    Medical Supplies:  CC-WH/SupplieStock

- Create new operation types (Receipts,Deliveries,Internals)

![Section 3 Operations types](settings/operations.png)

- Create Storage Categories(Child Meds, Dry and Cool, Medical Supplies)

![Section 3 Storage Categories](settings/storage_categories.png)

- Create Putaway rules so when Product arrives to A when can relocate it to B

![Section 3 Putaway rules](settings/putaway_rules.png)

### Inventory Settings > Products

Settings applied over Inventory Products section

- Create Products categories (Child Meds and Medical Supplies under Nursing)

![Section 4 Product Categories](settings/products_categories.png)

- Create Reordering Rules for Child Meds and Med Supplies with min and max qty per product      (Automatically Handled by Odoo)

![Section 4  Reordering rules ](settings/reordering_rules.png)

- Assign a vendor to each order

### Inventory Settings > Deliveries

Settings applied over Inventory Deliveries section

- Create package types

![Section 5 Packages types ](settings/packages_types.png)

## Users Workflow in the system

### Base Rules

1. All users must be internal users
2. All users must have its own related partner
3. All users must have an email assigned
4. All users must been able to receive Odoo notificactions.
5. All users must be active in the system

### Access and actions Rules

1. Storekeepers and Managers must have full access to Inventory
![Section 6 Nurse NR Access Menu ](workflow/module_location_admin.png)
2. Nurses can only access and request medical supplies and medications from the menu
![Section 6 Nurse NR Access Menu ](workflow/nursinRq_menu_nurse.png)
![Section 6 Nurse NR creation ](workflow/create_nursingRq.png)
3. Nurses can only see their own NR
![Section 6 Nurse NR ](workflow/draft_NR.png)
4. Nurses can edit its own NR while these are in Draft or Pending state
5. Nurses can cancel its own NR while these are in Draft or Pending states only
![Section 6 Nurse NR Edit ](workflow/create_nursingRq.png)
6. Nurses cant change the state of a NR once these is canceled or approved
7. Storekeepers and managers can see all NR and change its states from draft or pending to approved
![Section 6 Admins NR Management ](workflow/NR_storekeepr.png)
![Section 6 Admins NR Management ](workflow/pending_NR.png)
![Section 6 Admins NR Management ](workflow/approve_NR_storekeepr.png)
8. Storekeepers can't approve an already approved or canceled NR
![Section 6 Admins NR Management ](workflow/approved_NR.png)
![Section 6 Admins NR Management ](workflow/canceled_NR.png)
9. If the Storekeeper try to approve and NR with a product qty that exceed its stock, the NR automatically pass to Pending
![Section 6 Admins NR Management ](workflow/NR_approval_failed_storekeepr.png)
10. When the stock is updated, storekeepers can again try to approve the NR
11. Storekeepers can see all NRL, filter and print them as they want
![Section 6 Admins NRL Management ](workflow/nursingRL_admin.png)
![Section 6 Admins NRL Management ](workflow/print_NRL_storekepper.png)
![Section 6 Admins NRL Management ](workflow/print_NRL_storekeepr-2.png)
12. Storekeepers can manage and print the delivery orders related with the approved NRs
![Section 6 Admins NRL Management ](workflow/deliveries_storekeeper.png)
![Section 6 Admins NRL Management ](workflow/deliveries_details_storekeeper.png)
![Section 6 Admins NRL Management ](workflow/printed_delivery_storekeepr.png)

### Odoo Nofitications

- Nurse Notifications received:
![Section 6 Nurse Notifications ](workflow/nursinRq_menu_nurse.png)
- Approved NR notification sample:
![Section 6 Admins Notifications ](workflow/approved_NR_notification.png)

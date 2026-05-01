===================================
MSA I - Quick Reference
===================================

Client (VMWP1)
--------------

Netzwerk-Diagnose
~~~~~~~~~~~~~~~~~
.. code-block:: bash

   ncpa.cpl

.. code-block:: bash

   ipconfig /all

.. code-block:: bash

   ipconfig /flushdns

.. code-block:: bash

   nslookup <Ziel>

System-Tools
~~~~~~~~~~~~
.. code-block:: bash

   services.msc

.. code-block:: bash

   taskmgr

.. code-block:: bash

   eventvwr

.. code-block:: bash

   sysdm.cpl

.. code-block:: bash

   control

Festplatten
~~~~~~~~~~~
.. code-block:: bash

   diskpart

Server (VMWS1)
--------------

Active Directory & GPO
~~~~~~~~~~~~~~~~~~~~~~
.. code-block:: bash

   dsa.msc

.. code-block:: bash

   gpmc.msc

.. code-block:: bash

   netdom query fsmo

Server-Rollen
~~~~~~~~~~~~~
.. code-block:: bash

   dnsmgmt.msc

.. code-block:: bash

   dhcpmgmt.msc

.. code-block:: bash

   servermanager

Monitoring
~~~~~~~~~~
.. code-block:: bash

   perfmon

.. code-block:: bash

   resmon

PowerShell (Admin)
------------------

.. code-block:: powershell

   Get-WindowsCapability -Name RSAT* -Online

.. code-block:: powershell

   Get-Service | Where-Object {$_.Status -eq 'Stopped'}

.. code-block:: powershell

   Get-DnsServerZone
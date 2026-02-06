From Containers to Observability: Docker Compose Roadmap
========================================================

Monitoring (Prometheus & Grafana)
---------------------------------

Metrics monitoring allows you to see numbers (CPU, RAM, Request counts) over time.

- **Prometheus:** Collects and stores metrics (The Database).
- **Grafana:** Visualizes the metrics (The Dashboard).

Project Structure
^^^^^^^^^^^^^^^^^

.. code-block:: text

   project06/
   ├── docker-compose.yaml
   └── prometheus.yml

Step 1: The Prometheus Config
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: yaml
   :caption: prometheus.yml

   global:
     scrape_interval: 5s # Wie oft Prometheus Daten abfragt (Standard ist 15s)

   scrape_configs:
     - job_name: 'prometheus'
       static_configs:
         - targets: ['prometheus:9090'] # Wir nutzen den Servicenamen statt localhost

Step 2: The Compose File
^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: yaml
   :caption: docker-compose.yaml

   services:
     prometheus:
       image: prom/prometheus:latest
       container_name: prometheus
       ports:
         - "9090:9090"
       volumes:
         - ./prometheus.yml:/etc/prometheus/prometheus.yml
         - prometheus_data:/prometheus # Speichert Metriken dauerhaft

     grafana:
       image: grafana/grafana:latest
       container_name: grafana
       ports:
         - "3000:3000"
       depends_on:
         - prometheus
       volumes:
         - grafana_data:/var/lib/grafana # Verhindert Datenverlust der Dashboards

   volumes:
     prometheus_data:
     grafana_data:

Practical Exercise: View the Dashboard
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. Start the stack:

   .. code-block:: bash

      docker-compose up -d

2. Check if containers are running:

   .. code-block:: bash

      docker ps

3. Open Prometheus (Targets check):

   .. code-block:: text

      http://localhost:9090/targets

4. Open Grafana (Initial Setup):

   .. code-block:: text

      http://localhost:3000

   *(Default Login: admin / admin)*

5. Clean up (Important before next project):

   .. code-block:: bash

      docker-compose down


Alerting (Mattermost & Webhooks)
--------------------------------

Project Structure
^^^^^^^^^^^^^^^^^

.. code-block:: text

   project07/
   └── docker-compose.yaml

Step 1: The Compose File
^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: yaml
   :caption: docker-compose.yaml

   services:
     mattermost:
       image: mattermost/mattermost-preview
       container_name: mattermost
       ports:
         - "8065:8065"
       # Preview Image nutzt eine interne DB, ideal für Tests

Step 2: Integration Logic
^^^^^^^^^^^^^^^^^^^^^^^^^

1. Open Mattermost:

   .. code-block:: text

      http://localhost:8065

2. **Setup:** Erstelle einen Account und ein Team "DevOps".
3. **Webhook:** Gehe zu **Product Settings** -> **Integrations** -> **Incoming Webhooks**.
4. **Grafana Link:** In Grafana unter **Alerting** -> **Contact Points** den Typ "Webhook" wählen.

5. Test the Alert:

   .. code-block:: bash

      # Simuliere Last oder stoppe einen Service, um Alarm zu triggern
      docker-compose stop mattermost


Logging (The ELK Stack)
-----------------------

- **ElasticSearch:** Search engine for logs.
- **Logstash:** (Optional in basic setups) Processes logs.
- **Kibana:** The interface.

Project Structure
^^^^^^^^^^^^^^^^^

.. code-block:: text

   project08/
   └── docker-compose.yaml

Step 1: The Compose File
^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: yaml
   :caption: docker-compose.yaml

   services:
     elasticsearch:
       image: docker.elastic.co/elasticsearch/elasticsearch:8.10.2
       container_name: elasticsearch
       environment:
         - discovery.type=single-node # Verhindert Cluster-Suche (spart Ressourcen)
         - xpack.security.enabled=false # Deaktiviert Auth für lokale Tests
         - "ES_JAVA_OPTS=-Xms512m -Xmx512m" # Begrenzt RAM-Verbrauch der JVM
       ports:
         - "9200:9200"
       ulimits:
         memlock:
           soft: -1
           hard: -1

     kibana:
       image: docker.elastic.co/kibana/kibana:8.10.2
       container_name: kibana
       ports:
         - "5601:5601"
       environment:
         - ELASTICSEARCH_HOSTS=http://elasticsearch:9200
       depends_on:
         - elasticsearch

Practical Exercise: Searching Logs
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. Start (Wait for healthy status):

   .. code-block:: bash

      docker-compose up -d

2. Verify Elasticsearch is "Green":

   .. code-block:: text

      http://localhost:9200/_cluster/health?pretty

3. Access Kibana:

   .. code-block:: text

      http://localhost:5601

4. **Data View:** In Kibana unter **Stack Management** -> **Data Views** einen Index (z.B. `*`) erstellen, um Logs zu sehen.

Summary of Learning Path
^^^^^^^^^^^^^^^^^^^^^^^^

+------------------+-----------------------+---------------------------------------+
| Tool             | Best For              | Docker Skill Learned                  |
+==================+=======================+=======================================+
| **Prometheus**   | Numbers/Metrics       | Target Scraping & Config Mounting     |
+------------------+-----------------------+---------------------------------------+
| **Mattermost**   | Alerts/Chat           | Webhooks & External API links         |
+------------------+-----------------------+---------------------------------------+
| **ELK Stack**    | Text/Error Logs       | Resource Limits (RAM/Java Opts)       |
+------------------+-----------------------+---------------------------------------+
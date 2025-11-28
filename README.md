```mermaid
graph LR
    subgraph Client-Machine (LMU-Maschine)
        direction TB
        C_NODE[Node Exporter]
        C_FEAT[Filebeat]
    end

    subgraph Monitoring-Server (Kali-Maschine / Docker Compose)
        subgraph Logging-Stack (ELK)
            FEAT[Filebeat (lokal)]
            LS[Logstash]
            ES[Elasticsearch]
            KB[Kibana]
        end
        
        subgraph Metrik-Stack
            PROM[Prometheus]
            GF[Grafana]
            AM[Alertmanager]
        end
        
        subgraph Kommunikation
            MM[Mattermost]
        end
        
        direction LR
        LS --> ES
        
        direction TB
        subgraph Visualisierung
            KB
            GF
        end
        
        GF --> AM
        AM -- Webhook --> MM
    end
    
    PROM -- HTTP Scrape --> C_NODE
    C_FEAT -- Log Push --> LS
    FEAT --> LS
    PROM -- Scrape --> FEAT
    ES -- Data --> KB
    PROM -- Data --> GF
    ES -- Data --> GF
    
    style Client-Machine fill:#f0e68c,stroke:#333,stroke-width:2px
    style Monitoring-Server fill:#add8e6,stroke:#333,stroke-width:2px
```

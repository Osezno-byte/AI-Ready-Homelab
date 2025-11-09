# Architecture Diagrams

[← Back to README](../../../README.md)

This page contains all architecture diagrams for the AI-Ready Homelab Framework.
Each diagram is rendered directly on GitHub using Mermaid, and reflects the framework's core design patterns.

## Hybrid AI Architecture

The hybrid AI architecture shows how local and cloud AI work together with privacy guardrails.

```mermaid
graph TB
    subgraph "Local Infrastructure"
        HA[Home Assistant]
        FRIGATE[Frigate NVR]
        DOCKER[Docker Services]
        PROXMOX[Proxmox]
        PFSENSE[pfSense]

        MCP[MCP Tools<br/>65 tools across 7 servers]
        HA --> MCP
        FRIGATE --> MCP
        DOCKER --> MCP
        PROXMOX --> MCP
        PFSENSE --> MCP
    end

    subgraph "AI Layer (Hybrid)"
        OLLAMA[Local AI<br/>Ollama/LM Studio<br/>DEFAULT MODE]
        CLOUD[Cloud AI<br/>Claude/GPT<br/>Planning Only]

        SANITIZER[Preflight Sanitizer<br/>n8n workflow<br/>10 redaction rules]
    end

    subgraph "Execution Layer"
        CSE[CSE Guardrails<br/>Approval + Redline]
        N8N[n8n Workflows<br/>24/7 Monitoring]
    end

    subgraph "User Control"
        USER[Bear<br/>Human Operator]
        SIGNAL[Signal Notifications<br/>Approval Prompts]
    end

    %% Data flow: Local-only mode (DEFAULT)
    MCP -->|structured data| OLLAMA
    OLLAMA -->|proposed actions| CSE

    %% Data flow: Hybrid mode (optional)
    MCP -->|raw logs/config| SANITIZER
    SANITIZER -->|sanitized only| CLOUD
    CLOUD -->|suggested plan| OLLAMA
    OLLAMA -->|execute locally| CSE

    %% Approval workflow
    CSE -->|requires approval?| SIGNAL
    SIGNAL -->|approve/deny| USER
    USER -->|approval| CSE
    CSE -->|execute| MCP

    %% Monitoring
    N8N -->|health checks| MCP
    N8N -->|alerts| SIGNAL

    style OLLAMA fill:#90EE90
    style CLOUD fill:#FFE4B5
    style SANITIZER fill:#87CEEB
    style CSE fill:#FFB6C1
    style USER fill:#DDA0DD
```

## CSE Guardrails

The CSE (Claude Supervised Execute) guardrails provide policy-based approval workflow with redline protection.

```mermaid
flowchart TD
    START[AI Proposes Action] --> PARSE[Parse Command]
    PARSE --> CHECK_POLICY{Matches CSE Policy?}

    CHECK_POLICY -->|No policy match| DENY[❌ Auto-Deny<br/>Log to audit]
    CHECK_POLICY -->|Yes| CHECK_REDLINE{Redline Trigger?}

    CHECK_REDLINE -->|Yes<br/>rm -rf, dd, mkfs, etc| REDLINE[🚨 REDLINE<br/>Block immediately<br/>Alert user<br/>Require manual review]
    CHECK_REDLINE -->|No| CHECK_APPROVAL{Requires Approval?}

    CHECK_APPROVAL -->|Yes| NOTIFY[📱 Send to Signal/Telegram<br/>Show command + context<br/>Start 120s timeout]
    CHECK_APPROVAL -->|No<br/>Auto-approve mode| VALIDATE[Validate command syntax]

    NOTIFY --> WAIT{User Response?}
    WAIT -->|Approve within 120s| VALIDATE
    WAIT -->|Deny| DENY
    WAIT -->|Timeout| DENY

    VALIDATE --> CHECK_DRY{Dry-run Available?}
    CHECK_DRY -->|Yes| DRY_RUN[Execute with --dry-run]
    CHECK_DRY -->|No| EXECUTE

    DRY_RUN --> DRY_CHECK{Dry-run Success?}
    DRY_CHECK -->|No| DENY
    DRY_CHECK -->|Yes| EXECUTE[✅ Execute Command]

    EXECUTE --> LOG[Log to audit trail<br/>Command + user + timestamp]
    LOG --> VERIFY[Verify execution result]
    VERIFY --> REPORT[Report to user<br/>Success/failure + output]

    DENY --> REPORT
    REDLINE --> REPORT

    style REDLINE fill:#FF6B6B
    style DENY fill:#FFB6C1
    style EXECUTE fill:#90EE90
    style NOTIFY fill:#87CEEB
    style VALIDATE fill:#DDA0DD
```

## Mode Switch FSM

The mode switching finite state machine shows transitions between local-only, hybrid, and cloud-enhanced modes.

```mermaid
stateDiagram-v2
    [*] --> LocalOnly: Default Mode

    state "Local-Only Mode" as LocalOnly {
        [*] --> OllamaActive
        OllamaActive: Ollama/LM Studio
        OllamaActive: Zero cloud exposure
        OllamaActive: Full privacy
        OllamaActive: MCP tools only
    }

    state "Hybrid Mode" as Hybrid {
        [*] --> Sanitizing
        Sanitizing: Preflight sanitizer active
        Sanitizing: Cloud for planning
        Sanitizing: Local for execution
        Sanitizing --> CloudPlanning
        CloudPlanning: Claude/GPT receives sanitized logs
        CloudPlanning: Suggests remediation plan
        CloudPlanning --> LocalExecution
        LocalExecution: Ollama validates plan
        LocalExecution: CSE executes locally
    }

    state "Cloud-Enhanced Mode" as CloudEnhanced {
        [*] --> FullCloud
        FullCloud: Cloud AI for planning
        FullCloud: Mandatory sanitization
        FullCloud: Local execution only
        FullCloud: CSE approval required
    }

    LocalOnly --> Hybrid: User enables hybrid<br/>(complex troubleshooting)
    Hybrid --> LocalOnly: Troubleshooting complete<br/>(return to default)

    Hybrid --> CloudEnhanced: Escalate to cloud-enhanced<br/>(severe incident)
    CloudEnhanced --> Hybrid: Incident resolved<br/>(de-escalate)

    CloudEnhanced --> LocalOnly: Full return to privacy<br/>(manual override)

    note right of LocalOnly
        DEFAULT MODE
        99% of operations
        Full privacy
        Air-gapped capable
    end note

    note right of Hybrid
        OPTIONAL MODE
        Complex diagnostics
        Sanitized logs only
        Cloud planning + local execution
    end note

    note right of CloudEnhanced
        RARE MODE
        Severe incidents
        Maximum assistance
        Still sanitized + local execution
    end note
```

## Local AI Operations

Local-first AI operations architecture showing privacy-preserving infrastructure.

```mermaid
flowchart TB
    subgraph Internet["☁️ Internet (Optional)"]
        ModelRepo[Model Updates<br/>Ollama Registry]
    end

    subgraph Home_Network["🏠 Your Private Network<br/><b>EVERYTHING STAYS LOCAL</b>"]

        subgraph Local_AI["🤖 Local AI Layer (Air-Gap Compatible)"]
            direction TB
            Ollama[Ollama Server<br/>localhost:11434]

            subgraph Models["AI Models (Local Storage)"]
                LLaMA[LLaMA3.1 70B<br/>General ops]
                Mistral[Mistral 8x22B<br/>Complex reasoning]
                Qwen[Qwen2.5 72B<br/>Documentation]
            end

            Ollama --> Models
        end

        subgraph Agent_Layer["🛡️ Specialized Agents (10 total)"]
            direction LR
            HAValidator[ha-yaml-validator<br/>Prevents automation bugs]
            DockerTrouble[docker-troubleshooter<br/>Container diagnostics]
            BackupVal[backup-validator<br/>DR automation]
            SecurityAud[security-auditor<br/>Compliance scanning]
            Other[+ 6 more agents...]
        end

        subgraph CSE["🔐 CSE Guardrails<br/><b>Human-Gated Privileges</b>"]
            direction TB
            Policy[CSE Policy Engine<br/>Time-boxed access]
            Audit[Audit Log<br/>Every action recorded]
            Runbooks[Runbook References<br/>Required for approval]

            Policy --> Audit
            Policy --> Runbooks
        end

        subgraph MCP_Tools["🔧 MCP Tools (65 total - Local stdio transport)"]
            direction LR

            subgraph Infrastructure["Infrastructure (7 Systems)"]
                Docker[Docker Manager<br/>8 tools]
                HA[Home Assistant<br/>12 tools]
                Frigate[Frigate NVR<br/>7 tools]
                Proxmox[Proxmox<br/>8 tools]
                pfSense[pfSense<br/>10 tools]
                n8n[n8n<br/>8 tools]
                DB[Database<br/>12 tools]
            end
        end

        subgraph Services["🖥️ Your Infrastructure"]
            direction LR
            Containers[Docker Containers]
            VMs[Proxmox VMs/LXCs]
            Network[pfSense Firewall]
            Automation[Home Assistant]
            Monitoring[Frigate + n8n]
        end

        %% Connections
        Local_AI --> Agent_Layer
        Agent_Layer --> CSE
        CSE --> MCP_Tools
        MCP_Tools --> Services

        %% Optional internet for model updates only
        Internet -.->|Model Updates<br/>ONLY| Ollama
    end

    %% Styling
    classDef privateZone fill:#e1f5e1,stroke:#2d5016,stroke-width:3px
    classDef aiLayer fill:#fff3cd,stroke:#856404,stroke-width:2px
    classDef secureLayer fill:#f8d7da,stroke:#721c24,stroke-width:2px
    classDef toolLayer fill:#d1ecf1,stroke:#0c5460,stroke-width:2px
    classDef internetOptional fill:#f0f0f0,stroke:#999,stroke-width:2px,stroke-dasharray: 5 5

    class Home_Network privateZone
    class Local_AI,Agent_Layer aiLayer
    class CSE secureLayer
    class MCP_Tools,Infrastructure toolLayer
    class Internet,ModelRepo internetOptional
```

## Network Topology

VLAN-segmented homelab network with isolation and security zones.

```mermaid
flowchart LR
    subgraph Internet
        WAN[ISP]
    end

    WAN --> FW[pfSense Router<br/>10.27.27.1]

    subgraph VLANs["Network Segmentation"]
        V1[VLAN 1: LAN<br/>10.27.27.0/24<br/>Infrastructure]
        V10[VLAN 10: HomeNet<br/>10.27.10.0/24<br/>Trusted Devices]
        V20[VLAN 20: IoTNet<br/>10.27.20.0/24<br/>IoT Devices - ISOLATED]
        V30[VLAN 30: GuestNet<br/>10.27.30.0/24<br/>Guest WiFi - ISOLATED]
    end

    FW <-- DHCP, DNS, Routing --> V1
    FW <-- Segmented Rules --> V10
    FW <-- Strict Isolation --> V20
    FW <-- Internet Only --> V30

    subgraph Hypervisor["Proxmox VE (10.27.27.10)"]
        PVE[Proxmox Host]
        MC[(VM: media-core<br/>10.27.27.251)]
        DC[(VM: docker-core<br/>10.27.27.250)]
        HALXC[HA Green<br/>10.27.27.11<br/>Dedicated Hardware]
    end

    V1 <--> PVE
    PVE <--> MC
    PVE <--> DC
    V1 <--> HALXC

    subgraph Services_media["Services: media-core"]
        Frigate[Frigate NVR<br/>Object Detection]
        Jellyfin[Jellyfin<br/>Media Server]
        Sonarr[Sonarr/Radarr<br/>Media Automation]
        Ollama[Ollama<br/>Local LLM]
    end

    subgraph Services_docker["Services: docker-core"]
        MQTT[Mosquitto<br/>MQTT Broker]
        NPM[Nginx Proxy Manager<br/>Reverse Proxy]
        N8N[n8n<br/>Workflow Automation]
        UptimeKuma[Uptime Kuma<br/>Monitoring]
    end

    MC --> Services_media
    DC --> Services_docker

    V20 --> Frigate
    V10 --> Frigate
    V1 --> Frigate

    V1 <--> MQTT
    V1 <--> NPM
    V1 <--> N8N
    V1 <--> Ollama

    style FW fill:#f9f,stroke:#333,stroke-width:2px
    style PVE fill:#bbf,stroke:#333,stroke-width:2px
    style V20 fill:#faa,stroke:#333,stroke-width:2px
    style V30 fill:#faa,stroke:#333,stroke-width:2px
```

## Services Architecture

Service integration showing MCP tools, custom agents, and automation workflows.

```mermaid
flowchart TB
    subgraph AI_Layer["AI Integration Layer"]
        MCP[Model Context Protocol<br/>65 Tools Across 7 Servers]

        subgraph Agents["Custom Specialized Agents (10 total)"]
            AG1[ha-yaml-validator<br/>HA Automation Validation]
            AG2[docker-troubleshooter<br/>Container Diagnostics]
            AG3[doc-consolidator<br/>Documentation Maintenance]
            AG4[network-diagnostician<br/>VLAN & Firewall Analysis]
            AG5[backup-validator<br/>Backup Verification]
            AG6[security-auditor<br/>Security Scanning]
            AG7[database-optimizer<br/>DB Performance Tuning]
            AG8[integration-validator<br/>Cross-Service Testing]
            AG9[update-coordinator<br/>Update Planning]
            AG10[performance-analyzer<br/>Resource Analysis]
        end
    end

    MCP --> AG1
    MCP --> AG2
    MCP --> AG3
    MCP --> AG4
    MCP --> AG5
    MCP --> AG6
    MCP --> AG7
    MCP --> AG8
    MCP --> AG9
    MCP --> AG10

    subgraph Infrastructure["Infrastructure Access Points"]
        HA[Home Assistant<br/>12 MCP Tools]
        DOCKER[Docker<br/>8 MCP Tools]
        FRIGATE[Frigate NVR<br/>7 MCP Tools]
        PROXMOX[Proxmox<br/>8 MCP Tools]
        PFSENSE[pfSense<br/>10 MCP Tools]
        N8N_MCP[n8n<br/>8 MCP Tools]
        DB[Databases<br/>12 MCP Tools]
    end

    AG1 --> HA
    AG2 --> DOCKER
    AG3 --> Docs[Documentation Repo]
    AG4 --> PFSENSE
    AG5 --> PROXMOX
    AG6 --> SSH[SSH Audit & Config]
    AG7 --> DB
    AG8 --> HA
    AG8 --> N8N_MCP
    AG9 --> DOCKER
    AG9 --> PROXMOX
    AG10 --> DOCKER
    AG10 --> FRIGATE

    subgraph Automation["Automation & Monitoring"]
        N8N_WORKFLOWS[n8n Workflows<br/>9 Active Workflows]
        STATUS[STATUS.md<br/>Service Health Tracking]
    end

    AG1 -.->|Reports| N8N_WORKFLOWS
    AG2 -.->|Reports| N8N_WORKFLOWS
    AG3 -.->|Updates| STATUS
    AG4 -.->|Reports| STATUS
    AG5 -.->|Reports| N8N_WORKFLOWS
    AG6 -.->|Reports| STATUS

    N8N_WORKFLOWS -.->|Updates| STATUS

    style MCP fill:#9f9,stroke:#333,stroke-width:3px
    style Agents fill:#bbf,stroke:#333,stroke-width:2px
    style Infrastructure fill:#ffd,stroke:#333,stroke-width:2px
    style Automation fill:#faa,stroke:#333,stroke-width:2px
```

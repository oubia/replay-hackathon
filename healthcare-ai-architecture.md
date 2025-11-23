graph TD
    subgraph PatientLayer["Patient Interaction Layer"]
        A[Patient App/Web<br/>Chat, Forms, Media]
        B[Intake Agent<br/>LLM Orchestrator]
        A <--> B
    end
    
    subgraph ClinicalLayer["Clinical Context Layer"]
        C[EHR Connector<br/>FHIR/EMR APIs]
        D[Patient Context<br/>Builder]
        C --> D
        D --> C
    end
    
    subgraph AILayer["AI Services Layer"]
        E[AI Classification Service<br/>Model API: label+explain]
        F[Risk Scoring Engine<br/>Low/Med/High]
        E --> F
    end
    
    subgraph RoutingLayer["Decision Routing Layer"]
        G[Low Risk Path]
        H[Self-Care Advice<br/>Generator LLM]
        I[Patient Notification]
        J[Medium/High Risk Path]
        K[Doctor Review<br/>Task Creator]
        L[Doctor Review Portal<br/>Human-in-the-loop]
        M[Specialist Decision]
        N[Schedule Visit<br/>Tele/In-Person]
        O[Patient Feedback<br/>Summary]
        
        G --> H --> I
        J --> K --> L --> M
        M --> N
        M --> O
    end
    
    subgraph GovernanceLayer["Logging & Governance Layer"]
        P[Audit Logging<br/>Actions + AI]
        Q[Monitoring/MLOps<br/>Drift/Bias Watch]
        R[Model Retrain<br/>Pipeline]
    end
    
    B -->|Symptoms/Questions| D
    D -->|Symptoms + EHR| E
    F -->|Risk Level| G
    F -->|Risk Level| J
    
    I --> P
    O --> P
    P --> Q
    Q --> R
    R --> E
    
    style PatientLayer fill:#e1f5ff
    style ClinicalLayer fill:#fff4e1
    style AILayer fill:#f0e1ff
    style RoutingLayer fill:#e1ffe1
    style GovernanceLayer fill:#ffe1e1
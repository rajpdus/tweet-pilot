# Twitter Thread Generator Architecture

This document outlines the architecture and information flow of the Twitter Thread Generator application.

## System Overview

The application consists of three main components:
1. Research System (using Gemini API)
2. Content Processing
3. Twitter Integration

## Information Flow Diagram

```mermaid
flowchart LR
    subgraph Input
        Q[User Query/Topic]
    end

    subgraph Research ["Research Phase"]
        GC[Gemini API Client]
        RC[Research Client]
        Q --> RC
        RC --> GC
        GC --> RC
        RC --> T[Thread Content]
    end

    subgraph Processing ["Thread Processing"]
        T --> F[Format Thread]
        F --> V[Validate Length]
        V --> S[Split into Tweets]
    end

    subgraph Posting ["Twitter Posting"]
        TC[Twitter Client]
        S --> TC
        TC --> TW[Twitter API]
        TW --> P[Posted Thread]
    end

    style Research fill:#e1f5fe
    style Processing fill:#f3e5f5
    style Posting fill:#e8f5e9
    
    classDef api fill:#ff9800,color:white
    class GC,TW api
```

## Sequence Diagram

```mermaid
sequenceDiagram
    actor User
    participant RC as Research Client
    participant Gemini as Gemini API
    participant TC as Twitter Client
    participant Twitter as Twitter API

    User->>RC: Submit topic/query
    
    RC->>Gemini: Send research request
    Note over RC,Gemini: Using Google's Gemini API<br/>for deep research
    Gemini-->>RC: Return detailed research
    
    RC->>RC: Process and format content
    Note over RC: - Format as thread<br/>- Split into tweets<br/>- Validate lengths
    
    RC->>TC: Send formatted thread
    
    TC->>Twitter: Post first tweet
    Twitter-->>TC: Return tweet ID
    
    loop Remaining Tweets
        TC->>Twitter: Post reply tweet<br/>(with previous tweet ID)
        Twitter-->>TC: Return tweet ID
    end
    
    TC-->>User: Return thread URLs
```

## Component Details

### 1. Research System
- **Input**: User query/topic
- **Processing**: Deep research using Gemini API
- **Output**: Comprehensive research results
- **Key Features**:
  - AI-powered research
  - Context-aware responses
  - Source verification

### 2. Content Processing
- **Input**: Research results
- **Processing**: Content formatting and optimization
- **Output**: Twitter-ready thread
- **Key Features**:
  - Automatic thread splitting
  - Character limit validation
  - Hashtag optimization
  - Media handling

### 3. Twitter Integration
- **Input**: Formatted thread content
- **Processing**: API interaction and posting
- **Output**: Published thread
- **Key Features**:
  - OAuth authentication
  - Thread posting
  - Media upload support
  - Rate limit handling

## Error Handling

The system implements error handling at multiple levels:
1. Research failures
2. Content processing issues
3. Twitter API errors
4. Rate limiting
5. Authentication issues

## Configuration

The system uses environment variables for configuration:
- Twitter API credentials
- Gemini API credentials
- System settings

## Dependencies

- `tweepy`: Twitter API interaction
- `google-generativeai`: Gemini API integration
- `python-dotenv`: Environment management
- Additional utility libraries 
# Mentor Slot Booking System - Design Diagrams

## High-Level Design (HLD)

### System Architecture
```mermaid
graph TB
    subgraph Client Layer
        UI[User Interface]
        Browser[Web Browser]
    end

    subgraph Application Layer
        WS[Web Server]
        AS[Application Server]
        Auth[Authentication Service]
    end

    subgraph Data Layer
        DB[(Database)]
        Cache[(Cache)]
    end

    Browser --> UI
    UI --> WS
    WS --> AS
    AS --> Auth
    AS --> DB
    AS --> Cache
```

### Component Interaction
```mermaid
sequenceDiagram
    participant User
    participant UI
    participant Auth
    participant App
    participant DB

    User->>UI: Access System
    UI->>Auth: Login Request
    Auth->>DB: Validate Credentials
    DB-->>Auth: User Data
    Auth-->>UI: Authentication Result
    
    alt Successful Login
        UI->>App: Request Dashboard
        App->>DB: Fetch User Data
        DB-->>App: User Profile
        App-->>UI: Render Dashboard
    else Failed Login
        UI-->>User: Show Error
    end
```

### Data Flow
```mermaid
flowchart LR
    subgraph User Actions
        A[Login/Register]
        B[Book Slot]
        C[Create Slot]
        D[Cancel Booking]
    end

    subgraph System Processing
        E[Authentication]
        F[Slot Management]
        G[Notification]
    end

    subgraph Data Storage
        H[(User Data)]
        I[(Slot Data)]
        J[(Booking Data)]
    end

    A --> E
    B --> F
    C --> F
    D --> F
    E --> H
    F --> I
    F --> J
    F --> G
```

## Low-Level Design (LLD)

### Database Schema
```mermaid
erDiagram
    User ||--o{ Slot : creates
    User ||--o{ Booking : makes
    Slot ||--o{ Booking : has
    
    User {
        int id PK
        string full_name
        string sap_id
        string email
        string password_hash
        string department
        string user_type
        datetime created_at
        datetime updated_at
    }
    
    Slot {
        int id PK
        int mentor_id FK
        date date
        time start_time
        time end_time
        int max_students
        string description
        boolean is_recurring
        string recurring_type
        datetime created_at
        datetime updated_at
    }
    
    Booking {
        int id PK
        int slot_id FK
        int student_id FK
        datetime booked_at
        string status
        datetime created_at
        datetime updated_at
    }
```

### Class Diagram
```mermaid
classDiagram
    class User {
        +int id
        +string full_name
        +string sap_id
        +string email
        +string department
        +string user_type
        +create_slot()
        +book_slot()
        +cancel_booking()
        +get_bookings()
    }
    
    class Slot {
        +int id
        +int mentor_id
        +date date
        +time start_time
        +time end_time
        +int max_students
        +string description
        +boolean is_recurring
        +string recurring_type
        +create()
        +update()
        +delete()
        +check_availability()
    }
    
    class Booking {
        +int id
        +int slot_id
        +int student_id
        +datetime booked_at
        +string status
        +create()
        +cancel()
        +update_status()
    }
    
    User "1" -- "*" Slot : creates
    User "1" -- "*" Booking : makes
    Slot "1" -- "*" Booking : has
```

### API Endpoints
```mermaid
graph LR
    subgraph Authentication
        A1[POST /api/auth/login]
        A2[POST /api/auth/register]
        A3[POST /api/auth/logout]
    end

    subgraph User Management
        U1[GET /api/user/profile]
        U2[PUT /api/user/profile]
        U3[GET /api/user/bookings]
    end

    subgraph Slot Management
        S1[POST /api/slots]
        S2[GET /api/slots]
        S3[PUT /api/slots/:id]
        S4[DELETE /api/slots/:id]
    end

    subgraph Booking Management
        B1[POST /api/bookings]
        B2[GET /api/bookings]
        B3[PUT /api/bookings/:id]
        B4[DELETE /api/bookings/:id]
    end
```

### State Machine for Booking Process
```mermaid
stateDiagram-v2
    [*] --> Available
    Available --> Booked: Book Slot
    Booked --> Cancelled: Cancel Booking
    Booked --> Completed: Complete Session
    Cancelled --> Available: Release Slot
    Completed --> Available: Release Slot
```

### Component Details

#### Frontend Components
- **Authentication Components**
  - LoginForm
  - RegisterForm
  - PasswordResetForm

- **Dashboard Components**
  - StudentDashboard
  - MentorDashboard
  - StatisticsWidget
  - UpcomingSlotsList

- **Slot Management Components**
  - SlotCreationForm
  - SlotCalendar
  - TimeSlotSelector
  - BookingSummary

#### Backend Services
- **Authentication Service**
  - User authentication
  - Session management
  - Password hashing
  - JWT token generation

- **Slot Management Service**
  - Slot creation
  - Slot availability checking
  - Recurring slot handling
  - Slot updates and deletion

- **Booking Service**
  - Booking creation
  - Booking validation
  - Booking cancellation
  - Booking status updates

- **Notification Service**
  - Email notifications
  - In-app notifications
  - Booking reminders
  - Status updates

#### Database Indexes
- Users: sap_id, email
- Slots: mentor_id, date, start_time
- Bookings: slot_id, student_id, status

#### Caching Strategy
- User profile data
- Available slots
- Booking status
- Department list

#### Security Measures
- Password hashing (bcrypt)
- JWT authentication
- CSRF protection
- Rate limiting
- Input validation
- XSS prevention 

## Database Flow

### User Registration Flow
```mermaid
sequenceDiagram
    participant Client
    participant API
    participant DB
    participant Cache

    Client->>API: POST /api/auth/register
    API->>DB: Check if SAP ID exists
    DB-->>API: User exists?
    alt User exists
        API-->>Client: 400 Bad Request
    else User doesn't exist
        API->>DB: Hash password
        API->>DB: Create user record
        DB-->>API: User created
        API->>Cache: Invalidate user cache
        API-->>Client: 201 Created
    end
```

### Slot Creation Flow
```mermaid
sequenceDiagram
    participant Mentor
    participant API
    participant DB
    participant Cache

    Mentor->>API: POST /api/slots
    API->>DB: Validate mentor
    DB-->>API: Mentor valid
    API->>DB: Check slot conflicts
    DB-->>API: No conflicts
    API->>DB: Create slot record
    DB-->>API: Slot created
    API->>Cache: Invalidate slots cache
    API-->>Mentor: 201 Created
```

### Booking Flow
```mermaid
sequenceDiagram
    participant Student
    participant API
    participant DB
    participant Cache
    participant Notification

    Student->>API: POST /api/bookings
    API->>DB: Check slot availability
    DB-->>API: Slot available
    API->>DB: Check student eligibility
    DB-->>API: Student eligible
    API->>DB: Create booking record
    DB-->>API: Booking created
    API->>Cache: Invalidate bookings cache
    API->>Notification: Send confirmation
    API-->>Student: 201 Created
```

## API Flow

### Authentication Flow
```mermaid
graph TD
    A[Start] --> B{User Type?}
    B -->|Student| C[Student Login]
    B -->|Mentor| D[Mentor Login]
    
    C --> E[Validate Credentials]
    D --> E
    
    E -->|Valid| F[Generate JWT]
    E -->|Invalid| G[Return Error]
    
    F --> H[Set Session]
    H --> I[Redirect to Dashboard]
    
    G --> J[Show Error Message]
    J --> B
```

### Slot Management Flow
```mermaid
graph TD
    A[Start] --> B{Action Type?}
    
    B -->|Create| C[Create Slot]
    B -->|Update| D[Update Slot]
    B -->|Delete| E[Delete Slot]
    B -->|View| F[View Slots]
    
    C --> G[Validate Input]
    D --> G
    E --> H[Check Permissions]
    F --> I[Fetch from Cache]
    
    G -->|Valid| J[Save to DB]
    G -->|Invalid| K[Return Error]
    
    H -->|Allowed| L[Delete from DB]
    H -->|Denied| M[Return Error]
    
    I -->|Cache Hit| N[Return Data]
    I -->|Cache Miss| O[Fetch from DB]
    
    J --> P[Update Cache]
    L --> P
    O --> P
```

### Booking Management Flow
```mermaid
graph TD
    A[Start] --> B{Action Type?}
    
    B -->|Book| C[Book Slot]
    B -->|Cancel| D[Cancel Booking]
    B -->|View| E[View Bookings]
    
    C --> F[Check Availability]
    D --> G[Validate Cancellation]
    E --> H[Fetch Bookings]
    
    F -->|Available| I[Create Booking]
    F -->|Unavailable| J[Return Error]
    
    G -->|Allowed| K[Cancel Booking]
    G -->|Not Allowed| L[Return Error]
    
    H -->|Student| M[Fetch Student Bookings]
    H -->|Mentor| N[Fetch Mentor Bookings]
    
    I --> O[Update Cache]
    K --> O
    M --> P[Return Data]
    N --> P
```

### Data Flow Between Services
```mermaid
graph LR
    subgraph Frontend
        UI[User Interface]
        State[State Management]
    end

    subgraph API Layer
        Auth[Auth Service]
        Slot[Slot Service]
        Booking[Booking Service]
        Notify[Notification Service]
    end

    subgraph Data Layer
        DB[(Database)]
        Cache[(Cache)]
    end

    UI --> State
    State --> Auth
    State --> Slot
    State --> Booking
    
    Auth --> DB
    Slot --> DB
    Booking --> DB
    
    Auth --> Cache
    Slot --> Cache
    Booking --> Cache
    
    Slot --> Notify
    Booking --> Notify
```

### Error Handling Flow
```mermaid
graph TD
    A[API Request] --> B{Valid Request?}
    
    B -->|Yes| C{Authentication?}
    B -->|No| D[400 Bad Request]
    
    C -->|Valid| E{Authorization?}
    C -->|Invalid| F[401 Unauthorized]
    
    E -->|Allowed| G{Data Valid?}
    E -->|Denied| H[403 Forbidden]
    
    G -->|Valid| I[Process Request]
    G -->|Invalid| J[422 Unprocessable]
    
    I -->|Success| K[200 OK]
    I -->|Created| L[201 Created]
    I -->|Error| M[500 Server Error]
```

### Cache Invalidation Flow
```mermaid
graph TD
    A[Data Change] --> B{Change Type?}
    
    B -->|User| C[Invalidate User Cache]
    B -->|Slot| D[Invalidate Slot Cache]
    B -->|Booking| E[Invalidate Booking Cache]
    
    C --> F[Clear User Data]
    D --> G[Clear Slot Data]
    E --> H[Clear Booking Data]
    
    F --> I[Update Cache]
    G --> I
    H --> I
    
    I --> J[Notify Frontend]
``` 
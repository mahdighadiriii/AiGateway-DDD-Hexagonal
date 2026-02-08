# AI Gateway - System Architecture Documentation

## Executive Summary

This document describes the architecture of the AI Gateway system, designed to provide centralized control and management of AI provider usage across development teams. The system implements Domain-Driven Design (DDD) principles with Hexagonal Architecture to ensure maintainability, testability, and scalability.

---

## 1. Architectural Overview

### 1.1 Core Architectural Principles

The system is built on three foundational principles:

**Domain-Driven Design (DDD)**
- Business logic isolated in domain layer
- Bounded contexts for each major capability
- Ubiquitous language within each context
- Rich domain models with value objects

**Hexagonal Architecture (Ports & Adapters)**
- Domain layer has no dependencies on external systems
- All external integrations through ports (interfaces)
- Adapters implement ports for specific technologies
- Enables easy testing and provider substitution

**Separation of Concerns**
- Clear boundaries between contexts
- Each context owns its data and logic
- Communication through well-defined interfaces
- Shared kernel for common concepts

### 1.2 High-Level System Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         EXTERNAL CLIENTS                                │
│                  (Developer Applications, CLI Tools)                    │
└────────────────────────────────┬────────────────────────────────────────┘
                                 │
                                 │ HTTP/REST
                                 ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                          GATEWAY SERVICE                                │
│                     (API Entry Point & Routing)                         │
└────────────────────────────────┬────────────────────────────────────────┘
                                 │
                ┌────────────────┼────────────────┐
                │                │                │
                ▼                ▼                ▼
    ┌──────────────────┐  ┌──────────────┐  ┌──────────────┐
    │   COMPLETION     │  │   BILLING    │  │  WORKFLOW    │
    │    CONTEXT       │  │   CONTEXT    │  │   CONTEXT    │
    │                  │  │              │  │              │
    │  - Routing       │  │  - Usage     │  │  - Chaining  │
    │  - Caching       │  │  - Invoicing │  │  - Templates │
    │  - Retry Logic   │  │  - Analytics │  │  - Execution │
    └─────────┬────────┘  └──────┬───────┘  └──────┬───────┘
              │                  │                 │
              │                  │                 │
              ▼                  ▼                 ▼
    ┌─────────────────────────────────────────────────────┐
    │              SHARED KERNEL                          │
    │   (Common Types, Events, Base Abstractions)         │
    └─────────────────────────────────────────────────────┘
              │
              ▼
    ┌─────────────────────────────────────────────────────┐
    │           INFRASTRUCTURE LAYER                      │
    │                                                     │
    │  ┌──────────┐  ┌──────────┐  ┌──────────┐           │
    │  │ OpenAI   │  │Anthropic │  │  Google  │           │
    │  │ Adapter  │  │ Adapter  │  │ Adapter  │           │
    │  └──────────┘  └──────────┘  └──────────┘           │
    │                                                     │
    │  ┌──────────┐  ┌──────────┐  ┌──────────┐           │
    │  │  Cache   │  │ Database │  │  Events  │           │
    │  │ (Redis)  │  │(Postgres)│  │  (Pub)   │           │
    │  └──────────┘  └──────────┘  └──────────┘           │
    └─────────────────────────────────────────────────────┘
```

---

## 2. Bounded Contexts

### 2.1 Completion Context

**Responsibility:** Handle all AI completion requests with intelligent routing, caching, and retry logic.

**Core Capabilities:**
- Provider-agnostic completion interface
- Smart routing based on cost, speed, or quality
- Semantic caching to reduce redundant API calls
- Automatic retry with exponential backoff
- Provider health monitoring and failover

**Internal Structure:**

```
Completion Context
│
├── Domain Layer
│   ├── Value Objects
│   │   ├── Prompt (validates input)
│   │   ├── ModelName (validates model identifiers)
│   │   ├── Tokens (tracks usage)
│   │   └── Cost (calculates expenses)
│   │
│   ├── Entities
│   │   └── CompletionRequest (aggregate root)
│   │
│   └── Domain Services
│       ├── ProviderFactory (creates provider instances)
│       └── Routing Strategies
│           ├── CostStrategy (minimize cost)
│           ├── SpeedStrategy (minimize latency)
│           └── QualityStrategy (maximize output quality)
│
├── Application Layer
│   ├── Use Cases
│   │   └── CreateCompletionUseCase (orchestrates completion flow)
│   │
│   ├── Services
│   │   └── CompletionService (application-level coordination)
│   │
│   └── Decorators
│       ├── CacheDecorator (semantic caching)
│       └── RetryDecorator (fault tolerance)
│
├── Ports (Interfaces)
│   ├── ProviderPort (abstract AI provider)
│   ├── CachePort (abstract caching)
│   └── CompletionRepositoryPort (persistence)
│
└── Infrastructure (Adapters)
    ├── Providers
    │   ├── OpenAIAdapter
    │   ├── AnthropicAdapter
    │   └── GeminiAdapter
    │
    ├── Cache
    │   └── RedisCache
    │
    └── Persistence
        └── PostgresRepository
```

**Key Design Decisions:**

1. **Value Objects for Domain Concepts**
   - `Prompt`: Ensures prompts meet length and format requirements
   - `ModelName`: Validates model identifiers against supported models
   - `Tokens`: Immutable representation of token usage
   - `Cost`: Calculates costs based on token usage and pricing

2. **Strategy Pattern for Routing**
   - Routing logic encapsulated in interchangeable strategies
   - Enables runtime selection of routing algorithm
   - Easy to add new routing criteria without modifying core logic

3. **Factory Pattern for Provider Creation**
   - Centralizes provider instantiation logic
   - Manages provider credentials and configuration
   - Simplifies adding new AI providers

### 2.2 Billing Context

**Responsibility:** Track usage, calculate costs, generate invoices, and provide analytics.

**Core Capabilities:**
- Real-time usage tracking per team/project
- Cost calculation with provider-specific pricing
- Invoice generation and payment processing
- Budget alerts and threshold monitoring
- Usage analytics and reporting

**Domain Concepts:**
- Usage records (who used what, when, how much)
- Pricing rules (per-provider, per-model rates)
- Invoices (billing periods, line items, totals)
- Budget policies (limits, alert thresholds)

### 2.3 Workflow Context

**Responsibility:** Enable chaining of multiple AI operations into reusable workflows.

**Core Capabilities:**
- Workflow definition and storage
- Step sequencing and variable passing
- Conditional branching
- Error handling and retry policies
- Workflow templates and marketplace

**Domain Concepts:**
- Workflow (sequence of steps)
- WorkflowStep (single operation)
- Execution context (runtime state)
- Step results (output from each operation)

### 2.4 Platform Context

**Responsibility:** Cross-cutting concerns including authentication, authorization, and multi-tenancy.

**Core Capabilities:**
- Organization and team management
- API key generation and validation
- Role-based access control
- Audit logging
- Rate limiting enforcement

### 2.5 Gateway Service

**Responsibility:** HTTP API layer that routes requests to appropriate bounded contexts.

**Core Capabilities:**
- REST API endpoints
- Request validation and transformation
- Response serialization
- API versioning
- OpenAPI documentation

---

## 3. Hexagonal Architecture Implementation

### 3.1 Layer Responsibilities

**Domain Layer (Core)**
- Contains business logic and rules
- No dependencies on external frameworks
- Defines ports (interfaces) for external integrations
- Pure Python with no infrastructure concerns

**Application Layer**
- Orchestrates domain objects to fulfill use cases
- Implements application-specific business flows
- Coordinates between domain services
- Transaction boundaries and error handling

**Ports Layer**
- Defines abstract interfaces for external dependencies
- Inbound ports (use cases callable by outer layers)
- Outbound ports (services needed by domain)
- Technology-agnostic contracts

**Infrastructure Layer (Adapters)**
- Implements ports using specific technologies
- Database access (SQLAlchemy, Django ORM)
- External API clients (OpenAI, Anthropic, Google)
- Caching implementations (Redis)
- Message queues (RabbitMQ, Kafka)

### 3.2 Dependency Flow

```
┌─────────────────────────────────────────────┐
│         External Frameworks                 │
│    (FastAPI, SQLAlchemy, Redis)             │
└─────────────────┬───────────────────────────┘
                  │
                  │ implements
                  ▼
┌─────────────────────────────────────────────┐
│         Infrastructure Layer                │
│         (Adapters)                          │
└─────────────────┬───────────────────────────┘
                  │
                  │ depends on
                  ▼
┌─────────────────────────────────────────────┐
│         Ports Layer                         │
│         (Interfaces)                        │
└─────────────────┬───────────────────────────┘
                  ▲
                  │ defines
                  │
┌─────────────────┴───────────────────────────┐
│         Domain Layer                        │
│    (Business Logic - Pure Python)           │
└─────────────────────────────────────────────┘
```

**Key Principle:** Dependencies point inward. Domain layer has zero dependencies on outer layers.

### 3.3 Provider Adapter Pattern

Each AI provider is wrapped in an adapter that implements the `ProviderPort` interface:

```python
# Domain defines the contract
class ProviderPort(Protocol):
    def complete(self, prompt: Prompt, model: ModelName) -> CompletionResult:
        """Generate completion from provider"""
        pass
    
    def calculate_cost(self, tokens: Tokens) -> Cost:
        """Calculate cost for token usage"""
        pass

# Infrastructure implements for each provider
class OpenAIAdapter(ProviderPort):
    """Adapts OpenAI API to our domain interface"""
    def complete(self, prompt: Prompt, model: ModelName) -> CompletionResult:
        # Transform domain objects to OpenAI format
        # Call OpenAI API
        # Transform response back to domain objects
        pass

class AnthropicAdapter(ProviderPort):
    """Adapts Anthropic API to our domain interface"""
    # Similar implementation with Anthropic-specific details
    pass
```

**Benefits:**
- Domain logic doesn't know about specific provider APIs
- Switching providers requires no domain code changes
- Easy to mock for testing
- New providers added without touching existing code

---

## 4. Key Design Patterns

### 4.1 Strategy Pattern (Routing)

**Problem:** Need different algorithms for selecting AI providers based on varying criteria.

**Solution:** Encapsulate each routing algorithm in a separate strategy class.

```
RoutingStrategy (Interface)
    ├── CostStrategy (minimize cost)
    ├── SpeedStrategy (minimize latency)
    └── QualityStrategy (maximize quality)
```

**Implementation Location:** `completion_context/domain/services/routing/`

**Benefits:**
- Runtime selection of routing algorithm
- Easy to add new strategies
- Testable in isolation
- No conditional logic in domain model

### 4.2 Factory Pattern (Provider Creation)

**Problem:** Complex logic for instantiating provider clients with proper configuration.

**Solution:** Centralize creation logic in a factory service.

**Implementation Location:** `completion_context/domain/services/provider_factory.py`

**Benefits:**
- Single responsibility for object creation
- Encapsulates provider-specific initialization
- Simplifies adding new providers
- Manages credential injection

### 4.3 Decorator Pattern (Cross-Cutting Concerns)

**Problem:** Need to add caching and retry logic without modifying core business logic.

**Solution:** Wrap use cases with decorators that add behavior.

```python
@cache_decorator
@retry_decorator
def create_completion(request: CompletionRequest) -> CompletionResult:
    # Core business logic here
    pass
```

**Implementation Location:** `completion_context/application/decorators/`

**Benefits:**
- Separation of concerns
- Composable behaviors
- Non-invasive enhancements
- Easy to enable/disable features

### 4.4 Value Object Pattern (Domain Modeling)

**Problem:** Primitive obsession - using strings and numbers to represent domain concepts.

**Solution:** Create immutable value objects that enforce invariants.

**Examples:**
- `Prompt`: Ensures valid prompt format and length
- `ModelName`: Validates against supported models
- `Tokens`: Immutable token count with validation
- `Cost`: Monetary value with currency and precision

**Implementation Location:** `completion_context/domain/value_objects/`

**Benefits:**
- Self-validating objects
- Expressiveness in domain model
- Type safety
- Encapsulation of business rules

---

## 5. Inter-Context Communication

### 5.1 Communication Patterns

**Synchronous (Direct Calls):**
- Used for immediate consistency requirements
- Gateway Service → Completion Context (real-time completion)
- Completion Context → Billing Context (record usage)

**Asynchronous (Events):**
- Used for eventual consistency scenarios
- Completion Context publishes "CompletionCreated" event
- Billing Context subscribes to calculate costs
- Analytics Context subscribes to update dashboards

### 5.2 Event-Driven Architecture

```
┌──────────────────┐
│  Completion      │
│   Context        │
└────────┬─────────┘
         │ publishes
         │ CompletionCreated
         ▼
┌────────────────────────┐
│   Event Bus            │
│   (RabbitMQ/Kafka)     │
└───┬──────────────┬─────┘
    │              │
    │ subscribes   │ subscribes
    ▼              ▼
┌─────────┐   ┌─────────┐
│ Billing │   │Analytics│
│ Context │   │ Context │
└─────────┘   └─────────┘
```

**Event Types:**
- `CompletionCreated`: New completion request processed
- `CompletionFailed`: Request failed after retries
- `BudgetThresholdReached`: Team approaching budget limit
- `WorkflowCompleted`: Multi-step workflow finished

### 5.3 Shared Kernel

**Purpose:** Define common concepts used across multiple contexts.

**Contents:**
- Base value object classes
- Common event types
- Shared exceptions
- Utility functions

**Location:** `shared_kernel/`

**Principle:** Keep shared kernel minimal. Prefer duplication over coupling.

---

## 6. Infrastructure Decisions

### 6.1 Technology Stack

**Application Framework:**
- FastAPI (async support, automatic OpenAPI generation)
- Python 3.11+ (type hints, performance)

**Data Persistence:**
- PostgreSQL (relational data, ACID compliance)
- Redis (caching, session storage)

**Message Broker:**
- RabbitMQ or Apache Kafka (event streaming)

**Monitoring:**
- Prometheus (metrics)
- Grafana (dashboards)
- ELK Stack (log aggregation)

### 6.2 Deployment Architecture

```
┌─────────────────────────────────────────────┐
│         Load Balancer (Nginx)               │
└─────────────────┬───────────────────────────┘
                  │
        ┌─────────┴─────────┐
        ▼                   ▼
┌───────────────┐   ┌───────────────┐
│  Gateway      │   │  Gateway      │
│  Service      │   │  Service      │
│  (Instance 1) │   │  (Instance 2) │
└───────┬───────┘   └───────┬───────┘
        │                   │
        └─────────┬─────────┘
                  │
        ┌─────────┴─────────┬─────────┐
        ▼                   ▼         ▼
┌─────────────┐   ┌─────────────┐   ┌─────────────┐
│ Completion  │   │  Billing    │   │  Workflow   │
│ Service     │   │  Service    │   │  Service    │
└─────────────┘   └─────────────┘   └─────────────┘
        │                   │                │
        └─────────┬─────────┴────────────────┘
                  │
        ┌─────────┴─────────┬─────────┐
        ▼                   ▼         ▼
┌─────────────┐   ┌─────────────┐   ┌─────────────┐
│ PostgreSQL  │   │   Redis     │   │  RabbitMQ   │
│ (Primary)   │   │  (Cache)    │   │  (Events)   │
└─────────────┘   └─────────────┘   └─────────────┘
```

### 6.3 Scalability Strategy

**Horizontal Scaling:**
- Stateless service design
- All services can run multiple instances
- Load balancing across instances

**Vertical Separation:**
- Each bounded context can scale independently
- High-traffic contexts get more resources
- Database read replicas for analytics

**Caching Strategy:**
- L1: In-memory cache per instance
- L2: Distributed Redis cache
- Semantic similarity cache for AI completions

---

## 7. Testing Strategy

### 7.1 Test Pyramid

```
        ┌──────┐
        │  E2E │  (Few - Critical user journeys)
        └──────┘
       ┌────────┐
       │Integr. │   (Some - Context boundaries)
       └────────┘
      ┌──────────┐
      │   Unit   │    (Many - Domain logic, value objects)
      └──────────┘
```

### 7.2 Test Organization

**Unit Tests:**
- Location: `tests/unit/`
- Focus: Domain logic, value objects, strategies
- Tools: pytest, no external dependencies
- Coverage target: 90%+

**Integration Tests:**
- Location: `tests/integration/`
- Focus: Adapter implementations, database operations
- Tools: pytest, testcontainers
- Coverage: All adapters and repositories

**End-to-End Tests:**
- Location: `tests/e2e/`
- Focus: Complete user workflows
- Tools: pytest, test database
- Coverage: Happy paths and critical errors

### 7.3 Test Doubles

**Domain Layer Tests:**
- Use pure mocks (no framework dependencies)
- Test value object validation
- Test domain service logic

**Application Layer Tests:**
- Mock ports (use test doubles)
- Verify use case orchestration
- Test transaction boundaries

**Infrastructure Layer Tests:**
- Use real dependencies via containers
- Test actual API integrations
- Verify data persistence

---

## 8. Security Considerations

### 8.1 API Key Management

**Strategy:**
- API keys hashed before storage (bcrypt)
- Separate keys for different permission scopes
- Automatic key rotation support
- Rate limiting per key

### 8.2 Provider Credentials

**Strategy:**
- Stored encrypted in database
- Accessed via secret management service
- Never logged or exposed in responses
- Rotation without downtime

### 8.3 Data Protection

**Strategy:**
- TLS for all API communication
- Encryption at rest for sensitive data
- PII handling compliance (GDPR)
- Audit logs for all access

---

## 9. Monitoring & Observability

### 9.1 Metrics

**Business Metrics:**
- Requests per second per team
- Total tokens consumed
- Cost per completion
- Provider distribution

**Technical Metrics:**
- Response time (p50, p95, p99)
- Error rates per provider
- Cache hit ratio
- Queue depths

### 9.2 Logging

**Structure:**
- JSON format for all logs
- Correlation IDs for request tracing
- Separate log levels per context
- Centralized log aggregation

### 9.3 Alerting

**Critical Alerts:**
- Provider downtime
- Budget threshold exceeded
- Abnormal error rates
- Queue backlog growing

---

## 10. Development Workflow

### 10.1 Repository Structure

```
services/
├── completion_context/     (Bounded context)
├── billing_context/        (Bounded context)
├── workflow_context/       (Bounded context)
├── platform/               (Shared services)
├── gateway_service/        (API layer)
└── shared_kernel/          (Common types)
```

### 10.2 Development Guidelines

**Adding New Features:**
1. Identify affected bounded context
2. Define domain model changes
3. Update ports if external integration needed
4. Implement in domain → application → infrastructure
5. Add tests at each layer
6. Update API endpoints if needed

**Adding New Provider:**
1. Create adapter in `infrastructure/providers/`
2. Implement `ProviderPort` interface
3. Register in `ProviderFactory`
4. Add integration tests
5. Update documentation

### 10.3 Code Quality

**Tools:**
- Black (code formatting)
- Ruff (linting)
- MyPy (type checking)
- Pytest (testing)
- Coverage (test coverage)

**CI/CD Pipeline:**
1. Lint and format check
2. Type checking
3. Unit tests
4. Integration tests
5. Build Docker images
6. Deploy to staging
7. E2E tests
8. Deploy to production

---

## 11. Future Enhancements

### 11.1 Planned Features

**Phase 1 (Current):**
- Core completion routing
- Basic billing tracking
- Simple workflows

**Phase 2:**
- Advanced caching strategies
- Multi-model ensembles
- Workflow marketplace

**Phase 3:**
- AI model fine-tuning integration
- Custom model hosting
- Advanced analytics

### 11.2 Scalability Roadmap

**Stage 1:** Single deployment (< 100 requests/sec)
**Stage 2:** Multi-instance deployment (< 1000 requests/sec)
**Stage 3:** Microservices per context (< 10000 requests/sec)
**Stage 4:** Event-driven architecture (unlimited scale)

---

## 12. Conclusion

This architecture provides:

**Maintainability:**
- Clear separation of concerns
- Well-defined boundaries
- Minimal coupling between contexts

**Testability:**
- Pure domain logic testable without infrastructure
- Ports enable easy mocking
- Clear test boundaries

**Scalability:**
- Independent context scaling
- Event-driven communication
- Stateless service design

**Extensibility:**
- New providers via adapter pattern
- New routing strategies via strategy pattern
- New contexts without modifying existing ones

The DDD and Hexagonal Architecture patterns ensure the system remains flexible and maintainable as requirements evolve and scale increases.

---

## Appendix A: Glossary

**Bounded Context:** A logical boundary within which a particular domain model is defined and applicable.

**Aggregate Root:** The main entity that controls access to a cluster of related objects.

**Value Object:** An immutable object defined by its attributes rather than identity.

**Port:** An interface defining how the domain interacts with external systems.

**Adapter:** An implementation of a port using specific technology.

**Domain Service:** Business logic that doesn't naturally fit within an entity.

**Use Case:** An application service that orchestrates domain objects to fulfill a business goal.

---

## Appendix B: References

**Design Patterns:**
- Domain-Driven Design (Eric Evans)
- Hexagonal Architecture (Alistair Cockburn)
- Clean Architecture (Robert C. Martin)

**Implementation:**
- Python Type Hints (PEP 484)
- FastAPI Best Practices
- PostgreSQL Performance Tuning

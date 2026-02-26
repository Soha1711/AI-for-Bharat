# Design Document: Jan-Sahayak AI

## Overview

Jan-Sahayak AI is a serverless, voice-native civic assistance platform that enables Indian citizens to interact with government services through WhatsApp in their preferred language. The system leverages AWS serverless architecture with Amazon Bedrock for AI reasoning, Bhashini API for multi-language support, and Amazon Kendra for intelligent document search across government policy repositories.

The platform follows a microservices architecture with event-driven communication, ensuring scalability, reliability, and cost-effectiveness. Citizens can submit voice messages in any of 22+ Indian languages, receive accurate policy information backed by official government documents, and report civic grievances with automated tracking.

## Architecture

### High-Level Architecture

Architecture: WhatsApp -> API Gateway -> Lambda Orchestrator -> Bhashini/Bedrock/Kendra

### Component Architecture

The system is designed with clear separation of concerns across multiple layers:

1. **Interface Layer**: WhatsApp Business API handles user interactions
2. **Gateway Layer**: API Gateway provides secure, scalable entry point
3. **Orchestration Layer**: Central coordinator manages workflow and routing
4. **Processing Layer**: Specialized Lambda functions handle specific tasks
5. **AI/ML Layer**: External services provide language and reasoning capabilities
6. **Data Layer**: Multiple storage solutions optimized for different data types
7. **Security Layer**: Comprehensive security controls across all components

## Components and Interfaces

### 1. WhatsApp Business API Integration

**Purpose**: Primary user interface for voice and text interactions

**Interfaces**:
- **Webhook Endpoint**: Receives incoming messages from WhatsApp
- **Send Message API**: Delivers responses back to users
- **Media Download API**: Retrieves voice message files

**Key Features**:
- Webhook verification and security validation
- Voice message file handling (up to 5MB)
- Message status tracking and delivery confirmation
- Rate limiting and quota management

### 2. Orchestrator Lambda

**Purpose**: Central coordination service managing all user interactions

**Interfaces**:
- **WhatsApp Webhook Handler**: Processes incoming webhook events
- **SQS Publisher**: Routes messages to appropriate processing queues
- **SNS Publisher**: Sends responses back to users
- **DynamoDB Interface**: Manages conversation state and user sessions

**Key Features**:
- Message routing based on content type and user intent
- Session management and conversation context
- Error handling and retry logic
- Response aggregation and formatting

### 3. Voice Processing Lambda

**Purpose**: Handles audio message processing and speech-to-text conversion

**Interfaces**:
- **Bhashini ASR API**: Automatic Speech Recognition
- **S3 Interface**: Temporary audio file storage
- **SQS Consumer**: Receives voice processing requests

**Key Features**:
- Audio format validation and conversion
- Multi-language speech recognition
- Audio quality assessment and enhancement
- Transcription confidence scoring

### 4. Language Processing Lambda

**Purpose**: Manages translation, transliteration, and language detection

**Interfaces**:
- **Bhashini Translation API**: Multi-language translation services
- **Bhashini TTS API**: Text-to-speech synthesis
- **Language Detection Service**: Automatic language identification

**Key Features**:
- Support for 22+ Indian languages and dialects
- Context-aware translation maintaining meaning
- Voice synthesis with natural-sounding output
- Fallback mechanisms for unsupported languages

### 5. Policy Query Lambda

**Purpose**: Processes policy-related questions using RAG architecture

**Interfaces**:
- **Amazon Bedrock API**: LLM reasoning and response generation
- **Amazon Kendra API**: Intelligent document search
- **S3 Interface**: Access to policy document repository

**Key Features**:
- Semantic search across government documents
- Context-aware response generation
- Source citation and document references
- Confidence scoring and uncertainty handling

### 6. Grievance Processing Lambda

**Purpose**: Handles civic grievance reporting and tracking

**Interfaces**:
- **DynamoDB Interface**: Grievance storage and retrieval
- **SNS Interface**: Notification services
- **Location Services**: Geographic data processing

**Key Features**:
- Structured grievance data extraction
- Unique reference number generation
- Duplicate detection and consolidation
- Status tracking and updates

### 7. Amazon Bedrock Integration

**Purpose**: Provides LLM capabilities for natural language understanding and generation

**Configuration**:
- **Model**: Claude 3 Haiku for cost-effective processing
- **Knowledge Base**: RAG implementation with S3 document repository
- **Embedding Model**: Amazon Titan Embeddings for semantic search

**Key Features**:
- Contextual understanding of citizen queries
- Accurate response generation based on official documents
- Source attribution and citation generation
- Hallucination detection and prevention

### 8. Bhashini API Integration

**Purpose**: Enables comprehensive multi-language support

**Services Used**:
- **ASR (Automatic Speech Recognition)**: Voice-to-text conversion
- **NMT (Neural Machine Translation)**: Language translation
- **TTS (Text-to-Speech)**: Voice response generation
- **Transliteration**: Script conversion services

**Key Features**:
- Pipeline-based processing for complex language tasks
- Quality assessment and confidence scoring
- Fallback mechanisms for service unavailability
- Caching for improved performance

### 9. Amazon Kendra Search Index

**Purpose**: Intelligent search across government policy documents

**Configuration**:
- **Data Source**: S3 bucket with government policy PDFs
- **Index Type**: Enterprise edition for advanced features
- **Document Processing**: Custom enrichment for metadata extraction

**Key Features**:
- Semantic search with natural language queries
- Document ranking based on relevance
- Metadata-based filtering and faceting
- Real-time index updates for new documents

## Data Models

### User Session Model
- sessionId: string
- phoneNumber: string
- preferredLanguage: string
- conversationHistory: Message[]
- currentContext: string
- lastActivity: Date
- userProfile: location (optional), frequentTopics

### Message Model
- messageId: string
- sessionId: string
- timestamp: Date
- type: 'voice' or 'text'
- content: original text, translated text (optional), language
- processing: status, confidence, processingTime

### Policy Query Model
- queryId: string
- sessionId: string
- question: string
- language: string
- searchResults: documents, confidence, sources
- response: answer, citations, confidence
- timestamp: Date

### Grievance Model
- grievanceId: string
- referenceNumber: string
- citizenPhone: string
- description: string
- category: string
- location: address, coordinates (optional), district, state
- status: 'submitted', 'acknowledged', 'in_progress', 'resolved'
- priority: 'low', 'medium', 'high', 'urgent'
- attachments: string[]
- timeline: submitted, acknowledged (optional), resolved (optional)
- assignedDepartment: string (optional)

### Document Reference Model
- documentId: string
- title: string
- type: 'policy', 'guideline', 'notification', 'circular'
- department: string
- lastUpdated: Date
- s3Location: string
- kendraDocumentId: string
- metadata: language, tags, applicableStates, effectiveDate, expiryDate (optional)

### API Response Model
- success: boolean
- data: any (optional)
- error: code, message, details (optional)
- metadata: requestId, timestamp, processingTime, language

## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system—essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Property Reflection

After analyzing all acceptance criteria, I identified several areas where properties could be consolidated to eliminate redundancy:

- **Message Processing Properties**: Combined voice and text message handling into unified input processing properties
- **Language Processing Properties**: Consolidated translation accuracy and dialect handling into comprehensive language support properties  
- **Citation Properties**: Merged multiple citation requirements into a single comprehensive citation property
- **Performance Properties**: Combined various response time requirements into unified performance properties
- **Security Properties**: Consolidated encryption and access control requirements into comprehensive security properties

### Core System Properties

**Property 1: Universal Input Processing**
*For any* valid voice or text message submitted via WhatsApp, the system should successfully accept and process the input regardless of format or language
**Validates: Requirements 1.1, 1.2**

**Property 2: Language-Consistent Response Generation**
*For any* citizen interaction, the system should provide responses in the citizen's preferred language with maintained meaning and context
**Validates: Requirements 1.3, 2.4**

**Property 3: Message Queuing Resilience**
*For any* network connectivity failure, all submitted messages should be queued and processed successfully once connectivity is restored
**Validates: Requirements 1.5**

**Property 4: Multi-Language Processing Accuracy**
*For any* input in the 22 supported Indian languages or their regional dialects, the Language_Processor should accurately understand and translate the content
**Validates: Requirements 2.1, 2.2**

**Property 5: Policy Information Retrieval Completeness**
*For any* valid policy query, the Knowledge_Engine should retrieve all relevant information from the Policy_Repository and provide comprehensive coverage when multiple policies apply
**Validates: Requirements 3.1, 3.2**

**Property 6: Outdated Information Handling**
*For any* policy information that is outdated, the system should indicate the last update date and recommend verification
**Validates: Requirements 3.4**

**Property 7: Comprehensive Citation Requirement**
*For any* policy response generated by the Knowledge_Engine, the response should include specific source citations with document names and relevant sections
**Validates: Requirements 3.5, 6.2**

**Property 8: Complete Grievance Data Capture**
*For any* grievance submission, the system should capture all relevant details including location, issue type, and description, or request missing information through follow-up questions
**Validates: Requirements 4.1, 4.3**

**Property 9: Unique Reference Number Generation**
*For any* set of submitted grievances, all generated tracking reference numbers should be unique across the entire system
**Validates: Requirements 4.2**

**Property 10: Grievance Confirmation and Tracking**
*For any* successfully recorded grievance, the system should provide confirmation receipt and tracking reference to the citizen
**Validates: Requirements 4.4**

**Property 11: Duplicate Grievance Detection**
*For any* new grievance submission, if similar grievances exist in the system, the citizen should be informed about existing reports and their status
**Validates: Requirements 4.5**

**Property 12: Automatic Document Indexing**
*For any* policy document uploaded to the Policy_Repository, the Search_Index should automatically index the content and extract key metadata for retrieval
**Validates: Requirements 5.1, 5.3**

**Property 13: Document Update Re-indexing**
*For any* updated policy document, the Search_Index should re-index the content and mark previous versions as outdated
**Validates: Requirements 5.2**

**Property 14: Multi-Language Document Indexing**
*For any* document containing multiple languages, the Search_Index should index content in all available languages for comprehensive searchability
**Validates: Requirements 5.4**

**Property 15: Indexing Error Recovery**
*For any* indexing failure, the Search_Index should log errors and retry processing with alternative methods
**Validates: Requirements 5.5**

**Property 16: Verified Source Information Only**
*For any* policy query response, the Knowledge_Engine should only use information from verified government documents in the Policy_Repository
**Validates: Requirements 6.1**

**Property 17: Low Confidence Response Handling**
*For any* response where information confidence is below 95%, the Knowledge_Engine should indicate uncertainty and recommend direct government contact
**Validates: Requirements 6.3**

**Property 18: Conflicting Information Presentation**
*For any* query where conflicting information exists across documents, the Knowledge_Engine should present all perspectives and clearly indicate the conflict
**Validates: Requirements 6.4**

**Property 19: Auto-scaling Load Response**
*For any* increase or decrease in citizen request volume, the Orchestrator should automatically scale processing capacity up or down to handle the load efficiently
**Validates: Requirements 7.1, 7.2**

**Property 20: Fault-Tolerant Request Routing**
*For any* component failure, the Orchestrator should route requests to healthy instances and maintain service availability
**Validates: Requirements 7.3**

**Property 21: Component Coordination for Voice Processing**
*For any* voice message processing request, the Orchestrator should properly coordinate between Voice_Interface, Language_Processor, and Knowledge_Engine
**Validates: Requirements 7.4**

**Property 22: Universal Data Encryption**
*For any* voice message or personal data submitted by citizens, the system should encrypt all data during transmission and storage
**Validates: Requirements 8.1**

**Property 23: Access Control Enforcement**
*For any* attempt to access grievance data, the system should only allow access to authorized personnel and block unauthorized access attempts
**Validates: Requirements 8.3**

**Property 24: Data Deletion Compliance**
*For any* citizen request for data deletion, the system should permanently remove their information within 30 days
**Validates: Requirements 8.4**

**Property 25: Breach Notification Protocol**
*For any* detected data breach, the system should immediately notify affected citizens and relevant authorities
**Validates: Requirements 8.5**

**Property 26: API Rate Limit Handling**
*For any* integration with external APIs (Bhashini, Kendra), the system should handle rate limits and implement appropriate retry mechanisms
**Validates: Requirements 9.1, 9.3**

**Property 27: External Service Fallback**
*For any* unavailability of external services (Bhashini API, AWS services), the system should implement fallback mechanisms and maintain core functionality
**Validates: Requirements 9.2, 9.4**

**Property 28: Automatic Credential Refresh**
*For any* API credential expiration, the system should automatically refresh authentication and maintain service continuity
**Validates: Requirements 9.5**

**Property 29: Response Time Guarantees**
*For any* citizen interaction, the system should provide initial acknowledgment within 5 seconds and policy query responses within 30 seconds for 95% of requests
**Validates: Requirements 10.1, 10.2**

**Property 30: Performance Under Load**
*For any* high load condition, the system should maintain response times within acceptable limits through auto-scaling mechanisms
**Validates: Requirements 10.3**

**Property 31: Availability Monitoring and Recovery**
*For any* service availability drop below 99.5%, the system should trigger automated recovery procedures
**Validates: Requirements 10.4**

**Property 32: Clear Error Communication**
*For any* processing failure, the system should provide clear error messages and alternative contact methods to citizens
**Validates: Requirements 10.5**

## Error Handling

### Error Categories and Responses

**1. Input Processing Errors**
- Invalid audio formats: Convert to supported format or request resubmission
- Oversized messages: Reject with size limit explanation
- Corrupted data: Request message resubmission with error details

**2. Language Processing Errors**
- Unsupported language detection: Respond in Hindi/English with language options
- Translation confidence below threshold: Provide best-effort translation with uncertainty notice
- Bhashini API failures: Fall back to cached translations or alternative services

**3. Knowledge Retrieval Errors**
- No relevant documents found: Provide alternative resources and contact information
- Kendra service unavailability: Use cached results or provide manual assistance options
- Document access failures: Log error and provide alternative information sources

**4. System Integration Errors**
- AWS service outages: Implement graceful degradation with core functionality
- Database connection failures: Use read replicas and retry mechanisms
- External API rate limiting: Implement exponential backoff and queue management

**5. Security and Compliance Errors**
- Authentication failures: Require re-authentication with clear instructions
- Access control violations: Log security events and deny access with explanation
- Data encryption errors: Fail securely and notify administrators

### Error Recovery Strategies

**Automatic Recovery**:
- Retry mechanisms with exponential backoff
- Circuit breaker patterns for external services
- Automatic failover to backup systems
- Self-healing through health checks and restarts

**Manual Intervention**:
- Administrator notifications for critical failures
- Escalation procedures for unresolved issues
- Manual override capabilities for emergency situations
- Comprehensive logging for troubleshooting

## Testing Strategy

### Dual Testing Approach

The Jan-Sahayak AI platform requires both unit testing and property-based testing to ensure comprehensive coverage and correctness:

**Unit Tests**: Focus on specific examples, edge cases, and error conditions
- WhatsApp webhook validation with specific message formats
- Bhashini API integration with known language pairs
- Kendra search with predefined document sets
- Error handling scenarios with specific failure conditions
- Integration points between Lambda functions

**Property Tests**: Verify universal properties across all inputs
- Message processing correctness across all supported languages
- Translation accuracy through round-trip testing
- Search result relevance across diverse query types
- System performance under varying load conditions
- Security controls across all data access patterns

### Property-Based Testing Configuration

**Testing Framework**: Use Hypothesis (Python) for property-based testing
- Minimum 100 iterations per property test to ensure statistical confidence
- Custom generators for Indian language text, voice messages, and policy documents
- Shrinking strategies to find minimal failing examples

**Test Tagging**: Each property test must reference its design document property
- Tag format: **Feature: jan-sahayak-ai, Property {number}: {property_text}**
- Example: **Feature: jan-sahayak-ai, Property 1: Universal Input Processing**

**Coverage Requirements**:
- All 32 correctness properties must be implemented as property-based tests
- Each property test validates the universal behavior described in the property
- Edge cases identified in prework analysis should be covered by specific unit tests
- Integration tests should verify end-to-end workflows across all components

### Testing Infrastructure

**Test Environment**:
- Isolated AWS environment with all services configured
- Mock Bhashini API for consistent testing
- Sample government document repository for Kendra testing
- Automated test data generation for various Indian languages

**Continuous Testing**:
- Property tests run on every code change
- Performance benchmarks tracked over time
- Security tests integrated into CI/CD pipeline
- Compliance validation automated where possible

**Test Data Management**:
- Synthetic data generation for privacy compliance
- Multi-language test datasets covering all supported languages
- Government document samples for policy testing
- Load testing scenarios for performance validation
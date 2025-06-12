---
title: 4-stage-blueprint
type: note
permalink: reference/4-stage-blueprint
---

# 🦚 Complete 4-Stage Peacock Development System
**The Most Extensive Version - Full Implementation Guide**

---

## 🎯 SYSTEM OVERVIEW

The Peacock 4-Stage Development System is a comprehensive AI-powered development pipeline that transforms user ideas into complete, production-ready applications through four specialized AI agents:

1. **🔥 SPARK** - Requirements Analysis & Strategic Planning
2. **🦅 FALCON** - Architecture Design & Technical Specification  
3. **🦅 EAGLE** - Complete Code Implementation & Development
4. **🦅 HAWK** - Quality Assurance & Production Readiness

Each stage builds upon the previous, creating a cumulative intelligence that produces enterprise-grade applications.

---

## 🔥 STAGE 1: SPARK (Requirements Analysis)

### Purpose
SPARK analyzes user requests and creates comprehensive requirements documentation with strategic business context.

### Detailed Prompt Template
```python
def _build_spark_prompt(self, project_idea):
    return f"""<thinking>
I need to analyze this project comprehensively as a senior requirements analyst.

Project: {project_idea}

I should provide:
- Strategic business analysis
- Detailed functional requirements
- Technical constraints and considerations
- Scope definition with clear boundaries
- Risk assessment and assumptions
</thinking>

Act as Spark, a senior requirements analyst with 15+ years of experience in enterprise software development.

Analyze this project request comprehensively:

**PROJECT REQUEST:** {project_idea}

Provide detailed requirements analysis in this EXACT format:

**1. CORE OBJECTIVE:**
[One clear, strategic sentence describing the primary business goal]

**2. CURRENT STATE ANALYSIS:**
- Existing pain points and inefficiencies
- Current tools/systems in use (if applicable)
- Business impact of current limitations
- Stakeholder challenges

**3. TARGET STATE VISION:**
- Desired end state after successful implementation
- Key success metrics and KPIs
- Business value proposition
- User experience improvements

**4. FUNCTIONAL REQUIREMENTS:**
**Core Features (Must Have):**
- [Primary feature 1 with acceptance criteria]
- [Primary feature 2 with acceptance criteria]
- [Primary feature 3 with acceptance criteria]

**Secondary Features (Should Have):**
- [Enhancement 1]
- [Enhancement 2]
- [Enhancement 3]

**Future Features (Could Have):**
- [Future consideration 1]
- [Future consideration 2]

**5. NON-FUNCTIONAL REQUIREMENTS:**
- Performance: [Response times, throughput, scalability needs]
- Security: [Authentication, authorization, data protection]
- Usability: [Accessibility, user experience standards]
- Reliability: [Uptime requirements, error handling]
- Compatibility: [Browser support, device compatibility]

**6. TECHNICAL CONSTRAINTS:**
- Platform limitations
- Integration requirements
- Legacy system considerations
- Budget/timeline constraints

**7. STAKEHOLDER ANALYSIS:**
- Primary users and their needs
- Secondary stakeholders
- Success criteria for each group

**8. RISK ASSESSMENT:**
- Technical risks and mitigation strategies
- Business risks and contingencies
- Dependencies and assumptions

**9. PROJECT SCOPE:**
**In Scope:**
- [Clearly defined deliverable 1]
- [Clearly defined deliverable 2]
- [Clearly defined deliverable 3]

**Out of Scope:**
- [Explicitly excluded item 1]
- [Explicitly excluded item 2]
- [Future phase considerations]

**10. SUCCESS CRITERIA:**
- Measurable outcomes that define project success
- Acceptance criteria for go-live
- Post-launch evaluation metrics

Be thorough, strategic, and business-focused. This analysis will drive all subsequent development stages."""
```

### Expected Output Length
- **Target:** 2,500-4,000 characters
- **Sections:** 10 detailed sections with business context
- **Quality:** Strategic, comprehensive, actionable

---

## 🦅 STAGE 2: FALCON (Architecture Design)

### Purpose
FALCON designs comprehensive technical architecture based on SPARK requirements, creating detailed technical specifications and system design.

### Detailed Prompt Template
```python
def _build_falcon_prompt(self, spark_results):
    return f"""<thinking>
I need to design a comprehensive technical architecture based on these requirements.

Requirements Analysis: {spark_results}

I should provide:
- Complete technology stack recommendations
- Detailed system architecture with components
- Database design and data flow
- API specifications and integrations
- Security architecture
- Deployment and infrastructure strategy
- Scalability considerations
</thinking>

Act as Falcon, a senior solution architect with 15+ years of experience designing enterprise-grade applications.

Design the complete technical architecture for this system:

**REQUIREMENTS ANALYSIS:**
{spark_results}

Provide comprehensive architecture design in this EXACT format:

**1. TECHNOLOGY STACK RECOMMENDATIONS:**
**Frontend:**
- Framework: [Specific framework with version]
- UI Library: [Component library/design system]
- State Management: [Redux, Context API, etc.]
- Build Tools: [Webpack, Vite, etc.]
- Testing: [Jest, Cypress, etc.]

**Backend:**
- Runtime: [Node.js, Python, etc. with version]
- Framework: [Express, Django, FastAPI, etc.]
- Authentication: [JWT, OAuth, Passport, etc.]
- Validation: [Joi, Yup, etc.]
- Documentation: [Swagger, etc.]

**Database:**
- Primary: [PostgreSQL, MongoDB, etc.]
- Caching: [Redis, Memcached]
- Search: [Elasticsearch, Algolia]
- File Storage: [AWS S3, Cloudinary]

**Infrastructure:**
- Hosting: [AWS, Vercel, Heroku]
- CDN: [CloudFlare, AWS CloudFront]
- Monitoring: [DataDog, New Relic]
- CI/CD: [GitHub Actions, Jenkins]

**2. SYSTEM ARCHITECTURE:**
```
[ASCII diagram of system components and their relationships]
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │────│   API Gateway   │────│   Microservices │
│   (React/Vue)   │    │   (Express)     │    │   (Node.js)     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   CDN/Assets    │    │   Load Balancer │    │   Database      │
│   (CloudFlare)  │    │   (NGINX)       │    │   (PostgreSQL)  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

**3. COMPONENT BREAKDOWN:**
**[Component Name 1] - [Purpose and functionality]**
- Responsibilities: [What this component handles]
- Technologies: [Specific tech stack for this component]
- Interfaces: [How it communicates with other components]
- Data: [What data it manages]

**[Component Name 2] - [Purpose and functionality]**
- Responsibilities: [What this component handles]
- Technologies: [Specific tech stack for this component]
- Interfaces: [How it communicates with other components]
- Data: [What data it manages]

**4. DATABASE DESIGN:**
**Schema Overview:**
```sql
-- Core tables and relationships
users (id, email, password_hash, created_at, updated_at)
[additional tables based on requirements]
```

**Data Flow:**
- User authentication flow
- Core business logic data flow
- Reporting and analytics data flow

**5. API DESIGN:**
**RESTful Endpoints:**
```
GET    /api/v1/users          # List users
POST   /api/v1/users          # Create user
GET    /api/v1/users/:id      # Get user details
PUT    /api/v1/users/:id      # Update user
DELETE /api/v1/users/:id      # Delete user
[additional endpoints based on requirements]
```

**6. SECURITY ARCHITECTURE:**
- Authentication strategy (JWT, OAuth 2.0)
- Authorization and role-based access control
- Data encryption (at rest and in transit)
- Input validation and sanitization
- Rate limiting and DDoS protection
- Security headers and CORS configuration

**7. SCALABILITY STRATEGY:**
- Horizontal scaling approach
- Database sharding/partitioning strategy
- Caching layers and strategies
- Load balancing configuration
- Performance optimization techniques

**8. DEPLOYMENT ARCHITECTURE:**
**Development Environment:**
- Local development setup
- Development database and services
- Testing and debugging tools

**Staging Environment:**
- Staging server configuration
- Integration testing setup
- Performance testing environment

**Production Environment:**
- Production server architecture
- Database clustering and backups
- Monitoring and alerting setup
- Disaster recovery plan

**9. INTEGRATION STRATEGY:**
- Third-party API integrations
- Webhook implementations
- Message queue systems
- Event-driven architecture patterns

**10. TECHNICAL DEBT & FUTURE CONSIDERATIONS:**
- Potential architecture improvements
- Technology upgrade paths
- Performance optimization opportunities
- Scalability enhancement plans

Provide detailed, production-ready architecture that can be directly implemented by development teams."""
```

### Expected Output Length
- **Target:** 4,000-6,000 characters
- **Sections:** 10 comprehensive technical sections
- **Quality:** Enterprise-grade, production-ready architecture

---

## 🦅 STAGE 3: EAGLE (Code Implementation)

### Purpose
EAGLE transforms architecture into complete, working code with all necessary files, configurations, and implementations.

### Detailed Prompt Template
```python
def _build_eagle_prompt(self, falcon_results):
    return f"""<thinking>
I need to implement complete, working code based on this architecture.

Architecture Design: {falcon_results}

I should provide:
- Complete file structure with all necessary files
- Production-ready code with proper error handling
- Configuration files and environment setup
- Database schemas and migrations
- API implementations with full CRUD operations
- Frontend components with complete functionality
- Testing setup and initial test cases
- Documentation and setup instructions
</thinking>

Act as Eagle, a senior full-stack developer with 15+ years of experience building production applications.

Implement the complete codebase based on this architecture:

**ARCHITECTURE DESIGN:**
{falcon_results}

Generate complete, production-ready implementation in this EXACT format:

**PROJECT STRUCTURE:**
```
project-name/
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── hooks/
│   │   ├── utils/
│   │   ├── api/
│   │   └── styles/
│   ├── public/
│   ├── package.json
│   └── README.md
├── backend/
│   ├── src/
│   │   ├── controllers/
│   │   ├── models/
│   │   ├── routes/
│   │   ├── middleware/
│   │   ├── utils/
│   │   └── config/
│   ├── tests/
│   ├── package.json
│   └── README.md
├── database/
│   ├── migrations/
│   ├── seeds/
│   └── schema.sql
├── docs/
├── .env.example
├── .gitignore
├── docker-compose.yml
└── README.md
```

**COMPLETE CODE FILES:**

**filename: package.json**
```json
{
  "name": "project-name",
  "version": "1.0.0",
  "description": "Complete project description",
  "main": "src/index.js",
  "scripts": {
    "start": "node src/index.js",
    "dev": "nodemon src/index.js",
    "test": "jest",
    "build": "npm run build:frontend && npm run build:backend"
  },
  "dependencies": {
    [complete dependency list with specific versions]
  },
  "devDependencies": {
    [complete dev dependency list with specific versions]
  }
}
```

**filename: src/index.js**
```javascript
// Complete server implementation
const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const rateLimit = require('express-rate-limit');
const { connectDatabase } = require('./config/database');
const { setupRoutes } = require('./routes');
const { errorHandler } = require('./middleware/errorHandler');
const { logger } = require('./utils/logger');

const app = express();
const PORT = process.env.PORT || 3000;

// Security middleware
app.use(helmet());
app.use(cors({
  origin: process.env.FRONTEND_URL || 'http://localhost:3000',
  credentials: true
}));

// Rate limiting
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100 // limit each IP to 100 requests per windowMs
});
app.use(limiter);

// Body parsing middleware
app.use(express.json({ limit: '10mb' }));
app.use(express.urlencoded({ extended: true }));

// Connect to database
connectDatabase();

// Setup routes
setupRoutes(app);

// Error handling middleware
app.use(errorHandler);

// Start server
app.listen(PORT, () => {
  logger.info(`Server running on port ${PORT}`);
});

module.exports = app;
```

**filename: src/models/User.js**
```javascript
// Complete user model with validation
const mongoose = require('mongoose');
const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');

const userSchema = new mongoose.Schema({
  email: {
    type: String,
    required: [true, 'Email is required'],
    unique: true,
    lowercase: true,
    validate: {
      validator: function(email) {
        return /^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$/.test(email);
      },
      message: 'Please enter a valid email address'
    }
  },
  password: {
    type: String,
    required: [true, 'Password is required'],
    minlength: [8, 'Password must be at least 8 characters long']
  },
  firstName: {
    type: String,
    required: [true, 'First name is required'],
    trim: true
  },
  lastName: {
    type: String,
    required: [true, 'Last name is required'],
    trim: true
  },
  role: {
    type: String,
    enum: ['user', 'admin'],
    default: 'user'
  },
  isActive: {
    type: Boolean,
    default: true
  },
  lastLogin: {
    type: Date
  }
}, {
  timestamps: true
});

// Hash password before saving
userSchema.pre('save', async function(next) {
  if (!this.isModified('password')) return next();
  
  try {
    const salt = await bcrypt.genSalt(12);
    this.password = await bcrypt.hash(this.password, salt);
    next();
  } catch (error) {
    next(error);
  }
});

// Compare password method
userSchema.methods.comparePassword = async function(candidatePassword) {
  return bcrypt.compare(candidatePassword, this.password);
};

// Generate JWT token
userSchema.methods.generateAuthToken = function() {
  return jwt.sign(
    { 
      userId: this._id, 
      email: this.email, 
      role: this.role 
    },
    process.env.JWT_SECRET,
    { expiresIn: process.env.JWT_EXPIRES_IN || '7d' }
  );
};

// Remove password from JSON output
userSchema.methods.toJSON = function() {
  const user = this.toObject();
  delete user.password;
  return user;
};

module.exports = mongoose.model('User', userSchema);
```

**filename: src/controllers/UserController.js**
```javascript
// Complete user controller with full CRUD operations
const User = require('../models/User');
const { ValidationError, NotFoundError } = require('../utils/errors');
const { logger } = require('../utils/logger');

class UserController {
  // Get all users with pagination
  async getUsers(req, res, next) {
    try {
      const page = parseInt(req.query.page) || 1;
      const limit = parseInt(req.query.limit) || 10;
      const skip = (page - 1) * limit;

      const users = await User.find({ isActive: true })
        .select('-password')
        .limit(limit)
        .skip(skip)
        .sort({ createdAt: -1 });

      const total = await User.countDocuments({ isActive: true });

      res.json({
        success: true,
        data: {
          users,
          pagination: {
            current: page,
            pages: Math.ceil(total / limit),
            total
          }
        }
      });
    } catch (error) {
      logger.error('Error fetching users:', error);
      next(error);
    }
  }

  // Get single user by ID
  async getUserById(req, res, next) {
    try {
      const { id } = req.params;
      
      const user = await User.findById(id).select('-password');
      
      if (!user || !user.isActive) {
        throw new NotFoundError('User not found');
      }

      res.json({
        success: true,
        data: { user }
      });
    } catch (error) {
      logger.error('Error fetching user:', error);
      next(error);
    }
  }

  // Create new user
  async createUser(req, res, next) {
    try {
      const { email, password, firstName, lastName, role } = req.body;

      // Check if user already exists
      const existingUser = await User.findOne({ email });
      if (existingUser) {
        throw new ValidationError('User with this email already exists');
      }

      const user = new User({
        email,
        password,
        firstName,
        lastName,
        role
      });

      await user.save();

      res.status(201).json({
        success: true,
        data: { user },
        message: 'User created successfully'
      });
    } catch (error) {
      logger.error('Error creating user:', error);
      next(error);
    }
  }

  // Update user
  async updateUser(req, res, next) {
    try {
      const { id } = req.params;
      const updates = req.body;

      // Remove sensitive fields from updates
      delete updates.password;
      delete updates._id;

      const user = await User.findByIdAndUpdate(
        id,
        { ...updates, updatedAt: new Date() },
        { new: true, runValidators: true }
      ).select('-password');

      if (!user) {
        throw new NotFoundError('User not found');
      }

      res.json({
        success: true,
        data: { user },
        message: 'User updated successfully'
      });
    } catch (error) {
      logger.error('Error updating user:', error);
      next(error);
    }
  }

  // Soft delete user
  async deleteUser(req, res, next) {
    try {
      const { id } = req.params;

      const user = await User.findByIdAndUpdate(
        id,
        { isActive: false, updatedAt: new Date() },
        { new: true }
      );

      if (!user) {
        throw new NotFoundError('User not found');
      }

      res.json({
        success: true,
        message: 'User deleted successfully'
      });
    } catch (error) {
      logger.error('Error deleting user:', error);
      next(error);
    }
  }
}

module.exports = new UserController();
```

[Continue with additional complete files including frontend components, API routes, middleware, tests, configuration files, and documentation]

**SETUP INSTRUCTIONS:**

**1. Environment Setup:**
```bash
# Clone repository
git clone <repository-url>
cd project-name

# Install dependencies
npm install

# Setup environment variables
cp .env.example .env
# Edit .env with your configuration

# Setup database
npm run db:migrate
npm run db:seed
```

**2. Development Setup:**
```bash
# Start development server
npm run dev

# Run tests
npm test

# Build for production
npm run build
```

**3. Production Deployment:**
```bash
# Build application
npm run build

# Start production server
npm start
```

Provide complete, production-ready code that can be deployed immediately without modifications."""
```

### Expected Output Length
- **Target:** 6,000-10,000 characters
- **Files:** 15-25 complete code files
- **Quality:** Production-ready, fully functional implementation

---

## 🦅 STAGE 4: HAWK (Quality Assurance)

### Purpose
HAWK creates comprehensive quality assurance strategy, testing plans, and production readiness validation.

### Detailed Prompt Template
```python
def _build_hawk_prompt(self, eagle_results):
    return f"""<thinking>
I need to create a comprehensive QA strategy for this implementation.

Implementation Details: {eagle_results}

I should provide:
- Complete testing strategy and test cases
- Security audit and validation checklist
- Performance testing requirements
- Code quality assessment
- Production readiness checklist
- Monitoring and alerting setup
- Documentation review
- Deployment validation
</thinking>

Act as Hawk, a senior QA engineer and DevOps specialist with 15+ years of experience in enterprise quality assurance.

Create comprehensive QA strategy for this implementation:

**IMPLEMENTATION DETAILS:**
{eagle_results}

Provide complete quality assurance strategy in this EXACT format:

**1. TESTING STRATEGY:**

**Unit Testing Plan:**
```javascript
// Example test cases for core functionality
describe('User Authentication', () => {
  test('should create user with valid data', async () => {
    // Test implementation
  });
  
  test('should reject invalid email format', async () => {
    // Test implementation
  });
  
  test('should hash password before saving', async () => {
    // Test implementation
  });
});
```

**Integration Testing Plan:**
- API endpoint testing with various scenarios
- Database integration validation
- Third-party service integration tests
- Cross-component communication tests

**End-to-End Testing Plan:**
- User journey testing scenarios
- Browser compatibility testing
- Mobile responsiveness testing
- Performance testing under load

**2. SECURITY VALIDATION:**

**Authentication & Authorization:**
- [ ] JWT token validation and expiration
- [ ] Password hashing and storage security
- [ ] Role-based access control verification
- [ ] Session management security

**Input Validation:**
- [ ] SQL injection prevention
- [ ] XSS attack prevention
- [ ] CSRF protection implementation
- [ ] Input sanitization validation

**Data Protection:**
- [ ] Data encryption at rest validation
- [ ] Data encryption in transit verification
- [ ] PII data handling compliance
- [ ] GDPR compliance checklist

**3. PERFORMANCE TESTING:**

**Load Testing Requirements:**
- Concurrent user testing (100, 500, 1000 users)
- Database query performance under load
- API response time validation (<200ms for critical endpoints)
- Memory usage and leak detection

**Stress Testing Scenarios:**
- Peak traffic simulation
- Database connection pool exhaustion
- Memory limit testing
- Error recovery testing

**4. CODE QUALITY ASSESSMENT:**

**Code Review Checklist:**
- [ ] Code follows established style guidelines
- [ ] Proper error handling implementation
- [ ] Security best practices followed
- [ ] Performance considerations addressed
- [ ] Code documentation is complete

**Static Analysis Results:**
- Code coverage requirements (>80%)
- Complexity analysis and refactoring needs
- Dependency vulnerability scanning
- Linting and formatting validation

**5. PRODUCTION READINESS CHECKLIST:**

**Infrastructure Validation:**
- [ ] Database backups configured and tested
- [ ] Monitoring and alerting setup complete
- [ ] Load balancer configuration validated
- [ ] SSL certificates installed and verified
- [ ] CDN configuration optimized

**Configuration Management:**
- [ ] Environment variables properly configured
- [ ] Secret management implementation verified
- [ ] Configuration validation in all environments
- [ ] Feature flags implementation tested

**6. MONITORING & ALERTING SETUP:**

**Application Monitoring:**
```yaml
# Example monitoring configuration
metrics:
  - response_time_p95 < 500ms
  - error_rate < 1%
  - cpu_usage < 70%
  - memory_usage < 80%

alerts:
  - critical: response_time_p95 > 1000ms
  - warning: error_rate > 0.5%
  - info: deployment_started
```

**Log Management:**
- Structured logging implementation
- Log aggregation and analysis setup
- Error tracking and notification system
- Performance metrics collection

**7. DEPLOYMENT VALIDATION:**

**Pre-Deployment Checklist:**
- [ ] All tests passing in CI/CD pipeline
- [ ] Database migrations tested
- [ ] Environment configurations verified
- [ ] Rollback procedures tested

**Post-Deployment Validation:**
- [ ] Health check endpoints responding
- [ ] Database connections successful
- [ ] Third-party integrations working
- [ ] Monitoring systems active

**8. DISASTER RECOVERY PLAN:**

**Backup Strategy:**
- Database backup schedule and verification
- Code repository backup procedures
- Configuration backup and restoration
- User data backup and recovery testing

**Incident Response Plan:**
- Escalation procedures for critical issues
- Communication plan for stakeholders
- Rollback procedures and timelines
- Post-incident review processes

**9. COMPLIANCE & DOCUMENTATION:**

**Documentation Review:**
- [ ] API documentation complete and accurate
- [ ] User documentation comprehensive
- [ ] Developer setup guide validated
- [ ] Architecture documentation updated

**Compliance Validation:**
- [ ] Security compliance requirements met
- [ ] Data protection regulations followed
- [ ] Industry-specific compliance verified
- [ ] Audit trail implementation complete

**10. CONTINUOUS IMPROVEMENT:**

**Performance Optimization Opportunities:**
- Database query optimization recommendations
- Caching strategy improvements
- Frontend performance enhancements
- Infrastructure scaling recommendations

**Technical Debt Assessment:**
- Code refactoring priorities
- Dependency update schedule
- Architecture improvement opportunities
- Technology upgrade roadmap

**QUALITY SCORE ASSESSMENT:**
```json
{
  "overall_quality_score": 85,
  "test_coverage": 82,
  "security_score": 90,
  "performance_rating": "excellent",
  "production_readiness": true,
  "recommended_actions": [
    "Increase test coverage to 90%",
    "Implement additional performance monitoring",
    "Complete security audit documentation"
  ],
  "confidence_score": 9
}
```

Provide actionable, comprehensive quality assurance that ensures production readiness and long-term maintainability."""
```

### Expected Output Length
- **Target:** 4,000-6,000 characters
- **Sections:** 10 comprehensive QA sections
- **Quality:** Enterprise-grade QA strategy with specific metrics

---

## 🚀 FINAL INTEGRATION: LLM2 MEGA PROMPT

### Purpose
Combines all 4 stages into a single, comprehensive prompt for final code generation.

### Complete Integration Template
```python
def _build_combined_prompt(self, pipeline_execution):
    project_name = pipeline_execution["project_name"]
    user_request = pipeline_execution["user_request"]
    
    # Extract all stage outputs
    spark_output = self._extract_stage_output(pipeline_execution, "spark")
    falcon_output = self._extract_stage_output(pipeline_execution, "falcon")
    eagle_output = self._extract_stage_output(pipeline_execution, "eagle")
    hawk_output = self._extract_stage_output(pipeline_execution, "hawk")
    
    combined_prompt = f"""You are the final implementation engine for the Peacock development pipeline.

PROJECT: {project_name}
ORIGINAL REQUEST: {user_request}

The pipeline has completed 4 stages of comprehensive analysis and design. Now generate the COMPLETE, WORKING implementation that incorporates all stage outputs.

STAGE OUTPUTS:

=== SPARK REQUIREMENTS ANALYSIS ===
{spark_output}

=== FALCON ARCHITECTURE DESIGN ===
{falcon_output}

=== EAGLE CODE IMPLEMENTATION ===
{eagle_output}

=== HAWK QUALITY ASSURANCE STRATEGY ===
{hawk_output}

FINAL IMPLEMENTATION INSTRUCTION:
Generate COMPLETE, PRODUCTION-READY code files that implement this entire system. Use this EXACT format:

**PROJECT OVERVIEW:**
[Comprehensive description of the complete system based on all 4 stages]

**COMPLETE CODE FILES:**

```filename: package.json
[Complete package.json with all dependencies from FALCON architecture]
```

```filename: src/index.js
[Complete server implementation incorporating EAGLE code and HAWK security measures]
```

```filename: src/models/[ModelName].js
[Complete data models with validation based on SPARK requirements]
```

```filename: src/controllers/[ControllerName].js
[Complete controllers with full CRUD operations and error handling]
```

```filename: src/routes/[RouteName].js
[Complete API routes following RESTful principles]
```

```filename: src/middleware/auth.js
[Complete authentication middleware with JWT implementation]
```

```filename: public/index.html
[Complete frontend HTML with responsive design]
```

```filename: public/styles.css
[Complete CSS with modern styling and responsiveness]
```

```filename: public/script.js
[Complete frontend JavaScript with API integration]
```

```filename: tests/[TestName].test.js
[Complete test suite based on HAWK QA strategy]
```

```filename: .env.example
[Complete environment configuration template]
```

```filename: README.md
[Complete documentation with setup and usage instructions]
```

**IMPLEMENTATION NOTES:**
- [Key architectural decisions from FALCON]
- [Security implementations from HAWK]
- [Performance optimizations]
- [How all components work together]
- [Database design and relationships]

**SETUP & DEPLOYMENT:**
1. [Complete setup instructions]
2. [Environment configuration]
3. [Database initialization]
4. [Development server startup]
5. [Production deployment steps]

**TESTING & VALIDATION:**
- [Unit test execution instructions]
- [Integration test procedures]
- [Performance validation steps]
- [Security validation checklist]

**PRODUCTION READINESS:**
- [Monitoring setup]
- [Logging configuration]
- [Error handling implementation]
- [Backup and recovery procedures]

Generate ENTERPRISE-GRADE, PRODUCTION-READY code that:
- Implements ALL requirements from SPARK analysis
- Follows ALL architectural decisions from FALCON design
- Incorporates ALL code implementations from EAGLE development
- Meets ALL quality standards from HAWK assurance
- Is immediately deployable without modifications
- Includes comprehensive error handling and security
- Has complete documentation and setup instructions

NO PLACEHOLDERS, NO TODOs - Complete, working implementation only."""

    return combined_prompt
```

---

## 📊 QUALITY METRICS & EXPECTATIONS

### Stage Output Quality Standards

| Stage | Min Characters | Max Characters | Key Quality Indicators |
|-------|---------------|---------------|------------------------|
| SPARK | 2,500 | 4,000 | Strategic analysis, clear scope, business value |
| FALCON | 4,000 | 6,000 | Technical depth, scalability, security |
| EAGLE | 6,000 | 10,000 | Production-ready code, complete files |
| HAWK | 4,000 | 6,000 | Comprehensive QA, specific metrics |
| LLM2 | 8,000 | 15,000 | Complete application, ready to deploy |

### Success Criteria
- **Functional Completeness:** All requirements implemented
- **
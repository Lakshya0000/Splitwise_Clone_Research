# Splitwise Clone - Development Plan

## Executive Summary

Building a Splitwise alternative targeting high-CPM markets (US/UK/CA) with a **Flutter mobile app** (iOS + Android) and **Go backend with Protocol Buffers**. The app addresses Splitwise's critical failures: unlimited expense tracking, instant speed, free core features, and user-friendly monetization.

**Tech Stack:**
- **Frontend:** Flutter (iOS + Android)
- **Backend:** Go with gRPC/Protocol Buffers
- **Database:** PostgreSQL (strong typing, relational data model)
- **Auth:** Email/Google OAuth (avoiding expensive SMS)
- **Real-time Sync:** WebSockets or gRPC streaming
- **Storage:** S3/GCS for receipt images
- **Monetization:** Freemium (unlimited basic + paid premium features)

---

## Core Features (Based on Research)

### Free Tier (Competitive Advantages)
1. **Unlimited Expenses** - No daily limits, address the #1 complaint
2. **Instant Speed** - No ads, no delays, tap→type→save workflow
3. **Free Search** - Search all expenses instantly
4. **Free Charts** - Basic pie charts and category breakdowns
5. **Free Export** - Download data as CSV anytime
6. **Real-time Sync** - WebSocket-based instant sync across devices
7. **Smart Currency** - Auto-detect based on locale, persistent group settings
8. **Activity Log** - Immutable history of all edits and changes

### Premium Tier Features
1. **Receipt Photo Upload** - Attach photos to expenses (MVP)
2. **Receipt OCR/AI Scanning** - Auto-extract amounts from receipts (MVP)
3. **Advanced Analytics** - Trends, category insights, spending patterns
4. **Priority Support** - Email/chat support
5. **Unlimited Receipt Storage** - Free tier gets limited storage (e.g., 50 receipts)
6. **Export to Excel** - Advanced export formats beyond CSV
7. **Custom Categories** - User-defined expense categories

### Core Functionality (Table Stakes)
1. **Groups** - Create/manage expense groups (trips, roommates, etc.)
2. **Expense Entry** - Quick add with amount, description, payer, split method
3. **Settlement Calculation** - "Who owes who" with debt simplification algorithm
4. **Payment Deep Links** - Direct links to Venmo/Zelle/PayPal/Revolut (MVP)
5. **Multi-currency** - Support USD, GBP, CAD, EUR with exchange rates
6. **Split Methods** - Equal, unequal, percentage, shares, itemized
7. **Notifications** - Push notifications for new expenses, settlements, payments

---

## Screen Breakdown (Flutter App)

### 1. **Authentication Flow**
- **Splash Screen** - App branding, check auth status
- **Welcome/Onboarding** - Value proposition, feature highlights (3-4 screens)
- **Login Screen** - Email + password, "Continue with Google" button
- **Signup Screen** - Email, password, name, currency preference
- **Forgot Password** - Email-based password reset

### 2. **Main Navigation** (Bottom Tab Bar)
- **Dashboard** - Overview of all groups and balances
- **Groups** - List of expense groups
- **Activity** - Recent transactions and notifications
- **Profile/Settings** - User settings and preferences

### 3. **Dashboard Screen**
- **Summary Cards:**
  - Total you owe (across all groups)
  - Total owed to you (across all groups)
  - Recent activity feed (last 10 transactions)
- **Quick Actions:**
  - "Add Expense" FAB (Floating Action Button)
  - "Settle Up" button
- **Active Groups** - Grid/list of groups with balance preview

### 4. **Groups Screen**
- **Group List** - All groups with:
  - Group name and icon/avatar
  - Your net balance in that group (+$50 or -$30)
  - Number of members
  - Last activity timestamp
- **Actions:**
  - Create new group (+ button)
  - Search groups
  - Filter (active, archived)

### 5. **Group Detail Screen**
- **Header:**
  - Group name, avatar, member count
  - Your balance in this group (prominent)
  - "Add Expense" and "Settle Up" buttons
- **Tabs:**
  - **Expenses** - List of all expenses with filters (date, category, person)
  - **Balances** - Who owes who in this group (simplified debts)
  - **Activity Log** - All edits, additions, deletions (immutable history)
  - **Members** - List of group members, add/remove
- **Expense List Item:**
  - Date, description, category icon
  - Amount and currency
  - "Paid by [Name]" → "Split between [Names]"
  - Thumbnail of receipt (if uploaded)

### 6. **Add Expense Screen**
- **Input Fields:**
  - Description (text input, quick suggestions)
  - Amount (numeric keyboard, currency symbol)
  - Category (dropdown/modal: Food, Transport, Shopping, etc.)
  - Date (defaults to today, calendar picker)
  - Paid by (dropdown of group members)
  - Split method (Equal, Unequal, Percentage, Itemized)
  - Split between (multi-select members, checkboxes)
- **Actions:**
  - Camera icon → Capture receipt photo
  - Gallery icon → Upload from gallery
  - OCR button (Premium) → Scan receipt and auto-fill
  - Save button

### 7. **Receipt Capture/Upload Screen**
- **Camera View** - Live camera feed with capture button
- **Preview** - Show captured image, retake/confirm
- **OCR Processing (Premium):**
  - Loading spinner "Scanning receipt..."
  - Auto-fill amount and description
  - User confirms or edits extracted data
- **Manual Upload** - Gallery picker for existing photos

### 8. **Settle Up Screen**
- **Simplified Debts:**
  - "Alice pays Bob $50" (optimized transactions)
  - "Charlie pays Alice $30"
- **For Each Settlement:**
  - Amount and currency
  - From → To with avatars
  - "Mark as Paid" button
  - "Send Payment Reminder" button
  - Payment deep links (Venmo, Zelle, PayPal, Revolut icons)
- **Payment Link Modal:**
  - Choose payment method
  - Deep link with pre-filled amount
  - Copy payment link to clipboard

### 9. **Expense Detail Screen**
- **Full Details:**
  - Description, amount, date, category
  - Paid by [Name] with avatar
  - Split details (who owes how much)
  - Receipt image (full-screen view on tap)
  - Notes/comments section
- **Actions:**
  - Edit expense (pencil icon)
  - Delete expense (trash icon, confirmation dialog)
  - Share expense (export as image/text)

### 10. **Activity Feed Screen**
- **Timeline View:**
  - "Alice added expense 'Dinner' $60"
  - "Bob edited expense 'Taxi'"
  - "Charlie settled up $40 with Alice"
  - Grouped by date (Today, Yesterday, This Week, etc.)
- **Filters:**
  - All activity / Expenses only / Settlements only
  - By group
  - By person

### 11. **Profile/Settings Screen**
- **User Profile:**
  - Avatar, name, email
  - Default currency
  - Edit profile button
- **App Settings:**
  - Notifications (toggle, preferences)
  - Language/locale
  - Theme (light/dark mode)
- **Data Management:**
  - Export data (CSV download)
  - Delete account (with confirmation)
- **Premium:**
  - Upgrade to Premium button (if free user)
  - Manage subscription (if premium user)
- **Support:**
  - Help/FAQ
  - Contact support
  - Privacy policy / Terms of service

### 12. **Charts/Analytics Screen** (Free with Basic, Enhanced for Premium)
- **Summary Stats:**
  - Total expenses this month
  - Average daily spending
  - Most expensive category
- **Visualizations:**
  - Pie chart by category
  - Bar chart by month (Premium: trends over time)
  - Spending heatmap (Premium)
- **Filters:**
  - Date range
  - Group
  - Category

### 13. **Premium Upgrade Screen**
- **Feature Comparison Table:**
  - Free vs. Premium side-by-side
  - Highlight premium benefits (OCR, unlimited receipts, advanced charts)
- **Pricing:**
  - One-time payment option (e.g., $19.99 lifetime)
  - Annual subscription option (e.g., $9.99/year)
  - Monthly option (e.g., $1.99/month)
- **Call to Action:**
  - "Upgrade Now" button
  - Payment integration (Google Play / App Store)

### 14. **Search Screen**
- **Search Bar** - Search all expenses by description, amount, person
- **Filters:**
  - Date range
  - Group
  - Category
  - Person
  - Amount range
- **Results:**
  - List of matching expenses
  - Tap to view expense detail

### 15. **Notifications Screen**
- **Notification List:**
  - "Alice added you to group 'Paris Trip'"
  - "Bob added expense 'Groceries' $45"
  - "Payment reminder: You owe Charlie $30"
- **Actions:**
  - Tap to view related group/expense
  - Mark as read
  - Clear all

---

## Technical Architecture (High-Level)

### Backend (Go + Protocol Buffers + gRPC)

**Why Go + Protobuf:**
- Strong typing matches Flutter's Dart
- High performance, low memory footprint
- gRPC for efficient client-server communication
- Protobuf for type-safe API contracts

**Core Services:**
1. **Auth Service** - User registration, login, JWT tokens, OAuth integration
2. **User Service** - Profile management, settings, preferences
3. **Group Service** - Create/update/delete groups, manage members
4. **Expense Service** - CRUD operations for expenses, search, filtering
5. **Settlement Service** - Calculate simplified debts (debt minimization algorithm)
6. **Notification Service** - Push notifications via FCM (Firebase Cloud Messaging)
7. **Storage Service** - Receipt image upload to S3/GCS
8. **OCR Service** - Receipt scanning using Tesseract/Google Vision API (Premium)
9. **Payment Service** - Generate deep links for Venmo/Zelle/PayPal/Revolut
10. **Analytics Service** - Generate charts, trends, category breakdowns

**Database Schema (PostgreSQL):**
```
users (id, email, password_hash, name, avatar_url, default_currency, created_at)
groups (id, name, avatar_url, created_by, created_at)
group_members (group_id, user_id, joined_at)
expenses (id, group_id, description, amount, currency, category, date, paid_by_user_id, created_at, updated_at)
expense_splits (expense_id, user_id, amount_owed)
settlements (id, group_id, from_user_id, to_user_id, amount, currency, settled_at, payment_method)
receipts (id, expense_id, image_url, ocr_data, uploaded_at)
activity_log (id, group_id, user_id, action_type, entity_type, entity_id, timestamp)
```

**Real-time Sync:**
- WebSocket or gRPC streaming for live updates
- When Alice adds expense, Bob's app receives push instantly
- Optimistic UI updates on client, rollback on conflict

### Frontend (Flutter)

**State Management:**
- **Riverpod** or **Bloc** for predictable state management
- Separate providers/blocs for auth, groups, expenses, settings

**Key Packages:**
- `grpc` - gRPC client for Go backend
- `protobuf` - Generated Dart classes from .proto files
- `image_picker` - Camera/gallery access for receipts
- `fl_chart` - Charts and graphs
- `url_launcher` - Deep links to payment apps
- `firebase_messaging` - Push notifications
- `shared_preferences` - Local settings storage
- `sqflite` - Local SQLite cache for offline support (future)

**Architecture Pattern:**
- **Clean Architecture** - Presentation, Domain, Data layers
- **Repository Pattern** - Abstract data sources (remote API, local cache)

**Navigation:**
- Bottom navigation bar for main sections
- Stack-based navigation within each section
- Modal sheets for quick actions (add expense, settle up)

---

## MVP Development Phases

### Phase 1: Core Foundation (Weeks 1-3)
**Goal:** Basic expense tracking without premium features

**Backend:**
- Set up Go project with gRPC and Protocol Buffers
- PostgreSQL database setup and schema
- Auth service (email/password, JWT tokens)
- User service (profile CRUD)
- Group service (create, list, view, add members)
- Expense service (CRUD, simple split equal only)

**Frontend:**
- Flutter project setup with Riverpod/Bloc
- Authentication flow (login, signup, logout)
- Dashboard screen (basic layout)
- Groups list and group detail screens
- Add expense screen (text only, no receipts, equal split only)
- Basic expense list in group detail

**Deliverable:**
- Users can sign up, create groups, add expenses, see balances

---

### Phase 2: Settlement & Core Features (Weeks 4-5)
**Goal:** Complete the basic expense-splitting workflow

**Backend:**
- Settlement service with debt simplification algorithm
- Activity log service (track all changes)
- Search service for expenses

**Frontend:**
- Balances tab in group detail (who owes who)
- Settle up screen with simplified debts
- Activity feed screen
- Search functionality
- Edit and delete expenses
- Multi-currency support

**Deliverable:**
- Full expense-splitting workflow: add expenses → view balances → settle up

---

### Phase 3: Premium Features - Receipts (Weeks 6-7)
**Goal:** Receipt upload and OCR scanning

**Backend:**
- Storage service (S3/GCS integration)
- OCR service (Tesseract or Google Vision API)
- Receipt endpoints (upload, view, delete)

**Frontend:**
- Camera/gallery picker for receipts
- Receipt preview and upload
- OCR flow (scan → auto-fill → confirm)
- Receipt thumbnails in expense list
- Full-screen receipt view

**Deliverable:**
- Users can attach receipts and use OCR to auto-fill expense details (Premium)

---

### Phase 4: Payment Deep Links & Polish (Weeks 8-9)
**Goal:** Payment integrations and UX refinement

**Backend:**
- Payment service (generate deep links for Venmo, Zelle, PayPal, Revolut)
- Notification service (FCM push notifications)

**Frontend:**
- Payment deep link modal in settle up screen
- Push notifications setup
- Charts/analytics screen (basic pie charts)
- Profile and settings screens
- Premium upgrade screen
- Onboarding flow

**Deliverable:**
- Complete MVP with all core features + premium features ready for beta testing

---

### Phase 5: Testing & Launch Prep (Weeks 10-11)
**Goal:** Bug fixes, testing, app store preparation

**Tasks:**
- End-to-end testing (manual + automated)
- Performance optimization (reduce API calls, optimize images)
- Security audit (auth flows, data validation)
- App store assets (screenshots, descriptions, keywords)
- Privacy policy and terms of service
- Beta testing with 20-50 users
- Bug fixes based on feedback

**Deliverable:**
- Production-ready app for App Store and Google Play submission

---

### Phase 6: Post-Launch Iteration (Weeks 12+)
**Goal:** User feedback incorporation and feature expansion

**Potential Features:**
- Offline mode with sync
- Recurring expenses (rent, subscriptions)
- Expense templates
- Advanced split methods (percentage, itemized)
- Group statistics and insights
- Social features (invite friends, share groups)
- Integration with banking apps (Plaid)

---

## Open Questions & Decisions

### 1. Database Choice
- **PostgreSQL** (recommended) - Strong typing, relational model, excellent for financial data
- **Alternative:** MongoDB if document-based flexibility is preferred

### 2. Hosting & Infrastructure
- **Options:**
  - **Google Cloud Platform** - Kubernetes Engine, Cloud SQL, Cloud Storage
  - **AWS** - ECS/EKS, RDS, S3
  - **DigitalOcean** - Cheaper for MVP, App Platform + Managed PostgreSQL
- **Recommendation:** Start with DigitalOcean for cost efficiency, migrate to GCP/AWS if needed

### 3. OCR Provider
- **Tesseract** (free, open-source, self-hosted)
- **Google Cloud Vision API** (accurate, pay-per-use, ~$1.50/1000 images)
- **AWS Textract** (good for structured receipts)
- **Recommendation:** Google Vision API for MVP (best accuracy-to-cost ratio)

### 4. Payment Processing
- We're NOT processing payments (no Stripe/PayPal integration for money movement)
- Only deep links to existing payment apps
- This avoids regulatory compliance (PCI-DSS, money transmitter licenses)

### 5. Exchange Rates
- **Free API:** exchangerate-api.com (1500 requests/month free)
- **Paid API:** Open Exchange Rates, Fixer.io
- Cache rates daily to minimize API calls

### 6. Freemium Pricing
- **One-time:** $19.99 lifetime premium
- **Annual:** $9.99/year
- **Monthly:** $1.99/month
- Need to decide which to emphasize based on user research preference for one-time payments

### 7. App Name & Branding
- Avoid "Splitwise" trademark
- Suggestions: SplitEasy, FairShare, DivvyUp, SquareUp (check trademark availability)

---

## Success Metrics (Post-Launch)

### User Acquisition
- 10,000 downloads in first 3 months
- 20% conversion from download to active user (2,000 active users)

### Engagement
- Average 5+ expenses per user per month
- 60% monthly active user retention

### Monetization
- 5% conversion to premium (100 paying users from 2,000 active)
- Target: $500-1000 MRR in first 6 months

### Performance
- App load time < 2 seconds
- Expense add time < 3 seconds (tap to save)
- API response time < 200ms (p95)

---

## Next Steps

1. **Set up project structure:**
   - Backend Go project with gRPC scaffolding
   - Flutter app with Riverpod and folder structure
   - Define .proto files for all services

2. **Database setup:**
   - PostgreSQL schema creation
   - Migration scripts
   - Seed data for development

3. **Define API contracts:**
   - Complete .proto definitions for all services
   - Generate Go and Dart code

4. **Design system:**
   - Color palette, typography, component library
   - Match Flutter Material Design patterns
   - Create reusable widgets (buttons, cards, input fields)

5. **Development environment:**
   - Docker Compose for local development
   - CI/CD pipeline (GitHub Actions)
   - Testing frameworks setup

---

## Timeline Summary

| Phase | Duration | Milestone |
|-------|----------|-----------|
| Phase 1: Core Foundation | 3 weeks | Basic expense tracking |
| Phase 2: Settlement & Core | 2 weeks | Full workflow |
| Phase 3: Receipts & OCR | 2 weeks | Premium features |
| Phase 4: Payments & Polish | 2 weeks | MVP complete |
| Phase 5: Testing & Launch | 2 weeks | App store ready |
| **Total MVP:** | **11 weeks** | **Beta launch** |

**Target Launch:** ~3 months from project start

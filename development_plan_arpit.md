# Splitwise Clone - Development Plan (Updated Vision)

## Executive Summary

Building a **frictionless bill-splitting app** targeting high-CPM markets (US/UK/CA) with a **Flutter mobile app** (iOS + Android) and **Go backend with Protocol Buffers**. The app addresses Splitwise's critical failures with a revolutionary approach: **no signup required, natural language splitting, and viral URL sharing**.

**Core Innovation:**
- **Zero friction entry** - No accounts, no logins, instant use
- **Natural language splitting** - "split this in 4 equally" or "exclude Alice from alcohol"
- **Shareable URLs** - Each bill/outing gets a unique link (like Google Docs)
- **Bot integration** - @splitter bot for WhatsApp/Telegram updates
- **OCR/AI scanning** - Upload receipt photo, AI extracts items (Premium)

**Tech Stack:**
- **Frontend:** Flutter (iOS + Android)
- **Backend:** Go with gRPC/Protocol Buffers
- **Database:** PostgreSQL (strong typing, relational data model)
- **NLP:** OpenAI/Claude API or local LLM for parsing split commands
- **OCR:** Google Vision API or Tesseract for receipt scanning
- **Storage:** S3/GCS for receipt images
- **Bot:** Telegram/WhatsApp bot API integration
- **Monetization:** Freemium (free = 30-day storage, premium = permanent + OCR)

---

## Core Features

### Free Tier (Zero Friction)
1. **No Signup Required** - Open app → create bill → share URL (like Pastebin)
2. **Unlimited Bills** - No daily limits, address Splitwise's #1 complaint
3. **Natural Language Splitting** - Type or say "split this in 4" or "exclude Bob from drinks"
4. **Shareable URLs** - Each bill/outing gets a unique link (e.g., splitter.app/b/abc123)
5. **30-Day Storage** - Bills auto-delete after 30 days (reduce costs)
6. **Manual Entry** - Type total amount and items by hand
7. **Payment Deep Links** - Direct links to Venmo/Zelle/PayPal/UPI
8. **Mark as Paid** - Anyone can mark their share as paid
9. **Comments/Disputes** - Add notes or dispute splits in real-time

### Premium Tier Features ($9.99/year or $1.99/month)
1. **Receipt OCR/AI Scanning** - Upload photo → AI extracts items and amounts
2. **Permanent Storage** - Bills never expire, keep forever
3. **Advanced NLP** - Complex queries like "split alcohol items equally, rest by weight"
4. **Priority Support** - Email/chat support
5. **Export to Excel** - Download all bills as CSV/Excel
6. **Custom Branding** - Remove "Powered by Splitter" from shared URLs
7. **Analytics Dashboard** - Spending insights, trends, category breakdowns

### Two Usage Modes

#### 1. Adhoc Bill (One-time)
- User opens app → "New Bill"
- Upload receipt photo OR enter amount manually
- Use natural language to split: "split between me, Alice, Bob"
- Share URL via WhatsApp/Telegram
- Recipients view, mark paid, or dispute

#### 2. Outing/Trip (Multiple Bills)
- User creates "Outing" (e.g., "Vegas Trip")
- Add participant names in natural text: "Alice, Bob, Charlie, Me"
- Home screen shows list of outings
- Inside outing: add multiple bills over time
- Each bill follows same NL splitting flow
- Share outing URL for all bills
- See running totals and settlements

### Bot Integration (@splitter)
- WhatsApp/Telegram bot for updates
- Users can mention @splitter in group chats
- Commands:
  - "@splitter split $120 between Alice Bob Charlie"
  - "@splitter mark paid for bill abc123"
  - "@splitter show me my balance in Vegas Trip"
- Bot generates shareable URLs automatically

---

## Screen Breakdown (Flutter App)

### 1. **Splash/Home Screen** (NO LOGIN)
- **Hero Section:**
  - App logo and tagline: "Split bills in seconds"
  - Big "Split a Bill" button
  - "Create Outing" button
- **Recent Outings** (stored in device):
  - List of outings created from this device
  - Tap to open outing detail
  - Swipe to delete
- **Recent Bills** (stored in device):
  - Last 10 bills split from this device
  - Quick access to shared URLs
- **Bottom Bar:**
  - "Split Bill" (primary action)
  - "My Outings" (local list)
  - "Settings" (app preferences only)

### 2. **Create Bill Screen** (Core Flow)

**Step 1: Input Method**
- Two big buttons:
  - 📷 **"Scan Receipt"** (Premium) → Camera/gallery
  - ✍️ **"Enter Manually"** → Manual input form

**Step 2A: Manual Entry**
- **Total Amount** - Large numeric input with currency selector
- **Bill Description** - Optional (e.g., "Dinner at Joe's")
- **Items** (optional) - Add line items:
  - Item name + amount
  - "Add Item" button to create multiple
- **Continue** button → Go to Step 3

**Step 2B: Receipt Scan (Premium)**
- **Camera View** - Capture receipt photo
- **Processing** - "Scanning receipt..." with spinner
- **AI Extraction Result:**
  - Extracted items in list (name, price)
  - Total amount at bottom
  - Edit buttons for corrections
- **Continue** button → Go to Step 3

**Step 3: Split with Natural Language**
- **Top Section:**
  - Show total amount and bill description
  - Receipt thumbnail (if scanned)
- **Natural Language Input Box:**
  - Large text field: "How should we split this?"
  - Placeholder: "Try: Split this in 4 equally"
  - Microphone icon for voice input
- **Quick Templates (Tabs/Chips):**
  - "Split equally"
  - "Custom amounts"
  - "Exclude someone"
  - "By item"
- **Template Examples:**
  - "Split this between Alice, Bob, Charlie, and me"
  - "Split equally among 4 people"
  - "Don't include Bob in alcohol items"
  - "Alice pays for food, Bob pays for drinks"
- **Processing:** AI parses query and shows preview
- **Preview Split:**
  - Show who owes what
  - Edit button to adjust
- **Create & Share** button

### 3. **Split Preview Screen**
- **Header:**
  - Bill total and description
  - Receipt thumbnail (if available)
- **Split Breakdown:**
  - List of people with amounts:
    - "Alice: $25.50" (with avatar/initials)
    - "Bob: $30.00"
    - "You: $25.50"
  - Visual progress bars for each share
- **Item-Level Details** (if applicable):
  - Expandable sections showing which items each person is paying for
- **Actions:**
  - ✏️ **Edit Split** - Modify amounts or people
  - 🔗 **Share URL** - Generate and copy link
  - 💾 **Save to Outing** - Add to existing outing

### 4. **Share Bill Screen**
- **Generated URL:**
  - Large display: `splitter.app/b/abc123`
  - Copy button
  - QR code for easy sharing
- **Share Options:**
  - WhatsApp button (direct share)
  - Telegram button
  - SMS
  - Email
  - Generic "Share" (uses OS share sheet)
- **Pro Tip:**
  - "Recipients don't need the app to view!"

### 5. **Bill Detail Screen** (Shared URL View)
- **Header:**
  - Bill description and total
  - "Created by [Name/Anonymous]"
  - Receipt image (full-width, tappable for zoom)
- **Your Share** (highlighted):
  - "You owe: $25.50"
  - To whom (if specified)
  - Items you're paying for
- **Everyone's Shares:**
  - List of all participants
  - Amounts and items
  - ✅ "Paid" badges for settled shares
- **Actions:**
  - 💳 **Pay Now** - Payment deep links (Venmo/Zelle/PayPal/UPI)
  - ✅ **Mark as Paid** - Toggle paid status
  - 💬 **Add Comment** - Discuss or dispute
  - 📤 **Share Again** - Re-share URL
- **Comments Section:**
  - Real-time comments from all participants
  - "@splitter update my share to $30" - Bot commands

### 6. **Create Outing Screen**
- **Outing Name:**
  - Text input: "Vegas Trip", "Hawaii 2025"
- **Participants:**
  - Large text area: "Enter names (comma separated)"
  - Placeholder: "Alice, Bob, Charlie, Me"
  - OR: Import from contacts
- **Currency** (optional):
  - Dropdown: USD, EUR, GBP, etc.
- **Create** button → Shows outing detail screen

### 7. **Outing Detail Screen**
- **Header:**
  - Outing name with edit icon
  - Participant count and names
  - Share outing URL button
- **Tabs:**
  - **Bills** - List of all bills in this outing
  - **Balances** - Who owes who overall
  - **Summary** - Total spent, per person breakdown
- **Bills List:**
  - Each bill shows:
    - Description, date, total amount
    - Who paid
    - Thumbnail if receipt exists
  - Tap to view bill detail
- **Add Bill** FAB (Floating Action Button)
  - Opens Create Bill flow but pre-fills participants

### 8. **Outing Balances Screen**
- **Simplified Debts:**
  - "Alice owes Bob $50"
  - "You owe Charlie $30"
  - Net balances calculated across all bills
- **Settlement Actions:**
  - Mark as settled
  - Payment deep links
  - Send reminder

### 9. **Settings Screen** (No Account)
- **App Preferences:**
  - Default currency
  - Notification preferences (if enabled)
  - Theme (light/dark)
- **Data:**
  - Clear all local data (outings/bills stored on device)
- **Premium:**
  - Upgrade to Premium button
  - Restore purchases
- **Support:**
  - Help/FAQ
  - Contact support
  - Privacy policy / Terms

### 10. **Premium Upgrade Screen**
- **Hero Section:**
  - "Unlock Premium Features"
  - Key benefits: OCR scanning, permanent storage, advanced NLP
- **Feature Comparison:**
  - Free vs. Premium side-by-side table
- **Pricing:**
  - Annual: $9.99/year (best value)
  - Monthly: $1.99/month
- **Call to Action:**
  - "Start 7-Day Free Trial" button
  - Payment via Google Play / App Store

### Screen Count Summary
- **Total: 10 screens** (vs. 15 in original plan)
- Much simpler due to no authentication/signup
- Focus on core splitting flow and sharing

---

## Technical Architecture (High-Level)

### Backend (Go + Protocol Buffers + gRPC)

**Why Go + Protobuf:**
- Strong typing matches Flutter's Dart
- High performance, low memory footprint
- gRPC for efficient client-server communication
- Protobuf for type-safe API contracts
- Perfect for URL-based stateless operations

**Core Services:**

1. **Bill Service** - Create, read, update bills with unique URLs
   - Generate short URLs (e.g., splitter.app/b/abc123)
   - Store bill data (amount, description, items, participants, splits)
   - No authentication required

2. **Outing Service** - Create and manage outings (trips)
   - Generate outing URLs (e.g., splitter.app/o/xyz789)
   - Store participant names (no user accounts)
   - Associate multiple bills with one outing

3. **NLP Service** - Parse natural language split commands
   - Accept text: "split this in 4 equally"
   - Extract intent: split_type=equal, participant_count=4
   - Return structured split data
   - Hybrid approach: templates + OpenAI/Claude API for complex queries

4. **OCR Service** - Receipt scanning (Premium only)
   - Accept receipt image upload
   - Extract line items using Google Vision API
   - Return structured data: items[], amounts[], total
   - Verify premium status via in-app purchase receipt

5. **Storage Service** - Receipt image storage
   - Upload to S3/GCS with expiry (30 days free, permanent premium)
   - Generate temporary signed URLs for viewing
   - Auto-delete expired images (cost optimization)

6. **Payment Service** - Generate payment deep links
   - Create Venmo/Zelle/PayPal/UPI links with pre-filled amounts
   - No actual payment processing (regulatory compliance avoidance)

7. **Bot Service** - WhatsApp/Telegram bot integration
   - Handle bot commands: "@splitter split $120 between Alice Bob"
   - Create bills via bot interface
   - Send notifications when bills are created/updated

8. **Cleanup Service** - Background job for data expiry
   - Delete bills older than 30 days (free tier)
   - Delete orphaned images
   - Run daily cron job

**Database Schema (PostgreSQL):**
```sql
-- No users table! No authentication!

bills (
  id UUID PRIMARY KEY,
  short_code VARCHAR(8) UNIQUE, -- for URLs: splitter.app/b/abc123
  description TEXT,
  total_amount DECIMAL(10,2),
  currency VARCHAR(3),
  receipt_image_url TEXT,
  ocr_data JSONB, -- extracted items from OCR
  created_at TIMESTAMP,
  expires_at TIMESTAMP, -- 30 days for free, NULL for premium
  is_premium BOOLEAN DEFAULT false
)

bill_items (
  id UUID PRIMARY KEY,
  bill_id UUID REFERENCES bills(id),
  item_name TEXT,
  amount DECIMAL(10,2)
)

bill_participants (
  id UUID PRIMARY KEY,
  bill_id UUID REFERENCES bills(id),
  name TEXT, -- just a text name, no user ID!
  amount_owed DECIMAL(10,2),
  is_paid BOOLEAN DEFAULT false,
  items JSONB -- which items this person is paying for
)

outings (
  id UUID PRIMARY KEY,
  short_code VARCHAR(8) UNIQUE, -- splitter.app/o/xyz789
  name TEXT,
  participant_names TEXT[], -- array of names as strings
  currency VARCHAR(3),
  created_at TIMESTAMP,
  device_id TEXT -- to identify creator device for local storage
)

outing_bills (
  outing_id UUID REFERENCES outings(id),
  bill_id UUID REFERENCES bills(id),
  PRIMARY KEY (outing_id, bill_id)
)

comments (
  id UUID PRIMARY KEY,
  bill_id UUID REFERENCES bills(id),
  commenter_name TEXT, -- no user account, just name
  comment TEXT,
  created_at TIMESTAMP
)

premium_receipts (
  id UUID PRIMARY KEY,
  receipt_token VARCHAR(64), -- iOS/Android purchase receipt
  expires_at TIMESTAMP,
  created_at TIMESTAMP
)
```

**Key Architectural Decisions:**

1. **No User Accounts:**
   - Bills identified by UUID + short code
   - Anyone with URL can view/edit (like Google Docs with link sharing)
   - Device-local storage tracks "my outings" and "my bills"

2. **URL-Based Sharing:**
   - Short codes generated using base62 encoding (e.g., abc123)
   - URLs never expire for premium, 30 days for free
   - No authentication barrier for viewing bills

3. **Real-time Updates:**
   - WebSocket connection when viewing bill
   - Multiple people can view/comment simultaneously
   - Optimistic UI updates on client

4. **Device Identification:**
   - Use device_id (generated on first launch) to track "my outings"
   - Stored locally on device, sent with API calls
   - No server-side user sessions

### Frontend (Flutter)

**State Management:**
- **Riverpod** - Lightweight, works well without authentication
- Providers for bills, outings, NLP parsing, settings
- Local device storage for "my outings" and "my bills"

**Key Packages:**
- `grpc` - gRPC client for Go backend
- `protobuf` - Generated Dart classes from .proto files
- `image_picker` - Camera/gallery access for receipts
- `url_launcher` - Deep links to payment apps and sharing
- `qr_flutter` - Generate QR codes for bill URLs
- `share_plus` - Native share sheet integration
- `shared_preferences` - Store device_id and local data
- `hive` or `sqflite` - Local storage for outings/bills created on device
- `speech_to_text` - Voice input for natural language commands
- `web_socket_channel` - Real-time updates for bill viewing

**Architecture Pattern:**
- **Simplified MVC** - No complex clean architecture needed
- Screens directly consume providers
- Repository pattern for API calls and local storage

**Local Storage Strategy:**
- Device generates UUID on first launch → device_id
- Store array of "my outings" (short codes + metadata)
- Store array of "my bills" for quick access
- No sync to server (outings are server-side, device just tracks references)

**Navigation:**
- Simple stack-based navigation
- Modal sheets for bill creation flow
- Deep linking support for shared URLs (open app when bill URL clicked)

---

## MVP Development Phases (Revised)

### Phase 1: Core Bill Splitting (Weeks 1-2)
**Goal:** Basic bill splitting with manual entry and URL sharing

**Backend:**
- Set up Go project with gRPC and Protocol Buffers
- PostgreSQL database setup (bills, bill_items, bill_participants tables)
- Bill Service: Create bill, generate short code, store splits
- Simple NLP: Template-based splitting only ("split in X equally")
- API: CreateBill, GetBill (by short code)

**Frontend:**
- Flutter project setup with Riverpod
- Home screen with "Split a Bill" button
- Manual entry screen (amount, description, items)
- Simple split input: "How many people?" → Equal split
- Generate and display shareable URL
- Share screen with QR code + share buttons
- Bill detail view (from URL)

**Deliverable:**
- User can create bill → split equally → share URL → recipients view split

---

### Phase 2: Natural Language & Outings (Weeks 3-4)
**Goal:** Add NLP for flexible splitting and outing support

**Backend:**
- NLP Service: Integrate OpenAI/Claude API for parsing
  - "split this between Alice, Bob, Charlie"
  - "exclude Alice from alcohol"
  - Parse and return structured split data
- Outing Service: Create outing, add bills to outing
- API: CreateOuting, AddBillToOuting, GetOuting

**Frontend:**
- Natural language input box with templates/chips
- Voice input button (speech-to-text)
- Split preview screen showing parsed results
- Create outing screen (name + participants)
- Outing detail screen (list of bills, balances)
- Home screen shows "My Outings" list (local storage)

**Deliverable:**
- Full NL splitting: "split between me, Alice, Bob" works
- Outings created and bills added to them

---

### Phase 3: Premium Features - OCR (Weeks 5-6)
**Goal:** Receipt scanning and OCR extraction

**Backend:**
- Storage Service: S3/GCS integration for receipt images
- OCR Service: Google Vision API integration
  - Upload receipt → extract items and amounts
  - Return structured data for review
- Premium verification via in-app purchase receipt
- Expiry logic (30 days free, permanent premium)

**Frontend:**
- Camera/gallery picker
- OCR processing screen with loading
- Extracted items review/edit screen
- Premium paywall UI
- In-app purchase integration (Flutter in_app_purchase package)
- Premium upgrade screen

**Deliverable:**
- Premium users can scan receipts and auto-extract items

---

### Phase 4: Real-time & Payments (Weeks 7-8)
**Goal:** Real-time updates, comments, and payment links

**Backend:**
- WebSocket support for real-time bill updates
- Comments API (add/view comments on bills)
- Payment Service: Generate deep links
  - Venmo: venmo://paycharge?txn=pay&recipients=username&amount=X
  - Zelle/PayPal/UPI similar formats
- Mark as paid functionality

**Frontend:**
- WebSocket connection when viewing bill
- Real-time updates when someone marks paid or comments
- Comments section in bill detail
- Payment deep link buttons
- "Mark as Paid" toggle for participants

**Deliverable:**
- Real-time collaboration on bills
- Payment deep links functional

---

### Phase 5: Bot Integration (Weeks 9-10)
**Goal:** WhatsApp/Telegram bot for cross-platform access

**Backend:**
- Bot Service: Telegram Bot API integration
- Handle commands:
  - "/split $120 between Alice Bob Charlie"
  - "/bill abc123" → Show bill details
  - "/mark_paid abc123" → Mark as paid
- Create bills via bot and return shareable URLs

**Frontend:**
- No frontend changes needed (bot is backend-only)
- Documentation on how to use @splitter bot

**Deliverable:**
- Bot works in Telegram/WhatsApp
- Users can split bills without opening app

---

### Phase 6: Polish & Launch (Weeks 11-12)
**Goal:** Bug fixes, testing, app store preparation

**Tasks:**
- Cleanup service: Delete expired bills (cron job)
- End-to-end testing (manual + automated)
- Performance optimization
- App store assets (screenshots, descriptions)
- Privacy policy and terms of service
- Beta testing with 20-50 users
- Bug fixes based on feedback
- Analytics integration (PostHog/Mixpanel)

**Deliverable:**
- Production-ready app for App Store and Google Play

---

### Phase 7: Post-Launch Iteration (Weeks 13+)
**Goal:** User feedback and feature expansion

**Potential Features:**
- Advanced NLP: "split alcohol by weight, rest equally"
- Recurring outings (monthly roommate bills)
- Export to Excel/CSV
- Analytics dashboard for premium users
- WhatsApp bot (currently Telegram only)
- Custom branding for premium
- Offline mode (create bills without internet)

---

## Open Questions & Decisions

### 1. NLP Provider
- **Option A: OpenAI GPT-3.5/4** - Best accuracy, ~$0.002/request, requires API key management
- **Option B: Claude API** - Similar pricing, good at parsing instructions
- **Option C: Local/Open-source LLM** - Free but lower accuracy (Llama 2, Mistral)
- **Hybrid Approach (Recommended):** Templates for 80% of cases (free), fallback to API for complex queries
- **Cost Estimate:** If 20% of splits use AI at $0.002/req, 10K bills/month = $40/month

### 2. OCR Provider
- **Google Cloud Vision API** (recommended) - $1.50/1000 images, best accuracy
- **AWS Textract** - Similar pricing, good for receipts
- **Tesseract** (free, open-source) - Lower accuracy but no cost
- **Decision:** Start with Vision API, premium users only (cost passed to users)

### 3. Bot Platform Priority
- **Telegram** (easier) - Simple Bot API, no business verification needed
- **WhatsApp Business API** (harder) - Requires Facebook Business verification, more complex setup
- **Recommendation:** Launch Telegram bot first (Phase 5), WhatsApp post-launch

### 4. Hosting & Infrastructure
- **DigitalOcean** (recommended) - $12-24/month for MVP (App Platform + Managed PostgreSQL + Spaces)
- **Railway/Render** - Similar pricing, easier deployment
- **AWS/GCP** - Overkill for MVP, migrate later if needed
- **Decision:** DigitalOcean for MVP, scale to AWS if >100K users

### 5. URL Shortening
- **Base62 encoding** of UUID (recommended) - abc123 format, 8 characters
- **Hashids library** - Deterministic, reversible, short codes
- **External service (bit.ly)** - Adds dependency, not recommended
- **Decision:** Base62 encoding, self-hosted

### 6. Bill Expiry Policy
- **Free: 30 days** - Reduce storage costs
- **Premium: Permanent** - Never expire
- **Soft delete:** Mark as expired, hard delete after 60 days (grace period)
- **Cost impact:** 10K free bills/month = ~60 GB storage = ~$1.50/month

### 7. Data Privacy & Moderation
- **No user accounts = No GDPR user data**
- Bills are public via URL (anyone with link can view)
- Add "Report Abuse" button for inappropriate content
- Manual moderation initially, automated later

### 8. App Name & Branding
- Avoid "Splitwise" trademark
- Candidates: **Splitter**, **SplitIt**, **FairSplit**, **DivvyUp**
- Check domain availability (.app, .io)
- **Recommendation:** Test with focus group before finalizing

---

## Success Metrics (Post-Launch)

### Viral Growth (Key Metric)
- **Bills Created:** 1,000 bills/week in Month 1 → 10,000/week in Month 3
- **Unique Viewers:** Track how many people VIEW bills vs. CREATE (expect 5:1 ratio)
- **Viral Coefficient:** Average bills shared to 3-4 people → potential 3-4x viral growth
- **URL Clicks:** Track QR code scans + WhatsApp/Telegram link clicks

### User Acquisition (No-signup means different tracking)
- **App Downloads:** 10,000 in first 3 months (organic + word-of-mouth)
- **Bill Creators:** 2,000 users who create at least 1 bill (20% of downloads)
- **Outing Creators:** 500 users who create outings (5% of downloads)
- **Retention:** 30-day retention of bill creators (target: 40%)

### Engagement
- **Bills per Creator:** Average 3-5 bills/month
- **Outing Activity:** Users with outings create 2x more bills
- **Sharing Rate:** 80%+ of bills get shared (via URL or QR code)
- **Comments/Interaction:** 20% of bills have at least 1 comment

### Monetization
- **Premium Conversion:** 3-5% of active creators upgrade (60-100 premium users)
- **OCR Usage:** Track how many premium users actually use OCR (target: 60%)
- **Target Revenue:** $500-800 MRR in first 6 months
- **LTV:** $15-20 (annual subscription) vs. $2 CAC (organic growth)

### Performance
- **Bill Creation:** < 5 seconds from open app to shareable URL
- **NLP Processing:** < 2 seconds to parse and display split
- **OCR Processing:** < 5 seconds to extract items from receipt
- **Page Load:** Bill detail view loads in < 1 second (even from URL)

---

## Next Steps (Immediate Actions)

### Week 1: Foundation Setup

1. **Project Structure:**
   - Create Go backend repo with gRPC scaffolding
   - Create Flutter app repo with Riverpod
   - Set up monorepo or separate repos (decision needed)

2. **Database Schema:**
   - Create PostgreSQL schema (bills, bill_items, bill_participants, outings)
   - Write migration scripts (golang-migrate or similar)
   - Set up local Docker Compose for dev environment

3. **Define .proto Files:**
   - BillService: CreateBill, GetBill, UpdateBill
   - OutingService: CreateOuting, GetOuting, AddBillToOuting
   - Generate Go and Dart code from .proto files

4. **Design System:**
   - Choose color palette (modern, friendly, not Splitwise green)
   - Typography: Use Flutter default (Roboto/SF Pro)
   - Create reusable widgets: Button, Card, TextInput, Avatar
   - Design bill detail screen mockup (Figma/hand-drawn)

5. **Development Environment:**
   - Docker Compose: PostgreSQL + Go backend + hot reload
   - Flutter setup: Android Studio + iOS Simulator
   - CI/CD: GitHub Actions for linting and tests (later)

### Week 2-3: Build Phase 1 MVP

6. **Backend:**
   - Implement CreateBill API (accept amount, description, items, participants)
   - Generate short codes (base62 encoding)
   - Implement GetBill API (by short code)
   - Simple equal split logic (no NLP yet)

7. **Frontend:**
   - Home screen with "Split a Bill" button
   - Manual entry form (amount, description, items)
   - "How many people?" → Generate equal split
   - Display shareable URL + QR code
   - Bill detail view (when someone opens URL)

8. **Testing:**
   - Manual E2E test: Create bill → Share URL → Open on another device
   - Verify data persistence in PostgreSQL

---

## Timeline Summary (Revised)

| Phase | Duration | Milestone |
|-------|----------|-----------|
| **Phase 1:** Core Bill Splitting | 2 weeks | URL sharing works |
| **Phase 2:** NLP & Outings | 2 weeks | Natural language splits |
| **Phase 3:** OCR Premium | 2 weeks | Receipt scanning |
| **Phase 4:** Real-time & Payments | 2 weeks | Live updates + deep links |
| **Phase 5:** Bot Integration | 2 weeks | Telegram bot functional |
| **Phase 6:** Polish & Launch | 2 weeks | App store ready |
| **Total MVP:** | **12 weeks** | **Public launch** |

**Target Launch:** ~3 months from project start

### Key Milestones
- **End of Month 1:** Phase 1-2 complete, basic app works
- **End of Month 2:** Phase 3-4 complete, premium features live
- **End of Month 3:** Phase 5-6 complete, public launch on app stores

### Post-Launch Focus
- **Month 4:** Bot improvements, user feedback iteration
- **Month 5:** Analytics dashboard, advanced NLP
- **Month 6:** Growth hacking, influencer partnerships, ads (if needed)

---

## Competitive Advantages Summary

vs. **Splitwise:**
- ✅ No signup required (zero friction)
- ✅ Natural language splitting (not just dropdowns)
- ✅ Shareable URLs (no need for recipients to have app/account)
- ✅ Free forever for basic use (30-day storage)
- ✅ Premium is $9.99/year vs. their $36/year

vs. **Settleup/Splid:**
- ✅ Natural language (they use forms)
- ✅ OCR receipt scanning (they don't have it)
- ✅ Bot integration (cross-platform access)

vs. **Venmo/PayPal Groups:**
- ✅ No payment processing (no regulatory burden)
- ✅ Smarter split logic (NLP + item-level splits)
- ✅ Works globally (not just US like Venmo)

**The Big Bet:** Natural language + zero friction = viral growth via URL sharing

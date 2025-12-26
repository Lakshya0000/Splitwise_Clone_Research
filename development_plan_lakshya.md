# Koshbook (Splitter) - Lakshya's Development Plan

**Version:** 1.0  
**Author:** Lakshya Agarwal  
**Last Updated:** December 2025  
**Status:** Architecture & Prototyping Phase

---

## Project Context & Mission

### The Market Problem

The dominant player, **Splitwise**, has degraded its user experience by introducing hostile features to force monetization:

1. **Artificial Limits:** Free users are restricted to **3 expenses per day**, breaking the utility for trips and daily roommates.
2. **Ad Friction:** Users face mandatory **10-second delays** before adding expenses.
3. **Forced Accounts:** New users cannot participate without creating an account immediately.
4. **Expensive Subscription:** ₹2,900/year ($36/year) for basic functionality that was previously free.

### The "Anti-Splitwise" Mission

Koshbook aims to capture this dissatisfied market by adhering to a strict **"User-First" philosophy:**

- **Zero Barriers:** Installation to First Expense in **< 5 seconds**. No Login required initially.
- **Respectful Design:** No ads that block functionality. No artificial limits on data entry.
- **Speed:** Offline-first architecture ensures instant interactions, independent of network status.
- **Fair Pricing:** Premium at ₹799/year (~$10/year) for AI features, not basic functionality.

### Target Market

1. **Primary:** Frustrated Splitwise users actively seeking alternatives (evidenced by 16,000+ negative reviews)
2. **Secondary:** New expense-splitting users in India (UPI integration advantage)
3. **Tertiary:** International travelers who need quick, no-signup bill splitting

---

## Executive Summary

Building a **smart, user-centric expense splitting app** that addresses Splitwise's critical failures while introducing innovative identity and settlement features. The app offers **flexible identity models**, **intelligent settlement simplification**, and **seamless cross-group debt management**.

**Core Innovation Points:**
- **Dual Identity Model** - Users can operate with unique app-wide IDs OR use simple text names within groups
- **Zero-Friction Entry** - No mandatory signup, instant use with sharable links
- **Smart Settlement** - In-group (A→B→C becomes A→C) and inter-group debt simplification
- **Natural Language Splitting** - "Split dinner in 5, skip Amit from drinks"
- **UPI Deep Integration** - Direct payment links with pre-filled UPI handles
- **Personal Expense Tracking** - Daily expenses like milk, electricity integrated with group splitting
- **Receipt OCR** - AI-powered receipt parsing (Premium)
- **Global Borrow Tracker** - Cross-group debt consolidation for signed-in users

**Tech Stack:**
- **Frontend:** Flutter (iOS + Android + Web)
- **Backend:** Go with gRPC/Protocol Buffers
- **Database:** PostgreSQL (Cloud) + Isar (Local)
- **AI/NLP:** OpenAI/Claude API for natural language parsing
- **OCR:** Google Vision API for receipt scanning
- **Storage:** S3/GCS for receipt images
- **Real-time:** WebSockets for instant sync
- **Payments:** UPI deep links (no payment processing)

**Monetization Strategy:**
- **Free Tier (Guest):** Unlimited bills, manual splitting, 30-day link storage
- **Free Tier (Verified):** Cloud backup, real-time sync, global debt view, CSV export
- **Premium ($9.99/year):** AI splitting, OCR scanning, recurring bills, PDF reports

---

## 1. User Identity Model (The Dual Approach)

### The Core Decision: How Do We Identify Users?

This is a fundamental architectural decision that affects the entire system. We offer **two approaches** that work together:

### Option A: App-Wide Unique User ID (Signed-In Users)

**When to Use:** Users who want persistent identity, cross-group settlements, and data recovery.

**How It Works:**
1. User signs up via Email/Google (no SMS - cost prohibitive)
2. System generates a permanent `User_UUID`
3. User can be added to groups by their registered email/phone
4. Settlements between A and B are tracked **globally** across all groups
5. User can see "Net balance with Rahul" across trips, roommate groups, etc.

**Benefits:**
- ✅ Inter-group settlement simplification
- ✅ Global debt dashboard ("You owe Rahul ₹500 across 3 groups")
- ✅ Data recovery on new device
- ✅ Real-time sync across devices

**Technical Implementation:**
- `users` table with `id`, `email`, `phone_hash`, `display_name`
- `user_balances` table for global debt tracking
- Contact import creates hashed lookups for friend matching

### Option B: In-Group Text Names (Guest/Anonymous Mode)

**When to Use:** Quick trips, one-time splits, users who don't want to signup.

**How It Works:**
1. User opens app → Creates group immediately (no signup)
2. Adds participants as text strings: "Amit", "Priya", "Rahul"
3. These names exist **only within that group**
4. "Amit" in "Goa Trip" is completely separate from "Amit" in "Office Lunch"
5. Settlement A→B→C is simplified to A→C **within the group only**

**Benefits:**
- ✅ Zero friction - works in 5 seconds
- ✅ No signup barriers for group participants
- ✅ Sharable link allows anyone to view/edit
- ✅ Privacy - no need to share real identity

**Technical Implementation:**
- `group_members` table with `name` as text (no foreign key to users)
- Settlement graph computed per-group
- Links expire after 30 days (free) or never (premium)

### The Hybrid Approach: Best of Both Worlds

**The Magic:** A user can start as Guest and upgrade to Verified seamlessly.

**Upgrade Flow:**
1. Guest user creates groups, adds expenses
2. Later, Guest signs up with email
3. System prompts: "We found groups created from this device. Link them to your account?"
4. User confirms → All `device_id` references updated to `user_id`
5. If group has text-name "Rahul" and signed-in user is Rahul, prompt: "Is this you?"
6. User claims identity → Future settlements track globally

**The Contact Import Strategy:**
When adding people to a group, offer:
1. **Type name manually** → Creates text-only group member
2. **Import from contacts** → Creates hashed phone lookup
3. **Search registered users** → Links to actual user account

If contact is imported:
- Generate `SHA256(phone_number)` hash
- Store hash in `potential_users` table
- When that phone number signs up, auto-link their account

---

## 2. Core Features Breakdown

### Feature Comparison Matrix

| Feature | Free: Guest | Free: Verified | Premium |
|:--------|:-----------:|:--------------:|:-------:|
| **Identity & Access** ||||
| No Signup Required | ✅ | ❌ | ❌ |
| Device-Only Storage | ✅ | ❌ | ❌ |
| Cloud Backup | ❌ | ✅ | ✅ |
| Multi-Device Sync | ❌ | ✅ | ✅ |
| Data Recovery | ❌ | ✅ | ✅ |
| **Group Features** ||||
| Create Unlimited Groups | ✅ | ✅ | ✅ |
| Add Text-Name Members | ✅ | ✅ | ✅ |
| Contact Import | ✅ | ✅ | ✅ |
| Link to Registered Users | ❌ | ✅ | ✅ |
| Shareable Group Links | ✅ (30 days) | ✅ (Permanent) | ✅ (Permanent) |
| **Expense Features** ||||
| Unlimited Expenses | ✅ | ✅ | ✅ |
| No Ads/Timers | ✅ | ✅ | ✅ |
| Equal Split | ✅ | ✅ | ✅ |
| Unequal/Percentage Split | ✅ | ✅ | ✅ |
| Category Tagging | ✅ | ✅ | ✅ |
| Receipt Photo Attach | ✅ | ✅ | ✅ |
| Receipt OCR Parsing | ❌ | ❌ | ✅ |
| AI/NLP Splitting | ❌ | ❌ | ✅ |
| Recurring Expenses | ❌ | ❌ | ✅ |
| **Settlement Features** ||||
| In-Group Simplification | ✅ | ✅ | ✅ |
| Mark as Paid (Manual) | ✅ | ✅ | ✅ |
| UPI Deep Links | ✅ | ✅ | ✅ |
| Inter-Group Settlement | ❌ | ✅ | ✅ |
| Global Debt Dashboard | ❌ | ✅ | ✅ |
| **Personal Finance** ||||
| Daily Expense Tracking | ✅ | ✅ | ✅ |
| Category-wise Reports | ❌ | ✅ | ✅ |
| CSV Export | ❌ | ✅ | ✅ |
| PDF Reports | ❌ | ❌ | ✅ |
| **Sync & Storage** ||||
| Offline Creation | ✅ | ✅ | ✅ |
| Real-Time Sync | ❌ | ✅ | ✅ |
| Link Expiry | 30 days | Never | Never |
| Receipt Image Storage | 30 days | 90 days | Forever |

---

### 2.1 Group Management Features

#### Creating a Group
- **Name:** Required text field (e.g., "Goa Trip 2025")
- **Type:** Optional category chips (Trip, Home, Couple, Event, Other)
- **Cover:** Emoji or gradient color picker
- **Currency:** Auto-detected based on locale, changeable

#### Adding Members (The Flexible Approach)

**Method 1: Text Names (Guest-Friendly)**
```
Flow: Type "Amit" → Press Enter → Member added as text
Result: Creates group_member with name="Amit", user_id=NULL
```

**Method 2: Contact Import**
```
Flow: Tap "Add from Contacts" → Select contacts → Import
Result: Creates group_member with name from contact, phone_hash stored
Backend: When phone owner signs up, auto-link is offered
```

**Method 3: User Search (Verified Users Only)**
```
Flow: Type email/phone → Search registered users → Select
Result: Creates group_member linked to actual user_id
Benefit: Their expenses sync to their account, global debt tracked
```

#### Group Sharing
- **Generate Link:** `koshbook.app/g/{short_code}`
- **QR Code:** Scannable for in-person sharing
- **WhatsApp/Telegram:** One-tap share buttons
- **Access Control:**
  - Anyone with link can view
  - Anyone can add expenses (edit permission)
  - Only creator can delete group

---

### 2.2 Expense Management Features

#### The "Add Expense" Loop (Critical Path)

**Input Flow:**
1. **Amount** - Large calculator-style input (₹ 1500)
2. **Description** - Text with auto-suggest ("Dinner" → 🍽️ icon)
3. **Category** - Auto-detected from description, manual override available
4. **Paid By** - Defaults to "You", tap to change
5. **Split Method** - Equal (default), Unequal, Percentage, Shares, AI

**Split Methods Available:**

| Method | Free | Premium | Description |
|:-------|:----:|:-------:|:------------|
| Equal | ✅ | ✅ | Divide equally among selected members |
| Unequal | ✅ | ✅ | Enter specific amount for each person |
| Percentage | ✅ | ✅ | Assign percentage to each person |
| Shares | ✅ | ✅ | Assign share units (e.g., 2:1:1) |
| Exclude | ✅ | ✅ | Equal split but exclude specific people |
| Multi-Payer | ✅ | ✅ | Multiple people paid different amounts |
| Adjustment | ✅ | ✅ | Equal split with custom adjustments |
| AI/NLP | ❌ | ✅ | Natural language ("Split in 5, skip Amit") |

#### Multi-Payer Support

**Scenario:** A bill where multiple people paid portions (e.g., splitting the cash payment).

**Example:**
- Total Bill: ₹1000
- "Amit paid ₹400, Priya paid ₹600"
- Split equally among 4 people

**Validation Rules:**
- System prevents saving unless `Sum(Paid) == Total`
- Each participant's share is calculated after combining payer contributions

**UI Flow:**
1. Enter total amount: ₹1000
2. Tap "Paid By" → Select "Multiple People"
3. Enter: Amit: ₹400, Priya: ₹600
4. System validates sum = total
5. Select split method (Equal/Unequal)
6. Save expense

#### AI/NLP Splitting (Premium)

**Input Examples:**
- "Split this equally in 5"
- "Amit and Priya split 60-40"
- "Everyone except Rahul"
- "Split dinner equal, drinks only Amit and me"
- "Amit's share is 1000, rest equal"

**Processing Flow:**
1. User types/speaks natural language command
2. Send to NLP Service (OpenAI/Claude)
3. Parse intent and extract:
   - `split_type`: equal/unequal/percentage
   - `participants`: list of names
   - `exclusions`: who to skip
   - `custom_amounts`: specific amounts if any
4. Return structured split preview
5. User confirms or edits
6. Save expense

**Template Shortcuts** (Free users can use these):
- "Split equally" → All members, equal
- "Only me" → 100% to creator
- "50-50" → Two people, equal

---

### 2.3 Daily Expense Tracking (Personal Finance)

**Concept:** Beyond group splitting, users can track personal daily expenses.

**Use Cases:**
- Monthly milk bills
- Electricity/water bills
- Personal subscriptions
- Cash expenses

**Implementation:**
- Create a "Personal" pseudo-group (only you as member)
- Add expenses like any group expense
- Category tagging for reports
- Monthly summary: "You spent ₹5000 on Food this month"

**Integration with Groups:**
- Personal expense can be "promoted" to a group
- Example: "Add electricity bill to Flat 304 group"
- Splits the personal expense among roommates

---

### 2.4 Settlement Features

#### In-Group Settlement Simplification

**The Problem:**
- A owes B ₹500
- B owes C ₹300
- Naive: 2 transactions needed

**The Solution (Debt Simplification Algorithm):**
- Calculate net balance for each person
- Minimize number of transactions
- Result: A pays C ₹300, A pays B ₹200 (or simpler if possible)

**User Control:**
- B can choose to "Adjust Settlement"
- B says: "I'll handle A's payment to C"
- System records adjustment, updates ledger

#### Inter-Group Settlement (Verified Users)

**The Problem:**
- User A owes User B ₹500 in "Goa Trip"
- User B owes User A ₹200 in "Office Lunch"
- Naive: 2 transactions

**The Solution:**
- Global debt graph across all groups
- Net calculation: A owes B ₹300 overall
- Single "Settle All" transaction

**How It Works:**
1. Both A and B must be verified (signed-in) users
2. System aggregates all edges A↔B across groups
3. Dashboard shows: "Net: You owe Rahul ₹300"
4. User pays ₹300 → System auto-adjusts all group ledgers
5. Each affected group shows "Adjustment" entry

#### In-App Borrow Storage

**Concept:** Track informal borrows separate from group expenses.

**Example:**
- "Lent Amit ₹1000 for emergency"
- Not part of any group
- Tracked in personal ledger

**Implementation:**
- Separate `borrows` table
- Fields: `lender_id`, `borrower_id`, `amount`, `note`, `is_settled`
- Shows in Friends screen under person's name
- Can be marked as settled anytime

---

### 2.5 UPI Integration

**The Goal:** One-tap payment initiation.

**Setup:**
- Users can save their UPI ID in profile
- Group members can view each other's UPI IDs
- When settling, app generates UPI deep link

**UPI Deep Link Format:**
```
upi://pay?pa={upi_id}&pn={name}&am={amount}&cu=INR&tn={note}
```

**Payment Flow:**
1. User sees: "Pay ₹500 to Rahul"
2. Taps "Pay via UPI"
3. App shows grid: GPay, PhonePe, Paytm, etc.
4. User selects app
5. UPI app opens with pre-filled details
6. User completes payment
7. Returns to Koshbook
8. Prompt: "Did payment succeed?" → Yes/No
9. If Yes → Settlement recorded

**iOS Limitation Handling:**
- If deep link fails (app not installed)
- Show bottom sheet with UPI ID + Copy button
- User can manually paste in any UPI app

### 2.6 Payment Verification & Proof

**Scenario:** For Cash, Bank Transfer, or Non-UPI payments where automatic confirmation isn't possible.

**Payment Methods Supported:**
| Method | Verification | Auto-Confirm |
|:-------|:-------------|:-------------|
| UPI (GPay, PhonePe) | Prompt-based | User confirms |
| Cash | Proof upload | Payee confirms |
| Bank Transfer | Proof upload | Payee confirms |
| Other | Manual entry | Payee confirms |

**Manual Payment Verification Flow:**

1. **Payer Action:**
   - Records payment in app
   - Uploads Screenshot/Photo as proof
   - Adds optional note: "Paid via NEFT on Dec 25"

2. **State Change:**
   - Debt marked as **"Pending Verification"**
   - Payee receives push notification

3. **Payee Action:**
   - Reviews proof (image preview)
   - Taps **"Confirm Payment"** or **"Reject"**

4. **Final State:**
   - If confirmed → Debt is **settled**
   - If rejected → Debt remains, payer notified

**Implementation Details:**
- Proof images stored in S3 (Premium: forever, Free: 30 days)
- Settlement record links to proof URL
- Activity log shows: "Amit paid you ₹500 (Awaiting Confirmation)"

---

## 3. Detailed Screen Breakdown (Flutter App)

### 3.1 Splash & Onboarding

**Splash Screen:**
- App logo (Koshbook) centered
- Tagline: "Split bills. Track expenses. Stay fair."
- Loading spinner (checking local data)
- Duration: 1-2 seconds max

**First Launch Onboarding (3 screens):**
1. **Screen 1:** "No Signup Needed" - Illustration of instant use
2. **Screen 2:** "Smart Splitting" - NLP and equal split demo
3. **Screen 3:** "Settle with UPI" - Payment integration highlight
- Skip button on all screens
- Progress dots at bottom

### 3.2 Home Screen (Dashboard)

**Layout Structure:**

```
┌─────────────────────────────────────┐
│  [Menu ☰]   KOSHBOOK    [Profile 👤]│
├─────────────────────────────────────┤
│  ┌─────────────────────────────────┐│
│  │   NET BALANCE CARD              ││
│  │   ───────────────────           ││
│  │   You are owed ₹2,500          ││
│  │   (Green card if positive)      ││
│  │   or                            ││
│  │   You owe ₹1,200               ││
│  │   (Red card if negative)        ││
│  └─────────────────────────────────┘│
├─────────────────────────────────────┤
│  QUICK ACTIONS                      │
│  [+ Split Bill]  [+ New Group]     │
├─────────────────────────────────────┤
│  YOUR GROUPS                        │
│  ┌───────────────────────────────┐  │
│  │ 🏖️ Goa Trip 2025              │  │
│  │    You are owed ₹1,500    ☁️  │  │
│  ├───────────────────────────────┤  │
│  │ 🏠 Flat 304                   │  │
│  │    You owe ₹800           ☁️  │  │
│  ├───────────────────────────────┤  │
│  │ 💼 Office Lunch               │  │
│  │    Settled up             📴  │  │
│  └───────────────────────────────┘  │
├─────────────────────────────────────┤
│ [Groups] [Friends] [Activity] [You] │
└─────────────────────────────────────┘
```

**Elements:**
- **Header:** App name, hamburger menu (left), profile icon (right)
- **Net Balance Card:**
  - Large text: "You are owed ₹2,500" (green) or "You owe ₹1,200" (red)
  - Tap to see breakdown by person
  - Only shows for verified users
  - Guests see: "Sign up to track global balance"
- **Quick Actions:**
  - "+ Split Bill" - Opens quick expense entry
  - "+ New Group" - Create new group
- **Groups List:**
  - Group emoji/icon + Name
  - Individual balance in that group
  - Sync status icon: ☁️ (synced), 📴 (local only), 🔄 (syncing)
  - Tap to open Group Detail
  - Long press for quick actions (Share, Settings)
- **Bottom Navigation:**
  - Groups (current), Friends, Activity, You (Profile)

### 3.3 Create Group Screen

**Layout:**
```
┌─────────────────────────────────────┐
│  [← Back]    New Group    [Create] │
├─────────────────────────────────────┤
│  COVER                              │
│  [🏖️] [🏠] [💼] [🎉] [❤️] [✈️] [🎸] │
│  (Horizontal scroll of emojis)      │
├─────────────────────────────────────┤
│  GROUP NAME                         │
│  ┌─────────────────────────────────┐│
│  │ Goa Trip 2025                  ││
│  └─────────────────────────────────┘│
├─────────────────────────────────────┤
│  TYPE                               │
│  [Trip] [Home] [Couple] [Event]    │
│  (Chip selector)                    │
├─────────────────────────────────────┤
│  MEMBERS                            │
│  ┌─────────────────────────────────┐│
│  │ + Add member name or number    ││
│  └─────────────────────────────────┘│
│                                     │
│  [📱 Import from Contacts]         │
│                                     │
│  Added Members:                     │
│  [You] [Amit ✕] [Priya ✕] [Rahul ✕]│
├─────────────────────────────────────┤
│  CURRENCY                           │
│  [🇮🇳 INR ▼] (Auto-detected)       │
└─────────────────────────────────────┘
```

**Elements:**
- **Back Button:** Returns without saving
- **Create Button:** Enabled when name is entered, creates group
- **Cover Picker:** Horizontal scroll of emoji options + gradient colors
- **Group Name:** Large text input, auto-focus on screen load
- **Type Chips:** Trip, Home, Couple, Event, Other (optional)
- **Member Input:**
  - Text field for typing names
  - Press Enter to add as text member
  - Phone number triggers contact lookup
  - Email triggers user search (verified users)
- **Import Contacts:** Opens contact picker (requires permission)
- **Added Members:** Pill tags with X to remove
- **Currency Dropdown:** Auto-detected, changeable

### 3.4 Group Detail Screen

**Layout:**
```
┌─────────────────────────────────────┐
│  [← Back]  🏖️ Goa Trip   [⋮ Menu] │
├─────────────────────────────────────┤
│  ┌─────────────────────────────────┐│
│  │ TOTAL EXPENSES: ₹15,000        ││
│  │ Your Balance: +₹1,500          ││
│  │ [Share 🔗] [Settle Up 💰]      ││
│  └─────────────────────────────────┘│
├─────────────────────────────────────┤
│  [Expenses] [Balances] [Totals]    │
├─────────────────────────────────────┤
│  EXPENSES TAB:                      │
│  ┌───────────────────────────────┐  │
│  │ Dec 25 • Dinner at Beach Shack│  │
│  │ Rahul paid ₹2,500             │  │
│  │ You owe ₹625                  │  │
│  ├───────────────────────────────┤  │
│  │ Dec 25 • Uber to Hotel        │  │
│  │ You paid ₹400                 │  │
│  │ You are owed ₹300             │  │
│  ├───────────────────────────────┤  │
│  │ Dec 24 • Grocery Run          │  │
│  │ Amit paid ₹1,200              │  │
│  │ You owe ₹400                  │  │
│  └───────────────────────────────┘  │
├─────────────────────────────────────┤
│              [+ Add Expense]        │
└─────────────────────────────────────┘
```

**Tabs:**

**Expenses Tab:**
- List of all expenses, newest first
- Each row shows: Date, Description, Payer, Amount
- Your share highlighted (owe vs owed)
- Receipt thumbnail if attached
- Tap to view/edit expense detail

**Balances Tab:**
- Simplified debt list after settlement algorithm
- "Amit → Rahul: ₹500"
- "You → Priya: ₹300"
- Pay button next to amounts you owe
- Remind button next to amounts owed to you

**Totals Tab:**
- Pie chart: Spending by category
- Bar chart: Spending by person
- Total group spend
- Your total contribution

**Menu Options (⋮):**
- Edit Group Name/Cover
- Manage Members
- Group Settings
- Leave Group
- Delete Group (creator only)

### 3.5 Add Expense Screen

**Layout:**
```
┌─────────────────────────────────────┐
│  [✕ Cancel]  Add Expense    [✓ Save]│
├─────────────────────────────────────┤
│                                     │
│         ₹ 0                         │
│    (Large amount display)           │
│    [🇮🇳 INR ▼]                      │
│                                     │
├─────────────────────────────────────┤
│  DESCRIPTION                        │
│  ┌─────────────────────────────────┐│
│  │ 🍽️ Dinner at...                ││
│  └─────────────────────────────────┘│
│  Suggestions: [Food] [Taxi] [Hotel] │
├─────────────────────────────────────┤
│  PAID BY                            │
│  ┌─────────────────────────────────┐│
│  │ 👤 You                     [▼] ││
│  └─────────────────────────────────┘│
├─────────────────────────────────────┤
│  SPLIT                              │
│  ┌─────────────────────────────────┐│
│  │ Equally among all          [▼] ││
│  └─────────────────────────────────┘│
│  Split preview:                     │
│  You: ₹500 | Amit: ₹500 | Priya: ₹500│
├─────────────────────────────────────┤
│  [📷 Add Receipt]  [📅 Dec 25]     │
├─────────────────────────────────────┤
│  ┌─────────────────────────────────┐│
│  │  7  │  8  │  9  │      │       ││
│  │  4  │  5  │  6  │  +   │       ││
│  │  1  │  2  │  3  │  -   │       ││
│  │  .  │  0  │  ⌫  │  =   │       ││
│  └─────────────────────────────────┘│
└─────────────────────────────────────┘
```

**Elements:**
- **Amount Display:** Large, tappable, calculator-style input
- **Currency Selector:** Dropdown, defaults to group currency
- **Description:** Text input with category icon auto-detect
- **Suggestions:** Quick-tap chips based on common categories
- **Paid By:** Dropdown of group members, defaults to "You"
- **Split Selector:** Opens Split Modal (see 3.6)
- **Split Preview:** Shows each person's share inline
- **Receipt Button:** Camera/gallery picker
- **Date Picker:** Defaults to today, changeable
- **Calculator Keypad:** Custom numeric keyboard at bottom

### 3.6 Split Modal (Bottom Sheet)

**Layout:**
```
┌─────────────────────────────────────┐
│  SPLIT OPTIONS              [Done] │
├─────────────────────────────────────┤
│  [Equally] [Unequally] [%] [Shares]│
├─────────────────────────────────────┤
│  SPLIT WITH:                        │
│  ☑️ You          ₹500              │
│  ☑️ Amit         ₹500              │
│  ☑️ Priya        ₹500              │
│  ☐ Rahul        (excluded)         │
├─────────────────────────────────────┤
│  ✨ AI SPLIT (Premium)             │
│  ┌─────────────────────────────────┐│
│  │ "Split food equal, drinks..."  ││
│  │                           [🎤] ││
│  └─────────────────────────────────┘│
└─────────────────────────────────────┘
```

**Split Methods:**
- **Equally:** Checkbox for each member, divide by count
- **Unequally:** Enter specific amount for each person
- **Percentage:** Enter % for each, must total 100%
- **Shares:** Enter share units (2:1:1 ratio)

**AI Split (Premium):**
- Text input for natural language
- Microphone button for voice
- Examples shown as placeholder
- Parses and shows preview before confirming

### 3.7 Friends Screen

**Layout:**
```
┌─────────────────────────────────────┐
│  [← Back]      Friends      [+ Add]│
├─────────────────────────────────────┤
│  [All] [Owes You] [You Owe]        │
├─────────────────────────────────────┤
│  FRIENDS LIST:                      │
│  ┌───────────────────────────────┐  │
│  │ 👤 Amit                       │  │
│  │    Owes you ₹1,200       [▶]│  │
│  ├───────────────────────────────┤  │
│  │ 👤 Priya                      │  │
│  │    You owe ₹500          [▶]│  │
│  ├───────────────────────────────┤  │
│  │ 👤 Rahul                      │  │
│  │    Settled up            [▶]│  │
│  └───────────────────────────────┘  │
├─────────────────────────────────────┤
│  NOT ON KOSHBOOK:                   │
│  ┌───────────────────────────────┐  │
│  │ 👤 Sneha (from contacts)      │  │
│  │    [Invite to Koshbook]       │  │
│  └───────────────────────────────┘  │
└─────────────────────────────────────┘
```

**Elements:**
- **Filter Tabs:** All, Owes You, You Owe
- **Friend Cards:**
  - Avatar (photo or initials)
  - Name
  - Net balance across all groups
  - Arrow to view detail
- **Non-User Contacts:**
  - People added to groups but not signed up
  - Invite button sends app link
- **Tap on Friend:** Opens Friend Detail screen

### 3.8 Friend Detail Screen

**Layout:**
```
┌─────────────────────────────────────┐
│  [← Back]      Amit         [⋮]   │
├─────────────────────────────────────┤
│  ┌─────────────────────────────────┐│
│  │      👤 (Large Avatar)         ││
│  │      Amit Sharma               ││
│  │      amit@email.com            ││
│  │                                ││
│  │   NET BALANCE: +₹1,200         ││
│  │   (Amit owes you)              ││
│  │                                ││
│  │   [Remind]    [Settle Up]      ││
│  └─────────────────────────────────┘│
├─────────────────────────────────────┤
│  COMMON GROUPS:                     │
│  • Goa Trip (+₹500)                │
│  • Office Lunch (+₹400)            │
│  • Birthday Party (+₹300)          │
├─────────────────────────────────────┤
│  PERSONAL BORROWS:                  │
│  • Lent ₹1000 on Dec 20 (Pending)  │
│  [+ Add Personal Borrow]           │
├─────────────────────────────────────┤
│  RECENT ACTIVITY:                   │
│  • Dec 25: Amit added "Dinner"     │
│  • Dec 24: You added "Taxi"        │
│  • Dec 20: Amit paid you ₹200      │
└─────────────────────────────────────┘
```

**Sections:**
- **Profile Card:** Avatar, name, email/phone, net balance
- **Action Buttons:** Remind (send notification), Settle Up
- **Common Groups:** List of shared groups with per-group balance
- **Personal Borrows:** Non-group lending, add/edit/settle
- **Recent Activity:** Expense and payment history

### 3.9 Activity Screen

**Layout:**
```
┌─────────────────────────────────────┐
│  [← Back]      Activity            │
├─────────────────────────────────────┤
│  TODAY                              │
│  ┌───────────────────────────────┐  │
│  │ 🔴 Amit added "Dinner ₹2500"  │  │
│  │    in Goa Trip • 2m ago       │  │
│  ├───────────────────────────────┤  │
│  │ ✅ Priya paid you ₹500        │  │
│  │    in Office Lunch • 1h ago   │  │
│  └───────────────────────────────┘  │
├─────────────────────────────────────┤
│  YESTERDAY                          │
│  ┌───────────────────────────────┐  │
│  │ 👥 You were added to          │  │
│  │    "Birthday Party"           │  │
│  ├───────────────────────────────┤  │
│  │ ✏️ Rahul edited "Hotel ₹5000" │  │
│  │    Changed from ₹4500         │  │
│  └───────────────────────────────┘  │
├─────────────────────────────────────┤
│  EARLIER                            │
│  ┌───────────────────────────────┐  │
│  │ 🔔 Reminder: You owe ₹800     │  │
│  │    to Amit in Goa Trip        │  │
│  └───────────────────────────────┘  │
└─────────────────────────────────────┘
```

**Activity Types:**
- 🔴 **Expense Added:** "Amit added Dinner ₹2500"
- ✏️ **Expense Edited:** "Rahul changed Hotel from ₹4500 to ₹5000"
- ❌ **Expense Deleted:** "Priya deleted Snacks"
- ✅ **Payment Made:** "Priya paid you ₹500"
- 👥 **Group Joined:** "You were added to Birthday Party"
- 🔔 **Reminder:** "Amit sent you a reminder"

**UI Elements:**
- Red dot for unread items
- Grouped by: Today, Yesterday, Earlier
- Tap to navigate to relevant group/expense
- Mark all as read button

### 3.10 Settle Up Dashboard

**Layout:**
```
┌─────────────────────────────────────┐
│  [← Back]    Settle Up             │
├─────────────────────────────────────┤
│  YOU OWE:                           │
│  ┌───────────────────────────────┐  │
│  │ 👤 Amit                       │  │
│  │    ₹800 (across 2 groups)     │  │
│  │    [Pay Now →]                │  │
│  ├───────────────────────────────┤  │
│  │ 👤 Priya                      │  │
│  │    ₹300 (Goa Trip)            │  │
│  │    [Pay Now →]                │  │
│  └───────────────────────────────┘  │
├─────────────────────────────────────┤
│  OWED TO YOU:                       │
│  ┌───────────────────────────────┐  │
│  │ 👤 Rahul                      │  │
│  │    ₹1,500 (across 3 groups)   │  │
│  │    [Remind]  [Mark Paid]      │  │
│  └───────────────────────────────┘  │
├─────────────────────────────────────┤
│  PREMIUM: Multi-Settle             │
│  ┌───────────────────────────────┐  │
│  │ ☐ Select multiple to settle   │  │
│  │ [Settle All Selected]         │  │
│  └───────────────────────────────┘  │
└─────────────────────────────────────┘
```

**Sections:**
- **You Owe:** Red cards, sorted by amount (highest first)
- **Owed to You:** Green cards, sorted by amount
- **Actions:**
  - Pay Now: Opens Payment Screen
  - Remind: Sends push notification
  - Mark Paid: Record offline payment

### 3.11 Payment Screen

**Layout:**
```
┌─────────────────────────────────────┐
│  [← Back]      Pay Amit            │
├─────────────────────────────────────┤
│                                     │
│         👤 → 👤                     │
│        You   Amit                   │
│                                     │
│      ┌─────────────────┐           │
│      │    ₹ 800        │           │
│      └─────────────────┘           │
│      (Editable amount)              │
│                                     │
├─────────────────────────────────────┤
│  PAY VIA:                           │
│  ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐  │
│  │GPay │ │PhonePe│ │Paytm│ │BHIM │  │
│  └─────┘ └─────┘ └─────┘ └─────┘  │
│                                     │
│  [💵 Record Cash Payment]          │
│  [🏦 Record Bank Transfer]         │
├─────────────────────────────────────┤
│  NOTE (optional)                    │
│  ┌─────────────────────────────────┐│
│  │ For Goa Trip expenses          ││
│  └─────────────────────────────────┘│
├─────────────────────────────────────┤
│  Amit's UPI: amit@okaxis           │
│  [Copy UPI ID]                     │
└─────────────────────────────────────┘
```

**Elements:**
- **Avatar Animation:** Your avatar → Their avatar
- **Amount:** Pre-filled with total owed, editable
- **UPI Apps Grid:** Detects installed apps, shows icons
- **Cash/Bank Options:** For offline payments
- **Note Field:** Optional, included in settlement record
- **UPI ID Display:** Fallback for manual payment

### 3.12 Profile & Settings Screen

**Layout:**
```
┌─────────────────────────────────────┐
│  [← Back]      Profile             │
├─────────────────────────────────────┤
│  ┌─────────────────────────────────┐│
│  │     👤 (Large Avatar)          ││
│  │     Lakshya Agarwal            ││
│  │     lakshya@email.com          ││
│  │     ✅ Verified Member          ││
│  │     [Edit Profile]             ││
│  └─────────────────────────────────┘│
│  OR (for guests):                   │
│  ┌─────────────────────────────────┐│
│  │     👤 Guest User              ││
│  │     ⚠️ Sign up to backup data   ││
│  │     [🔐 Create Account]        ││
│  └─────────────────────────────────┘│
├─────────────────────────────────────┤
│  MY PAYMENT DETAILS                 │
│  UPI ID: [lakshya@upi     ] [Save] │
├─────────────────────────────────────┤
│  PREFERENCES                        │
│  Default Currency    [INR ▼]       │
│  Theme              [Dark ▼]       │
│  Notifications      [On ▼]        │
├─────────────────────────────────────┤
│  DATA                               │
│  [☁️ Sync Now]                     │
│  [📊 Export CSV]                   │
│  [📄 Export PDF] (Premium)         │
├─────────────────────────────────────┤
│  PREMIUM                            │
│  ┌─────────────────────────────────┐│
│  │ ✨ Upgrade to Premium           ││
│  │ AI Splitting • OCR • PDF Export ││
│  │ [$9.99/year]                    ││
│  └─────────────────────────────────┘│
├─────────────────────────────────────┤
│  SUPPORT                            │
│  [❓ Help & FAQ]                   │
│  [📧 Contact Support]              │
│  [📜 Privacy Policy]               │
│  [📜 Terms of Service]             │
├─────────────────────────────────────┤
│  [🚪 Log Out]  (or Sign Up if guest)│
└─────────────────────────────────────┘
```

### 3.13 Premium Upgrade Screen

**Layout:**
```
┌─────────────────────────────────────┐
│  [✕ Close]                         │
├─────────────────────────────────────┤
│                                     │
│        ✨ KOSHBOOK PRO ✨          │
│                                     │
│   Unlock the full power of         │
│   expense splitting                 │
│                                     │
├─────────────────────────────────────┤
│  FEATURES:                          │
│                                     │
│  🤖 AI-Powered Splitting           │
│     "Split dinner equal, skip Amit" │
│                                     │
│  📷 Receipt OCR                     │
│     Photo → Automatic item extraction│
│                                     │
│  🔄 Recurring Expenses              │
│     Auto-add rent on the 1st        │
│                                     │
│  📄 PDF Reports                     │
│     Professional expense reports    │
│                                     │
│  ♾️ Permanent Storage               │
│     Links never expire              │
│                                     │
├─────────────────────────────────────┤
│  PRICING:                           │
│  ┌─────────────────────────────────┐│
│  │ ⭐ ANNUAL (Best Value)         ││
│  │    ₹799/year (₹66/month)       ││
│  │    [Subscribe]                  ││
│  ├─────────────────────────────────┤│
│  │ 📅 MONTHLY                     ││
│  │    ₹149/month                   ││
│  │    [Subscribe]                  ││
│  └─────────────────────────────────┘│
├─────────────────────────────────────┤
│  ✓ 7-Day Free Trial                │
│  ✓ Cancel Anytime                  │
│  ✓ Restore Purchases               │
└─────────────────────────────────────┘
```

### 3.14 Receipt Scanner Screen (Premium)

**Layout:**
```
┌─────────────────────────────────────┐
│  [← Back]    Scan Receipt          │
├─────────────────────────────────────┤
│                                     │
│  ┌─────────────────────────────────┐│
│  │                                 ││
│  │                                 ││
│  │      📷 CAMERA VIEW            ││
│  │                                 ││
│  │      [Align receipt in frame]  ││
│  │                                 ││
│  └─────────────────────────────────┘│
│                                     │
│  [📸 Capture]  [📁 Gallery]        │
│                                     │
├─────────────────────────────────────┤
│  After capture:                     │
│  ┌─────────────────────────────────┐│
│  │ 🔄 Processing...               ││
│  │ Extracting items from receipt   ││
│  └─────────────────────────────────┘│
├─────────────────────────────────────┤
│  Extracted Items:                   │
│  ┌───────────────────────────────┐  │
│  │ ☑️ Burger           ₹250     │  │
│  │ ☑️ Pizza            ₹400     │  │
│  │ ☑️ Coke x2          ₹80      │  │
│  │ ☑️ Tax              ₹73      │  │
│  ├───────────────────────────────┤  │
│  │ TOTAL:              ₹803     │  │
│  └───────────────────────────────┘  │
│                                     │
│  [✏️ Edit Items]  [✓ Use These]   │
└─────────────────────────────────────┘
```

### Screen Count Summary

| Screen | Purpose |
|:-------|:--------|
| 1. Splash & Onboarding | First launch experience |
| 2. Home Dashboard | Main navigation hub |
| 3. Create Group | New group setup |
| 4. Group Detail | View group expenses/balances |
| 5. Add Expense | Core expense entry |
| 6. Split Modal | Split method selection |
| 7. Friends List | Global friend view |
| 8. Friend Detail | Individual friend history |
| 9. Activity Feed | Notifications/updates |
| 10. Settle Up Dashboard | Payment overview |
| 11. Payment Screen | UPI/cash payment flow |
| 12. Profile & Settings | User preferences |
| 13. Premium Upgrade | Subscription purchase |
| 14. Receipt Scanner | OCR capture (Premium) |

**Total: 14 Core Screens**

---

## 4. Technical Architecture

### 4.1 System Overview

**Architecture Pattern:** Microservices with Event Sourcing for Offline-First sync.

```
┌──────────────────────────────────────────────────────────────┐
│                      FLUTTER APP                              │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐         │
│  │ Riverpod│  │  Isar   │  │  gRPC   │  │ WorkMgr │         │
│  │ State   │  │ Local DB│  │ Client  │  │ BG Sync │         │
│  └─────────┘  └─────────┘  └─────────┘  └─────────┘         │
└──────────────────────────────────────────────────────────────┘
                              │
                              ▼ HTTPS/gRPC
┌──────────────────────────────────────────────────────────────┐
│                      API GATEWAY                              │
│                 (Kong / Nginx / Envoy)                        │
│              Rate Limiting, Auth, Routing                     │
└──────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        ▼                     ▼                     ▼
┌───────────────┐    ┌───────────────┐    ┌───────────────┐
│  Identity     │    │  Core         │    │  Sync         │
│  Service      │    │  Service      │    │  Service      │
│  (auth-svc)   │    │  (core-svc)   │    │  (sync-svc)   │
└───────────────┘    └───────────────┘    └───────────────┘
        │                     │                     │
        └─────────────────────┼─────────────────────┘
                              ▼
┌──────────────────────────────────────────────────────────────┐
│                     PostgreSQL                                │
│  Users | Groups | Expenses | Settlements | Mutations         │
└──────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        ▼                     ▼                     ▼
┌───────────────┐    ┌───────────────┐    ┌───────────────┐
│  AI Service   │    │  Storage Svc  │    │  Notif Svc    │
│  (NLP + OCR)  │    │  (S3/GCS)     │    │  (FCM/APNs)   │
└───────────────┘    └───────────────┘    └───────────────┘
```

### 4.2 Backend Services (Go Microservices)

#### Service 1: Identity Service (`auth-svc`)

**Purpose:** Manages the Hybrid Identity model (Guest → Verified → Premium).

**Endpoints:**

| Endpoint | Method | Description |
|:---------|:-------|:------------|
| `/identity/guest` | POST | Create guest session with device_id |
| `/identity/signup` | POST | Convert guest to verified (email/Google) |
| `/identity/login` | POST | Authenticate existing user |
| `/identity/merge` | POST | Link guest data to verified account |
| `/identity/profile` | GET/PUT | Get or update user profile |
| `/identity/upi` | PUT | Save UPI ID for payments |

**Key Logic:**

1. **Guest Authentication:**
   - Accept `device_uuid` from client
   - Generate `guest_token` (JWT, 30-day expiry)
   - Store in `users` table with `is_guest = true`

2. **Account Merge Flow:**
   ```
   Input: { device_id, email, auth_token }
   
   1. Verify email (Google OAuth or Magic Link)
   2. Check if email already exists in users
      - If YES: Return error "Account exists"
      - If NO: Continue
   3. Find all records with device_id:
      - Users, Groups, Expenses, Settlements
   4. Create new user with email, is_guest = false
   5. Update all found records: device_id → user_id
   6. Delete guest user record
   7. Issue new auth_token for verified user
   ```

3. **Premium Verification:**
   - Receive App Store/Play Store receipt
   - Validate with Apple/Google servers
   - Update `is_premium = true`, `premium_expires_at`

---

#### Service 2: Core Service (`core-svc`)

**Purpose:** The source of truth for Groups, Expenses, Members, and Balances.

**Endpoints:**

| Endpoint | Method | Description |
|:---------|:-------|:------------|
| `/groups` | POST | Create new group |
| `/groups/{id}` | GET/PUT/DELETE | Manage group |
| `/groups/{id}/members` | GET/POST/DELETE | Manage members |
| `/groups/{id}/expenses` | GET/POST | List/add expenses |
| `/expenses/{id}` | GET/PUT/DELETE | Manage expense |
| `/groups/{id}/balances` | GET | Get simplified balances |
| `/settlements` | POST | Record a settlement |
| `/users/{id}/global-balance` | GET | Cross-group net balance |
| `/borrows` | GET/POST/PUT | Personal borrow tracker |

**Key Logic:**

1. **Expense Creation (with Idempotency):**
   ```
   Input: {
     idempotency_key: "client-uuid-123",
     group_id: "...",
     amount: 1500,
     description: "Dinner",
     payer_id: "...",
     split_map: { "user1": 500, "user2": 500, "user3": 500 },
     category: "food",
     receipt_url: null
   }
   
   1. Check idempotency_key in redis/cache
      - If found: Return existing expense (no duplicate)
   2. Validate group_id exists, payer is member
   3. Validate split_map sums to amount
   4. Insert into expenses table
   5. Update group_members.balance for each participant
   6. Log mutation to mutation_log table
   7. Store idempotency_key with TTL (24h)
   8. Broadcast via WebSocket to group members
   ```

2. **Balance Calculation:**
   ```
   For each member in group:
     paid = SUM(expenses WHERE payer_id = member)
     owes = SUM(split_map[member] for all expenses)
     net_balance = paid - owes
   
   Simplify debts using greedy algorithm:
     creditors = members with positive balance
     debtors = members with negative balance
     
     While debts remain:
       Match highest debtor with highest creditor
       Transfer min(abs(debt), credit)
       Update both balances
   ```

3. **Global Balance (Verified Users):**
   ```
   For verified user A:
     For each other verified user B:
       edges = SELECT SUM(net) FROM all groups WHERE A and B are members
       global_balance[A][B] = SUM(edges)
   ```

---

#### Service 3: Sync Service (`sync-svc`)

**Purpose:** Bi-directional offline sync using Delta Log pattern.

**Endpoints:**

| Endpoint | Method | Description |
|:---------|:-------|:------------|
| `/sync/push` | POST | Push local mutations to server |
| `/sync/pull` | GET | Pull server mutations since last sync |
| `/sync/status` | GET | Check sync health |

**Key Logic:**

1. **Push Flow (Client → Server):**
   ```
   Input: {
     last_ack_id: "mutation-456",
     mutations: [
       { type: "CREATE_EXPENSE", data: {...}, timestamp: "..." },
       { type: "UPDATE_GROUP", data: {...}, timestamp: "..." }
     ]
   }
   
   For each mutation:
     1. Validate mutation (auth, data integrity)
     2. Check for conflicts (LWW by timestamp)
     3. Apply mutation to database
     4. Store in mutation_log with server_timestamp
   
   Return: { ack_id: "mutation-789", conflicts: [...] }
   ```

2. **Pull Flow (Server → Client):**
   ```
   Input: { last_sync_timestamp: "2024-12-25T10:00:00Z" }
   
   1. Query mutation_log WHERE timestamp > last_sync_timestamp
   2. Filter by user's group memberships
   3. Return mutation batch
   
   Output: {
     mutations: [...],
     new_sync_timestamp: "2024-12-26T15:30:00Z"
   }
   ```

3. **Conflict Resolution (Last Write Wins):**
   ```
   If client_timestamp > server_timestamp:
     Accept client version
   Else:
     Reject, return server version as conflict
   
   Client must merge conflict locally
   ```

---

#### Service 4: AI Service (`ai-svc`) [Premium]

**Purpose:** Natural Language Processing for splitting and OCR for receipts.

**Endpoints:**

| Endpoint | Method | Description |
|:---------|:-------|:------------|
| `/ai/parse-split` | POST | Parse NL split command |
| `/ai/ocr` | POST | Extract items from receipt image |

**Key Logic:**

1. **NLP Parsing:**
   ```
   Input: {
     text: "Split dinner equal but Amit pays for drinks",
     group_members: ["You", "Amit", "Priya", "Rahul"],
     total_amount: 2000
   }
   
   1. Send to OpenAI/Claude with structured prompt:
      "Parse this expense split instruction.
       Members: [...]
       Total: ₹2000
       Instruction: ..."
   
   2. Parse AI response into structured format:
      {
        split_type: "mixed",
        items: [
          { name: "dinner", amount: 1500, split: "equal", members: ["all"] },
          { name: "drinks", amount: 500, split: "full", members: ["Amit"] }
        ]
      }
   
   3. Calculate final split_map:
      { "You": 375, "Amit": 875, "Priya": 375, "Rahul": 375 }
   ```

2. **OCR Processing:**
   ```
   Input: { image_url: "s3://bucket/receipt.jpg" }
   
   1. Download image from S3
   2. Send to Google Vision API
   3. Extract text blocks with coordinates
   4. Apply heuristic parser:
      - Find currency symbols (₹, $)
      - Find item-price pairs
      - Find total line
   5. Return structured items:
      {
        items: [
          { name: "Burger", price: 250 },
          { name: "Pizza", price: 400 }
        ],
        total: 650,
        confidence: 0.92
      }
   ```

---

#### Service 5: Storage Service (`storage-svc`)

**Purpose:** Manage receipt image uploads and signed URLs.

**Endpoints:**

| Endpoint | Method | Description |
|:---------|:-------|:------------|
| `/storage/upload-url` | GET | Get pre-signed upload URL |
| `/storage/download-url` | GET | Get pre-signed download URL |

**Key Logic:**
- Generate S3/GCS pre-signed URLs (15-minute expiry for upload)
- Store metadata in database (user_id, file_key, uploaded_at)
- Cleanup job: Delete files older than 30 days (free) or 90 days (verified)

---

#### Service 6: Notification Service (`notif-svc`)

**Purpose:** Push notifications and reminders.

**Endpoints:**

| Endpoint | Method | Description |
|:---------|:-------|:------------|
| `/notify/send` | POST | Send notification to user |
| `/notify/remind` | POST | Send payment reminder |

**Notification Types:**
- `expense_added`: "Amit added Dinner ₹2500 in Goa Trip"
- `expense_edited`: "Rahul updated Hotel to ₹5000"
- `payment_received`: "Priya paid you ₹500"
- `payment_reminder`: "Hey! You owe Amit ₹800"
- `group_invite`: "Priya added you to Birthday Party"

---

### 4.3 Database Schema (PostgreSQL)

```sql
-- =============================================================================
-- TABLE: users (Hybrid Identity)
-- =============================================================================
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- Identity
    email VARCHAR(255) UNIQUE,           -- NULL for guests
    phone_hash VARCHAR(64),              -- SHA256(phone) for matching
    display_name VARCHAR(100) NOT NULL,
    avatar_url TEXT,
    
    -- Device tracking
    device_id VARCHAR(100),              -- Links guests to their data
    fcm_token TEXT,                      -- For push notifications
    
    -- Account status
    is_guest BOOLEAN DEFAULT TRUE,
    is_premium BOOLEAN DEFAULT FALSE,
    premium_expires_at TIMESTAMP,
    
    -- Payment
    upi_id VARCHAR(100),                 -- For UPI deep links
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    last_active_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_users_device ON users(device_id);
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_phone ON users(phone_hash);

-- =============================================================================
-- TABLE: groups
-- =============================================================================
CREATE TABLE groups (
    id UUID PRIMARY KEY,                  -- Client-generated (offline support)
    
    -- Details
    name VARCHAR(100) NOT NULL,
    cover_emoji VARCHAR(10),
    cover_color VARCHAR(7),               -- Hex color #RRGGBB
    group_type VARCHAR(20),               -- trip, home, couple, event, other
    currency VARCHAR(3) DEFAULT 'INR',
    
    -- Ownership
    created_by UUID REFERENCES users(id),
    device_id VARCHAR(100),               -- Fallback for guest creators
    
    -- Sharing
    short_code VARCHAR(8) UNIQUE,         -- For URLs: koshbook.app/g/{code}
    is_public BOOLEAN DEFAULT FALSE,      -- Anyone with link can view
    
    -- Sync status
    sync_state VARCHAR(20) DEFAULT 'local', -- local, syncing, synced
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    expires_at TIMESTAMP                  -- NULL for verified users
);

CREATE INDEX idx_groups_short_code ON groups(short_code);
CREATE INDEX idx_groups_created_by ON groups(created_by);

-- =============================================================================
-- TABLE: group_members (The Link Table)
-- =============================================================================
CREATE TABLE group_members (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    group_id UUID REFERENCES groups(id) ON DELETE CASCADE,
    
    -- Member identity (flexible)
    user_id UUID REFERENCES users(id),    -- NULL for text-only members
    name VARCHAR(100) NOT NULL,           -- Display name in group
    phone_hash VARCHAR(64),               -- For future linking
    
    -- Balance (cached)
    balance DECIMAL(12,2) DEFAULT 0,      -- Positive = owed, Negative = owes
    
    -- Role
    is_admin BOOLEAN DEFAULT FALSE,
    
    -- Timestamps
    joined_at TIMESTAMP DEFAULT NOW(),
    
    UNIQUE(group_id, user_id),
    UNIQUE(group_id, name)                -- No duplicate names in group
);

CREATE INDEX idx_gm_group ON group_members(group_id);
CREATE INDEX idx_gm_user ON group_members(user_id);

-- =============================================================================
-- TABLE: expenses (The Ledger)
-- =============================================================================
CREATE TABLE expenses (
    id UUID PRIMARY KEY,                  -- Client-generated (offline support)
    group_id UUID REFERENCES groups(id) ON DELETE CASCADE,
    
    -- Amount
    amount DECIMAL(12,2) NOT NULL,
    currency VARCHAR(3) DEFAULT 'INR',
    
    -- Details
    description VARCHAR(255) NOT NULL,
    category VARCHAR(50),                 -- food, transport, entertainment, etc.
    
    -- Payer
    payer_id UUID REFERENCES group_members(id),
    
    -- Split
    split_type VARCHAR(20) DEFAULT 'equal', -- equal, unequal, percentage, shares
    split_map JSONB NOT NULL,             -- { "member_id": amount, ... }
    
    -- Receipt
    receipt_url TEXT,
    ocr_data JSONB,                       -- Extracted items if OCR used
    
    -- Recurring
    is_recurring BOOLEAN DEFAULT FALSE,
    recurrence_rule TEXT,                 -- RRULE format for recurring
    parent_expense_id UUID,               -- Link to parent for instances
    
    -- Sync
    idempotency_key VARCHAR(100) UNIQUE,
    sync_state VARCHAR(20) DEFAULT 'local',
    
    -- Timestamps
    expense_date DATE DEFAULT CURRENT_DATE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    deleted_at TIMESTAMP                  -- Soft delete
);

CREATE INDEX idx_expenses_group ON expenses(group_id);
CREATE INDEX idx_expenses_payer ON expenses(payer_id);
CREATE INDEX idx_expenses_date ON expenses(expense_date);
CREATE INDEX idx_expenses_idempotency ON expenses(idempotency_key);

-- =============================================================================
-- TABLE: settlements (Payments)
-- =============================================================================
CREATE TABLE settlements (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- Parties
    payer_id UUID REFERENCES group_members(id),   -- Who paid
    payee_id UUID REFERENCES group_members(id),   -- Who received
    
    -- Linked user IDs (for global tracking)
    payer_user_id UUID REFERENCES users(id),
    payee_user_id UUID REFERENCES users(id),
    
    -- Amount
    amount DECIMAL(12,2) NOT NULL,
    currency VARCHAR(3) DEFAULT 'INR',
    
    -- Context
    group_id UUID REFERENCES groups(id),  -- Optional: NULL for global settlement
    note TEXT,
    
    -- Payment method
    payment_method VARCHAR(20),           -- upi, cash, bank, other
    payment_reference TEXT,               -- UPI transaction ID if available
    
    -- Timestamps
    settled_at TIMESTAMP DEFAULT NOW(),
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_settlements_group ON settlements(group_id);
CREATE INDEX idx_settlements_payer ON settlements(payer_user_id);
CREATE INDEX idx_settlements_payee ON settlements(payee_user_id);

-- =============================================================================
-- TABLE: borrows (Personal Lending)
-- =============================================================================
CREATE TABLE borrows (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- Parties
    lender_id UUID REFERENCES users(id) NOT NULL,
    borrower_id UUID REFERENCES users(id),
    borrower_name VARCHAR(100),           -- If borrower not on platform
    
    -- Amount
    amount DECIMAL(12,2) NOT NULL,
    currency VARCHAR(3) DEFAULT 'INR',
    
    -- Details
    note TEXT,
    is_settled BOOLEAN DEFAULT FALSE,
    
    -- Timestamps
    borrowed_at TIMESTAMP DEFAULT NOW(),
    settled_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_borrows_lender ON borrows(lender_id);
CREATE INDEX idx_borrows_borrower ON borrows(borrower_id);

-- =============================================================================
-- TABLE: mutation_log (For Sync)
-- =============================================================================
CREATE TABLE mutation_log (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- Target
    entity_type VARCHAR(50) NOT NULL,     -- expense, group, settlement, etc.
    entity_id UUID NOT NULL,
    
    -- Operation
    operation VARCHAR(20) NOT NULL,       -- create, update, delete
    
    -- Data
    mutation_data JSONB NOT NULL,
    
    -- Context
    user_id UUID REFERENCES users(id),
    device_id VARCHAR(100),
    client_timestamp TIMESTAMP NOT NULL,
    server_timestamp TIMESTAMP DEFAULT NOW(),
    
    -- Sequence
    sequence_id BIGSERIAL
);

CREATE INDEX idx_mutations_entity ON mutation_log(entity_type, entity_id);
CREATE INDEX idx_mutations_timestamp ON mutation_log(server_timestamp);
CREATE INDEX idx_mutations_sequence ON mutation_log(sequence_id);

-- =============================================================================
-- TABLE: activity_log (For Notifications)
-- =============================================================================
CREATE TABLE activity_log (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- Target user
    user_id UUID REFERENCES users(id) NOT NULL,
    
    -- Activity
    activity_type VARCHAR(50) NOT NULL,   -- expense_added, payment_received, etc.
    title VARCHAR(255) NOT NULL,
    body TEXT,
    
    -- Reference
    group_id UUID REFERENCES groups(id),
    expense_id UUID REFERENCES expenses(id),
    settlement_id UUID REFERENCES settlements(id),
    
    -- Status
    is_read BOOLEAN DEFAULT FALSE,
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_activity_user ON activity_log(user_id);
CREATE INDEX idx_activity_created ON activity_log(created_at DESC);
```

---

### 4.4 Frontend Architecture (Flutter)

#### Architecture Pattern: Repository + Riverpod

```
┌─────────────────────────────────────────────────────────────┐
│                   PRESENTATION LAYER                         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐          │
│  │   Screens   │  │   Widgets   │  │  Providers  │          │
│  │  (14 total) │  │ (Reusable)  │  │ (Riverpod)  │          │
│  └─────────────┘  └─────────────┘  └─────────────┘          │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    DOMAIN LAYER                              │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐          │
│  │  Entities   │  │  UseCases   │  │ Exceptions  │          │
│  │  (freezed)  │  │  (Business) │  │  (Errors)   │          │
│  └─────────────┘  └─────────────┘  └─────────────┘          │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                     DATA LAYER                               │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐          │
│  │Repositories │  │    Isar     │  │    gRPC     │          │
│  │ (Interface) │  │ Local Cache │  │Remote Client│          │
│  └─────────────┘  └─────────────┘  └─────────────┘          │
└─────────────────────────────────────────────────────────────┘
```

#### Key Packages

| Package | Version | Purpose |
|:--------|:--------|:--------|
| `flutter_riverpod` | ^2.4.0 | State management |
| `isar` | ^3.1.0 | Local NoSQL database |
| `grpc` | ^3.2.0 | Backend communication |
| `freezed` | ^2.4.0 | Immutable entities |
| `go_router` | ^12.0.0 | Navigation |
| `workmanager` | ^0.5.0 | Background sync |
| `share_plus` | ^7.0.0 | Native sharing |
| `url_launcher` | ^6.2.0 | UPI deep links |
| `image_picker` | ^1.0.0 | Receipt camera |
| `speech_to_text` | ^6.3.0 | Voice input |
| `fl_chart` | ^0.65.0 | Charts/graphs |
| `in_app_purchase` | ^3.1.0 | Premium subscription |

#### Local Database Schema (Isar)

```dart
@collection
class LocalGroup {
  Id id = Isar.autoIncrement;
  
  @Index(unique: true)
  late String uuid;          // Server UUID
  
  late String name;
  String? coverEmoji;
  String? shortCode;
  
  @enumerated
  late SyncStatus syncStatus; // clean, dirty, syncing
  
  DateTime createdAt = DateTime.now();
  DateTime? lastSyncedAt;
  
  final members = IsarLinks<LocalMember>();
  final expenses = IsarLinks<LocalExpense>();
}

@collection
class LocalExpense {
  Id id = Isar.autoIncrement;
  
  @Index(unique: true)
  late String uuid;
  
  late String groupUuid;
  late double amount;
  late String description;
  late String payerMemberUuid;
  
  late String splitMapJson;   // JSON string of split
  
  @enumerated
  late SyncStatus syncStatus;
  
  DateTime expenseDate = DateTime.now();
  DateTime createdAt = DateTime.now();
  
  final group = IsarLink<LocalGroup>();
}

enum SyncStatus { clean, dirty, syncing, conflict }
```

#### Provider Structure

```dart
// Auth Provider
final authProvider = StateNotifierProvider<AuthNotifier, AuthState>((ref) {
  return AuthNotifier(ref.watch(authRepositoryProvider));
});

// Groups Provider
final groupsProvider = FutureProvider<List<Group>>((ref) async {
  final repo = ref.watch(groupRepositoryProvider);
  return repo.getAllGroups();
});

// Single Group Provider
final groupProvider = FutureProvider.family<Group, String>((ref, id) async {
  final repo = ref.watch(groupRepositoryProvider);
  return repo.getGroup(id);
});

// Expenses Provider
final expensesProvider = FutureProvider.family<List<Expense>, String>((ref, groupId) async {
  final repo = ref.watch(expenseRepositoryProvider);
  return repo.getExpenses(groupId);
});

// Global Balance Provider (Verified Users)
final globalBalanceProvider = FutureProvider<Map<String, double>>((ref) async {
  final repo = ref.watch(balanceRepositoryProvider);
  return repo.getGlobalBalance();
});

// Sync Status Provider
final syncStatusProvider = StateProvider<SyncStatus>((ref) {
  return SyncStatus.idle;
});
```

---

### 4.5 Data Flow & Lifecycle

#### Flow 1: Create Expense (Offline-First)

```
┌──────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐
│  User    │     │  Screen  │     │ Provider │     │   Isar   │
│  Action  │     │          │     │          │     │   (DB)   │
└────┬─────┘     └────┬─────┘     └────┬─────┘     └────┬─────┘
     │                │                │                │
     │ Tap "Save"     │                │                │
     │───────────────▶│                │                │
     │                │ addExpense()   │                │
     │                │───────────────▶│                │
     │                │                │ Generate UUID  │
     │                │                │───────────────▶│
     │                │                │                │ Save with
     │                │                │                │ syncStatus=dirty
     │                │                │◀───────────────│
     │                │◀───────────────│                │
     │                │ UI Updates     │                │
     │◀───────────────│ Instantly      │                │
     │                │                │                │
     │                │                │    ┌──────────┐│
     │                │                │    │WorkManager││
     │                │                │    └────┬─────┘│
     │                │                │         │       │
     │                │                │ Background Sync │
     │                │                │◀────────┼───────│
     │                │                │         │       │
     │                │                │    ┌────▼─────┐ │
     │                │                │    │  gRPC    │ │
     │                │                │    │  Server  │ │
     │                │                │    └────┬─────┘ │
     │                │                │         │       │
     │                │                │◀────────┘       │
     │                │                │ syncStatus=clean│
     │                │                │─────────────────▶
```

**Steps:**
1. User taps Save
2. Generate client-side UUID
3. Save to Isar with `syncStatus = dirty`
4. UI updates immediately (optimistic)
5. WorkManager picks up dirty records
6. Push to server via gRPC
7. On success, update `syncStatus = clean`

#### Flow 2: Sync Pull (Server → Client)

```
┌──────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐
│WorkManager│     │ SyncRepo │     │   gRPC   │     │  Server  │
│          │     │          │     │  Client  │     │          │
└────┬─────┘     └────┬─────┘     └────┬─────┘     └────┬─────┘
     │                │                │                │
     │ Trigger        │                │                │
     │───────────────▶│                │                │
     │                │ pullMutations()│                │
     │                │───────────────▶│                │
     │                │                │ GET /sync/pull │
     │                │                │───────────────▶│
     │                │                │                │
     │                │                │   Mutations[]  │
     │                │                │◀───────────────│
     │                │◀───────────────│                │
     │                │                │                │
     │                │ For each mutation:              │
     │                │ ─────────────────               │
     │                │ 1. Check local version          │
     │                │ 2. If server newer, apply       │
     │                │ 3. Update last_sync_timestamp   │
     │                │                │                │
     │◀───────────────│                │                │
     │                │                │                │
```

#### Flow 3: UPI Payment

```
┌──────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐
│  User    │     │ Payment  │     │ UPI App  │     │   Ours   │
│          │     │  Screen  │     │ (GPay)   │     │  Server  │
└────┬─────┘     └────┬─────┘     └────┬─────┘     └────┬─────┘
     │                │                │                │
     │ Tap "Pay ₹800" │                │                │
     │───────────────▶│                │                │
     │                │ Build UPI URL  │                │
     │                │ upi://pay?...  │                │
     │                │───────────────▶│                │
     │                │                │ Opens GPay     │
     │                │                │ Pre-filled     │
     │                │                │                │
     │                │◀───────────────│ User returns   │
     │                │                │                │
     │ "Did it work?" │                │                │
     │◀───────────────│                │                │
     │                │                │                │
     │ Tap "Yes"      │                │                │
     │───────────────▶│                │                │
     │                │ recordSettlement()             │
     │                │─────────────────────────────────▶│
     │                │                │                │ Update balances
     │                │◀────────────────────────────────│
     │ "Settlement    │                │                │
     │  recorded!"    │                │                │
     │◀───────────────│                │                │
```

---

## 5. Algorithms & Logic

### 5.1 Debt Simplification Algorithm

**Problem:** Minimize number of transactions to settle all debts in a group.

**Input:**
```
balances = {
  "Amit": +1000,   # Owed to Amit
  "Priya": -600,   # Priya owes
  "Rahul": -400,   # Rahul owes
  "You": 0         # Settled
}
```

**Algorithm (Greedy):**
```python
def simplify_debts(balances):
    creditors = [(name, bal) for name, bal in balances.items() if bal > 0]
    debtors = [(name, -bal) for name, bal in balances.items() if bal < 0]
    
    # Sort by amount descending
    creditors.sort(key=lambda x: -x[1])
    debtors.sort(key=lambda x: -x[1])
    
    transactions = []
    
    i, j = 0, 0
    while i < len(creditors) and j < len(debtors):
        creditor, credit = creditors[i]
        debtor, debt = debtors[j]
        
        amount = min(credit, debt)
        transactions.append({
            "from": debtor,
            "to": creditor,
            "amount": amount
        })
        
        credit -= amount
        debt -= amount
        
        if credit == 0:
            i += 1
        else:
            creditors[i] = (creditor, credit)
            
        if debt == 0:
            j += 1
        else:
            debtors[j] = (debtor, debt)
    
    return transactions
```

**Output:**
```
[
  { "from": "Priya", "to": "Amit", "amount": 600 },
  { "from": "Rahul", "to": "Amit", "amount": 400 }
]
```

### 5.2 Global Debt Aggregation

**Problem:** Calculate net balance between two users across all groups.

**Algorithm:**
```sql
-- For users A and B
WITH group_balances AS (
  SELECT 
    g.id as group_id,
    g.name as group_name,
    COALESCE(
      (SELECT balance FROM group_members WHERE group_id = g.id AND user_id = A),
      0
    ) as a_balance,
    COALESCE(
      (SELECT balance FROM group_members WHERE group_id = g.id AND user_id = B),
      0
    ) as b_balance
  FROM groups g
  WHERE EXISTS (SELECT 1 FROM group_members WHERE group_id = g.id AND user_id = A)
    AND EXISTS (SELECT 1 FROM group_members WHERE group_id = g.id AND user_id = B)
)
SELECT 
  SUM(a_balance - b_balance) as net_balance
FROM group_balances;

-- If positive: B owes A
-- If negative: A owes B
```

### 5.3 Sync Conflict Resolution (LWW)

**Problem:** Two devices edit same expense offline.

**Resolution:**
```python
def resolve_conflict(local_mutation, server_mutation):
    if local_mutation.client_timestamp > server_mutation.server_timestamp:
        # Local wins - push to server
        return "push_local"
    else:
        # Server wins - apply server version
        return "accept_server"
```

**Edge Cases:**
- Exact same timestamp: Server wins (arbitrary but consistent)
- Delete vs Update: Delete wins (tombstone)
- Both delete: No conflict

### 5.4 NLP Split Parser

**Template Matching (Free Tier):**
```python
TEMPLATES = {
    r"split (equally|equal)": "equal",
    r"split in (\d+)": "equal_count",
    r"(\d+)-(\d+)": "ratio",
    r"everyone except (.+)": "exclude",
    r"only (.+)": "include_only"
}

def parse_simple(text, members):
    text = text.lower().strip()
    
    for pattern, split_type in TEMPLATES.items():
        match = re.search(pattern, text)
        if match:
            if split_type == "equal":
                return {"type": "equal", "members": members}
            elif split_type == "equal_count":
                count = int(match.group(1))
                return {"type": "equal", "count": count}
            # ... handle other types
    
    return None  # Needs AI
```

**AI Parsing (Premium):**
```python
SYSTEM_PROMPT = """
You are an expense splitting assistant. Parse the user's instruction and return JSON.

Available members: {members}
Total amount: ₹{amount}

Return format:
{
  "splits": [
    {"member": "name", "amount": 123.45}
  ]
}

Rules:
- Splits must sum to total amount
- Use exact member names
- Handle exclusions and custom amounts
"""

def parse_with_ai(text, members, amount):
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT.format(
                members=members, amount=amount
            )},
            {"role": "user", "content": text}
        ],
        response_format={"type": "json_object"}
    )
    return json.loads(response.choices[0].message.content)
```

---

## 6. MVP Development Phases (14 Weeks)

### Phase 1: Offline Foundation (Weeks 1-3)

**Goal:** A fully functional local-only expense tracker.

**Week 1: Project Setup**
- Flutter project with Riverpod, Isar, go_router
- Go backend with gRPC scaffolding
- PostgreSQL schema migration scripts
- Docker Compose for local dev

**Week 2: Local CRUD**
- Create Group (local storage)
- Add Members (text names)
- Add Expense (equal split only)
- View Group with expense list
- Calculate in-group balances

**Week 3: Polish Local Features**
- Unequal/percentage/shares split
- Category selection
- Expense edit/delete
- Balance simplification algorithm

**Deliverable:** APK that works 100% offline.

---

### Phase 2: Cloud Sync (Weeks 4-6)

**Goal:** Shareable links and cloud backup.

**Week 4: Backend Core**
- Deploy Go services to cloud
- Implement Group and Expense APIs
- Generate short codes for URLs
- Basic authentication (device_id)

**Week 5: Sync Engine**
- Push mutations to server
- Pull mutations from server
- Conflict resolution (LWW)
- Background sync with WorkManager

**Week 6: Sharing**
- Generate shareable links
- Web view for non-app users
- QR code generation
- WhatsApp/Telegram share buttons

**Deliverable:** Groups shareable via URL.

---

### Phase 3: Identity & Payments (Weeks 7-9)

**Goal:** Verified accounts and UPI integration.

**Week 7: Authentication**
- Email/Google sign-in
- Guest to Verified merge flow
- Profile screen
- Contact import with hashing

**Week 8: UPI Integration**
- Save UPI ID in profile
- Generate payment deep links
- Payment confirmation flow
- Settlement recording

**Week 9: Global Debt**
- Cross-group balance calculation
- Friends screen with net balances
- Settle Up dashboard
- Payment reminders

**Deliverable:** Full identity and payment flow.

---

### Phase 4: Premium Features (Weeks 10-12)

**Goal:** Monetization-ready with AI features.

**Week 10: NLP Splitting**
- OpenAI/Claude integration
- Natural language parser
- Voice input with speech_to_text
- Template shortcuts for free tier

**Week 11: OCR & Receipts**
- Google Vision API integration
- Receipt camera flow
- Item extraction and editing
- Receipt storage (S3)

**Week 12: Subscription**
- In-app purchase setup
- Premium feature gating
- Recurring expenses (Premium)
- PDF export (Premium)

**Deliverable:** Premium tier fully functional.

---

### Phase 5: Polish & Launch (Weeks 13-14)

**Goal:** Production-ready application.

**Week 13: Quality**
- End-to-end testing
- Performance optimization
- Error handling & edge cases
- Analytics integration

**Week 14: Launch Prep**
- App Store assets (screenshots, descriptions)
- Privacy policy & terms
- Beta testing (50 users)
- Bug fixes from beta

**Deliverable:** Production release on Play Store & App Store.

---

## 7. Open Questions & Decisions

### 7.1 Authentication Strategy

| Option | Cost | UX | Recommendation |
|:-------|:-----|:---|:---------------|
| SMS OTP | ₹0.20/SMS | Best (India) | ❌ Too expensive |
| Email Magic Link | ₹0.0001/email | Good | ✅ Primary method |
| Google Sign-In | Free | Good | ✅ Secondary option |
| Apple Sign-In | Free | Good (iOS) | ✅ Required for iOS |

**Decision:** Email + Google/Apple. No SMS.

### 7.2 NLP Provider

| Provider | Cost/Request | Quality | Latency |
|:---------|:-------------|:--------|:--------|
| GPT-3.5-turbo | $0.0005 | Good | 500ms |
| GPT-4o-mini | $0.0001 | Better | 300ms |
| Claude Haiku | $0.00025 | Good | 400ms |
| Local (Llama) | Free | Lower | 1000ms |

**Decision:** Start with GPT-4o-mini. Fallback to templates for 80% of cases.

### 7.3 Hosting Infrastructure

| Provider | Monthly Cost | Pros | Cons |
|:---------|:-------------|:-----|:-----|
| DigitalOcean | $24/month | Simple, cheap | Limited scaling |
| Railway | $20/month | Easy deploy | Variable pricing |
| AWS | $50+/month | Scalable | Complex |

**Decision:** DigitalOcean for MVP. Migrate to AWS at 100K users.

### 7.4 Data Expiry Policy

| Tier | Link Expiry | Receipt Storage | Rationale |
|:-----|:------------|:----------------|:----------|
| Guest | 30 days | 30 days | Reduce storage costs |
| Verified | Never | 90 days | Value prop for signup |
| Premium | Never | Forever | Paid benefit |

### 7.5 Privacy Considerations

- **Contact Hashing:** Only store SHA256(phone), never raw numbers
- **No Tracking:** No third-party analytics (self-hosted PostHog)
- **Data Export:** Users can download all their data anytime
- **Account Deletion:** Full data purge within 30 days

---

## 8. Success Metrics

### 8.1 Growth Metrics

| Metric | Month 1 | Month 3 | Month 6 | Target |
|:-------|:--------|:--------|:--------|:-------|
| Downloads | 5,000 | 25,000 | 100,000 | Viral growth |
| DAU | 500 | 3,000 | 15,000 | Engagement |
| Groups Created | 1,000 | 10,000 | 50,000 | Core usage |
| Expenses Added | 10,000 | 100,000 | 500,000 | Stickiness |

### 8.2 Engagement Metrics

| Metric | Target | Measurement |
|:-------|:-------|:------------|
| D7 Retention | 40% | Users returning after 7 days |
| D30 Retention | 25% | Users returning after 30 days |
| Expenses/User/Month | 5+ | Active usage |
| Share Rate | 60%+ | Groups that get shared |

### 8.3 Conversion Metrics

| Metric | Target | Funnel |
|:-------|:-------|:-------|
| Guest → Verified | 20% | Signup conversion |
| Verified → Premium | 5% | Monetization |
| Trial → Paid | 30% | Premium conversion |

### 8.4 Revenue Targets

| Metric | Month 1 | Month 6 | Year 1 |
|:-------|:--------|:--------|:-------|
| Premium Users | 50 | 1,000 | 5,000 |
| MRR | ₹4,000 | ₹80,000 | ₹4,00,000 |
| ARR | ₹48,000 | ₹9,60,000 | ₹48,00,000 |

### 8.5 Technical Metrics

| Metric | Target | Monitoring |
|:-------|:-------|:-----------|
| API Latency (p95) | <200ms | Grafana |
| Sync Success Rate | >99.5% | Error tracking |
| Crash Rate | <0.1% | Firebase Crashlytics |
| App Launch Time | <2s | Performance monitoring |

---

## 9. Roadmap & Next Steps

### Immediate Actions (Week 1)

1. **Repository Setup**
   - Create `koshbook-app` (Flutter) repo
   - Create `koshbook-api` (Go) repo
   - Set up CI/CD with GitHub Actions

2. **Development Environment**
   - Docker Compose: Postgres, Redis
   - Flutter dev setup
   - gRPC tooling

3. **Design System**
   - Color palette (not Splitwise green)
   - Typography (Inter/Roboto)
   - Core components

### Short-term (Month 1-2)

- Complete Phases 1-2
- Basic app with sharing
- Internal dogfooding

### Medium-term (Month 3-4)

- Complete Phases 3-4
- Payment integration
- Premium features
- Private beta (100 users)

### Long-term (Month 5-6)

- Complete Phase 5
- Public launch
- Marketing push
- User feedback iteration

---

## 10. Competitive Advantages Summary

### vs. Splitwise

| Feature | Splitwise | Koshbook |
|:--------|:----------|:---------|
| Daily Limit | 3 expenses | ✅ Unlimited |
| Ads/Timers | 10-sec wait | ✅ None |
| Signup Required | Yes | ✅ No (Guest mode) |
| UPI Integration | Basic | ✅ Deep links |
| Global Debt | Yes | ✅ Yes + Borrows |
| Pricing | ₹2,900/year | ✅ ₹799/year |

### vs. Splid

| Feature | Splid | Koshbook |
|:--------|:------|:---------|
| NLP Splitting | No | ✅ Yes |
| OCR Receipts | No | ✅ Yes |
| Cloud Sync | Basic | ✅ Real-time |
| Personal Expenses | No | ✅ Yes |

### vs. Tricount

| Feature | Tricount | Koshbook |
|:--------|:---------|:---------|
| Offline-First | Partial | ✅ Full |
| Cross-Group Settle | No | ✅ Yes |
| AI Features | No | ✅ Yes |
| Modern UI | Dated | ✅ Premium |

---

## 11. Risk Assessment

### Technical Risks

| Risk | Impact | Mitigation |
|:-----|:-------|:-----------|
| Sync conflicts | High | LWW + conflict UI |
| OCR accuracy | Medium | Manual edit option |
| AI costs spike | Medium | Rate limiting, caching |
| Server downtime | High | Multi-region, offline-first |

### Business Risks

| Risk | Impact | Mitigation |
|:-----|:-------|:-----------|
| Low adoption | High | Focus on viral sharing |
| Low conversion | High | Value-add premium features |
| Competitive response | Medium | Speed to market |
| Regulatory (UPI) | Low | No payment processing |

### Operational Risks

| Risk | Impact | Mitigation |
|:-----|:-------|:-----------|
| Data loss | Critical | Multi-region backups |
| Privacy breach | Critical | Encryption, minimal data |
| Support overload | Medium | In-app FAQ, chatbot |

---

## 12. Explicit Feature List (Inventory)

### A. Onboarding & Home

- [ ] **Splash Screen:** Instant load, checks for `Device_UUID`
- [ ] **Dashboard:**
    - [ ] "Total Net Worth" Card (Green/Red balance)
    - [ ] List of "Recent Groups"
    - [ ] "Add Expense" Floating Action Button (FAB)
- [ ] **Global Search:** Find expenses across all groups by description/amount
- [ ] **Onboarding Carousel:** 3 screens explaining key features

### B. Group Management

- [ ] **Create Group:** Input Name + Cover Emoji/Color
- [ ] **Group Types:** Trip, Home, Couple, Event, Other
- [ ] **Add Members (Guest):** Input text names ("Mom", "Rahul")
- [ ] **Add Members (Verified):** Import from Contacts (Hash Check) or Search by ID
- [ ] **Group Settings:** Rename group, Leave group, Export CSV
- [ ] **Viral Share:** "Share Link" button → Generates `koshbook.app/g/...`
- [ ] **QR Code:** Scannable for in-person sharing

### C. Expense Engine

- [ ] **Add Expense UI:**
    - [ ] Amount Keypad (Calculator style)
    - [ ] Currency Selector (Auto-detect)
    - [ ] Category Selector (Auto-icon)
    - [ ] Description Input with suggestions
    - [ ] "Paid By" Selector (Single/Multiple)
    - [ ] "Split By" Selector (Equal/Unequal/Shares/Percent)
    - [ ] Receipt Camera Button
    - [ ] Date Picker
- [ ] **Expense List:** Chronological feed of bills
- [ ] **Expense Detail:** View full split breakdown + Comments
- [ ] **Edit/Delete Expense:** With audit trail
- [ ] **Multi-Payer Support:** Multiple people paid different amounts

### D. Splitting Methods

- [ ] **Equal Split:** Divide by member count
- [ ] **Unequal Split:** Manual amounts per person
- [ ] **Percentage Split:** % allocation
- [ ] **Shares Split:** Unit-based (2:1:1)
- [ ] **Exclusion:** Skip specific people from split
- [ ] **Adjustment:** Equal split with +/- adjustments
- [ ] **AI/NLP Split (Premium):** Natural language parsing
- [ ] **Voice Input (Premium):** Speech-to-text for splitting

### E. Settlement & Payments

- [ ] **Balances Tab:** "Who owes who" graph within group
- [ ] **Debt Simplification:** Minimize transactions (A→B→C becomes A→C)
- [ ] **Settle Up UI:**
    - [ ] Select Payer → Payee
    - [ ] Enter Amount (editable)
    - [ ] **"Pay via UPI"** Button (Intent)
    - [ ] **"Record Cash"** Button
    - [ ] **"Record Bank Transfer"** Button
- [ ] **UPI App Grid:** Detects installed apps (GPay, PhonePe, Paytm)
- [ ] **Proof Upload:** Attach screenshot to settlement record
- [ ] **Verification Flow:** Payee gets "Confirm Payment" button
- [ ] **Global Settlement (Verified):** Cross-group net balance

### F. Friends & Global View

- [ ] **Friends List:** All people across groups
- [ ] **Filter Tabs:** All | Owes You | You Owe
- [ ] **Friend Detail:** Per-person balance breakdown
- [ ] **Personal Borrows:** Non-group lending tracker
- [ ] **Invite to App:** Share invite link to non-users

### G. Activity & Notifications

- [ ] **Activity Feed:** Chronological action log
- [ ] **Activity Types:**
    - [ ] Expense Added/Edited/Deleted
    - [ ] Payment Made/Received
    - [ ] Group Joined/Left
    - [ ] Reminders
- [ ] **Push Notifications:** FCM integration
- [ ] **Unread Markers:** Red dot for unseen items

### H. Profile & Settings

- [ ] **Identity Card:** Avatar, Name, Email/Phone
- [ ] **Auth Action:** "Sign Up / Log In" (for Guests)
- [ ] **Account Merge:** Link Guest data to Verified account
- [ ] **Payment Settings:** Save UPI VPA
- [ ] **App Settings:** Currency, Theme (Dark/Light), Notifications
- [ ] **Data Export:** CSV download
- [ ] **Privacy:** Clear data, Delete account

### I. Premium Features (Locked)

- [ ] **AI Input:** Microphone button → NLP Processing
- [ ] **OCR Input:** "Scan Receipt" → Auto-fill items
- [ ] **Receipt Storage:** Permanent cloud storage
- [ ] **Recurring Expenses:** Auto-add on schedule
- [ ] **PDF Reports:** "Download PDF Report"
- [ ] **Multi-Settle:** Settle multiple debts at once

---

## 13. Future Scope / Post-MVP

### Phase 1 Enhancements (Month 4-6)

- [ ] **WhatsApp/Telegram Bot:** "@koshbook split ₹1000 between Amit, Priya"
- [ ] **Widget:** Home screen widget showing net balance
- [ ] **Apple Watch / WearOS:** Quick expense entry

### Phase 2 Features (Month 6-9)

- [ ] **Personal Expense Tracker:** Standalone mode for daily logging
- [ ] **Budget Categories:** Set monthly budgets with alerts
- [ ] **Multi-Currency:** Auto-conversion for international trips
- [ ] **Expense Reminders:** "Hey, you haven't logged today's expenses"

### Phase 3 Vision (Year 2)

- [ ] **Bill Scanner Plus:** Parse itemized receipts for per-item splitting
- [ ] **Integration APIs:** Connect to accounting software
- [ ] **Family Mode:** Shared family expense tracking
- [ ] **Business Mode:** Invoice generation, tax reporting

### Technical Debt Items

- [ ] **Migration to gRPC-web:** For better browser support
- [ ] **Multi-region Deploy:** EU, US, Asia data centers
- [ ] **Kubernetes:** For auto-scaling
- [ ] **GraphQL Gateway:** Alternative API option

---

## 14. Formal Protocol

This document serves as the **Project Constitution** for Koshbook development.

**Document Rules:**
- Any changes to these requirements must be explicitly updated here before code changes
- Feature additions require corresponding Technical Architecture updates
- All team members (AI or human) must align with this specification

**Version Control:**
- Major versions: Significant feature or architecture changes
- Minor versions: Clarifications and detail additions
- All changes logged with date and author

---

*End of Lakshya's Development Plan*

*Version: 1.0*  
*Last Updated: December 2025*  
*Author: Lakshya Agarwal*


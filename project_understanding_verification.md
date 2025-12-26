# Koshbook (Splitter) - Project Manifesto & Requirement Specification

## 1. Project Context & Mission
**Product Name:** Koshbook (Working Title: "Splitter")
**Tagline:** Frictionless Finance.

### 1.1 The Market Problem
The dominant player, Splitwise, has degraded its user experience by introducing hostile features to force monetization:
1.  **Artificial Limits:** Free users are restricted to 3 expenses per day, breaking the utility for trips and daily roommates.
2.  **Ad Friction:** Users face mandatory 10-second delays before adding expenses.
3.  **Forced Accounts:** New users cannot participate without creating an account immediately.

### 1.2 The "Anti-Splitwise" Mission
Koshbook aims to capture this dissatisfied market by adhering to a strict "User-First" philosophy:
*   **Zero Barriers:** Installation to First Expense in < 5 seconds. No Login required initially.
*   **Respectful Design:** No ads that block functionality. No artificial limits on data entry.
*   **Speed:** Offline-first architecture ensures instant interactions, independent of network status.

---

## 2. User Experience (UX) Principles

### 2.1 The "Hybrid" Identity Model
The application must handle two distinct user states seamlessly.

#### A. The Guest User (Default State)
*   **Definition:** A user who has downloaded the app but not signed in.
*   **Identity:** `Device_UUID` (Generated locally on first launch).
*   **Data Scope:** Local Device Only (Isar Database).
*   **Capabilities:**
    *   Create unlimited Groups.
    *   Add unlimited Expenses.
    *   Participants are "Virtual Strings" (e.g., "Mom", "Roommate"). These names have no global existence and are unique to the specific group they are created in.
    *   **Limitation:** If the app is uninstalled, all data is lost.

#### B. The Verified Member (Opt-In State)
*   **Definition:** A user who has chosen to secure their data via Email or Mobile auth.
*   **Identity:** `User_ID` (Global, Cloud-mapped).
*   **Data Scope:** Cloud Synced (PostgreSQL) + Local Cache.
*   **Capabilities:**
    *   **Data Persistence:** Restore history on any new device.
    *   **Real Users:** Can search and add other Verified Members to groups.
    *   **Global Context:** The app understands that "User A" in Group X is the same person as "User A" in Group Y.

### 2.2 Viral Sharing (The "Magic Link")
*   **Objective:** Allow Guests to share bills without forcing the recipient to install the app.
*   **Mechanism:**
    1.  Guest taps "Share Group".
    2.  App bundles local data (JSON) -> Uploads to Temporary Cloud Storage.
    3.  Generates a short URL: `koshbook.app/view/xyz`.
    4.  **Recipient View:** Opens a read-only Mobile Web view of the ledger.
    5.  **Recipient Action:** "Open in App" button deep-links to import the group locally.

---

## 3. Detailed Feature Specifications

### 3.1 Expense Management Engine
The core utility must be robust enough for complex financial scenarios.

*   **Multi-Payer Support:**
    *   *Input:* "Total Bill: ₹1000".
    *   *Payer Selection:* "Multiple People" -> "Amit paid ₹400, Priya paid ₹600".
    *   *Validation:* System prevents saving unless `Sum(Paid) == Total`.
*   **Split Methods:**
    1.  **Equally:** `Total / N`.
    2.  **Unequally:** Manual input (e.g., A: 200, B: 800).
    3.  **Percentages:** Slider UI (A: 20%, B: 80%).
    4.  **Shares:** Unit-based (A: 2 shares, B: 1 share).
    5.  **Adjustment:** "Equal split, but Amit pays +₹50".

### 3.2 Global Settlement (Verified Only)
*   **Concept:** The "Net Worth" Dashboard.
*   **Algorithm:**
    *   Fetch all debts involving the Verified User across *all* groups.
    *   Calculate `Net Balance = (Total Owed to Me) - (Total I Owe)`.
    *   **Cross-Group Balancing:** If I owe User B ₹100 in Group 1, and User B owes me ₹40 in Group 2, the Global Dashboard displays a single line item: "You owe User B ₹60".
*   **Settlement Action:** Paying ₹60 triggers the system to auto-generate "Payment Records" in both Group 1 (₹100) and Group 2 (₹40) to clear the books.

### 3.3 Payments & Proof
*   **UPI Integration (India):**
    *   Users save their VPA (UPI ID) in Profile.
    *   "Pay Now" button generates `upi://pay` intent link.
    *   Opens installed apps (GPay, PhonePe, Paytm) directly.
*   **Manual Payment Verification:**
    *   For Cash/Bank Transfer/Non-UPI methods.
    *   **Payer Action:** Records payment -> Uploads Screenshot/Photo Proof.
    *   **State:** Debt is marked "Pending Verification".
    *   **Payee Action:** Receives notification -> Reviews Proof -> Taps "Confirm".
    *   **Final State:** Debt is settled.

---

## 4. Monetization Strategy (Free vs. Premium)

| Feature | Tier | Rationale |
| :--- | :--- | :--- |
| **Unlimited Expenses** | **Free** | Core competitive advantage. Must be free. |
| **Unlimited Groups** | **Free** | Encourages viral growth. |
| **Global Settlement** | **Free** | Incentive to become a "Verified Member" (Sign up). |
| **CSV Export** | **Free** | Basic data ownership. |
| **AI Voice Splitting** | **Premium** | Costs compute/API credits. High convenience value. |
| **OCR Receipt Scan** | **Premium** | Costs API credits (Google Vision). |
| **Auto-Recurring Bills** | **Premium** | Server-side automation convenience. |
| **PDF/Excel Reports** | **Premium** | Professional value for accountants/landlords. |
| **WhatsApp Bot** | **Premium** | High convenience ("Text to Split"). |
| **Cloud Receipt Storage** | **Premium** | Costs storage (S3). Free tier gets compressed/local only. |

---

## 5. Technical Architecture Principles

### 5.1 Offline-First (The "Isar" Core)
*   **Primary Source of Truth:** The Local Database (Isar).
*   **UI Behavior:** The UI *always* reads from and writes to the Local DB first. This ensures 60fps performance and zero network lag.
*   **Sync Logic:**
    *   Writes are queued in a "Mutation Log" (Insert/Update/Delete).
    *   Background Service (WorkManager) pushes mutations to the server when online.
    *   Server resolves conflicts using "Last Write Wins" (LWW).

### 5.2 Strict Identity Separation
*   **Logic:** The system treats "Virtual Strings" and "Real Users" as fundamentally different data types.
*   **Rule:** We do **NOT** attempt to "Guess" or "Auto-Merge" identities.
    *   If User A adds "Amit" (Virtual) in Group 1.
    *   And adds "Amit" (Real) in Group 2.
    *   They remain separate entities.
    *   **Why?** To prevent data corruption and privacy leaks. Users must explicitly add the Real User to gain Global Settlement benefits.

---

## 6. Formal Protocol

This document serves as the **Project Constitution**.
*   **Versioning:** Any changes to these requirements must be explicitly updated here before code changes.
*   **Authorization:** The existence of this document implies understanding, **not** execution. The Developer (AI) requires an explicit "Start" command to proceed to the Technical Implementation Plan.

---

## 7. Explicit Feature List (Inventory)

### A. Onboarding & Home
- [ ] **Splash Screen:** Instant load, checks for `Device_UUID`.
- [ ] **Dashboard:**
    - [ ] "Total Net Worth" Card (Green/Red balance).
    - [ ] List of "Recent Groups".
    - [ ] "Add Expense" Floating Action Button (FAB).
- [ ] **Global Search:** Find expenses across all groups by description/amount.

### B. Group Management
- [ ] **Create Group:** Input Name + Cover Icon.
- [ ] **Add Members (Guest):** Input text names ("Mom", "Rahul").
- [ ] **Add Members (Verified):** Import from Contacts (Hash Check) or Search by ID.
- [ ] **Group Settings:** Rename group, Leave group, Export CSV.
- [ ] **Viral Share:** "Share Link" button -> Generates `koshbook.app/view/...`.

### C. Expense Engine
- [ ] **Add Expense UI:**
    - [ ] Amount Keypad.
    - [ ] Category Selector (Auto-icon).
    - [ ] Description Input.
    - [ ] "Paid By" Selector (Single/Multiple).
    - [ ] "Split By" Selector (Equal/Unequal/Shares/Percent).
    - [ ] Receipt Camera Button.
- [ ] **Expense List:** Chronological feed of bills.
- [ ] **Expense Detail:** View full split breakdown + Comments.

### D. Settlement & Payments
- [ ] **Balances Tab:** "Who owes who" graph within a group.
- [ ] **Settle Up UI:**
    - [ ] Select Payer -> Payee.
    - [ ] Enter Amount.
    - [ ] **"Pay via UPI"** Button (Intent).
    - [ ] **"Record Cash"** Button.
- [ ] **Proof Upload:** Attach screenshot to settlement record.
- [ ] **Verification:** Payee gets "Confirm Payment" button.

### E. Profile & Settings
- [ ] **Identity Card:** Avatar, Name, Email/Phone.
- [ ] **Auth Action:** "Sign Up / Log In" (for Guests).
- [ ] **Payment Settings:** Save UPI VPA.
- [ ] **App Settings:** Currency, Theme (Dark/Light), Notifications.

### F. Premium Features (Locked)
- [ ] **AI Input:** Microphone button -> NLP Processing.
- [ ] **OCR Input:** "Scan Receipt" -> Auto-fill items.
- [ ] **Reports:** "Download PDF Report".

---

## 8. Future Scope / Post-MVP
*   **Personal Trackers:** Daily loggers for Milk, Newspaper, etc.
*   **Recurring Reminders:** Local notifications for manually tracked bills.
*   **Multi-Currency:** Auto-conversion for international trips.

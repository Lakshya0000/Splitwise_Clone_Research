# Koshbook (Project Splitter) - Product Requirements Document

## 1. App Overview & Vision
**App Name:** Koshbook (Working Title: Splitter)
**Core Concept:** A friction-free expense splitting app that solves the "awkwardness" of money. It is designed to be **Offline-First**, **Fast**, and **Private**.
**Primary Differentiator:** Unlike competitors that force login immediately, Koshbook allows users to download the app and start splitting bills in **< 5 seconds** (Guest Mode). It converts to a robust cloud synced app (Verified Mode) only when the user chooses.

---

## 2. User Modes & Experience Levels
The app functionality changes based on the user's "Tier". It is critical to distinguish these three states clearly.

### A. The "Guest" Experience (Free, Default)
*Target: New users, quick trips, roommates who don't want to signup.*
*   **Identity:** Anonymous. Identified solely by `Device_UUID`.
*   **Storage:** Local Database (Isar) on the phone. Data is permanent locally but lost if the app is uninstalled.
*   **Key Capabilities:**
    *   **Offline Creation:** Can create groups and add expenses without internet.
    *   **Unlimited Expenses:** No artificial limits on how many bills can be added.
    *   **Manual Publish:** Can "Publish" a group to the cloud to generate a sharable link (`koshbook.app/g/xyz`).
    *   **30-Day Limit:** Published links work for other people for 30 days.

### B. The "Verified" Experience (Free, Login)
*Target: Regular users, friends who travel together often.*
*   **Identity:** Email Address (via Google/Magic Link).
*   **Storage:** Cloud Database (Postgres) + Local Cache.
*   **Key Capabilities:**
    *   **Everything in Guest, plus:**
    *   **Real-Time Sync:** Changes made by one person appear instantly on others' phones (WebSockets).
    *   **Global Debt Dashboard:** A single view showing "Who do I owe across *all* my groups?".
    *   **Data Recovery:** Can login to a new phone and restore all history.
    *   **Multi-Device:** Use on Android Phone and iPad simultaneously.

### C. The "Premium" Experience (Paid)
*Target: Power users, accountants, large groups.*
*   **Key Capabilities:**
    *   **AI Splitting:** Voice/Text commands like "Split 5000 for dinner but exclude Amit from drinks".
    *   **Receipt Scanning (OCR):** Take a photo of a bill, and the app auto-extracts items and prices.
    *   **Recurring Expenses:** Set up "Rent" to auto-add on the 1st of every month.
    *   **PDF Exports:** professional accounting reports.

---

## 3. Core User Flows
These are the specific actions a user performs.

### Flow 1: Initialization (The "5-Second" Rule)
1.  User opens app.
2.  **No Login Screen.** They land directly on the "Home Dashboard".
3.  Background logic checks: "Do I have a User ID? No? Generate a Guest ID."

### Flow 2: Creating a Group
1.  User taps "Create Group".
2.  **Input:** Enters Name ("Goa Trip") and selects a Cover Icon/Color.
3.  **Add People:**
    *   *Guest Mode:* Types names manually ("Amit", "Priya").
    *   *Verified Mode:* Selects from "Recent Friends" or "Phone Contacts".
4.  **Result:** A Group is created locally. If internet is off, it still works.

### Flow 3: Adding an Expense (The "Core Loop")
1.  User taps group -> Taps "Add Expense" FAB.
2.  **Amount:** Types "₹ 1500" on a large calculator-style keypad.
3.  **Details:** Types "Lunch". App auto-selects a "Burger" icon.
4.  **Payer:** Defaults to "You". Can be changed to "Amit".
5.  **Splitting:** Defaults to "Equally".
    *   *User can tap:* change to "Unequally", "Shares", or "Percentages".
6.  **Save:** User taps Checkmark.
    *   *Immediate Result:* Expense appears in list. Balances update.
    *   *Background:* If online, it syncs. If offline, it waits.

### Flow 4: Settling Up (Paying back)
1.  User sees red card: "You owe Amit ₹500". Taps "Pay".
2.  **Payment Screen:** Shows "Paying ₹500 to Amit".
3.  **Action:** User taps "Pay via UPI".
4.  **App Switch:** Opens GPay/PhonePe with Amit's VPA pre-filled.
5.  **Return:** User returns to Koshbook. App asks "Did payment succeed?".
6.  **Confirmation:** User taps "Yes". A "Payment" record is added to the group ledger, reducing the debt to zero.

---

## 4. UI & Screen Specifications
What the user actually sees.

*   **Home Screen:** List of active groups. A "Net Balance" card at the top (Green/Red). Quick actions to "Split Bill".
*   **Friends Screen:** A rolodex of people you know. Filter by "Who owes you" vs "Who you owe".
*   **Activity Tab:** A notification feed ("Amit added 'Taxi'", "Priya paid you").
*   **Group Detail:** The main ledger. Tabs for "Expenses" (List), "Balances" (Simplified "Who owes who"), and "Totals" (Charts).
*   **Profile/Settings:** Where Guests go to "Sign Up / Merge Account" and Verified users go to "Export Data" or "Manage UPI ID".

---

## 5. Technical Constraints & Logic (For the Developer)
*   **Offline Sync:** The app must work 100% offline. Sync happens via a "Delta Log" mechanism when internet returns.
*   **Conflict Resolution:** Last Write Wins (LWW).
*   **Tech Stack:**
    *   **Frontend:** Flutter (Mobile).
    *   **Backend:** Go (Golang) Microservices.
    *   **Database:** PostgreSQL (Cloud) + Isar (Local).

---

## 6. Raw Prompt History (User's Exact Instructions)
*These are the verbatim prompts given by the user to shape this document. They contain critical context on tone, structure, and priorities.*

1.  "2 ki main heading kha gye. 2 mei do subheadings: free tier, premium tier. dono ke brackets mei their pricing. in free tier again 2 sub headings guest mode, verified mode. jo chizen common h unhe free tier ke under daal do. and those are for guest mode keep in guest and for verified keep in verified. so that better readability"
2.  "don't ask for git changes again and again. in core features make it indentation one space for a and b so that there appears a difference that a and b are under 2.1. or make a large table with two columns: free tier and premium tier. in free tier again 2 sub columns: guest mode, verified mode. then in features tick and cross or some text written in each filed explaining hteir chracterisitic in that feature"
3.  "in free tier history for 30 days mntion that and other things as well use some tick cross features as well so a difference can be seen in free tier and premiuim tier. if you are not sure any feature ask me"
4.  "splitting you mentioned mannuak ai voice instead create 3 features. manual equal/shares, ai (voice/nlp). aise points badhao so that difference appears in free tier and premium tier"
5.  "make this table more focuuseed on tick cross rather than explicit text make it more grnular"
6.  "Now in detailed screen background section make sure instead of explaining the logic it focuses more on what will be in UI not how ui will be processed. and think about all the screens whether it is a normal screen only... 1. Splash/Home Screen... Bottom Bar... something in this manner in points like in arpit's plan"
7.  "where is friends screen and activity screen make sure you keep consistency everywhere as you mentioned in home screen. and in settle up screen there can be multiple settlements so show multiple settlements. then there can be a settlement screen where we will see the details for that settlement and their payment options. and think more in UI perspective"
8.  "Now Improve the technical architecture section. first understand the core requirements from the above details then create the texhnical architecture what all aservices are required what will be the tech stack and how we're gonnal implement them and for structuring refer to arpit's dev plan technical architecture. but make sure to keep the tech architecture in details and include schema and flow. and instead of more code try to focus on schema and fields that are reuired everywhere like what is needed and what will be the output"
9.  "in technical architecture also include how each service will work and how each data entry will be updated, inserted and used in the frontend"
10. "arey upar toh kaafi features daale the kya sabhi cover hogye technical architecture mie?"
11. "and how expenses are linekd to group?"
12. "now do one thing prepare a different doc name it as koshbook.md. write all the features and arpit's dev plan features to an extent that explains what is the app and what are it's features and what action they will perform and what is the user flow and what are different modes clearly. so that I can give it to an ai and prepare a dev doc as you are not preparing for my level as i want"

---

## 7. Initial Project Vision (The Origin)
*The core philosophy that started the project (from `user_requirements.md`).*

**Product Vision:**
Koshbook is a simple, no-nonsense shared expense tracker.
**The Goal:** To remove the friction from sharing money. When a user buys something for the group, recording it should be as fast as sending a text message.

**Core Philosophy:**
*   **Zero Barriers:** No limits on how many times you can use it.
*   **Zero Waiting:** No ads, no timers, no loading screens for basic actions.
*   **Transparency:** Everyone sees exactly what changed and when.

**Key User Flows (The "Must Haves"):**
1.  **Creating a Space:** Users must be able to create a distinct "Space" or "Group" for different contexts (e.g., "Apartment 304", "Goa Trip").
2.  **The "Add Expense" Loop:** This is the most used feature. It must be effortless. (Tap "+" -> Amount -> Description -> Save).
3.  **Viewing Balances:** Users need to know their financial standing immediately. (Green "You are owed" / Red "You owe").
4.  **Settling Up:** When actual money changes hands (Cash, UPI), the app must record it to reset the balance.
5.  **Activity Log:** To prevent disputes, every action must be visible.

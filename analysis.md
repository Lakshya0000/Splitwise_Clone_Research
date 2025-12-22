# Market Analysis: The Opportunity for a Splitwise Alternative

## 1. Executive Summary
**The Core Finding:** Users are angry. Splitwise, once a beloved utility, has introduced aggressive restrictions that make the free version almost unusable for its primary use cases: **group trips** and **daily roommate expenses**.

This document outlines exactly *why* users are leaving and *what* they are looking for in a replacement, backed by real user feedback.

---

## 2. The Problem: Why Users Are Leaving (Deep Dive)
Based on our analysis of **16,000+ negative reviews**, here are the specific problems users face.

### A. The "3-Expense" Wall (The Dealbreaker)
**What it is:** Free users can now only add **3 expenses per day**.

**Why it hurts:**
*   **The Vacation Scenario:** Imagine you are on a trip with friends. You pay for breakfast, a taxi, and coffee. You are done. You cannot add lunch or dinner until tomorrow. The app becomes useless for tracking a busy day.
*   **The Roommate Scenario:** A household buys groceries, internet, and cleaning supplies on Saturday. The limit is hit immediately.

**Authentication (Real Reviews):**
> *"Ruined the app with their horrible decision of implementing a 3 transaction per day limit... I'm hoping I can find an alternative to what used to be a perfect app."*
> — **User Review (483 Thumbs Up)**

> *"It is SO inconvenient when on a trip (3 payments a day - really???). You saw green, and because of corporate greed, you ruined what was once an amazing app to use with friends when in vacation."*
> — **User Review (392 Thumbs Up)**

### B. The "Awkward Wait" (The 10-Second Delay)
**What it is:** Before adding an expense, free users must stare at a "Pro" advertisement for 10 seconds.

**The "Social" Problem:**
*   You are at a cash register. You want to quickly enter "I paid $40".
*   **The Friction:** You have to stand there awkwardly holding your phone while a timer counts down. It disrupts the flow of the moment.

**Authentication (Real Reviews):**
> *"Forcing users to watch a 10 second ad everytime they want to add an expense is ridiculous... The hunt for a replacement app starts today."*
> — **User Review (257 Thumbs Up)**

> *"Now you can only add a handful of expenses before they lock you out... They also make you wait a 10 second timer before adding each expense... pretty scummy business practices."*
> — **User Review (182 Thumbs Up)**

### C. The "Ransom" Subscription Model
**What it is:** Splitwise moved from "Pay for extra features" to "Pay to use the basic app." Users are willing to pay a small **one-time fee**, but not a monthly subscription for a calculator app.

**Authentication (Real Reviews):**
> *"I'm not against paying for it, but making the free tier useless and also having an expensive subscription model instead of a one time payment is a surefire way of shooting yourself in the foot."*
> — **User Review (483 Thumbs Up)**

> *"There's no justification for an annual 36 fee for what this app offers... This just destroyed the usability and user trust completely."*
> — **User Review (6 Thumbs Up)**

### D. Technical Frustrations
**What it is:** Aside from the limits, users report significant issues with syncing data between friends and getting stuck in login loops.

**Authentication (Real Reviews):**
> *"Doesn't simplify expenses... developers deliberately enshittified their app and removed features... wouldn't recommend setting up on this app if you're not already using it."*
> — **User Review (3 Thumbs Up)**

---

## 3. What is Splitwise? (Context)
For context, here is what the app is supposed to do.

**The Goal:** A shared digital notebook for expenses.

**How it works:**
1.  **Groups:** You create a group (e.g., "Road Trip").
2.  **Add Expense:** You enter an amount and who paid.
3.  **The Math:** The app calculates "Who owes who."
4.  **Simplification:** Instead of 10 small payments between 5 people, the app calculates the easiest way to settle up (e.g., "Bob pays Alice $50").

---

## 4. The Solution: "The Clone" Strategy
To win these users over, we do not need to invent new features. We just need to **fix the broken ones**.

### The "Winning" Features (MVP)
| Feature | The Splitwise Problem | Your Clone's Solution |
| :--- | :--- | :--- |
| **Adding Expenses** | **Blocked.** Limited to 3/day. | **Unlimited.** Add 50 expenses a day if you want. |
| **Speed** | **Slow.** Forced 10s wait. | **Instant.** Tap -> Type -> Save. |
| **Search** | **Restricted.** Hard to find old bills. | **Free.** Search any past expense instantly. |
| **Graphs** | **Paid.** Locked behind "Pro". | **Free.** Simple pie charts of spending. |
| **Data Export** | **Paid.** | **Free.** Download your data as CSV anytime. |

### Technical Architecture Approach
To solve the "Sync Lag" problem, we will build a "Real-Time First" system.
*   **Works Offline:** You can add expenses on a plane or in a remote cabin.
*   **Instant:** It feels faster because it saves to the phone first, then syncs.

### Roadmap
*   **Phase 1 (The Fix):** A clean app with **Unlimited Expenses** and **Groups**. Target the users leaving Splitwise right now.
*   **Phase 2 (The Polish):** Add "Debt Simplification" math and Receipt Uploads.
*   **Phase 3 (Sustainability):** Add optional paid features that *don't* block basic usage (like AI receipt scanning).
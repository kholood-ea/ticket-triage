# Taxonomy (v1.0 - FINALIZED)

Rule: Every ticket gets exactly ONE category (the primary issue) and ONE priority.
Write this BEFORE labeling anything. Change it only with a version bump and re-label.

## Categories

| name | one-line definition | NOT this (confusable with) | example (your own words) |
|---|---|---|---|
| billing_charges | Unexplained, duplicate, or incorrect fees/charges deducted or billed | payment_failure (transaction never settled or recipient didn't receive) | "اتخصم مني 50 جنيه رسوم إدارية ومش مكتوبة في الشروط" / "تم سحب مبلغ مرتين لنفس الفاتورة" *(Charged administrative fee not in terms / debited twice for same invoice)* |
| payment_failure | A payment, transfer, or top-up failed, got stuck, timed out, or recipient never received funds | billing_charges (disputing legitimate fee/amount) | "حولت 500 ريال لصديقي والمبلغ اتخصم من عندي وما وصله" / "الدفع بالفيزا معلق ورافض يكتمل" *(Transferred money but friend didn't receive / payment pending and won't complete)* |
| account_access | Cannot log in, forgotten PIN/password, account locked, OTP not arriving, KYC verification blocked | security_fraud (unauthorized actor gained access) | "مش عارف أسجل دخول ورسالة كود التحقق OTP مش بتوصلني خالص" / "الحساب مقفول ومحتاج إعادة تعيين كلمة المرور" *(Can't log in and OTP not arriving / account locked needing password reset)* |
| service_outage | Widespread platform downtime, whole service unavailable, network gateway down | technical_issue (isolated bug affecting a single user/device) | "التطبيق كله واقع ومش بيفتح مع أي حد وبيجيب خطأ في السيرفر 500" / "خدمة التحويلات متوقفة في السيستم كله" *(App is down for everyone with 500 server error / transfer service down platform-wide)* |
| technical_issue | Specific app bug, UI glitch, button unresponsive, crash on specific action for a single user | service_outage (widespread system failure) | "كل ما اضغط على زرار تحميل كشف الحساب التطبيق بيقفل ويخرج لوحده" / "الشاشة بتفضل بيضاء لما افتح صفحة البطاقات" *(App crashes when clicking download statement / white screen on cards tab)* |
| security_fraud | Suspected or confirmed unauthorized transaction, account compromise, stolen card/device, scam | account_access (routine forgotten credentials) | "جالي إشعار بعملية شراء من كارتي في لندن وأنا في مصر والكارت معايا!" / "حد اخترق حسابي وغير رقم التليفون" *(Got notification for transaction in London while card is in Egypt / account hacked and phone changed)* |
| request_information | Asking how something works, transfer limits, fees, exchange rates, or required documents | complaint about a failure | "عايز أعرف الحد الأقصى للتحويل اليومي كام؟" / "إيه الأوراق المطلوبة لفتح حساب فرعي للشركات؟" *(What is the daily transfer limit? / What documents are needed for a sub-account?)* |
| other_unclear | Doesn't fit, unclassifiable intent, unintelligible text, gibberish, spam, or too vague to label | Any actionable complaint or query (use sparingly; track its rate) | "سلام" / "؟؟؟؟" / "asdfgh" / "شكراً" *(Greetings with no issue / punctuation only / gibberish)* |

## Tie-Breaking Hierarchy
When a customer ticket contains multiple distinct complaints or overlapping issues, apply the tie-breaker in strict priority sequence (first matching wins):

1. `security_fraud` (Protect funds and customer safety first)
2. `payment_failure` (Resolve stuck or delayed capital)
3. `account_access` (Restore customer access to system)
4. `billing_charges` (Correct financial balances)
5. `service_outage` (Acknowledge systemic disruption)
6. `technical_issue` (Address functional software defects)
7. `request_information` (Answer informational inquiries)
8. `other_unclear` (Fallback only when zero actionable content exists)

### Multi-Intent Conflict Examples
- *"حسابي مقفول ومش عارف ادخل وفي عملية غريبة اتعملت من نص ساعة"* (Account locked and unfamiliar transaction occurred 30 mins ago):
  Matches `account_access` and `security_fraud` -> **`security_fraud`** (action on fraud comes first).
- *"حولت فلوس والعملية فشلت وكمان التطبيق هنج وقفل"* (Transferred money and transaction failed, plus app froze and crashed):
  Matches `payment_failure` and `technical_issue` -> **`payment_failure`** (financial transaction issue takes precedence over UI crash).
- *"الرسوم عالية جداً وعايز اعرف بتتحسب إزاي"* (Fees are very high and I want to know how they are calculated):
  Matches `billing_charges` and `request_information` -> **`billing_charges`** (dispute regarding fees takes precedence over informational request).

## Priority (3 levels, defined by observable facts, not by tone)

- **high**:
  - Direct money lost or actively at risk (unauthorized transaction, stolen card/credentials).
  - Security/fraud alert or account takeover attempt.
  - Account fully locked preventing critical access.
  - Regulated deadline or legal escalation notice.
  - Widespread service outage affecting operations.
- **medium**:
  - Service or transaction impaired or delayed, but a workaround exists.
  - Non-critical feature inaccessible while primary account features work.
  - Repeated contact regarding an unresolved issue.
- **low**:
  - General questions, "how-to" inquiries, and fee schedule requests.
  - Minor cosmetic UI inconvenience with no financial or operational impact.
  - Feedback, compliment, or general greeting.

### Tone Invariance Calibration (Test Deliberately)
Angry tone alone does NOT raise priority. Calm tone does NOT lower it. In your 60-ticket dataset, include calm high-priority and angry low-priority tickets:

- **Calm + HIGH**:
  *"مساء الخير، أرجو التكرم بالتحقق حيث يوجد سحب بقيمة 2000 دولار من حسابي لم أقم به. شكراً لتعاونكم."*
  *(Customer is polite, calm, and courteous, but has active unauthorized money drain -> **HIGH** priority).*
- **Angry + LOW**:
  *"تطبيق زبالة وخدمة عملاء فاشلة وضيعتوا وقتي عشان زرار الإعدادات لونه باهت ومش عاجبني غيروه حالاً يا فشلة!!!"*
  *(Customer is screaming, insulting, and furious, but the issue is purely aesthetic with zero functional or money impact -> **LOW** priority).*

## Operational Guardrails & Day 2 Settlement
- **Domain focus**: Calibrated for digital banking, fintech, and payments customer support in Arabic, covering primary customer touchpoints while maintaining standard SaaS operational compatibility.
- **`other_unclear` Rate Threshold**: Target is **< 5%**. If the rate of `other_unclear` exceeds **10%** in any evaluation batch or the 60-ticket dataset, consider the taxonomy broken or incomplete, pause labeling, and issue a version bump (v1.1) to add the missing category.

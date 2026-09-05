# Where the Marketplace Leaks
## Diagnosing Uber Delhi-NCR's demand-to-completion gap — calendar year 2024

**Individual Case Analysis · 3 questions × 10 marks = 30 marks**
Big Data Analytics — MBA (Business Analytics), SBM-NMIMS

---

## 1. Management context

It is December 2024. Uber India's leadership is closing its Delhi-NCR review before 2025 planning. Bookings and gross booking value across the product range — bike, e-bike, auto, economy cab, sedan, premium and larger vehicles — are up on the year. Leadership is not reassured: it believes the next wave of competition will arrive not citywide but at the level of a vehicle type, in a set of neighbourhoods, in a particular time window — wherever Uber's own marketplace is quietly failing riders.

Uber has no competitor transaction data and will not be given any. It has its own booking log for the whole of 2024.

The India Head's question:

> **"Where is Uber failing to convert demand into successfully completed rides, why might those failures be occurring, and where should management intervene first?"**

The Head of Marketplace Analytics' framing:

> **"If you were a competitor entering Delhi-NCR in 2025 with limited capital, where would you attack first — using nothing but the weaknesses visible in Uber's own data?"**

One statement from the review meeting will matter later. A senior operations leader asserted, without evidence: **"Drivers are cancelling because Uber pays them too little."**

## 2. Your role

Analyst, Uber India Strategy & Marketplace Analytics, Delhi-NCR pod. You have the 2024 booking file, a Spark/Databricks environment and 7 days. Your report goes to the India Head and the Head of Marketplace Analytics. Both will challenge your denominators, your labels and every causal word you use.

## 3. The dataset

One row per booking request, Delhi-NCR, 1 January–31 December 2024.

| Field | What it holds | Expected to be populated on (verify) |
|---|---|---|
| Date, Time | Request timestamp | All rows |
| Booking ID | Request identifier | All rows (expected unique — verify) |
| Booking Status | **Completed / No Driver Found / Cancelled by Driver / Cancelled by Customer / Incomplete** | All rows |
| Customer ID | Rider identifier | All rows |
| Vehicle Type | Product requested | All rows |
| Pickup Location, Drop Location | Named locations; no coordinates | All rows |
| Avg VTAT | Vehicle time-to-arrive at pickup, minutes, per booking (see data dictionary) | Matched bookings |
| Avg CTAT | Customer turnaround / trip time, minutes, per booking (see data dictionary) | Started trips |
| Cancelled Rides by Customer · Reason for cancelling by Customer | Flag and stated reason | Customer cancellations |
| Cancelled Rides by Driver · Driver Cancellation Reason | Flag and stated reason | Driver cancellations |
| Incomplete Rides · Incomplete Rides Reason | Flag and stated reason | Incomplete rides |
| Booking Value | Gross value of the booking, ₹ | Started / completed trips |
| Ride Distance | km | Started / completed trips |
| Driver Ratings, Customer Rating | Post-trip ratings | Completed trips |
| Payment Method | Instrument used | Completed trips |

Know three things before you open it. **Most nulls are structural** — a "No Driver Found" record has no fare, distance or rating because no trip happened; a null is a data-quality problem only once you have ruled out that the field is logically empty for that status. **"Avg VTAT" and "Avg CTAT" are per-booking values** despite their names; confirm the definitions and state the interpretation you use. **Booking Value is gross transaction value, not Uber revenue** — no commission or take-rate is provided.

## 4. Rules of evidence  -- Gets you bonus marks but not compulsory 

- Individual work. Core pipeline in PySpark / Spark SQL; Python for charts is fine; Excel-only work will not be marked.
- Every rate must state numerator, denominator and the rows on which it is valid.
- Tag every finding **[Observation]**, **[Inference]**, **[Hypothesis]** or **[Causal claim]** (the last only if defensible from this data).
- Where the data cannot support a statement, write exactly: *"Cannot be established from the provided dataset."* and say what would be needed.
- No outside facts about Uber, competitors, driver economics, schemes or market share. Competitors are hypothetical entrants only. The data is 2024; nothing after it.
- Do not drop, impute or zero-fill nulls without a stated reason. Do not manufacture data.
- Set and justify a minimum sample size before you rank any segment.
- Marks reward judgement, not volume.

## 5. Working assumptions

- **A1.** One row = one booking request; Booking ID expected unique (verify).
- **A2.** Booking Status is the final reported status.
- **A3.** Booking Value = gross booking value (₹); not revenue.
- **A4.** Ratings on a 1–5 scale (verify).
- **A5.** Pickup Location is the geographic unit ("micro-market").
- **A6.** Default time buckets (redefine with justification; one scheme throughout): Late Night 00:00–05:59 · Morning Peak 06:00–09:59 · Midday 10:00–15:59 · Evening Peak 16:00–19:59 · Night 20:00–23:59.
- **A7.** Weekend = Saturday and Sunday.
- **A8.** No driver-side data exists.

---

## 6. Questions — 30 marks

### Q1. Frame the problem and trust the data — 15 marks

**1.1 (4 marks).** The India Head has been told "bookings and gross booking value both grew in 2024, so the marketplace is healthy." Explain, in no more than one page, why that reading does not answer the question being asked. Distinguish demand from fulfilment. Map the five Booking Status values onto a marketplace funnel and state precisely what each status can and cannot tell you about *where* a request failed, given the events this file does and does not contain. Explain why gross booking value is not revenue and what you would need to compute revenue.

**1.2 (6 marks).** Define the KPI set for the diagnosis — at minimum Completion Rate, No-Driver-Found Rate, Driver Cancellation Rate, Customer Cancellation Rate and Incomplete Ride Rate — each with its exact numerator, denominator and valid rows, plus at least one further metric of your own defined with the same precision. For each of Booking Value, Ride Distance, Avg VTAT, Avg CTAT, Driver Ratings, Customer Rating and Payment Method, state on which statuses the field is meaningfully populated and therefore on which rows any average or share must be computed. Compute the citywide 2024 baseline for every KPI.

**1.3 (5 marks).** Audit the dataset. Classify nulls field by field as structural or invalid. Check duplicate Booking IDs, rating ranges, impossible distances and values, categorical inconsistencies, and consistency between Booking Status and the other fields — including the cancellation and incomplete flag columns. Write at least five validation rules in IF … THEN … form, report how many rows violate each, and state what you did with the violators and why.

### Q2. Diagnose the marketplace — 15 marks

**2.1 (4 marks).** Build a micro-market table at the grain **Pickup Location × Vehicle Type × Time Bucket**, and separately cut by **Day of Week** (weekday vs weekend at minimum). For each cell report demand (requests), the five KPI rates, mean VTAT and CTAT on valid rows with coverage counts, and mean Booking Value and ₹ per km on completed rides. **Before interpreting any cell, state and justify a minimum-support threshold.** If the three-way grain is too sparse to be stable, roll up — to two-way cuts or to the highest-demand pickup locations — and justify the roll-up. Include the table in an appendix.

**2.2 (4 marks).** Implement 2.1 as a reproducible Spark pipeline (DataFrame API or Spark SQL) showing parsing of Date and Time; derivation of hour, day of week and time bucket; one 0/1 flag per status; aggregation by **summing flags**; the threshold filter; and the reclassification you define in 2.3, so that the table carries both the official and the effective metrics side by side. In no more than 150 words, explain why your grain is the right one for the management decision and why flag-then-sum is the correct aggregation.

**2.3 (3 marks).** Inspect the values of *Reason for cancelling by Customer*. Some describe driver behaviour rather than customer choice. Define an **Effective Driver-Induced Failure Rate**: state the reclassification rule, defend it, identify the ambiguous reasons and how you treated them, show how the citywide attribution of failures between drivers and customers changes under your rule, and say what changes in management's interpretation as a result.

**2.4 (4 marks).** Identify the **three** vulnerabilities that matter most commercially. For each: WHERE, WHEN, WHICH VEHICLE, the dominant failure mode (No Driver Found vs driver cancellation — official and effective — vs customer cancellation vs incomplete), the KPI evidence against the relevant vehicle-type baseline, and what you can and cannot infer about the cause. Explain why these three outrank everything else — in particular why a high-failure, low-demand cell was or was not selected. Where the differences between segments are small, say so.

### Q3. Decide, defend and scale — 15 marks

**3.1 (4 marks).** Build a transparent **Competitive Vulnerability score** to rank micro-markets. State the components, how each is normalised, the weights and the reasoning behind them, and run at least one sensitivity check (change the weights or the threshold; report whether your top three changes). Then, answering as a hypothetical competitor: which single **Vehicle Type + Pickup Geography + Time Window** would you attack first, and what are three pieces of quantitative evidence from the dataset that justify it?

**3.2 (5 marks).** Switch chairs. *"If you had enough resources to fix only ONE Delhi-NCR micro-market tomorrow, which one would you choose, why, and what would you do?"* Answer in this format:

> **Where:** · **When:** · **Product:** · **Problem:** · **Evidence:** (three KPIs) · **Recommended intervention:** · **Success metric and how you would measure it:** · **What remains unknown:**

The intervention must follow from the diagnosed failure mode, and you must explain why the obvious alternatives are worse for this specific cell.

**3.3 (3 marks).** "Drivers are cancelling because Uber pays them too little." Can this be established from the dataset? State what the dataset *can* show about driver cancellation, what it *cannot*, why any pattern you found is consistent with — but does not prove — that explanation, and at least one alternative explanation equally consistent with the data.

**3.4 (3 marks).** List the additional data (fields and sources) required to test that claim properly and why each is needed. Then assume Uber India receives hundreds of millions of marketplace events per month. Explain how the single-file analysis you ran would evolve into a scalable architecture able to ingest those sources, join them to bookings and re-run your Q2 table routinely: where Kafka, distributed storage (HDFS or object storage), partitioning (by what, and why), Hive tables and Spark fit; which flows should be streaming and which batch; and what would break if you kept the flat-file approach.

---

## 7. Submission

- **Report:** maximum 8 pages (A4, 11 pt) plus an appendix with the micro-market tables and validation results.
- **Notebook:** `.ipynb` or Databricks export that runs end to end from the raw file to the Q2 tables. Hard-coded numbers earn no credit for the associated computation.
- **First page must state:** the data is treated as a 2024 baseline; the observation / inference / hypothesis / causal-claim convention is used; the time-bucket scheme and minimum-support threshold adopted.
- **Declaration:** individual work; tools used, including any GenAI assistant.

## 8. How you will be marked

| Question | Marks | CLO split |
|---|---|---|
| Q1 Frame the problem and trust the data | 10 | CLO1 3 · CLO2 7 |
| Q2 Diagnose the marketplace | 10 | CLO2 3 · CLO4 2 · CLO1 5 |
| Q3 Decide, defend and scale | 10 | CLO3 5 · CLO1 2 · CLO4 3 |
| **Total** | **30** | **CLO1 10 · CLO2 10 · CLO3 5 · CLO4 5** |

Each sub-question is marked on three bands — Below Expectation, Meeting Expectation, Exceeding Expectation. The upper band is reached through insight — correct denominators, the right grain, scepticism about labels, honest treatment of what the data cannot show, and recommendations that follow from evidence — not through more charts or more code.

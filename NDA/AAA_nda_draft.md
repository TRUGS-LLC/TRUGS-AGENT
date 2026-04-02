# AAA: Mutual Non-Disclosure Agreement — Washington State

## Phase 1: VISION

I need a mutual NDA for TRUGS LLC. We're entering conversations with potential partners, investors, and contractors who will see proprietary technology (the TRUGS specification, TRL language, patent-pending graph substrate). The NDA must be enforceable in Washington State under RCW 19.108, be mutual (both parties share confidential information), and be written in plain English — no legalese. It should be firm enough to protect IP but not so aggressive that it scares off collaborators.

## Phase 2: FEASIBILITY

<trl>
RECORD nda SHALL COMPLY WITH ENDPOINT RCW_19_108 — Washington Uniform Trade Secrets Act.
RECORD nda SHALL BE RECORD mutual — BOTH PARTY SHALL HAVE EQUAL RECORD obligation.
RECORD nda SHALL USE RECORD plain_english — NO RECORD legalese.
AGENT SHALL REFERENCE RECORD template FROM ENDPOINT bonterms_mutual_nda OR ENDPOINT unda.
</trl>

**Decision:** GO. Washington has adopted the UTSA (RCW 19.108) and the federal DTSA provides additional protection. Mutual NDAs are standard for business discussions. Open-source NDA templates (Bonterms, uNDA) provide solid starting points.

### Risks

<trl>
IF RECORD definition_of_confidential_info IS OVERBROAD THEN RECORD nda MAY BE INVALID.
IF RECORD term EXCEEDS 5 YEARS THEN RECORD nda MAY BE UNENFORCEABLE IN SOME ENDPOINT jurisdiction.
IF RECORD nda SHALL_NOT CONTAIN RECORD exclusions THEN RECORD nda IS INVALID.
RECORD nda SHALL CONTAIN RECORD whistleblower_immunity PURSUANT_TO ENDPOINT DTSA.
</trl>

## Phase 3: SPECIFICATIONS

### Clauses Required

<trl>
RECORD nda SHALL CONTAIN RECORD definition_of_parties.
RECORD nda SHALL CONTAIN RECORD definition_of_confidential_info.
RECORD nda SHALL CONTAIN RECORD exclusions FROM RECORD confidential_info.
RECORD nda SHALL CONTAIN RECORD obligations OF PARTY receiving.
RECORD nda SHALL CONTAIN RECORD permitted_disclosures.
RECORD nda SHALL CONTAIN RECORD term AND RECORD termination.
RECORD nda SHALL CONTAIN RECORD remedies.
RECORD nda SHALL CONTAIN RECORD return_of_materials.
RECORD nda SHALL CONTAIN RECORD governing_law — ENDPOINT Washington_State.
RECORD nda SHALL CONTAIN RECORD whistleblower_notice PURSUANT_TO ENDPOINT DTSA.
RECORD nda MAY CONTAIN RECORD non_solicitation.
RECORD nda SHALL CONTAIN RECORD signature_block.
</trl>

### Key Specifications

<trl>
RECORD definition_of_confidential_info SHALL BE SPECIFIC — NOT "all information".
RECORD definition_of_confidential_info SHALL INCLUDE DATA technical AND DATA business AND DATA financial.
RECORD exclusions SHALL INCLUDE RECORD publicly_known AND RECORD independently_developed AND RECORD prior_possession AND RECORD third_party_disclosure.
RECORD term SHALL BE 2 YEARS FROM RECORD effective_date.
RECORD survival SHALL BE 3 YEARS AFTER RECORD termination FOR RECORD trade_secret.
PARTY receiving SHALL_NOT DISCLOSE RECORD confidential_info TO ANY PARTY EXCEPT RECORD authorized_representative.
PARTY receiving SHALL PROTECT RECORD confidential_info WITH RECORD reasonable_measures.
RECORD governing_law SHALL BE ENDPOINT Washington_State.
RECORD dispute_resolution SHALL BE ENDPOINT King_County_Washington.
</trl>

### Audit Criteria (Phase 8 checks against these)

<trl>
RECORD nda SHALL CONTAIN ALL 12 REQUIRED RECORD clause.
EACH RECORD obligation SHALL USE RECORD modal "SHALL" OR "SHALL_NOT".
RECORD definition_of_confidential_info SHALL BE SPECIFIC AND BOUNDED.
RECORD exclusions SHALL CONTAIN ALL 4 STANDARD RECORD exclusion.
RECORD whistleblower_notice SHALL REFERENCE ENDPOINT DTSA SECTION 1833(b).
RECORD governing_law SHALL REFERENCE ENDPOINT RCW_19_108.
RECORD nda SHALL USE RECORD plain_english — Flesch reading score ABOVE 40.
NO RECORD clause SHALL CONTAIN RECORD unilateral_obligation — ALL RECORD obligation SHALL BE RECORD mutual.
EACH RECORD trl_block SHALL COMPILE — NO RECORD syntax_error.
</trl>

## Phase 4: ARCHITECTURE

### Document Structure

<trl>
RECORD nda SHALL BE ORGANIZED AS RECORD preamble THEN RECORD definitions THEN RECORD obligations THEN RECORD exclusions THEN RECORD permitted_disclosures THEN RECORD term THEN RECORD remedies THEN RECORD general_provisions THEN RECORD signature.
EACH RECORD clause SHALL CONTAIN RECORD trl_block DEFINING RECORD obligation.
RECORD trl_block SHALL PRECEDE RECORD plain_english IN EACH RECORD clause.
</trl>

### Design Decisions

**ADR-NDA-01:** Plain English with TRL specs. Each clause opens with a `<trl>` block that formally specifies the obligation, followed by plain English that says the same thing. The TRL is the contract; the English is the explanation.

**ADR-NDA-02:** 2-year term, 3-year survival for trade secrets. Industry standard for technology discussions. Short enough to not scare collaborators, long enough to protect IP through patent filing.

**ADR-NDA-03:** King County, WA jurisdiction. Home jurisdiction for TRUGS LLC. RCW 19.108 governs trade secret claims.

### Coding Plan

<trl>
AGENT SHALL DRAFT RECORD preamble AND RECORD definitions FIRST.
AGENT SHALL DRAFT RECORD obligations AND RECORD exclusions THEN RECORD permitted_disclosures.
AGENT SHALL DRAFT RECORD term AND RECORD remedies THEN RECORD general_provisions.
AGENT SHALL DRAFT RECORD whistleblower_notice AND RECORD signature_block FINALLY.
AGENT SHALL WRITE RECORD trl_block FOR EACH RECORD clause BEFORE RECORD plain_english.
</trl>

## Phase 5: VALIDATION

**HITM Gate — Human approves before drafting.**

- [x] Vision → specs → architecture consistent
- [x] All 12 required clauses specified
- [x] WA state law (RCW 19.108) referenced
- [x] DTSA whistleblower immunity included
- [x] Mutual obligations confirmed
- [x] Audit criteria defined in Phase 3
- [x] Drafting order defined in Phase 4

**APPROVED — proceed to execution.**

## Phase 6: CODING

Status: COMPLETE — see EXAMPLE_nda_mutual.md

## Phase 7: TESTING

Status: COMPLETE

- All 12 required clauses present
- All obligations use SHALL/SHALL_NOT modals
- All obligations are mutual
- 4 standard exclusions included
- DTSA § 1833(b) whistleblower notice present
- RCW 19.108 referenced in governing law
- Plain English throughout

## Phase 8: AUDIT

Status: COMPLETE

Checking against Phase 3 audit criteria:

- [x] 12 required clauses present
- [x] All obligations use SHALL/SHALL_NOT modals
- [x] Definition of Confidential Information is specific and bounded
- [x] All 4 standard exclusions present
- [x] Whistleblower notice references DTSA § 1833(b)
- [x] Governing law references RCW 19.108
- [x] Plain English — no legalese
- [x] All obligations are mutual
- [x] All TRL blocks compile

## Phase 9: DEPLOYMENT

Status: EXAMPLE — this is a demonstration, not a live deployment.

# Bug Report Examples — Bug Reporter Module

> These reports were generated using the **Bug Reporter** module of the Test Plan Generator.  
> The analyst described each defect in plain language; the AI produced the structured formal report.  
> All client references, endpoint paths, and field names have been anonymized for portfolio purposes.

---

## Index

| # | Title | Type | Severity | Priority |
|---|-------|------|----------|----------|
| BR-001 | Incorrect error message for non-existent Customer ID | Bug | Medium | Medium |
| BR-002 | Missing format and existence validation for relational ID fields | Bug | High | High |
| BR-003 | Missing referential integrity validation between hierarchical entities | Bug | High | High |
| BR-004 | Incorrect error message and validation for oversized numeric value | Bug | High | High |
| BR-005 | Conditional scope validation allows persistence of irrelevant fields | Bug | Medium | Medium |
| BR-006 | PATCH endpoint ignores updates to scope and conditional fields | Bug | Medium | Medium |
| BR-007 | PATCH does not clear non-applicable fields when scope changes | Bug | High | High |
| BR-008 | GET endpoint missing descriptive fields and advanced filter/sort params | Improvement | Medium | Medium |

---

## BR-001 — Incorrect error message for non-existent Customer ID

| Field | Value |
|-------|-------|
| **Type** | Bug |
| **Severity** | Medium |
| **Priority** | Medium |
| **ISO 25010 characteristic** | Functional suitability |
| **Affected endpoint** | `POST /api/v1/maximum-amount` |

**Description**  
When attempting to create a maximum amount record using a Customer ID that does not exist
in the database, the system returns the message *"the entered customer is not active"*
instead of the correct message *"the customer does not exist"*.  
Both validations must be differentiated according to the existence and status of the
customer, as defined in the acceptance criteria.

**Steps to reproduce**
1. Send a `POST` request to `/api/v1/maximum-amount` with a non-existent `CUSTOMER_ID`.
2. Observe the response returned by the system.

**Actual result**  
The system responds with: *"the entered customer is not active"*

**Expected result**  
The system must respond with *"the customer does not exist"* when the `CUSTOMER_ID` is not
present in the database.

**Affected acceptance criterion**  
Validate that `CUSTOMER_ID` exists and is active before saving.

**Additional notes**  
None.

---

## BR-002 — Missing format and existence validation for relational ID fields

| Field | Value |
|-------|-------|
| **Type** | Bug |
| **Severity** | High |
| **Priority** | High |
| **ISO 25010 characteristic** | Functional suitability |
| **Affected endpoints** | `POST /api/v1/maximum-amount`, `PATCH /api/v1/maximum-amount/{id}` |

**Description**  
The fields `fleet`, `work_order`, and `aircraft` — defined as strings — currently accept
any value without UUID format verification or existence validation in their corresponding
database tables. This allows persistence of invalid data and compromises referential
integrity.

**Steps to reproduce**
1. Send a `POST` or `PATCH` request using non-UUID, non-existent, or random values for
   `fleet`, `work_order`, and/or `aircraft`.
2. Verify that the API accepts and persists those values.

**Actual result**  
The system accepts any string value — including invalid or non-existent ones — and stores
them without validation.

**Expected result**  
The system must validate that values are valid UUIDs and correspond to existing records
in the relevant tables before accepting the request.

**Affected acceptance criterion**  
Conditional validation by scope, and referential consistency with existing records.

**Additional notes**  
Existence validation must occur before saving to prevent data inconsistencies.

---

## BR-003 — Missing referential integrity validation between hierarchical entities

| Field | Value |
|-------|-------|
| **Type** | Bug |
| **Severity** | High |
| **Priority** | High |
| **ISO 25010 characteristic** | Functional suitability |
| **Affected endpoints** | `POST /api/v1/maximum-amount`, `PATCH /api/v1/maximum-amount/{id}` |

**Description**  
The backend does not validate that the associations between Aircraft, Work Order, and
Customer are coherent: Aircraft must belong to the Customer, and Work Order must be
associated with the corresponding Aircraft, as defined in the acceptance criteria for
`SCOPE='WO'`. Cross-entity data belonging to different customers can currently be inserted,
compromising referential integrity.

**Steps to reproduce**
1. Send a create or update request with an `AIRCRAFT_ID` belonging to one `CUSTOMER_ID`,
   but associate a `WORK_ORDER` linked to an Aircraft from a different customer.
2. Observe that the system accepts the operation without error.

**Actual result**  
Cross-referenced records can be inserted and persisted without validating the hierarchical
relationship between customer, aircraft, and work order.

**Expected result**  
On create or update, the system must validate that the linked aircraft belongs to the
customer, and that the work order belongs to that aircraft.

**Affected acceptance criterion**  
Conditional validation by scope and uniqueness of validity period, verifying consistency
across entity IDs.

**Additional notes**  
This generates risks of functional errors and inconsistent reports for end users.

---

## BR-004 — Incorrect error message and validation for oversized numeric amount

| Field | Value |
|-------|-------|
| **Type** | Bug |
| **Severity** | High |
| **Priority** | High |
| **ISO 25010 characteristic** | Functional suitability |
| **Affected endpoints** | `POST`, `PUT`, `PATCH /api/v1/maximum-amount` |

**Description**  
When registering a record with a `MAXIMUM_AMOUNT` value exceeding 16 integer digits
(e.g., `12345678912345678.72`), the system incorrectly returns a validation error about
decimal places (*"maximum_amount must have at most 2 decimals"*), even though the value
has exactly 2 decimal places. The actual error is caused by exceeding the allowed digit
count, but the validation message does not reflect this, which may confuse the user.

**Steps to reproduce**
1. Send a `POST`/`PUT`/`PATCH` request with `MAXIMUM_AMOUNT = 12345678912345678.72`.
2. Observe the validation message returned.

**Actual result**  
System returns: *"maximum_amount must have at most 2 decimals"*, even though the value
has exactly 2 decimal places.

**Expected result**  
The system should accept any amount greater than zero with a maximum of 2 decimal places,
without an upper limit, per the defined acceptance criterion. If a database-level digit
limit exists (`DECIMAL(16,2)`), the error message must be accurate and specific —
e.g., *"Maximum amount must have up to 16 integer digits and 2 decimal places"*.

**Affected acceptance criterion**  
`MAXIMUM_AMOUNT` must be greater than 0, with a maximum of 2 decimal places. No upper
limit is defined in the acceptance criteria.

**Additional notes**  
Since a database constraint exists (`DECIMAL(16,2)`), the validation message must be
corrected and properly communicated to the user.

---

## BR-005 — Conditional scope validation allows persistence of irrelevant fields

| Field | Value |
|-------|-------|
| **Type** | Bug |
| **Severity** | Medium |
| **Priority** | Medium |
| **ISO 25010 characteristic** | Functional suitability |
| **Affected endpoints** | `POST /api/v1/maximum-amount`, `PATCH /api/v1/maximum-amount/{id}` |

**Description**  
The system allows receiving, recording, and persisting fields that do not correspond to
the selected `SCOPE`. For example, sending `fleet` when `SCOPE='WO'` is accepted without
error. This contradicts the required conditional validation and may cause data
inconsistencies, complicating record maintenance and downstream data filtering.

**Steps to reproduce**
1. Send a `POST` request with `SCOPE='WO'` and include the `fleet` field in the payload.
2. Verify that the record is created and persisted including the non-applicable field.

**Actual result**  
The system accepts and stores additional fields not required by the selected scope.

**Expected result**  
The system must reject fields that do not correspond to the selected scope and inform
the user accordingly.

**Affected acceptance criterion**  
Conditional validation by scope.

**Additional notes**  
Review serialization/deserialization logic and DTO implementation to explicitly condition
allowed fields per scope.

---

## BR-006 — PATCH endpoint ignores updates to scope and conditional fields

| Field | Value |
|-------|-------|
| **Type** | Bug |
| **Severity** | Medium |
| **Priority** | Medium |
| **ISO 25010 characteristic** | Functional suitability |
| **Affected endpoint** | `PATCH /api/v1/maximum-amount/{id}` |

**Description**  
The `PATCH` endpoint does not update the values of the fields `scope`, `ipc`, and `cap`
on an existing record. When attempting to update these fields, the system ignores the new
value and retains the original, making it impossible to modify the scope of an existing
record or validate uniqueness of validity period across different scopes via `PATCH`.

**Steps to reproduce**
1. Create a record (`POST`) with a specific `scope` value.
2. Send a `PATCH` request modifying the `scope` field to a different value.
3. Retrieve the record (`GET`) and verify the `scope` value.

**Actual result**  
The `scope` field is not modified; the original value remains unchanged. Fields `ipc` and
`cap` are also not updated when changed from `"Y"` to `null`.

**Expected result**  
The `scope` field must be updated if provided in the request, respecting all corresponding
validations.

**Affected acceptance criterion**  
Uniqueness of validity period. The existence of an active record for a given customer and
scope must also be validatable via `PATCH`.

**Additional notes**  
None.

---

## BR-007 — PATCH does not clear non-applicable fields when scope changes

| Field | Value |
|-------|-------|
| **Type** | Bug |
| **Severity** | High |
| **Priority** | High |
| **ISO 25010 characteristic** | Functional suitability |
| **Affected endpoint** | `PATCH /api/v1/maximum-amount/{id}` |

**Description**  
When updating a record via `PATCH` and modifying the `scope` value, fields associated
with the previous scope retain their prior values even though they no longer apply under
the new scope's conditional validation rules.  

**Example:** A record with `scope="F"` (requiring `fleet`) is updated to `scope="WO"`
(requiring `work_order` and `aircraft`). After the update, the `fleet` field retains its
previous value, creating residual data that may cause downstream inconsistencies and
incorrect validations.

**Steps to reproduce**
1. Create a record with `scope="F"` and populate the `fleet` field.
2. Send a `PATCH` request changing `scope` to `"WO"` and providing values for
   `work_order` and `aircraft`.
3. Retrieve the updated resource via `GET`.

**Actual result**  
The `fleet` field retains its previously assigned value even though the new scope `"WO"`
does not require it. This residual value remains stored in the database.

**Expected result**  
Fields that do not correspond to the new `scope` value (e.g., `fleet` in this example)
must be automatically set to `null` during the update, ensuring data integrity aligned
with business validation rules.

**Affected acceptance criterion**  
Conditional validation by scope — residual data remains in fields not required by the
selected scope.

**Additional notes**  
This behavior may cause uniqueness of validity period issues and incorrect validations
in subsequent operations.

---

## BR-008 — GET endpoint missing descriptive fields and advanced filter/sort parameters

| Field | Value |
|-------|-------|
| **Type** | Improvement |
| **Severity** | Medium |
| **Priority** | Medium |
| **ISO 25010 characteristic** | Functional suitability |
| **Affected endpoint** | `GET /api/v1/maximum-amount` |

**Description**  
The `GET /api/v1/maximum-amount` endpoint currently does not return the following
descriptive fields in its payload:  
`work_order.description`, `aircraft.registration`, `aircraft.type`,
`fleet.description`, `start_date`.

This limits the frontend's ability to render the required data table. Additionally,
the available query parameters do not include: `customer_code`, `customer_name`,
`maximum_amount`, `work_order_description`, `aircraft_registration`, `aircraft_type`,
`fleet_description`, or `start_date` — preventing users from performing advanced
filtering and sorting from the interface.

**Steps to reproduce**
1. Send a `GET` request to `/api/v1/maximum-amount`.
2. Observe the fields returned in the response payload.
3. Attempt to filter by `customer_name`, `aircraft_registration`, or `fleet_description`.

**Actual result**  
The endpoint does not return the listed descriptive fields, and the listed filter/sort
parameters are not available.

**Expected result**  
The endpoint must:
- Return all listed descriptive fields in its payload.
- Accept the following as query parameters for filtering and sorting:
  `customer_code`, `customer_name`, `maximum_amount`, `work_order_description`,
  `aircraft_registration`, `aircraft_type`, `fleet_description`, `start_date`.
- Support sort functionality for all listed parameters.

**Affected acceptance criterion**  
Data management and visualization requirements for the frontend grid.

**Additional notes**  
`customer_name` must also be added as a searchable/filterable parameter.

---

## About this document

These reports were produced using the **Bug Reporter** module of the
[Test Plan Generator](https://github.com/Yisus-Ga/test-plan-generator).

**Workflow:**  
1. QA analyst describes the defect in plain language during exploratory or scripted testing.  
2. The Bug Reporter processes the description using an ISO 25010 / ISTQB-aligned prompt.  
3. The AI generates the structured formal report with all required fields populated.  
4. The QA engineer reviews, validates, and submits to the defect tracking system (Jira).

**Standards applied:**  
- ISO/IEC 25010 — Software product quality characteristics  
- ISTQB — Defect report structure and severity/priority classification  

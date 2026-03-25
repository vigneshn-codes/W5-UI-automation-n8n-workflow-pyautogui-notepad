# 🔁 n8n UI automation RPA Mastery Guide

> A comprehensive reference for mastering n8n's core nodes — Set Node, File Operations, Conditional Logic, and JSON fundamentals.

---

## 📋 Table of Contents

- [1. Mastering the Set Node](#1-mastering-the-set-node)
- [2. File Operation Nodes](#2-file-operation-nodes)
- [3. Mastering Conditional Logic Nodes](#3-mastering-conditional-logic-nodes)
- [4. What is JSON?](#4-what-is-json)

---

## 1. Mastering the Set Node

The **Set Node** is one of the most fundamental nodes in n8n. It allows you to define, assign, or transform data as it flows through your workflow.

### 1.1 Assign Manual Value / Create a Static Value

Use the Set Node to hardcode a value into your workflow data — useful for adding constants, labels, flags, or default values.

**Example use cases:**
- Setting a `status` field to `"active"` for all items
- Injecting a timestamp or environment label
- Resetting a field to a known default before passing to the next node

```json
// Output example
{
  "status": "active",
  "source": "n8n-workflow",
  "retryCount": 0
}
```

---

### 1.2 Use Multiple Data Types

The Set Node supports a rich set of data types to match your workflow needs:

| Data Type | Description | Example Value |
|-----------|-------------|---------------|
| `String`  | Plain text  | `"Hello World"` |
| `Integer` | Whole numbers | `42` |
| `Boolean` | True/false flag | `true` |
| `Array`   | Ordered list of values | `["a", "b", "c"]` |
| `Object`  | Key-value pairs (JSON) | `{ "key": "value" }` |

> 💡 **Tip:** Always match the data type to what the downstream node expects. Mismatched types can cause silent failures or unexpected behavior.

---

### 1.3 Use "Ignore Type Conversion Errors"

When working with strict data pipelines, enable **Ignore Type Conversion Errors** to prevent the workflow from stopping when it encounters an incompatible type.

- **When enabled:** The node will skip conversion errors and pass through the original value as-is.
- **When disabled (default):** Any type mismatch throws an error and halts the node.

**Best practice:** Enable this only when you're confident the downstream nodes can handle mixed types, or when you're doing exploratory development.

---

### 1.4 Settings

#### 1.4.1 Always Output Data

> **Toggle:** `Always Output Data` → ON/OFF

When enabled, the Set Node will **pass the input data through as output** even if an error occurs internally. This prevents silent workflow stalls.

- ✅ Use when you want the flow to continue regardless of node-level issues.
- ❌ Avoid when data integrity is critical and errors must surface.

---

#### 1.4.2 On Error → Continue

> **Setting:** `On Error` → `Continue`

When an error occurs, the workflow **continues execution** without throwing a hard stop. The errored item is skipped or passed forward depending on configuration.

```
[Set Node Error] → ⚠️ Logged → [Next Node] ✅ Continues
```

---

#### 1.4.3 On Error → Stop Workflow

> **Setting:** `On Error` → `Stop Workflow`

When an error occurs, the **entire workflow halts immediately**. Use this when downstream nodes depend on the Set Node's output and invalid data would cause cascading failures.

```
[Set Node Error] → 🛑 Workflow Stopped
```

---

## 2. File Operation Nodes

n8n provides a powerful suite of file operation nodes for reading, writing, converting, and extracting data from various file formats.

---

### 2.1 Binary Data (010101)

Binary data in n8n represents raw file content — images, PDFs, audio, video, or any non-text format. Binary items are stored in a special `binary` property on each item.

```json
{
  "binary": {
    "data": {
      "mimeType": "image/png",
      "fileName": "screenshot.png",
      "data": "base64encodedstring..."
    }
  }
}
```

> 💡 Most file nodes produce or consume binary data. Always inspect the binary key when debugging file-related nodes.

---

### 2.2 CSV / XLSX File

Read from or write to spreadsheet files.

**Read:** Parses rows into individual n8n items — each row becomes one item.

**Write:** Takes n8n items and outputs them as a structured spreadsheet file.

**Common parameters:**
- `File Path` — local path or binary input
- `Sheet Name` — for XLSX files with multiple sheets
- `Header Row` — whether the first row is a header

---

### 2.3 JSON File

Read from or write structured JSON to/from the filesystem.

**Read:** Parses a `.json` file and maps it into n8n items.

**Write:** Takes current item data and serializes it to a `.json` file.

> ⚠️ When reading JSON arrays, each element becomes a separate n8n item automatically.

---

### 2.4 Text File (Read / Write)

Handles plain `.txt` files.

- **Read:** Loads file contents as a string into item data.
- **Write:** Writes a string expression or field value to a text file.

Useful for log writing, config reading, or raw data ingestion.

---

### 2.5 Convert to File

Converts your n8n workflow data into a downloadable file format.

#### 2.5.1 Supported Output Formats

| Format | Description |
|--------|-------------|
| `CSV`  | Comma-separated values |
| `HTML` | Web page markup |
| `ICS`  | Calendar event format |
| `JSON` | Structured data |
| `ODS`  | OpenDocument Spreadsheet |
| `RTF`  | Rich Text Format |
| `Text File` | Plain `.txt` |
| `XLS`  | Legacy Excel format |
| `XLSX` | Modern Excel format |
| `Base64 String → File` | Decode base64 data to raw file |

#### 2.5.2 Data Flow

```
[Previous Node Output] → [Convert to File Node] → 📄 File Binary Output
```

The node reads the structured data from the previous node's output and serializes it into the selected file format.

---

### 2.6 Extract from File

Extracts structured data from a binary file input and makes it available as n8n items.

#### 2.6.1 Supported Input Formats

| Format | Notes |
|--------|-------|
| `CSV`  | Each row becomes an item |
| `HTML` | Parses DOM structure |
| `ICS`  | Extracts calendar events |
| `JSON` | Maps JSON to items |
| `ODS`  | OpenDocument Spreadsheet |
| `RTF`  | Rich Text Format |
| `PDF`  | Extracts text content |
| `Text File` | Raw string content |
| `XML`  | Parses XML structure |
| `XLS`  | Legacy Excel |
| `XLSX` | Modern Excel |
| `Base64 String` | Converts base64 to usable data |

> 💡 **Pro Tip:** Chain `Extract from File` → `Set Node` → `Convert to File` to build powerful file transformation pipelines.

---

## 3. Mastering Conditional Logic Nodes

Conditional nodes allow your workflow to make decisions and route data along different paths based on criteria you define.

---

### 3.1 If Node (True / False)

The **If Node** evaluates a single condition and routes items down one of two branches:

- ✅ **TRUE branch** — condition is met
- ❌ **FALSE branch** — condition is not met

**Supported condition types:**
- String: equals, contains, starts with, ends with, regex
- Number: equal, greater than, less than, between
- Boolean: is true, is false
- DateTime: before, after, between
- Array: contains, empty

**Visual flow:**

```
                    ┌──────────────┐
                    │   If Node    │
                    │  age > 18?   │
                    └──────┬───────┘
                           │
              ┌────────────┴────────────┐
              ▼                         ▼
        ✅ TRUE                    ❌ FALSE
    [Adult Workflow]           [Minor Workflow]
```

> 💡 Use multiple If Nodes in sequence for complex multi-condition logic.

---

### 3.2 Switch Node

The **Switch Node** evaluates a value against **multiple conditions** and routes items to the matching output. Think of it as a multi-branch `if/else if/else` structure.

**Key features:**
- Supports up to N output branches
- Each branch has its own condition
- A **Fallback** (default) output can catch unmatched cases
- Works with strings, numbers, and expressions

**Visual flow:**

```
                    ┌──────────────┐
                    │ Switch Node  │
                    │  status = ?  │
                    └──────┬───────┘
                           │
         ┌─────────────────┼──────────────────┐
         ▼                 ▼                  ▼
    "pending"          "approved"         "rejected"
  [Notify Team]     [Trigger Action]   [Send Rejection]
```

> 💡 **Switch vs If:** Use **If** for binary true/false decisions. Use **Switch** when you have 3 or more distinct routing paths based on a single value.

---

## 4. What is JSON?

**JSON** (JavaScript Object Notation) is the primary data format used throughout n8n. Every item that flows through your workflow is a JSON object.

---

### 4.1 JSON Structure — Simple vs Nested

JSON consists of **key-value pairs** organized into objects and arrays.

#### Simple Object

```json
{
  "name": "Alice",
  "age": 30,
  "active": true
}
```

#### Array of Simple Objects

```json
[
  { "id": 1, "name": "Alice" },
  { "id": 2, "name": "Bob" },
  { "id": 3, "name": "Charlie" }
]
```

> In n8n, each element in a top-level array becomes a **separate item**.

#### Nested Object

```json
{
  "user": {
    "name": "Alice",
    "address": {
      "city": "Chennai",
      "country": "India"
    }
  },
  "orders": [
    { "id": "ORD001", "total": 1500 },
    { "id": "ORD002", "total": 3200 }
  ]
}
```

#### Accessing Nested Values in n8n Expressions

```
{{ $json.user.name }}              → "Alice"
{{ $json.user.address.city }}      → "Chennai"
{{ $json.orders[0].id }}           → "ORD001"
{{ $json.orders.length }}          → 2
```

---

### JSON Quick Reference

| Syntax | Type | Example |
|--------|------|---------|
| `"text"` | String | `"Hello"` |
| `123` | Integer | `42` |
| `12.5` | Float | `3.14` |
| `true / false` | Boolean | `true` |
| `null` | Null | `null` |
| `{ }` | Object | `{ "key": "value" }` |
| `[ ]` | Array | `[1, 2, 3]` |

---

## 🗺️ Learning Path

```
Start Here
    │
    ▼
📦 Set Node ──────────────────────► Assign / Transform Data
    │
    ▼
📄 File Operations ───────────────► Read / Write / Convert / Extract
    │
    ▼
🔀 Conditional Logic ─────────────► If → TRUE/FALSE | Switch → Multi-route
    │
    ▼
🧩 JSON Mastery ──────────────────► Simple → Nested → n8n Expressions
    │
    ▼
🚀 Build Production Workflows!
```

---

## 🛠️ Tech Stack

- **Platform:** [n8n](https://n8n.io) — Open-source workflow automation
- **Docs:** https://docs.n8n.io
- **Node Reference:** https://docs.n8n.io/integrations/builtin/core-nodes/

---

## 📝 Notes

- All examples use n8n expression syntax: `{{ $json.fieldName }}`
- Binary data is handled separately from JSON data in each item
- Always test conditional branches with both true and false cases
- Use the **Set Node** liberally — it's the Swiss Army knife of n8n

---

## ✍️ Author

*Happy automating! 🤖*

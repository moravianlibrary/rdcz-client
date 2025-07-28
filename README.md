# Registr Digitalizace CZ Client

A Python client library for querying the [Registr digitalizace](https://registrdigitalizace.cz/rdcz/) (RDcz) Solr endpoint. This tool provides a typed interface to RDcz data, including documents and issue metadata, and simplifies querying and filtering using composable search expressions.

---

## Features

* Fully typed RDcz document model with Pydantic
* Composable query API based on Solr query syntax
* Query issues or records using RDcz-specific fields and states
* Automatic population of related record states
* Enum-based field/value definitions with alias support
* Integrated with the `solrify` query and client engine

---


## Installation

### Installing from GitHub using version tag

You can install **rdcz** directly from GitHub for a specific version tag:

```bash
pip install git+https://github.com/moravianlibrary/rdcz-client.git@v1.2.3
```

*Replace `v1.2.3` with the desired version tag.*

To always install the most recent version, use the latest tag:

```bash
pip install git+https://github.com/moravianlibrary/rdcz-client.git@latest
```

### Installing local dev environment

Install required dependencies using `pip`:

```bash
pip install -r requirements.txt
```

---

## Usage

### Basic search

```python
from rdcz import RDczClient, RDczField, RDczState
from solrify import SolrConfig, F

config = SolrConfig(base_url="https://registrdigitalizace.cz/rdcz/search/rdcz/select")
client = RDczClient(config)

# Search for finished issues for a specific record
query = F(RDczField.RecordId, "12345") & F(RDczField.State, RDczState.Finished)

for doc in client.search(query):
    print(doc.issue_id, doc.title)
```

### Get a specific issue

```python
issue = client.get_issue("123")
print(issue.title, issue.state)
```

### Get all issues for a record (title)

```python
issues = client.get_all_issues("12345")
for issue in issues:
    print(issue.volume_year, issue.state)
```

---

## Data Model

### `RDczDocument`

Represents a single document (issue) from RDcz with fields like:

* `issue_id`, `record_id`
* `barcode`, `control_number`, `nbn`, `signature`
* `title`, `volume_year`, `volume_number`, `bundle`
* `state` — current Solr state
* `record_state` — all known states for the record

### `RDczField`

Enum-based access to field names like `RDczField.Title`, `RDczField.State`, etc.

### `RDczState`

Enum for standardized digitization states:

* `Finished`
* `InProgress`
* `Planned`
* `Revision`

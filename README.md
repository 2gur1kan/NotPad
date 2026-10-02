# NotPad

**NotPad** is a lightweight desktop information management application developed with Python and PyQt5. The application provides a structured environment for storing, organizing, retrieving, and modifying personal information through a local SQLite database.

The primary design objective of NotPad is to provide a simple and efficient interface for managing frequently accessed information without requiring an external server, cloud service, or network connection.

## Overview

NotPad implements a local record-management architecture in which each record consists of a title, an information field, optional notes, and one or more user-defined tags.

The application is particularly suitable for managing small collections of structured information that need to be retrieved quickly through keyword-based search and categorical filtering.

All persistent data is stored locally using SQLite, allowing the application to operate independently of external databases or network services.

## Features

### Record Management

NotPad provides the following operations for stored records:

* Create new records
* Edit existing records
* Delete records
* View complete record details
* Store additional free-form notes
* Validate required fields before saving
* Display records in a structured table

Each record contains:

* **Title** — identifies the stored item.
* **Information** — stores the primary value associated with the record.
* **Notes** — provides optional additional information.
* **Tags** — enables categorical organization and filtering.

### Search and Filtering

The application provides real-time record retrieval based on the title field.

Users can:

* Search records using keywords.
* Filter records by tags.
* Combine textual search with tag-based filtering.
* Automatically refresh the displayed record list after modifications.

The search mechanism is implemented at the database layer using parameterized SQL queries and `LIKE` expressions.

### Tag-Based Organization

NotPad implements a many-to-many relationship between records and tags.

Users can:

* Create custom tags.
* Assign multiple tags to a record.
* Filter records according to a selected tag.
* Remove tags when they are no longer required.
* Modify tag associations while editing a record.

This structure allows the same record to belong to multiple logical categories without duplicating data.

### Information Visibility Control

Information fields containing potentially sensitive values are displayed using password-style masking by default.

The interface provides a visibility toggle that allows the user to temporarily reveal the stored value when required.

This functionality is implemented at the user-interface level using PyQt5's password echo mode.

> **Security Note:** NotPad currently stores information locally in SQLite without application-level encryption. Password masking should therefore be considered a user-interface privacy feature rather than a cryptographic security mechanism.

### Record Editing

Selecting the **Open** action displays a dedicated record-detail dialog.

The dialog provides access to:

* Complete record information
* Additional notes
* Assigned tags
* Editable title and information fields
* Save and close operations

Changes are validated before being committed to the database.

## System Architecture

NotPad follows a modular desktop application structure that separates the graphical interface from the persistence layer.

```text
+--------------------------------------------------+
|                    NotPad                        |
+--------------------------------------------------+
|                                                  |
|                Presentation Layer                |
|                                                  |
|  +-------------------+   +-------------------+   |
|  |    MainWindow     |   | RecordDetailDialog|   |
|  |                   |   |                   |   |
|  | Record Listing    |   | Record Editing    |   |
|  | Search            |   | Tag Management    |   |
|  | Filtering         |   | Data Validation   |   |
|  +---------+---------+   +---------+---------+   |
|            |                       |             |
+------------+-----------------------+-------------+
             |
             v
+--------------------------------------------------+
|              Data Access Layer                   |
|                                                  |
|                 database.py                      |
|                                                  |
|  - Database initialization                       |
|  - Record CRUD operations                        |
|  - Tag management                                |
|  - Search and filtering                          |
|  - Relationship management                       |
+-------------------------+------------------------+
                          |
                          v
+--------------------------------------------------+
|                  SQLite Database                 |
|                                                  |
|  kayitlar                                        |
|  etiketler                                       |
|  kayit_etiket                                    |
+--------------------------------------------------+
```

The separation between the presentation and data-access layers reduces coupling between the graphical interface and persistence mechanisms. Database operations are encapsulated within `database.py`, while the user interface is primarily implemented in `main_window.py` and `record_detail_dialog.py`.

## Database Design

The application uses SQLite as its persistent storage mechanism.

The database consists of three primary tables.

### `kayitlar`

Stores the main application records.

| Field    | Type    | Description               |
| -------- | ------- | ------------------------- |
| `id`     | INTEGER | Primary key               |
| `baslik` | TEXT    | Record title              |
| `bilgi`  | TEXT    | Primary information       |
| `notlar` | TEXT    | Optional additional notes |

### `etiketler`

Stores unique user-defined tags.

| Field | Type    | Description     |
| ----- | ------- | --------------- |
| `id`  | INTEGER | Primary key     |
| `ad`  | TEXT    | Unique tag name |

### `kayit_etiket`

Represents the many-to-many relationship between records and tags.

| Field       | Type    | Description                         |
| ----------- | ------- | ----------------------------------- |
| `kayit_id`  | INTEGER | Foreign key referencing `kayitlar`  |
| `etiket_id` | INTEGER | Foreign key referencing `etiketler` |

The relationship table uses a composite primary key consisting of `kayit_id` and `etiket_id`, preventing duplicate record-tag associations.

Foreign-key constraints with cascading deletion are also enabled to maintain referential integrity.

## Project Structure

```text
NotPad/
│
├── main.py
├── main_window.py
├── record_detail_dialog.py
├── database.py
├── flow_layout.py
├── styles.py
├── requirements.txt
├── notlar.db
│
└── .idea/
```

### `main.py`

Acts as the application entry point.

It is responsible for:

* Initializing the database.
* Configuring Qt high-DPI support.
* Configuring the Qt platform plugin path when necessary.
* Creating the `QApplication` instance.
* Applying the global stylesheet.
* Initializing and displaying the main window.

### `main_window.py`

Implements the primary application interface.

Its responsibilities include:

* Creating the main window.
* Managing record creation.
* Displaying stored records.
* Implementing search functionality.
* Implementing tag filtering.
* Managing tags.
* Opening record-detail dialogs.
* Deleting records.
* Updating the interface after database operations.

### `record_detail_dialog.py`

Implements the detailed record-management interface.

It provides functionality for:

* Loading an existing record.
* Editing record fields.
* Managing tag assignments.
* Displaying complete notes.
* Saving modifications.

### `database.py`

Implements the application's SQLite persistence layer.

It provides functions for:

* Database initialization.
* Establishing SQLite connections.
* Creating database tables.
* Creating, reading, updating, and deleting records.
* Creating and deleting tags.
* Retrieving records and tags.
* Managing record-tag relationships.
* Searching and filtering records.

Parameterized SQL statements are used for database modifications and search parameters, reducing the risk of SQL injection caused by direct string interpolation.

## Technology Stack

| Technology  | Purpose                  |
| ----------- | ------------------------ |
| Python      | Application development  |
| PyQt5       | Graphical user interface |
| SQLite      | Local persistent storage |
| PyInstaller | Application packaging    |

The project currently specifies:

* **PyQt5 5.15.9**
* **PyInstaller 5.13.2**

## Installation

### Requirements

Python 3.x is required to run the application.

Install the project dependencies using:

```bash
pip install -r requirements.txt
```

### Running the Application

After installing the dependencies, execute:

```bash
python main.py
```

The application initializes the SQLite database automatically when it starts.

## Data Persistence

NotPad uses a local SQLite database named:

```text
notlar.db
```

The database is located in the project directory and is initialized automatically if the required tables do not already exist.

The application also contains database initialization logic capable of migrating records from an earlier database schema into the current record structure.

This approach allows the application to evolve its internal data model while preserving previously stored information.

## Design Considerations

The application was designed around several principles:

### Local-First Architecture

All application data is stored locally. No external API or remote database is required.

This provides:

* Offline operation
* Low infrastructure requirements
* Fast local data access
* Independence from network availability

### Modular Responsibility

The graphical interface and database operations are separated into dedicated modules.

This makes the codebase easier to maintain and provides a foundation for future architectural improvements.

### Referential Integrity

The database uses primary keys, foreign keys, unique constraints, and cascading deletion to maintain consistency between records and their associated tags.

### Usability

The interface emphasizes direct interaction and minimal navigation. Frequently used operations such as searching, filtering, creating records, and deleting records are available from the main window.

## Limitations

The current implementation is intentionally lightweight and has several limitations:

* Data is stored locally without encryption.
* There is no authentication mechanism.
* There is no cloud synchronization.
* There is no multi-user or concurrent database architecture.
* Search is primarily based on the record title.
* There is currently no automated testing framework included in the repository.

These limitations define potential directions for future development.

## Future Improvements

Potential extensions to the project include:

1. **Database Encryption**
   Introduce encrypted local storage for sensitive information.

2. **Advanced Search**
   Support searching across titles, information, notes, and tags.

3. **Backup and Restore**
   Provide mechanisms for exporting and importing application data.

4. **Cross-Platform Packaging**
   Provide distributable builds for Windows, Linux, and macOS.

5. **Automated Testing**
   Introduce unit and integration tests for database and interface functionality.

6. **Improved Security Architecture**
   Introduce secure credential handling and stronger protection for sensitive records.

7. **Data Synchronization**
   Provide an optional synchronization mechanism while preserving the application's local-first design.

## Development Objective

NotPad was developed as a compact desktop software project demonstrating the integration of graphical user interfaces, relational data modeling, local persistence, and interactive information retrieval.

From a software engineering perspective, the project demonstrates practical implementation of:

* Desktop GUI development
* Event-driven programming
* Relational database design
* CRUD operations
* Many-to-many relationships
* Data validation
* Search and filtering
* Modular software organization
* Local data persistence
* Application packaging

The project therefore serves both as a functional desktop utility and as an example of integrating a Python-based graphical interface with a relational persistence layer.

## License

This project is currently provided without an explicitly specified open-source license.

If the project is intended for public distribution or collaboration, an appropriate license should be added to the repository.

## Repository

The complete source code is available on GitHub:

[NotPad — GitHub Repository](https://github.com/2gur1kan/NotPad?utm_source=chatgpt.com)

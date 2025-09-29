<a name="readme-top"></a>

<div align="center">
  <img src="https://cdn.prod.website-files.com/66a1237564b8afdc9767dd3d/66df7b326efdddf8c1af9dbb_Momentum%20Logo.svg" height="80">
  <h1>FHIR MCP Server</h1>
  <p><strong>Model Context Protocol (MCP) Server for Fast Healthcare Interoperability Resources (FHIR)</strong></p>

  [![Contact us](https://img.shields.io/badge/Contact%20us-AFF476.svg?style=for-the-badge&logo=mail&logoColor=black)](mailto:hello@themomentum.ai?subject=FHIR%20MCP%20Server%20Inquiry)
  [![Visit Momentum](https://img.shields.io/badge/Visit%20Momentum-1f6ff9.svg?style=for-the-badge&logo=safari&logoColor=white)](https://themomentum.ai)
  [![MIT License](https://img.shields.io/badge/License-MIT-636f5a.svg?style=for-the-badge&logo=opensourceinitiative&logoColor=white)](LICENSE)
</div>

## 📋 Table of Contents

- [🔍 About](#-about-the-project)
- [💡 Demo](#-demo)
- [🚀 Getting Started](#-getting-started)
- [📝 Usage](#-usage)
- [🔧 Configuration](#-configuration)
- [🐳 Docker Setup](#-docker-setup)
- [🛠️ MCP Tools](#️-mcp-tools)
- [🗺️ Roadmap](#️-roadmap)
- [👥 Contributors](#-contributors)
- [📄 License](#-license)

## 🔍 About The Project

**FHIR MCP Server** implements a complete Model Context Protocol (MCP) server, designed to facilitate seamless interaction between LLM-based agents and a FHIR-compliant backend. It provides a standardized interface that enables full CRUD operations on FHIR resources through a comprehensive suite of tools - accessible from MCP-compatible clients such as Claude Desktop, allowing users to query and manipulate clinical data using natural-language prompts.

### ✨ Key Features

- **🚀 FastMCP Framework**: Built on FastMCP for high-performance MCP server capabilities
- **🏥 FHIR Resource Management**: Full CRUD operations for all major FHIR resources
- **📄 Intelligent Document Processing**: AI-powered document ingestion and chunking for multiple formats including TXT, CSV, JSON, and PDF
- **🔍 Semantic Search**: Advanced document search using vector embeddings (via Pinecone)
- **🧠 RAG-Ready**: Retrieval-Augmented Generation pipeline with context-aware document queries
- **🔐 Secure Authentication**: OAuth2 token management for FHIR API integration
- **📊 LOINC Integration**: Standardized medical terminology lookup and validation
- **🐳 Container Ready**: Docker support for easy deployment and scaling
- **🔧 Configurable**: Extensive ```.env```-based configuration options

### 🏗️ Architecture

The server is built with a modular architecture:

- **MCP Tools**: Dedicated tools for selected FHIR resource types, with others handled by a generic tool
- **Fhir Server Client**: Handles FHIR API communication and authentication (OAuth2 and more planned)
- **RAG Services**: Embedding-based document processing and semantic retrieval
- **Vector Store**: Pinecone integration for similarity-based search
- **LOINC Client**: Integration with LOINC API for terminology resolution and validation

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## 💡 Demo

This demo shows how Claude uses the `fhir-mcp-server` to communicate with a FHIR server (in this case Medplum) to answer questions. You will see, among other things:

- utilization of the `request_patient_resource` tool which retrieves basic patient information
- utilization of the `request_condition_resource` tool to answer the question whether any of the previously diagnosed diseases may cause symptoms that the patient is currently complaining about
- utilization of the `request_medication_resource`, `request_encounter_resource`, `request_generic_resource` tools to answer the question whether the patient has already received any treatment for hypertension

You can observe how Claude automatically selects the tools worth using to answer the question based on the user's query.

https://github.com/user-attachments/assets/3a3a8ed3-f881-447d-af03-5f24432a2cdd

<details>
<summary>Lab History Analysis</summary>

Here you can observe how Claude first uses the tool searching for LOINC codes for the lipid panel specific codes, but not finding any related observations in FHIR server, it repeats the search for individual biomarkers that make up such a panel.

https://github.com/user-attachments/assets/2fb39801-d5d6-4461-bedd-9f58ab4d52ec

</details>

<details>
<summary>FHIR Synthetic Data Generator</summary>

Developers working with FHIR often need to generate specific test data to validate FHIR server functionality, such as search capabilities and data relationships. While you can use Synthea to generate synthetic data and then manually import the resulting bundles to your server, fhir-mcp-server streamlines this process by allowing you to generate and deploy test data directly through Claude.

This eliminates the typical workflow of running [synthea](https://github.com/synthetichealth/synthea) separately, downloading bundles, and manually importing them to your FHIR server. Instead, you can create targeted test scenarios, generate appropriate synthetic data, and populate your server all within Claude's interface.

https://github.com/user-attachments/assets/d87da1d8-6401-4a9e-a6f0-50ba23396e12

**Note:** fhir-mcp-server was not designed with this use case in mind, so as you'll see in the demo, it doesn't work perfectly - what can be observed, however, is how well the LLM handles using trial and error to correct any wrong choices.

</details>

## 🚀 Getting Started

Follow these steps to set up FHIR MCP Server in your environment.

### Prerequisites

- **Docker (recommended) or uv**: For dependency management

   👉 [uv Installation Guide](https://docs.astral.sh/uv/getting-started/installation/)
- **FHIR Server Account**: Access to FHIR API (e.g. Medplum)
- **Pinecone API key** (required for document search): Enables vector-based search over processed documents. Without it, semantic retrieval features will be unavailable.

   👉 [Create Pinecone Account](https://www.pinecone.io/)
- **LOINC Account** (optional): Enables retrieval of the latest LOINC codes from the official API. Without it, the system relies on static or language model-inferred codes, which may be outdated or imprecise.

   👉[Create LOINC Account](https://loinc.org/join/)

### Installation & Setup

1. **Clone the repository**:
   ```sh
   git clone https://github.com/the-momentum/fhir-mcp-server
   cd fhir-mcp-server
   ```

2. **Set up environment variables**:
   ```sh
   cp config/.env.example config/.env
   ```
   Edit the `config/.env` file with your credentials and configuration. See [Environment Variables](#-Environment-Variables)

3. **Install Dependencies**

   For Docker-based execution run:
   ```sh
   make build
   ```
   For uv-based execution run:
   ```sh
   make uv
   ```

4. **Update the MCP Client configuration**

   e.g. Claude Desktop -> edit ```claude_desktop_config.json```

- **Docker**

   ```json
   {
      "mcpServers": {
         "docker-mcp-server": {
            "command": "docker",
            "args": [
               "run",
               "-i",
               "--rm",
               "--init",
               "--name",
               "fhir-mcp-server",
               "--mount", // optional - volume for reload
               "type=bind,source=<your-project-path>/app,target=/root_project/app", // optional - volume for reload
               "--mount",
               "type=bind,source=<your-project-path>/config/.env,target=/root_project/config/.env",
               "-e", "TRANSPORT_MODE=stdio", // Set transport mode: stdio, http, or https
               "mcp-server:latest"
            ]
         }
      }
   }
   ```
   Make sure to replace ```<your-project-path>``` with the actual path to your installation

- **uv**

   Firstly, get uv path from terminal:

   - Windows:
      ```
      (Get-Command uv).Path
      ```

   - MacOS/Linux:
      ```
      which uv
      ```
   Then, update config file:

   ```json
   {
      "mcpServers": {
         "uv-mcp-server": {
            "command": "uv",
            "args": [
               "run",
               "--frozen",
               "--directory",
               "<your-project-path>",
               "start"
            ],
            "env": {
            "PATH": "<uv-bin-folder-path>"
            }
         }
      }
   }
   ```
   Make sure to replace <uv-bin-folder-path> with the actual uv path (to bin folder)

5. **Restart MCP Client**

   After completing all of the above steps, restart the MCP Client to apply the changes. In some cases, you may need to terminate all related processes using Task Manager or your system's process manager. This ensures that:

   - The updated configuration is properly loaded
   - Environment variables are correctly applied
   - The FHIR MCP client initializes with the correct settings


<p align="right">(<a href="#readme-top">back to top</a>)</p>


## 🔧 Configuration

### 🔐 Security & Encryption

The FHIR MCP Server includes built-in encryption infrastructure to protect sensitive configuration values. Sensitive fields like API keys and passwords are automatically encrypted and decrypted at runtime.

You are allowed to store passwords as a plain text, but if you want to have them encrypted, follow the instruction below.

#### Setting Up Encryption

<details>
<summary>Automated Setup (Recommended)</summary>

For most users, use the automated setup script:

```bash
# uv method
uv run scripts/cryptography/setup_encryption.py

# docker method
docker exec fhir-mcp-server uv run scripts/cryptography/setup_encryption.py
```

This script will:
1. Check for `MASTER_KEY` in `config/.env` and generate one if needed
2. Automatically encrypt all sensitive values (`LOINC_PASSWORD`, `FHIR_SERVER_CLIENT_SECRET`, `PINECONE_API_KEY`)
3. Update your `.env` file with encrypted values
4. Skip empty variables and already encrypted values

</details>

<details>
<summary>Manual Setup</summary>

1. **Generate a Master Key**:
   ```bash
   # uv method
   uv run scripts/cryptography/generate_master_key.py

   # docker method
   docker exec fhir-mcp-server uv run scripts/cryptography/generate_master_key.py
   ```
   Put that key as a MASTER_KEY environment variable in .env.

2. **Encrypt Sensitive Values**:
   ```bash
   # uv method
   uv run scripts/cryptography/encrypt_setting.py "your_secret_value"

    # docker method
   docker exec fhir-mcp-server uv run scripts/cryptography/encrypt_setting.py "your_secret_value"
   ```

3. **Decrypt Values** (for verification):
   ```bash
   # uv method
   uv run scripts/cryptography/decrypt_setting.py "encrypted_value"

    # docker method
   docker exec fhir-mcp-server uv run scripts/cryptography/decrypt_setting.py "encrypted_value"
   ```

</details>


#### Encrypted Configuration Fields

The following fields are automatically encrypted when using `EncryptedField`:

- `FHIR_SERVER_CLIENT_SECRET` - OAuth2 client secret for FHIR server
- `LOINC_PASSWORD` - LOINC account password
- `PINECONE_API_KEY` - Pinecone API key for vector search

#### Environment Variables

| Variable | Description | Example Value | Encryption |
|----------|-------------|---------------|------------|
| MASTER_KEY | Master encryption key | `gAAAAABl...` | Required |
| FHIR_SERVER_HOST | FHIR API host URL | `https://api.medplum.com` | No |
| FHIR_BASE_URL | FHIR base path | `/fhir/R4` | No |
| FHIR_SERVER_CLIENT_ID | OAuth2 client ID for FHIR | `019720e7...` | No |
| FHIR_SERVER_CLIENT_SECRET | OAuth2 client secret for FHIR | `gAAAAABl...` | **Yes** |
| LOINC_ENDPOINT | LOINC API search endpoint | `https://loinc.regenstrief.org/searchapi/loincs` | No |
| LOINC_USERNAME | LOINC account username | `loinc-user` | No |
| LOINC_PASSWORD | LOINC account password | `gAAAAABl...` | **Yes** |
| PINECONE_API_KEY | Pinecone API key | `gAAAAABl...` | **Yes** |
| EMBEDDING_MODEL | Hugging Face embedding model name | `NeuML/pubmedbert-base-embeddings` | No |

<p align="right">(<a href="#readme-top">back to top</a>)</p>


## 🛠️ MCP Tools

The FHIR MCP Server provides a comprehensive set of tools for interacting with FHIR resources and document management:

### FHIR Resource Tools

| Tool | Resource Type | Description |
|------|---------------|-------------|
| `request_patient_resource` | Patient | Manage patient demographic and administrative information |
| `request_observation_resource` | Observation | Handle clinical measurements and assessments |
| `request_condition_resource` | Condition | Manage patient problems and diagnoses |
| `request_medication_resource` | Medication | Handle medication information and orders |
| `request_immunization_resource` | Immunization | Manage vaccination records |
| `request_encounter_resource` | Encounter | Handle patient visits and interactions |
| `request_allergy_intolerance_resource` | AllergyIntolerance | Manage patient allergy information |
| `request_family_member_history_resource` | FamilyMemberHistory | Handle family health history |
| `request_generic_resource` | Any FHIR Resource | Operate on any FHIR resource not covered by specific tools |

### Document Management Tools

| Tool | Description |
|------|-------------|
| `request_document_reference_resource` | Manage FHIR DocumentReference resources |
| `add_document_to_pinecone` | Ingests documents into the vector database for semantic search |
| `search_pinecone` | Performs semantic search across indexed documents using vector embeddings |

### LOINC Terminology Tools

| Tool | Description |
|------|-------------|
| `get_loinc_codes` | Retrieves standardized LOINC codes for medical observations and laboratory tests |

### Tool Features

- **Full Resource Management**: All FHIR resource tools support Create, Read, Update, and Delete operations
- **Data Validation**: Tools enforce FHIR resource validation and prevent data corruption
- **Error Handling**: Comprehensive error responses with detailed failure information
- **Security**: OAuth2 authentication and proper access control for all operations
- **Semantic Search**: AI-powered document search using vector embeddings
- **Multi-format Support**: Document ingestion supports TXT, PDF, CSV, and JSON formats

<p align="right">(<a href="#readme-top">back to top</a>)</p>


## 🗺️ Roadmap

We're continuously enhancing FHIR MCP Server with new capabilities. Here's what's on the horizon:

- [ ] **Extended Authentication Options**: In addition to OAuth2 (already supported), we plan to add support for other authentication methods for connecting to FHIR servers
- [ ] **Expanded File Format Support for RAG**: Extend document ingestion capabilities to support additional formats
- [ ] **Table-Aware Document Chunking**: Improve the document chunking pipeline by detecting tables in documents and treating them as separate, atomic chunks.
- [ ] **OCR Support for Scanned Documents**: Implement Optical Character Recognition capabilities to enable extraction of text from scanned PDFs and image files before chunking and indexing

Have a suggestion? We'd love to hear from you! Contact us or contribute directly.

## 👥 Contributors

<a href="https://github.com/the-momentum/fhir-mcp-server/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=the-momentum/fhir-mcp-server" />
</a>

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## 📄 License

Distributed under the MIT License. See [MIT License](LICENSE) for more information.

---

<div align="center">
  <p><em>Built with ❤️ by <a href="https://themomentum.ai">Momentum</a> • Transforming healthcare data management with AI</em></p>
</div>

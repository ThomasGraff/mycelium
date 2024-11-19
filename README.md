<div align="center">
  <img src="frontend/mycelium/src/assets/logo.png" alt="Mycelium Logo" width="200"/>

  # Mycelium: Data Contract Editor

  [![License: AGPL v3](https://img.shields.io/badge/License-AGPL_v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)
  [![GitHub Stars](https://img.shields.io/github/stars/ThomasGraff/mycelium.svg)](https://github.com/ThomasGraff/mycelium/stargazers)
  [![GitHub Forks](https://img.shields.io/github/forks/ThomasGraff/mycelium.svg)](https://github.com/ThomasGraff/mycelium/network)
  [![GitHub Issues](https://img.shields.io/github/issues/ThomasGraff/mycelium.svg)](https://github.com/ThomasGraff/mycelium/issues)

  <p align="center">
    A powerful platform designed to simplify the creation and management of Data Contracts, bridging systems for seamless data ingestion.
    <br />
    <a href="#documentation"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/ThomasGraff/mycelium/issues/new?template=bug_report.md">Report Bug</a>
    ·
    <a href="https://github.com/ThomasGraff/mycelium/issues/new?template=feature_request.md">Request Feature</a>
  </p>
</div>

---

<details open>
<summary><h2 align="center">📖 Overview</h2></summary>

Mycelium serves as a central platform for managing data contracts efficiently, connecting business teams, IT services, and data services such as data factories. Our platform streamlines the data contract lifecycle with AI-powered automation and intuitive visualization tools.

</details>

---

<details open>
<summary><h2 align="center">✨ Key Features</h2></summary>

<div align="center">
  <table>
    <tr>
      <td align="center">
        <img src="https://img.icons8.com/color/48/000000/artificial-intelligence.png" width="30"/>
        <br />
        <b>AI-Powered Contracts</b>
        <br />
        Auto-generate data contracts using advanced LLM technology
      </td>
      <td align="center">
        <img src="https://img.icons8.com/color/48/000000/speed.png" width="30"/>
        <br />
        <b>Fast Ingestion</b>
        <br />
        Automated configuration and streamlined pipeline setup
      </td>
    </tr>
    <tr>
      <td align="center">
        <img src="https://img.icons8.com/color/48/000000/dashboard.png" width="30"/>
        <br />
        <b>Smart Visualization</b>
        <br />
        Track contracts and map data sources in real-time
      </td>
      <td align="center">
        <img src="https://img.icons8.com/color/48/000000/collaboration.png" width="30"/>
        <br />
        <b>Team Collaboration</b>
        <br />
        Unite teams with centralized contract management
      </td>
    </tr>
  </table>
</div>

</details>

---

<details open>
<summary><h2 align="center">🚀 Quick Start</h2></summary>

### Prerequisites

<div align="center">
  <table>
    <tr>
      <td align="center" width="50%">
        <img src="https://img.icons8.com/color/48/000000/docker.png" width="30"/>
        <br />
        <b>Local Usage</b>
        <br />
        <ul align="left">
          <li>Docker and Docker Compose</li>
          <li>Git</li>
        </ul>
      </td>
      <td align="center" width="50%">
        <img src="https://img.icons8.com/color/48/000000/code.png" width="30"/>
        <br />
        <b>Development</b>
        <br />
        <ul align="left">
          <li>Node.js (v18+)</li>
          <li>Yarn (preferred over npm)</li>
          <li>Python (v3.10+)</li>
          <li>Poetry</li>
          <li>Git</li>
        </ul>
      </td>
    </tr>
  </table>
</div>

### Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/ThomasGraff/mycelium.git
   cd mycelium
   ```

2. **Environment Setup**
   ```bash
   cp .env.example .env
   # Configure your environment variables (see environment variables section)
   ```

3. **Launch the Application**
   ```bash
   docker-compose up -d
   ```

4. **Access the Applications**  

   Go on `http://localhost:8080`

### Environment Variables

<div align="center">
  <table>
    <tr>
      <th>Variable</th>
      <th>Required</th>
      <th>Default</th>
      <th>Description</th>
    </tr>
    <tr>
      <td><code>PG_PASS</code></td>
      <td>✅</td>
      <td>-</td>
      <td>PostgreSQL password for Authentik</td>
    </tr>
    <tr>
      <td><code>FRONTEND_PORT</code></td>
      <td>❌</td>
      <td>8080</td>
      <td>Frontend application port</td>
    </tr>
    <tr>
      <td><code>BACKEND_PORT</code></td>
      <td>❌</td>
      <td>8000</td>
      <td>Backend API port</td>
    </tr>
    <tr>
      <td><code>AUTHENTIK_PORT_HTTP</code></td>
      <td>❌</td>
      <td>9000</td>
      <td>Authentik HTTP port</td>
    </tr>
    <tr>
      <td><code>AUTHENTIK_PORT_HTTPS</code></td>
      <td>❌</td>
      <td>9443</td>
      <td>Authentik HTTPS port</td>
    </tr>
  </table>
</div>

</details>

---

<details open>
<summary><h2 align="center">🤝 Contributing</h2></summary>

<div align="center">
  <table>
    <tr>
      <td align="center">
        <img src="https://img.icons8.com/color/48/000000/code-fork.png" width="30"/>
        <br />
        <b>1. Fork</b>
        <br />
        Fork the repository
      </td>
      <td align="center">
        <img src="https://img.icons8.com/color/48/000000/split.png" width="30"/>
        <br />
        <b>2. Branch</b>
        <br />
        <code>git checkout -b feat/YourFeature</code>
      </td>
      <td align="center">
        <img src="https://img.icons8.com/color/48/000000/commit-git.png" width="30"/>
        <br />
        <b>3. Commit</b>
        <br />
        <code>git commit -m 'Add feature'</code>
      </td>
    </tr>
    <tr>
      <td align="center">
        <img src="https://img.icons8.com/color/48/000000/upload-to-cloud.png" width="30"/>
        <br />
        <b>4. Push</b>
        <br />
        <code>git push origin feat/YourFeature</code>
      </td>
      <td align="center">
        <img src="https://img.icons8.com/color/48/000000/pull-request.png" width="30"/>
        <br />
        <b>5. Pull Request</b>
        <br />
        Open a PR on GitHub
      </td>
      <td align="center">
        <img src="https://img.icons8.com/color/48/000000/communication.png" width="30"/>
        <br />
        <b>6. Discuss</b>
        <br />
        Engage in review process
      </td>
    </tr>
  </table>
</div>

</details>
